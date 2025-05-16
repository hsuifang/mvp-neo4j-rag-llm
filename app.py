from pathlib import Path
from src.qa.chain_builder import build_chain
import sys
project_root = Path(__file__).resolve()
# Add project root to sys.path
sys.path.append(str(project_root))

import streamlit as st

# 建 chain
chain = build_chain()

# Step 6: Streamlit 前端介面
st.title("供應商搜尋問答系統 Demo 🌟")
st.markdown("請輸入你的問題，例如：『台灣北部有哪些生產扣件且有 ISO 27001 的公司？』")
# 初始化 Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 使用者輸入區
user_input = st.text_input("🔍 請輸入查詢問題：", key="user_question")

# 按鈕觸發
if st.button("🚀 查詢"):
    if user_input:
        with st.spinner("LLM 正在生成查詢與查圖中..."):
            try:
                # 問答查詢
                result = chain.invoke({"query": user_input})
                answer = result["result"]
                print(result)
                cypher = result.get("cypher_query", "(無法取得查詢語句)")

                # 存入聊天歷史
                st.session_state.chat_history.append({
                    "question": user_input,
                    "cypher": cypher,
                    "answer": answer
                })

            except Exception as e:
                st.error(f"⚠️ 查詢失敗：{e}")
    else:
        st.warning("請輸入問題後再查詢")
# 顯示聊天歷史
if st.session_state.chat_history:
    st.subheader("🧠 查詢紀錄")
    for i, chat in enumerate(reversed(st.session_state.chat_history)):
        with st.expander(f"📌 查詢 {len(st.session_state.chat_history)-i}: {chat['question']}"):
            st.markdown("**🔗 生成的 Cypher 查詢：**")
            st.code(chat["cypher"], language="cypher")
            st.markdown("**✅ 回答：**")
            st.success(chat["answer"])
# if st.button("送出查詢"):
#     if user_question:
#         with st.spinner("查詢中..."):
#             response = chain.invoke({"query": user_question})
#             st.success(response["result"])
#     else:
#         st.warning("請先輸入問題！")