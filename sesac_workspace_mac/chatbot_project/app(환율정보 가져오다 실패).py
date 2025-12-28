# ============================================================
# 0. 기본 설정 & 라이브러리
# ============================================================
import os
import glob
import re
import requests
import streamlit as st
from dotenv import load_dotenv
from typing import List, Optional

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

load_dotenv()

st.set_page_config(
    page_title="워홀 RAG 챗봇",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌍 워홀 RAG 챗봇")
st.caption("공식 문서 기반 워킹홀리데이 상담 챗봇")

# ============================================================
# 1. 국가 & 통화 설정
# ============================================================
BASE_DATA_DIR = "data"

COUNTRY_MAP = {
    "🇦🇺 호주": "australia",
    "🇯🇵 일본": "japan",
    "🇨🇦 캐나다": "canada",
    "🇳🇿 뉴질랜드": "newzealand",
    "🇩🇪 독일": "germany",
}

COUNTRY_KEYWORDS = {
    "호주": "australia",
    "일본": "japan",
    "캐나다": "canada",
    "뉴질랜드": "newzealand",
    "독일": "germany",
}

REV_COUNTRY = {v: k for k, v in COUNTRY_MAP.items()}

CURRENCY_MAP = {
    "australia": "AUD",
    "canada": "CAD",
    "japan": "JPY",
    "newzealand": "NZD",
    "germany": "EUR",
}

# ============================================================
# 1-1. 국가별 추천 질문
# ============================================================
SUGGESTED_QUESTIONS = {
    "australia": [
        "호주 워홀 처음인데, 준비는 어디서부터 해야 해?",
        "호주 워홀 비자 신청할 때 잔고 증명은 어느 정도 필요해?",
        "호주랑 캐나다 워홀 조건을 비교해줘",
    ],
    "japan": [
        "일본 워홀은 나이 제한이 어떻게 돼?",
        "일본 워홀 비자 신청 절차를 순서대로 알려줘",
        "일본이랑 독일 워홀을 비교해줘",
    ],
    "canada": [
        "캐나다 워홀은 아무나 신청할 수 있어?",
        "캐나다 워홀은 경쟁이 치열하다고 하던데 왜 그래?",
        "호주랑 캐나다 워홀 조건을 비교해줘",
    ],
    "newzealand": [
        "뉴질랜드 워홀은 다른 나라보다 어떤 점이 달라?",
        "뉴질랜드 워홀 비자 신청 전에 준비해야 할 서류가 뭐야?",
        "뉴질랜드랑 호주 워홀 중에 어디가 더 나을까?",
    ],
    "germany": [
        "독일 워홀은 영어만으로도 가능한가요?",
        "독일 워홀 비자 신청 조건을 정리해줘",
        "독일이랑 일본 워홀을 비교해줘",
    ],
    None: [
        "워홀 국가를 아직 못 정했는데, 어떤 기준으로 선택하면 좋아?",
        "호주, 일본, 캐나다 워홀을 한 번에 비교해줘",
        "워홀 처음인데, 나라 고르기 전에 뭘 알아야 해?",
    ]
}

# ============================================================
# 2. 환율 처리 유틸
# ============================================================
# @st.cache_data(ttl=3600)
# def get_exchange_rate(base: str) -> float:
#     url = "https://api.exchangerate.host/latest"
#     params = {"base": base, "symbols": "KRW"}
#     r = requests.get(url, params=params, timeout=5)
#     return r.json()["rates"]["KRW"]


# def append_krw_amount(text: str, country: str) -> str:
#     if country not in CURRENCY_MAP:
#         return text

#     currency = CURRENCY_MAP[country]
#     rate = get_exchange_rate(currency)

#     patterns = [
#         rf"{currency}\s?([\d,]+)",
#         rf"{currency[0]}\$\s?([\d,]+)",
#         r"¥\s?([\d,]+)" if currency == "JPY" else None,
#         r"€\s?([\d,]+)" if currency == "EUR" else None,
#     ]

#     for p in filter(None, patterns):
#         m = re.search(p, text)
#         if not m:
#             continue

#         amount = int(m.group(1).replace(",", ""))
#         krw = int(amount * rate / 10000) * 10000
#         text += f"\n\n※ 참고: {currency} {amount:,} ≈ 약 {krw:,}원 (환율 기준)"
#         break

#     return text

@st.cache_data(ttl=3600)
def get_exchange_rate(base: str) -> float | None:
    try:
        url = "https://api.exchangerate.host/latest"
        params = {"base": base, "symbols": "KRW"}
        r = requests.get(url, params=params, timeout=5)

        # HTTP 에러
        if r.status_code != 200:
            st.warning(f"환율 API HTTP 오류: {r.status_code}")
            return None

        data = r.json()

        # 응답 구조 검증
        if not isinstance(data, dict):
            st.warning("환율 API 응답이 JSON 객체가 아님")
            return None

        if "rates" not in data or "KRW" not in data["rates"]:
            st.warning(f"환율 정보 누락: {data}")
            return None

        return data["rates"]["KRW"]

    except Exception as e:
        st.warning(f"환율 조회 중 오류 발생: {e}")
        return None


def append_krw_amount(text: str, country: str) -> str:
    if country not in CURRENCY_MAP:
        return text

    currency = CURRENCY_MAP[country]
    rate = get_exchange_rate(currency)

    # ❗ 환율 못 가져오면 그냥 원문 반환
    if rate is None:
        return text

    patterns = [
        rf"{currency}\s?([\d,]+)",
        rf"{currency[0]}\$\s?([\d,]+)",
        r"¥\s?([\d,]+)" if currency == "JPY" else None,
        r"€\s?([\d,]+)" if currency == "EUR" else None,
    ]

    for p in filter(None, patterns):
        m = re.search(p, text)
        if not m:
            continue

        amount = int(m.group(1).replace(",", ""))
        krw = int(amount * rate / 10000) * 10000
        text += f"\n\n※ 참고: {currency} {amount:,} ≈ 약 {krw:,}원 (환율 기준)"
        break

    return text


# ============================================================
# 3. 문서 로딩 & 벡터스토어
# ============================================================
def load_documents() -> List[Document]:
    docs = []
    for country in COUNTRY_MAP.values():
        path = os.path.join(BASE_DATA_DIR, country)
        if not os.path.isdir(path):
            continue
        for fp in glob.glob(os.path.join(path, "**", "*.txt"), recursive=True):
            with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read().strip()
            if text:
                docs.append(Document(
                    page_content=text,
                    metadata={"country": country}
                ))
    return docs


@st.cache_resource
def build_vectorstore():
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = splitter.split_documents(load_documents())
    return FAISS.from_documents(
        chunks,
        OpenAIEmbeddings(model="text-embedding-3-small")
    )


vectorstore = build_vectorstore()

# ============================================================
# 4. 검색 & 비교 판단
# ============================================================
def retrieve_by_countries(query: str, countries: List[str], k=4):
    results = vectorstore.similarity_search(query, k=40)
    buckets = {c: [] for c in countries}
    for d in results:
        c = d.metadata.get("country")
        if c in buckets and len(buckets[c]) < k:
            buckets[c].append(d)
    return buckets


def format_context(docs: List[Document], max_len=2000) -> str:
    text = ""
    for d in docs:
        if len(text) > max_len:
            break
        text += d.page_content + "\n\n"
    return text.strip()


def extract_countries(q: str) -> List[str]:
    return list({v for k, v in COUNTRY_KEYWORDS.items() if k in q})


def is_comparison(q: str, mentioned: List[str], base: Optional[str]) -> bool:
    return (
        len(mentioned) >= 2
        or any(t in q for t in ["비교", "vs", "차이", "어디"])
        or base is None
    )

# ============================================================
# 5. LLM
# ============================================================
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)


def answer_single(question: str, country: str) -> str:
    docs = retrieve_by_countries(question, [country])[country]
    answer = llm.invoke(f"""
[기준 국가]
{REV_COUNTRY[country]}

[공식 문서]
{format_context(docs)}

[질문]
{question}

추가 지침:
- 답변이 끝난 뒤,
  "다음으로 도움이 될 수 있는 내용"이라는 제목으로
  다음 단계에서 준비하면 좋은 내용이나
  이어서 많이 묻는 질문을
  최대 3개까지 bullet point로 정리하세요.
- 각 bullet point는 한 줄로 간결하게 작성하세요.
- 새로운 질문을 강요하지 말고,
  정리 형태로만 제공하세요.
- 추천이나 판단은 하지 마세요.
""").content.strip()

    return append_krw_amount(answer, country)


def answer_compare(question: str, countries: List[str]) -> str:
    blocks = []
    buckets = retrieve_by_countries(question, countries, k=3)
    for c in countries:
        blocks.append(f"### {REV_COUNTRY[c]}\n{format_context(buckets[c], 1200)}")

    return llm.invoke(f"""
공식 문서만을 근거로 국가를 비교하세요.
반드시 표로 작성하고, 없는 정보는 '자료 없음'으로 표시하세요.

{chr(10).join(blocks)}

질문: {question}
""").content.strip()

# ============================================================
# 6. 세션 상태
# ============================================================
for k, v in {
    "onboarded": False,
    "base_country": None,
    "messages": []
}.items():
    st.session_state.setdefault(k, v)

# ============================================================
# 7. 온보딩
# ============================================================
if not st.session_state.onboarded:
    choice = st.radio(
        "기준 국가 선택",
        list(COUNTRY_MAP.keys()) + ["➕ 아직 정하지 않았어요"]
    )
    if st.button("시작하기"):
        st.session_state.base_country = (
            None if choice.endswith("어요") else COUNTRY_MAP[choice]
        )
        st.session_state.onboarded = True
        st.session_state.messages = [
            {"role": "assistant", "content": "궁금한 걸 자유롭게 물어봐 😊"}
        ]
        st.rerun()
    st.stop()

# ============================================================
# 8. 사이드바
# ============================================================
with st.sidebar:
    st.subheader("⚙️ 설정")
    options = list(COUNTRY_MAP.keys()) + ["➕ 아직 정하지 않았어요"]
    current = st.session_state.base_country
    idx = options.index(
        "➕ 아직 정하지 않았어요" if current is None else REV_COUNTRY[current]
    )

    new = st.selectbox("기준 국가 변경", options, index=idx)
    if st.button("기준 국가 적용"):
        st.session_state.base_country = None if new.endswith("어요") else COUNTRY_MAP[new]
        st.rerun()

    if st.button("🗑️ 대화 초기화"):
        st.session_state.messages = [
            {"role": "assistant", "content": "대화를 초기화했어! 다시 질문해줘 😊"}
        ]
        st.rerun()

# ============================================================
# 9. 추천 질문 (첫 화면 전용)
# ============================================================
if len(st.session_state.messages) == 1:
    st.markdown(
        "💡 **아래는 사람들이 자주 묻는 질문이에요. "
        "버튼을 눌러 바로 질문해도 되고, 직접 입력해도 괜찮아요.**"
    )

    questions = SUGGESTED_QUESTIONS.get(
        st.session_state.base_country,
        SUGGESTED_QUESTIONS[None]
    )

    cols = st.columns(3)
    for col, q in zip(cols, questions):
        with col:
            if st.button(q):
                st.session_state.pending_question = q
                st.rerun()

# ============================================================
# 10. 채팅
# ============================================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_q = st.chat_input("질문을 입력하세요")

if "pending_question" in st.session_state:
    user_q = st.session_state.pop("pending_question")

if user_q:
    st.session_state.messages.append({"role": "user", "content": user_q})
    with st.chat_message("user"):
        st.markdown(user_q)

    mentioned = extract_countries(user_q)
    compare = is_comparison(user_q, mentioned, st.session_state.base_country)

    if compare:
        targets = mentioned or list(COUNTRY_MAP.values())
        answer = answer_compare(user_q, targets)
    else:
        country = mentioned[0] if mentioned else st.session_state.base_country
        if country is None:
            answer = answer_compare(user_q, list(COUNTRY_MAP.values()))
        else:
            answer = answer_single(user_q, country)

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
