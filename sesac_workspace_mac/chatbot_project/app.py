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
# Streamlit Page Config
# -----------------------------
st.set_page_config(page_title="호주 워홀 챗봇 (공식문서 기반)", page_icon="🇦🇺", layout="wide")
st.title("🇦🇺 호주 워홀 챗봇 (공식문서 기반)")
st.caption("출처: 재외동포청 워킹홀리데이인포센터 PDF를 TXT로 정리한 데이터")

DATA_DIR = "data/australia"
SOURCE_HOME = "https://whic.mofa.go.kr/whic/nation/info.jsp?boardNo=100002"

# -----------------------------
# Helper: Load TXT files
# -----------------------------
def load_txt_documents(data_dir: str) -> list[Document]:
    file_paths = sorted(glob.glob(os.path.join(data_dir, "*.txt")))
    docs: list[Document] = []

    if not file_paths:
        return docs

    for fp in file_paths:
        with open(fp, "r", encoding="utf-8") as f:
            text = f.read().strip()

        docs.append(
            Document(
                page_content=text,
                metadata={
                    "source_file": os.path.basename(fp),
                    "source_url": SOURCE_HOME,
                    "country": "Australia",
                },
            )
        )
    return docs

# -----------------------------
# Build VectorStore (FAISS)
# -----------------------------
@st.cache_resource
def build_vectorstore():
    docs = load_txt_documents(DATA_DIR)
    if not docs:
        return None, "❌ data/australia 폴더에 .txt 파일이 없어요. 파일 경로/이름을 확인해줘!"

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
        separators=["\n\n", "\n", "•", "-", " ", ""],
    )
    chunks = splitter.split_documents(docs)

    # 임베딩/LLM은 OPENAI_API_KEY 필요
    if not os.getenv("OPENAI_API_KEY"):
        return None, "❌ OPENAI_API_KEY 환경변수가 없어요. 키 설정 후 다시 실행해줘!"

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vs = FAISS.from_documents(chunks, embeddings)
    return vs, None

# -----------------------------
# LLM
# -----------------------------
def get_llm():
    # 필요하면 모델 변경 가능
    return ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

# -----------------------------
# Prompt (RAG)
# -----------------------------
SYSTEM_PROMPT = """
너는 '호주 워킹홀리데이' 정보 도우미야.
반드시 제공된 문서(Context)에 근거해서만 답변해.
모르면 "문서에 근거가 부족해 확답하기 어렵다"라고 말해.
답변은 한국어로, 핵심을 먼저, 그 다음에 상세를 bullet로 정리해.
마지막에 참고한 source_file 목록과 source_url을 표기해.
"""

def format_context(docs: list[Document]) -> str:
    # 문서 조각 + 출처 파일명 붙여서 LLM에게 근거를 명확히 제공
    blocks = []
    for i, d in enumerate(docs, 1):
        src = d.metadata.get("source_file", "unknown.txt")
        blocks.append(f"[문서{i} | {src}]\n{d.page_content}")
    return "\n\n---\n\n".join(blocks)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.subheader("설정")
    k = st.slider("검색할 문서 조각 수 (top-k)", 2, 8, 4)
    st.markdown("---")
    st.markdown("**데이터 위치**")
    st.code(DATA_DIR)
    st.markdown("**공식 출처(홈)**")
    st.write(SOURCE_HOME)
    st.markdown("---")
    st.markdown("**예시 질문**")
    st.write("- 호주 워홀 나이 제한 알려줘")
    st.write("- 2nd/3rd 비자 연장 조건 뭐야?")
    st.write("- TFN은 왜 필요하고 어떻게 신청해?")
    st.write("- 귀국 전에 세금 환급은 언제 해?")

# -----------------------------
# Initialize VectorStore
# -----------------------------
vectorstore, error_msg = build_vectorstore()
if error_msg:
    st.error(error_msg)
    st.stop()

retriever = vectorstore.as_retriever(search_kwargs={"k": k})
llm = get_llm()

# -----------------------------
# Chat State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕! 호주 워홀(비자/정착/취업/귀국) 관련해서 궁금한 거 물어봐 😊"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# Chat Input
# -----------------------------
user_q = st.chat_input("질문을 입력하세요 (예: 2차 비자 조건 알려줘)")
if user_q:
    st.session_state.messages.append({"role": "user", "content": user_q})
    with st.chat_message("user"):
        st.markdown(user_q)

    # Retrieve relevant chunks
    # docs = retriever.get_relevant_documents(user_q)
    docs = retriever.invoke(user_q)
    context = format_context(docs)

    # Make final prompt
    final_prompt = f"""
{SYSTEM_PROMPT}

[Context]
{context}

[User Question]
{user_q}
"""

    with st.chat_message("assistant"):
        with st.spinner("문서에서 근거 찾는 중..."):
            resp = llm.invoke(final_prompt)
            answer = resp.content

        # 출처(중복 제거)
        used_files = []
        for d in docs:
            sf = d.metadata.get("source_file")
            if sf and sf not in used_files:
                used_files.append(sf)

        # Answer + Sources
        st.markdown(answer)
        st.markdown("---")
        st.markdown("### 📌 참고 출처")
        st.write("문서:", ", ".join(used_files) if used_files else "N/A")
        st.write("공식 링크:", SOURCE_HOME)

    st.session_state.messages.append({"role": "assistant", "content": answer})
