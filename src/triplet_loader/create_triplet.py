import json
from neo4j import GraphDatabase
import os

# 連接 Neo4j
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def load_triplets(json_path="data/sample_triplets.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def create_triplet(tx, subject, predicate, obj):
    if predicate in ["生產", "提供"]:
        subject_label = "Supplier"
        object_label = "Product"
        relation = "PRODUCES"
    elif predicate in ["具備證書"]:
        subject_label = "Supplier"
        object_label = "Certificate"
        relation = "HAS_CERTIFICATE"
    elif predicate in ["位於"]:
        subject_label = "Supplier"
        object_label = "Location"
        relation = "LOCATED_IN"
    else:
        print(f"⚠️ 未知 predicate：{predicate}，略過")
        return

    tx.run(
        f"""
        MERGE (s:{subject_label} {{name: $subject}})
        MERGE (o:{object_label} {{name: $object}})
        MERGE (s)-[:{relation}]->(o)
        """,
        subject=subject,
        object=obj
    )

def import_triplets():
    triplets = load_triplets()
    with driver.session() as session:
        for triplet in triplets:
            try:
                session.write_transaction(
                    create_triplet,
                    triplet["subject"],
                    triplet["predicate"],
                    triplet["object"]
                )
            except Exception as e:
                print(f"❌ 匯入失敗：{triplet}，錯誤：{e}")
    print("✅ Triplet 資料匯入完成！")

if __name__ == "__main__":
    import_triplets()
