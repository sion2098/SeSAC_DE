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

def load_all_documents(base_dir: str) -> list[Document]:
    """
    data/ 아래의 common + 모든 국가 폴더의 TXT를 전부 로딩
    """
    docs = []

    for root, dirs, files in os.walk(base_dir):
        for fname in files:
            if not fname.endswith(".txt"):
                continue

            fp = os.path.join(root, fname)
            with open(fp, "r", encoding="utf-8") as f:
                text = f.read().strip()

            # country 추출 (data/japan/xxx.txt → japan)
            parts = os.path.normpath(fp).split(os.sep)
            country = parts[1] if len(parts) > 1 else "unknown"

            docs.append(
                Document(
                    page_content=text,
                    metadata={
                        "source_file": fname,
                        "country": country,  # 🔥 핵심
                        "full_path": fp,
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
# Load global vectorstore
# -----------------------------
vectorstore = build_global_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": k})
llm = get_llm()


# -----------------------------
# Chat state
# -----------------------------

# 국가 변경 감지용
if "prev_country" not in st.session_state:
    st.session_state.prev_country = country_label


# 국가 변경 시 토스트 팝업 노출(대화는 유지)
if st.session_state.prev_country != country_label:
    st.toast(f"{st.session_state.prev_country} → {country_label}로 국가가 변경되었습니다", icon="ℹ️")
    st.session_state.prev_country = country_label


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
