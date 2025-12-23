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
st.caption("워킹홀리데이 인포센터 문서 기반으로 답변하고, 참고한 파일을 함께 표시합니다.")

BASE_DATA_DIR = "data"
COMMON_DIR = os.path.join(BASE_DATA_DIR, "common")

COUNTRY_MAP = {
    "🇦🇺 호주": "australia",
    "🇨🇦 캐나다": "canada",
    "🇯🇵 일본": "japan",
    "🇳🇿 뉴질랜드": "newzealand",
    "🇩🇪 독일": "germany"
}

# -----------------------------
# Helpers
# -----------------------------
def list_txt_files(country_dir: str) -> list[str]:
    return sorted(glob.glob(os.path.join(country_dir, "*.txt")))

def load_txt_documents(country_dir: str) -> list[Document]:
    # 국가별 TXT
    country_files = list_txt_files(country_dir)

    # 공통 TXT (워킹홀리데이 제도 설명)
    common_files = []
    if os.path.isdir(COMMON_DIR):
        common_files = list_txt_files(COMMON_DIR)

    all_files = country_files + common_files
    docs = []

    for fp in all_files:
        with open(fp, "r", encoding="utf-8") as f:
            text = f.read().strip()

        docs.append(
            Document(
                page_content=text,
                metadata={
                    "source_file": os.path.basename(fp),
                    "source_type": "common"
                    if fp.startswith(COMMON_DIR)
                    else "country",
                    "country_dir": os.path.basename(country_dir),
                },
            )
        )
    return docs


def format_context(docs: list[Document]) -> str:
    # LLM에 근거를 명확히 주기 위해 "파일명"을 같이 붙임
    blocks = []
    for i, d in enumerate(docs, 1):
        src = d.metadata.get("source_file", "unknown.txt")
        blocks.append(f"[근거{i} | {src}]\n{d.page_content}")
    return "\n\n---\n\n".join(blocks)

SYSTEM_PROMPT = """
당신은 워킹홀리데이 준비를 돕는 전문 상담 챗봇입니다.

규칙:
- 반드시 제공된 문서(Context)에 기반해서만 답변하세요.
- 문서에 없는 내용은 추측하지 말고 "제공된 자료에는 해당 정보가 없습니다"라고 말하세요.
- 국가, 비자 조건, 나이 제한, 준비 서류, 주의사항을 명확하게 구분해서 설명하세요.
- 한국어로 친절하고 이해하기 쉽게 설명하세요.
- 필요하면 항목별 목록 형태로 정리하세요.
"""

def get_llm():
    return ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

def get_embeddings():
    return OpenAIEmbeddings(model="text-embedding-3-small")

# -----------------------------
# Build vectorstore per country (cached)
# -----------------------------
@st.cache_resource
def build_vectorstore(country_dir: str):
    # API 키 확인
    if not os.getenv("OPENAI_API_KEY"):
        return None, "❌ OPENAI_API_KEY 환경변수가 없습니다. 키 설정 후 다시 실행하세요."

    if not os.path.isdir(country_dir):
        return None, f"❌ 폴더가 없습니다: {country_dir}"

    docs = load_txt_documents(country_dir)
    if not docs:
        return None, f"❌ TXT 파일이 없습니다: {country_dir}/*.txt"

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
        separators=["\n\n", "\n", "•", "-", " ", ""],
    )
    chunks = splitter.split_documents(docs)

    vs = FAISS.from_documents(chunks, get_embeddings())
    return vs, None

# -----------------------------
# Sidebar UI
# -----------------------------
with st.sidebar:
    st.subheader("설정")
    country_label = st.selectbox("국가 선택", list(COUNTRY_MAP.keys()), index=0)
    country_key = COUNTRY_MAP[country_label]
    country_dir = os.path.join(BASE_DATA_DIR, country_key)

    k = st.slider("검색 문서 조각 수(top-k)", 2, 10, 5)
    show_context = st.checkbox("근거(Context) 보기", value=False)

    st.markdown("---")
    # st.markdown("**데이터 폴더**")
    # st.code(country_dir)
    # st.markdown("**TXT 파일 목록**")
    # files = list_txt_files(country_dir)
    # if files:
    #     for f in files:
    #         st.write("-", os.path.basename(f))
    # else:
    #     st.write("없음")

# -----------------------------
# Load vectorstore
# -----------------------------
vectorstore, err = build_vectorstore(country_dir)
if err:
    st.error(err)
    st.stop()

retriever = vectorstore.as_retriever(search_kwargs={"k": k})
llm = get_llm()

# -----------------------------
# Chat state
# -----------------------------

# 국가 변경 감지용
if "prev_country" not in st.session_state:
    st.session_state.prev_country = country_label


# 🔥 국가가 바뀌었을 때 → 대화 초기화 + rerun
if st.session_state.prev_country != country_label:
    prev = st.session_state.prev_country    # 이전 국가
    curr = country_label    # 변경된 국가

    st.toast(f"{prev} → {curr}로 국가가 변경되어 대화가 새로 시작됩니다 ✨", icon="🔄")

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": f"{curr} 워홀 관련해서 궁금한 거 물어봐! (비자/정착/취업/안전/귀국)"
        }
    ]
    st.session_state.prev_country = curr
    st.rerun()

# 최초 실행 시
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": f"{country_label} 워홀 관련해서 궁금한 거 물어봐! (비자/정착/취업/안전/귀국)"
        }
    ]

# 국가 바꾸면 대화 초기화 옵션(자동은 X)
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🧹 대화 초기화"):
        st.session_state.messages = [
            {"role": "assistant", "content": f"{country_label} 워홀 관련해서 궁금한 거 물어봐!"},
        ]
        st.rerun()

# render messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# Chat input
# -----------------------------
user_q = st.chat_input("질문을 입력하세요 (예: 워홀 비자 조건 / 세금 환급 / 긴급전화)")
if user_q:
    st.session_state.messages.append({"role": "user", "content": user_q})
    with st.chat_message("user"):
        st.markdown(user_q)

    # retrieve
    docs = retriever.invoke(user_q)
    context = format_context(docs)

    final_prompt = f"""
{SYSTEM_PROMPT}

[Country]
{country_label}

[Context]
{context}

[User Question]
{user_q}
"""

    # generate
    with st.chat_message("assistant"):
        with st.spinner("문서에서 근거 찾는 중..."):
            resp = llm.invoke(final_prompt)
            answer = resp.content

        # used files
        used_files = []
        for d in docs:
            sf = d.metadata.get("source_file")
            if sf and sf not in used_files:
                used_files.append(sf)

        st.markdown(answer)
        st.markdown("---")
        st.markdown("### 📌 참고 파일")
        st.write(", ".join(used_files) if used_files else "N/A")

        if show_context:
            st.markdown("### 🔎 근거(Context)")
            st.code(context)

    st.session_state.messages.append({"role": "assistant", "content": answer})
