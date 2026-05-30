from neo4j import GraphDatabase
URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "valdemiro"

driver = GraphDatabase.driver(
    URI,
    auth=(USER, PASSWORD)
)

products = {
    1: "Camisa",
    2: "Calça Jeans",
    3: "Jaqueta",
    4: "Vestido",
    5: "Shorts",
    6: "Moletom",
    7: "Bola de Futebol",
    8: "Bola de Basquete",
    9: "Luvas de Boxe",
    10: "Tênis Esportivo",
    11: "Caneleira",
    12: "Raquete de Tênis",
    13: "Notebook",
    14: "Mouse Gamer",
    15: "Headset",
    16: "Teclado Mecânico",
    17: "Monitor",
    18: "Webcam",
    19: "SSD",
    20: "Placa de Vídeo"
}

try:
    with driver.session() as session:
        result = session.run(
            "MATCH (n) RETURN count(n) AS total"
        )

        total = result.single()["total"]

        print("\n===================================")
        print("CONECTADO AO NEO4J COM SUCESSO")
        print(f"Total de nós no banco: {total}")
        print("===================================\n")

except Exception as e:
    print("Erro ao conectar ao Neo4j:")
    print(e)
    exit()


print("===== SISTEMA DE RECOMENDAÇÃO =====\n")

for key, value in products.items():
    print(f"{key} - {value}")


try:
    choice = int(input("\nEscolha um produto: "))

except ValueError:
    print("Digite apenas números.")
    driver.close()
    exit()

selected_product = products.get(choice)


if selected_product is None:
    print("Produto inválido.")
    driver.close()
    exit()


query = """
MATCH (u:User)-[:COMPROU]->(p1:Product)
WHERE p1.nome = $product

MATCH (u)-[:COMPROU]->(recommended:Product)
WHERE recommended.nome <> $product

RETURN recommended.nome AS product,
       COUNT(*) AS score

ORDER BY score DESC
LIMIT 5
"""


try:

    with driver.session() as session:

        result = session.run(
            query,
            product=selected_product
        )

        print(
            f"\nRecomendações para quem comprou "
            f"{selected_product}:\n"
        )

        found = False

        for record in result:

            found = True

            print(
                f"- {record['product']} "
                f"(score: {record['score']})"
            )

        if not found:
            print(
                "Nenhuma recomendação encontrada."
            )

except Exception as e:
    print("Erro ao executar a recomendação:")
    print(e)


driver.close()