'''
이건 최소한의 코드만 수정한 버전
'''

# ============================================================
# 0. 기본 설정 & 라이브러리
# ============================================================
import os
import glob
import re
import streamlit as st
from dotenv import load_dotenv
from typing import List, Optional

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

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
# 1. 국가 설정
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

# ============================================================
# 1-1. 국가별 추천 질문
# ============================================================
SUGGESTED_QUESTIONS = {
    "australia": [
        "호주 비자 받는 방법 순서대로 알려줘",
        # "호주 워홀 비자 신청할 때 잔고 증명은 어느 정도 필요해?",
        "호주 취업 준비 방법은 뭐가 있어?",
        "TFN 신청 절차 알려줘",
        "호주 워홀중에 사고가 나서 응급 상황이 발생하면 어떻게 해야해?"
    ],
    "japan": [
        "일본 워홀은 나이 제한이 어떻게 돼?",
        "일본 워홀 비자 신청 절차를 순서대로 알려줘",
        "일본 취업 준비 방법은 뭐가 있어?",
    ],
    "canada": [
        "캐나다 워홀은 신청 자격 조건이 어떻게 돼?",
        "캐나다 워홀 비자 신청 절차를 단계별로 알려줘?",
        "호주랑 캐나다 워홀 조건을 비교해줘",
    ],
    "newzealand": [
        "뉴질랜드 워홀은 처음인데, 준비는 어디서부터 해야 해?",
        "뉴질랜드 워홀 비자 신청 전에 준비해야 할 서류가 뭐야?",
        "뉴질랜드랑 호주 워홀 중에 어디가 더 나을까?",
    ],
    "germany": [
        "독일 워홀은 영어만으로도 가능한가요?",
        "독일 워홀 비자 신청 조건을 정리해줘",
        "독일이랑 일본 워홀을 비교해줘",
    ],
    None: [
        "워홀 국가를 아직 못 정했는데, 국가별로 간단하게 비교해줘",
        "호주, 일본, 캐나다 워홀을 한 번에 비교해줘",
        "워홀 처음인데, 나라 고르기 전에 뭘 알아야 해?",
    ]
}

# ============================================================
# 2. 출처 URL
# ============================================================
def infer_section_from_filename(fp: str) -> str:
    """
    txt 파일명에 포함된 키워드를 기준으로
    '비자 / 취업 / 정착' 등의 섹션을 추론
    """
    name = os.path.basename(fp).lower()
    if "visa" in name:
        return "워홀비자 관련 정보"
    if "job" in name or "work" in name:
        return "취업 및 구직 정보"
    if "settle" in name or "life" in name:
        return "초기 정착 정보"
    if "safety" in name or "law" in name:
        return "안전 정보"
    return "기타 공식 정보"

def country_page_url(country: str) -> str:
    COUNTRY_URL_MAP = {
        "australia": "https://whic.mofa.go.kr/whic/nation/info.jsp?boardNo=100002",
        "japan": "https://whic.mofa.go.kr/whic/nation/info.jsp?boardNo=100012",
        "canada": "https://whic.mofa.go.kr/whic/nation/info.jsp?boardNo=100013",
        "newzealand": "https://whic.mofa.go.kr/whic/nation/info.jsp?boardNo=100003",
        "germany": "https://whic.mofa.go.kr/whic/nation/info.jsp?boardNo=100010",
    }
    return COUNTRY_URL_MAP.get(country, "https://whic.mofa.go.kr/whic/main/")

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

            if not text:
                continue

            docs.append(
                Document(
                    page_content=text,
                    metadata={
                        "country": country,
                        "site": "워킹홀리데이 인포센터 (외교부)",
                        "url": country_page_url(country)
                    }
                )
            )

    return docs

# ============================================================
# 벡터스토어 저장 경로
# ============================================================
VECTORSTORE_DIR = "vectorstore/faiss"


@st.cache_resource
def get_vectorstore():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # ✅ 이미 저장된 벡터스토어가 있으면 로드
    if os.path.exists(VECTORSTORE_DIR):
        return FAISS.load_local(
            VECTORSTORE_DIR,
            embeddings,
            allow_dangerous_deserialization=True
        )

    # ❌ 없으면 새로 생성
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(load_documents())

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    # ✅ 파일로 저장
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    vectorstore.save_local(VECTORSTORE_DIR)

    return vectorstore

vectorstore = get_vectorstore()


# ============================================================
# 3-1. 비교용 항목 정의 (항목별 retriever용)
# ============================================================
# COMPARE_FIELDS = {
#     "모집 인원": "모집 인원 연간 인원 정원",
#     "신청 기간": "신청 기간 연중 분기별 접수",
#     "신청 자격 요건": "연령 나이 자격 조건 초기 자금",
#     "비자 주요 특징": "체류 기간 취업 제한 학업 가능"
# }
COMPARE_FIELDS = {
    "모집 인원": "모집 인원 정원 인원 수",
    "신청 기간": "신청 기간 접수 기간",
    "신청 자격 요건": "신청 자격 요건 조건",
    # "연령 요건": "만 세 이상 이하 연령",
    "체류 가능 기간": "체류 기간 개월"
}


# ============================================================
# 4. 검색 & 질문 유형 판단
# ============================================================
def retrieve_by_countries(query: str, countries: List[str], k=6):
    search_query = f"""
    {query}
    워킹홀리데이 비자
    모집 인원 연간 인원 쿼터
    신청 기간 분기별
    연령 나이 제한
    체류 기간
    초기 자금 잔고
    비자 특징
    """

    results = vectorstore.similarity_search(search_query, k=40)

    buckets = {c: [] for c in countries}
    for d in results:
        c = d.metadata.get("country")
        if c in buckets and len(buckets[c]) < k:
            buckets[c].append(d)

    return buckets

def retrieve_by_field(country: str, field_query: str, k=5):
    query = f"""
    {REV_COUNTRY[country]} 워킹홀리데이 비자
    {field_query}
    """

    results = vectorstore.similarity_search(query, k=k)

    return [
        d for d in results
        if d.metadata.get("country") == country
    ]

def format_context(docs: List[Document], max_len=2000) -> str:
    text = ""
    for d in docs:
        if len(text) > max_len:
            break
        text += d.page_content + "\n\n"
    return text.strip()

def build_compare_context(country: str) -> str:
    """
    비교 질문 전용 컨텍스트 생성
    항목별로 문서를 나눠서 LLM에 전달
    """
    context = f"### {REV_COUNTRY[country]}\n"

    for field, query in COMPARE_FIELDS.items():
        docs = retrieve_by_field(country, query, k=3)
        snippet = format_context(docs, max_len=400)

        context += f"\n[{field}]\n"
        context += snippet if snippet else "검색된 문서 범위 내에서 확인되지 않음"
        context += "\n"

    return context

def extract_countries(q: str) -> List[str]:
    return list({v for k, v in COUNTRY_KEYWORDS.items() if k in q})


def is_comparison(q: str, mentioned: List[str], base: Optional[str]) -> bool:
    return (
        len(mentioned) >= 2
        or any(t in q for t in ["비교", "vs", "차이", "어디"])
    )

# ============================================================
# 4-1. "다음으로 도움이 될 수 있는 내용" 검증용 유틸(추가 뻑나면 지우기)
# ============================================================

def extract_followup_candidates(answer: str) -> List[str]:
    """
    LLM 답변에서 '다음으로 도움이 될 수 있는 내용' 섹션의
    질문 후보만 추출
    """
    lines = answer.splitlines()
    collecting = False
    candidates = []

    for line in lines:
        if "다음으로 도움이 될 수 있는 내용" in line:
            collecting = True
            continue

        if collecting:
            if line.strip().startswith("-"):
                q = line.strip().lstrip("-").strip()
                if q:
                    candidates.append(q)
            elif line.strip() == "":
                continue
            else:
                break

    return candidates


def filter_answerable_questions(
    questions: List[str],
    country: Optional[str],
    min_docs: int = 1
) -> List[str]:
    """
    질문 후보 중 실제로 문서 검색이 되는 질문만 통과
    (최대 3개)
    """
    valid = []

    for q in questions:
        if country:
            docs = retrieve_by_countries(q, [country])[country]
        else:
            docs_dict = retrieve_by_countries(q, list(COUNTRY_MAP.values()))
            docs = sum(docs_dict.values(), [])

        if len(docs) >= min_docs:
            valid.append(q)

        if len(valid) >= 3:
            break

    return valid

# ============================================================
# 5. 출처 포맷 (국가별 1개만)
# ============================================================

def format_sources_by_country(docs: List[Document]) -> str:
    seen = set()
    blocks = []

    for d in docs:
        country = d.metadata.get("country")
        site = d.metadata.get("site")
        url = d.metadata.get("url")

        if not country or country in seen:
            continue

        seen.add(country)

        country_label = REV_COUNTRY.get(country, country)

        blocks.append(
            f"- [{site} – {country_label}]({url})"
        )

    if not blocks:
        return ""

    return "\n\n---\n📄 **참고 출처**\n" + "\n".join(blocks)


# ============================================================
# 6. LLM
# ============================================================
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

# ============================================================
# 7. 단일 국가 답변
# ============================================================

SINGLE_COUNTRY_PROMPT = """
당신은 워킹홀리데이 공식 안내 문서를 기반으로 정보를 정리하는 안내 도우미입니다.
아래 지침을 반드시 모두 준수하여 답변하세요.

이 챗봇은 제공된 문서(txt 파일)에 기반해서만 답변한다.

[답변 범위]
각 파일의 역할은 다음과 같다:
- safety.txt : 사고, 범죄, 여권 분실·도난, 응급상황, 긴급 연락처, 재외공관, 위기 대응 절차
- visa.txt : 비자 종류, 신청 절차, 자격 요건, 모집 인원, 체류 기간, 취업·학업 제한, 비자 연장 조건
- jobs.txt : 취업 준비, TFN, 이력서·면접, 임금, 근무 조건, 노동법, 불법 고용 주의
- settlement.txt : 주거 형태, 생활비, 은행 계좌, 휴대폰·인터넷, 초기 정착, 일상생활 정보
- return.txt : 세금 환급, 연금 환급, 귀국 준비, 계좌·계약 해지, 이삿짐 정리
- region.txt : 국가·지역 정보, 대사관·총영사관, 공식 지원 채널, 지역별 행정 정보

- 질문이 특정 상황(예: 여권 분실, 재발급, 긴급 대응)에 해당할 경우, 반드시 해당 내용을 포함한 파일을 우선적으로 참고하여 답변하라.
- 관련 정보가 여러 파일에 나뉘어 있을 경우, 각 파일에서 관련된 내용을 모두 종합하여 답변하라.
- 이 질문은 단일 국가에 대한 설명입니다.
- 국가 간 비교, 장단점 비교, 추천, 개인 의견은 절대 포함하지 마세요.

[금지 사항]
- 표(table) 형태로 정리하지 마세요.
- 수도, 언어, 관광, 문화, 체험 프로그램(WWOOF/HelpX 등) 설명 금지
- 공식 문서에 근거하지 않은 추측성 내용 금지

[구성 방식]
- 반드시 단계별 구조(1 → 2 → 3)로 작성하세요.
- 각 단계 제목은 굵게 표시하세요.
- 각 조건은 단순 나열하지 말고, 의미를 2~3문장으로 설명하세요.
- **중요 조건, 제한 사항, 주의할 점은 굵게 표시하세요.**
- 번호 이모지(1️⃣ 2️⃣ 3️⃣) 사용 가능

[출력 형식 규칙]
- 아래 형식은 예시가 아니라 **모든 조건 항목에 반복 적용해야 하는 출력 규칙**입니다.
- 공식 문서에 포함된 모든 자격 요건 및 절차 항목에 대해
  1️⃣ → 2️⃣ → 3️⃣ 순서로 **누락 없이 끝까지 작성하세요.**
- 첫 번째 항목만 작성하고 답변을 종료하지 마세요.

- 각 항목은 반드시 아래 구조를 따르세요.

  1️⃣ **항목 제목**
  설명 문장은 반드시 다음 줄에 작성하세요.
  제목 줄과 설명 줄을 같은 줄에 작성하지 마세요.

- 굵게 표시된 제목 뒤에는 반드시 줄바꿈을 하세요.
- 설명은 하이픈(-) 없이 일반 문장으로 작성해도 됩니다.
- 각 항목 사이에는 한 줄 공백을 두어 가독성을 확보하세요.
- 위 형식을 하나라도 위반하면 답변을 다시 작성해야 합니다.
- 조건이 1개만 확인되더라도, 해당 항목이 마지막 항복임을 명시하고 형식을 유지하세요


[단일 사실 질문 처리]
- 숫자, 기간, 횟수 등 단일 사실 질문은
  핵심 답변만 한 문장으로 작성하세요.

[링크 출력 규칙]
- 공식 사이트, 정부 기관, 안내 페이지 등 URL이 포함된 정보는
  반드시 마크다운 링크 형식으로 작성하세요.
- 형식: [링크 설명](https://example.com)
- URL을 일반 텍스트로 풀어 쓰지 마세요.
- 링크 설명은 간결하게 작성하세요.


[마무리]
- 답변 마지막에 반드시 아래 섹션을 포함하세요.

### 다음으로 도움이 될 수 있는 내용
- 아래 항목은 "질문 후보"입니다.
- 실제로 답변 가능한 질문만 노출됩니다.
- 문서에 없는 내용은 질문을 생성하지 마세요.
- 최대 3개까지 제시하세요.

"""

def answer_single(question: str, country: str) -> str:
    docs = retrieve_by_countries(question, [country])[country]

    prompt = ChatPromptTemplate.from_messages([
        ("system", SINGLE_COUNTRY_PROMPT),
        ("system", f"""
[기준 국가]
{REV_COUNTRY[country]}

[공식 문서]
{format_context(docs)}
"""),
        ("human", question)
    ])

    answer = llm.invoke(prompt.format_messages()).content.strip()
    # ============================================================
    # 🔽 "다음으로 도움이 될 수 있는 내용" 검증 로직 (추가)(여기도 뻑나면 삭제))
    # ============================================================
    candidates = extract_followup_candidates(answer)
    filtered = filter_answerable_questions(
        candidates,
        country=country
    )

    if filtered:
        answer = re.sub(
            r"### 다음으로 도움이 될 수 있는 내용[\s\S]*$",
            "### 다음으로 도움이 될 수 있는 내용\n"
            + "\n".join(f"- {q}" for q in filtered),
            answer
        )
    else:
        # 하나도 통과 못 하면 섹션 자체 제거
        answer = re.sub(
            r"### 다음으로 도움이 될 수 있는 내용[\s\S]*$",
            "",
            answer
        )
    # ============================================================
    answer += format_sources_by_country(docs)
    return answer

# ============================================================
# 8. 국가 비교 답변
# ============================================================
COMPARE_COUNTRY_PROMPT = """
당신은 워킹홀리데이 공식 안내 문서(txt 파일)에 기반하여
여러 국가의 제도를 **비교 정리하는 안내 도우미**입니다.
아래 지침을 반드시 모두 준수하세요.

이 챗봇은 제공된 문서에 기반한 정보만 사용합니다.

[답변 범위]
각 파일의 역할은 다음과 같다:
- safety.txt : 사고, 범죄, 여권 분실·도난, 응급상황, 긴급 연락처, 재외공관, 위기 대응 절차
- visa.txt : 비자 종류, 신청 절차, 자격 요건, 모집 인원, 체류 기간, 취업·학업 제한, 비자 연장 조건
- jobs.txt : 취업 준비, TFN, 이력서·면접, 임금, 근무 조건, 노동법, 불법 고용 주의
- settlement.txt : 주거 형태, 생활비, 은행 계좌, 휴대폰·인터넷, 초기 정착, 일상생활 정보
- return.txt : 세금 환급, 연금 환급, 귀국 준비, 계좌·계약 해지, 이삿짐 정리

[파일별 정보 활용 지침]
- 모집 인원, 신청 기간, 신청 자격 요건, 연령 요건, 체류 가능 기간은 visa.txt 파일을 우선적으로 참고하세요.
- 비자 주요 특징(취업·학업 제한, 체류 조건)은 visa.txt와 jobs.txt의 내용을 함께 참고하세요.
- 특정 항목에 대한 정보가 한 파일에 없을 경우, 위 파일 범위 내에서 관련 내용을 종합하여 정리하세요.
- 위 파일들에 근거가 전혀 없는 경우에만 "검색된 문서 범위 내에서 확인되지 않음"으로 표기하세요.


[비교 대상 국가]
- 비교 대상 국가는 다음과 같습니다: {countries}
- 위에 명시된 국가 외의 국가는 포함하지 마세요.

[비교 기준]
- 기본 비교 항목은 아래 4개입니다.

모집 인원  
신청 기간  
신청 자격 요건  
체류 가능 기간  

- 사용자가 비교 항목을 명시하지 않은 경우,
  위 4개 항목을 기준으로 **전체 비교 표**를 작성하세요.
- 사용자가 특정 비교 항목을 명시한 경우,
  해당 항목에 대해서만 **국가별로 더 구체적으로 비교**하세요.

[출력 형식 규칙]
- 반드시 **표(table)** 형태로 작성하세요.
- 행(row): 국가
- 열(column): 비교 항목
- 모든 셀을 채우세요.
- 문서 근거가 전혀 없는 경우에만
  "검색된 문서 범위 내에서 확인되지 않음"으로 표기하세요.
- 임의 요약, 추측, 일반 상식 사용은 금지됩니다.


[금지 사항]
- 개인적인 추천, 판단, 우열 비교 표현 금지
- 서술형 설명 금지 (표 외 형식 금지)
- 수도, 언어, 관광, 문화, 체험 프로그램 설명 금지

[마무리]
- 표 아래에 반드시 아래 섹션을 포함하세요.

### 다음으로 도움이 될 수 있는 내용
- 최대 3개 bullet point
- 한 줄씩 간결하게
- 추천·판단·질문 유도 금지

====================
[국가별 공식 문서]
====================
{contexts}

질문:
{question}
"""

ALL_COUNTRIES = ["australia", "japan", "canada", "newzealand", "germany"]

def answer_compare(question: str, countries: List[str]) -> str:
    # 1️⃣ 국가 미지정 → 전체 국가 비교
    if not countries:
        countries = ALL_COUNTRIES

    # 2️⃣ 국가별 비교 컨텍스트 생성
    context_blocks = []
    for c in countries:
        ctx = build_compare_context(c)
        context_blocks.append(f"[{c.upper()} 공식 문서]\n{ctx}")

    prompt = COMPARE_COUNTRY_PROMPT.format(
        countries=", ".join(countries),
        contexts="\n\n".join(context_blocks),
        question=question
    )

    answer = llm.invoke(prompt).content.strip()

    # ============================================================
    # 🔽 비교 답변용 "다음으로 도움이 될 수 있는 내용" 검증 (뻑나면 삭제)
    # ============================================================
    candidates = extract_followup_candidates(answer)
    filtered = filter_answerable_questions(
        candidates,
        country=None  # 비교는 국가 전체 기준
    )

    if filtered:
        answer = re.sub(
            r"### 다음으로 도움이 될 수 있는 내용[\s\S]*$",
            "### 다음으로 도움이 될 수 있는 내용\n"
            + "\n".join(f"- {q}" for q in filtered),
            answer
        )
    else:
        answer = re.sub(
            r"### 다음으로 도움이 될 수 있는 내용[\s\S]*$",
            "",
            answer
        )
    # ============================================================

    # 3️⃣ 출처 정리
    source_docs = [
        Document(
            page_content="",
            metadata={
                "country": c,
                "site": "워킹홀리데이 인포센터 (외교부)",
                "url": country_page_url(c)
            }
        )
        for c in countries
    ]

    answer += format_sources_by_country(source_docs)
    return answer

# ============================================================
# 9. 세션 상태 초기화
# ============================================================
for k, v in {
    "onboarded": False,
    "base_country": None,
    "prev_country": None,
    "messages": [],
    "pending_question": None, 
}.items():
    st.session_state.setdefault(k, v)

# ============================================================
# 10. 온보딩
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
# 11. 사이드바 (설정)
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

        # ✅ 국가가 실제로 변경된 경우에만 알림
        if prev != new_country:
            st.session_state.messages.append({
                "role": "assistant",
                "content": (
                    "🌍 **기준 국가가 변경되었습니다**\n\n"
                    f"- 이전 기준: **{REV_COUNTRY.get(prev, '없음')}**\n"
                    f"- 현재 기준: **{REV_COUNTRY.get(new_country, '없음')}**\n\n"
                    "이후 답변은 현재 기준 국가의 자료를 우선 참고합니다.\n"
                    "다른 국가에 대한 질문도 계속 가능합니다."
                )
            })

        st.session_state.base_country = new_country
        st.session_state.prev_country = new_country
        st.rerun()

    if st.button("🗑️ 대화 초기화"):
        st.session_state.messages = [
            {"role": "assistant", "content": "대화를 초기화했어! 다시 질문해줘 😊"}
        ]
        st.rerun()

# ============================================================
# 12. 추천 질문 UI
# ============================================================
# if len(st.session_state.messages) == 1:
if len(st.session_state.messages) == 1 and not st.session_state.get("pending_question"):
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
# 13. 채팅 UI
# ============================================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# chat_input은 항상 호출
user_input = st.chat_input("질문을 입력하세요")

# 질문 소스 결정
if st.session_state.get("pending_question"):
    user_q = st.session_state.pending_question
    st.session_state.pending_question = None
else:
    user_q = user_input

if user_q:
    # 1️⃣ 먼저 세션에 저장
    st.session_state.messages.append(
        {"role": "user", "content": user_q}
    )

    # 2️⃣ 답변 생성
    mentioned = extract_countries(user_q)
    print("mentioned:",mentioned)
    compare = is_comparison(user_q, mentioned, st.session_state.base_country)
    print("compare:",compare)

    if compare:
        targets = mentioned or list(COUNTRY_MAP.values())
        print("targets:",targets)
        answer = answer_compare(user_q, targets)
    else:
        country = mentioned[0] if mentioned else st.session_state.base_country
        if country is None:
            answer = answer_compare(user_q, list(COUNTRY_MAP.values()))
        else:
            answer = answer_single(user_q, country)

    # 3️⃣ 답변도 세션에 저장
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    # 4️⃣ rerun으로 화면 다시 그림 (중요!)
    st.rerun()
