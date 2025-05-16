def create_triplet(tx, subject, predicate, obj):
    # 決定節點類型
    if predicate in ["生產"]:
        subject_label = 'Supplier'
        object_label = 'Product'
        relation = 'PRODUCES'
    elif predicate in ["具備證書"]:
        subject_label = "Supplier"
        object_label = "Certificate"
        relation = "HAS_CERTIFICATE"
    elif predicate in ["位於"]:
        subject_label = "Supplier"
        object_label = "Location"
        relation = "LOCATED_IN"
    else:
        # 若遇到未知的 predicate，可以選擇跳過或自訂處理
        print(f"未知 predicate: {predicate}，略過。")
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