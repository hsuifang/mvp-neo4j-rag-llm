# 🔍 MVP 供應商問答系統（Graph RAG Demo）
這是一個結合 Neo4j + Langchain + Grok 模型（xAI）的問答系統。
使用者可透過自然語言查詢，如「北台灣有哪些生產扣件且具備 ISO 27001 的公司？」

>💡 MVP 發想源自對技術原理的好奇，參考論文〈Integrating Graph Retrieval-Augmented Generation With Large Language Models for Supplier Discovery〉，實作語意查詢與知識>圖譜整合流程，以加深對相關技術的理解。

<img src="./pic.png">
---

## TECH

- [Langchain-XAI](https://github.com/langchain-ai/langchain-xai)
- [Neo4j](https://neo4j.com/)
- [Grok xAI 模型（透過 ChatXAI）](https://x.ai)
- [Streamlit](https://streamlit.io)

```

project_root/
│
├── app.py                    # Streamlit 啟動主程式
├── requirements.txt          # 所有套件依賴
├── README.md                 # 使用說明
│
├── src/                      # 🔹 Python 主邏輯程式碼區
│   ├── __init__.py
│   ├── prompts/ # 多版本 Prompt 對照組
│   │   ├── system_prompt.txt         # System Prompt 設定
│   │   └── cypher_prompt.txt         # Cypher Prompt 設定
│   │
│   ├── qa/
│   │   ├── __init__.py
│   │   ├── chain_builder.py          # 建立強化版 GraphCypherQAChain 的模組
│   │   └── utils.py                  # 讀取 prompt、其他共用工具
│   │
│   └── triplet_loader/
│       ├── __init__.py
│       └── create_triplet.py         # 匯入 triplet 到 Neo4j 的腳本
│
├── data/                     # 測試資料或 triplet.json 可放這裡
│   └── sample_triplets.json
│
├── tests/                    # 🔍 Prompt 測試框架
   ├── __init__.py
   ├── questions.json                 # 測試問題集
   ├── expected_answers.json          # 對應標準答案（可選）
   └── test_prompt_versions.py       # 主測試程式（含語法審查）
```
---

## 🚀 METHODS

1. 建立 `.env` 並填入：
```
   GROK_API_KEY=你的金鑰
   NEO4J_PASSWORD=你的neo4j密碼
```
2. 安裝必要套件:
```
pip install -r requirements.txt
```
3. 啟動前端：
```
streamlit run app.py
```

## FUTURE LOGS
* 增加UX - 顯示 GPT 生成的 Cypher 查詢（在 UI 中)
* 增加錯誤診斷輸出
* CHATGPT 建議
   * 建立 Prompt 評估機制
   * 後端 API 化（FastAPI or Flask）
   * 圖譜資料管理後台
   * CI/CD & Docker 化


## 參考文獻

- [Integrating Graph Retrieval-Augmented Generation With Large Language Models for Supplier Discovery](https://asmedigitalcollection.asme.org/computingengineering/article-abstract/25/2/021010/1210337/Integrating-Graph-Retrieval-Augmented-Generation?redirectedFrom=fulltext)