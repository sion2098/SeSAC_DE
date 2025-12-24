import os
import glob
import streamlit as st

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


# -----------------------------
# Streamlit basic config
# -----------------------------
st.set_page_config(page_title="워홀 RAG 챗봇", page_icon="🌍", layout="wide")
st.title("🌍 워홀 챗봇")
st.caption("워킹홀리데이 인포센터 문서 기반으로 답변하고, 기준 기반 추천을 제공합니다.")


# -----------------------------
# Data config
# -----------------------------
BASE_DATA_DIR = "data"

COUNTRY_MAP = {
    "🇦🇺 호주": "australia",
    "🇨🇦 캐나다": "canada",
    "🇯🇵 일본": "japan",
    "🇳🇿 뉴질랜드": "newzealand",
    "🇩🇪 독일": "germany",
}


# -----------------------------
# 추천 기준 & 점수표
# -----------------------------
CRITERIA = {
    "income": "수입/임금",
    "settlement": "초기 정착 난이도",
    "language": "언어 장벽",
    "visa": "비자 안정성/연장",
    "culture": "문화·생활 적응도",
}

BASE_SCORE = {
    "australia": {
        "income": 5,
        "settlement": 3,
        "language": 2,
        "visa": 4,
        "culture": 3,
    },
    "japan": {
        "income": 2,
        "settlement": 4,
        "language": 4,
        "visa": 3,
        "culture": 5,
    },
}


# -----------------------------
# Helpers
# -----------------------------
def load_all_documents(base_dir: str) -> list[Document]:
    docs = []
    for root, _, files in os.walk(base_dir):
        for fname in files:
            if not fname.endswith(".txt"):
                continue

            fp = os.path.join(root, fname)
            with open(fp, "r", encoding="utf-8") as f:
                text = f.read().strip()

            parts = os.path.normpath(fp).split(os.sep)
            country = parts[1] if len(parts) > 1 else "unknown"

            docs.append(
                Document(
                    page_content=text,
                    metadata={
                        "source_file": fname,
                        "country": country,
                        "full_path": fp,
                    },
                )
            )
    return docs


def format_context(docs: list[Document]) -> str:
    blocks = []
    for i, d in enumerate(docs, 1):
        src = d.metadata.get("source_file", "unknown.txt")
        blocks.append(f"[근거{i} | {src}]\n{d.page_content}")
    return "\n\n---\n\n".join(blocks)


def priority_to_weight(p1, p2, p3):
    weights = {k: 0 for k in CRITERIA.keys()}
    weights[p1] = 3
    weights[p2] = 2
    weights[p3] = 1
    return weights


def calc_country_score(country_key: str, weights: dict) -> int:
    return sum(BASE_SCORE[country_key][k] * w for k, w in weights.items())


# -----------------------------
# LLM / Vectorstore
# -----------------------------
def get_llm():
    return ChatOpenAI(model="gpt-4o-mini", temperature=0.2)


def get_embeddings():
    return OpenAIEmbeddings(model="text-embedding-3-small")


@st.cache_resource
def build_global_vectorstore():
    docs = load_all_documents(BASE_DATA_DIR)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
        separators=["\n\n", "\n", "-", "•", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    return FAISS.from_documents(chunks, get_embeddings())


vectorstore = build_global_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
llm = get_llm()


# -----------------------------
# Sidebar UI
# -----------------------------
with st.sidebar:
    st.subheader("⚙️ 설정")

    country_label = st.selectbox("국가 선택", list(COUNTRY_MAP.keys()), index=0)
    country_key = COUNTRY_MAP[country_label]

    st.markdown("---")
    st.subheader("🏁 국가 추천 기준 (우선순위)")

    p1 = st.selectbox(
        "1️⃣ 가장 중요한 기준",
        list(CRITERIA.keys()),
        format_func=lambda x: CRITERIA[x],
    )

    p2 = st.selectbox(
        "2️⃣ 두 번째 기준",
        [k for k in CRITERIA.keys() if k != p1],
        format_func=lambda x: CRITERIA[x],
    )

    p3 = st.selectbox(
        "3️⃣ 세 번째 기준",
        [k for k in CRITERIA.keys() if k not in (p1, p2)],
        format_func=lambda x: CRITERIA[x],
    )

    show_context = st.checkbox("근거(Context) 보기", value=False)


# -----------------------------
# Chat state
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": f"{country_label} 워홀 관련해서 궁금한 거 물어봐!",
        }
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# -----------------------------
# Chat input
# -----------------------------
user_q = st.chat_input("질문을 입력하세요 (예: 호주 vs 일본 추천)")
if user_q:
    st.session_state.messages.append({"role": "user", "content": user_q})
    with st.chat_message("user"):
        st.markdown(user_q)

    docs = retriever.invoke(user_q)
    context = format_context(docs)

    # 🔥 추천 질문 감지
    is_recommend = any(k in user_q for k in ["추천", "어디", "비교"])

    with st.chat_message("assistant"):
        with st.spinner("답변 생성 중..."):

            if is_recommend:
                weights = priority_to_weight(p1, p2, p3)
                au_score = calc_country_score("australia", weights)
                jp_score = calc_country_score("japan", weights)

                recommended = "호주" if au_score > jp_score else "일본"

                prompt = f"""
당신은 워킹홀리데이 전문 상담가입니다.

[사용자 우선순위]
1순위: {CRITERIA[p1]}
2순위: {CRITERIA[p2]}
3순위: {CRITERIA[p3]}

[국가별 점수]
- 호주: {au_score}
- 일본: {jp_score}

[Context]
{context}

[Instruction]
- 점수와 문서 근거를 기반으로
- 왜 {recommended}가 더 적합한지 설명하세요
- 단정하지 말고 조건부 추천으로 마무리하세요
"""
            else:
                prompt = f"""
당신은 워킹홀리데이 준비를 돕는 전문 상담 챗봇입니다.

[Country]
{country_label}

[Context]
{context}

[User Question]
{user_q}
"""

            resp = llm.invoke(prompt)
            answer = resp.content

        st.markdown(answer)

        if show_context:
            st.markdown("### 🔎 근거(Context)")
            st.code(context)

    st.session_state.messages.append({"role": "assistant", "content": answer})
