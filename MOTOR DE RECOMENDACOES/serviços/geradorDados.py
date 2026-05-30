from neo4j import GraphDatabase
from faker import Faker
import random
fake = Faker()
URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "valdemiro"
driver = GraphDatabase.driver(
    URI,
    auth=(USER, PASSWORD)
)
products = [
    ("Camisa", "Roupas"),
    ("Calça Jeans", "Roupas"),
    ("Jaqueta", "Roupas"),
    ("Vestido", "Roupas"),
    ("Shorts", "Roupas"),
    ("Moletom", "Roupas"),
    ("Bola de Futebol", "Esportes"),
    ("Bola de Basquete", "Esportes"),
    ("Luvas de Boxe", "Esportes"),
    ("Tênis Esportivo", "Esportes"),
    ("Caneleira", "Esportes"),
    ("Raquete de Tênis", "Esportes"),
    ("Notebook", "Eletronicos"),
    ("Mouse Gamer", "Eletronicos"),
    ("Headset", "Eletronicos"),
    ("Teclado Mecânico", "Eletronicos"),
    ("Monitor", "Eletronicos"),
    ("Webcam", "Eletronicos"),
    ("SSD", "Eletronicos"),
    ("Placa de Vídeo", "Eletronicos"),
    ("Sapato Social", "Calcados"),
    ("Tênis Nike", "Calcados"),
    ("Sandália", "Calcados"),
    ("Bota", "Calcados"),
    ("Relógio", "Acessorios"),
    ("Mochila", "Acessorios"),
    ("Óculos", "Acessorios"),
    ("Pulseira", "Acessorios"),
    ("Boné", "Acessorios"),
    ("Ventilador", "Casa"),
    ("Liquidificador", "Casa"),
    ("Microondas", "Casa"),
    ("Panela", "Casa"),
    ("iPhone", "Telemoveis"),
    ("Samsung Galaxy", "Telemoveis"),
    ("Carregador", "Telemoveis"),
   ]
def create_produtos(tx):
   for i, (product, category) in enumerate(products):
        tx.run(
            """
            CREATE (:Product {
                productId:$id,
                nome:$name,
                categoria:$category
            })
            """,
            id=i,
            name=product,
            category=category
        )
       
def create_usuarios(tx):
    for i in range(10000):
        tx.run(
            """
            CREATE (:User {
                userId:$id,
                nome:$name,
                cidade:$city
            })
            """,
            id=i,
            name=fake.name(),
            city=fake.city()
        )
def create_compras(tx):
    for i in range(50000):
        user_id = random.randint(0,9999)
        product_id = random.randint(0,9999)
        tx.run(
            """
            MATCH (u:User {userId:$uid})
            MATCH (p:Product {productId:$pid})
            CREATE (u)-[:COMPROU]->(p)
            """,
            uid=user_id,
            pid=product_id
        )
def create_amizades(tx):
    for i in range(70000):
        u1 = random.randint(0,9999)
        u2 = random.randint(0,9999)
        if u1 != u2:
            tx.run(
                """
                MATCH (a:User {userId:$u1})
                MATCH (b:User {userId:$u2})
                CREATE (a)-[:AMIGO_DE]->(b)
                """,
                u1=u1,
                u2=u2
            )
with driver.session() as session:
    session.execute_write(create_produtos)
    print("Produtos criados")
    session.execute_write(create_usuarios)
    print("Users criados")
    session.execute_write(create_compras)
    print("Compras criadas")
    session.execute_write(create_amizades)
    print("Amizades criadas")
driver.close()
print("Base populada com sucesso!")