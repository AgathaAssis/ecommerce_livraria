from datetime import datetime
from mongo_config import get_mongo_db
import mysql.connector
from mysql_config import get_connection

def etl_criar_cliente(cliente):
    db = get_mongo_db()
    collection = db["clientesCriados"]

    document = {
        "cliente_id": cliente["id"],
        "nome": cliente["nome"],
        "email": cliente["email"],
        "senha": cliente["senha"],
        "endereco": cliente["endereco"]
    }

    collection.insert_one(document)
    print(f"Cliente {cliente['nome']} registrado no MongoDB com todos os dados.")


def etl_login(cliente_id, nome):
    db = get_mongo_db()
    collection = db["logins"]

    document = {
        "cliente_id": cliente_id,
        "nome": nome,
        "data_login": datetime.now().isoformat()
    }

    collection.insert_one(document)
    print(f"Login de {nome} registrado no MongoDB.")


def etl_criar_livro(livro):
    db = get_mongo_db()
    collection = db["livrosCriados"]

    document = {
        "livro_id": livro["id"],
        "titulo": livro["titulo"],
        "genero": livro["genero"],
        "autor": livro["autor_nome"],
        "preco": float(livro["preco"])
    }

    collection.insert_one(document)
    print(f"Livro '{livro['titulo']}' registrado no MongoDB.")


def etl_faturar_pedido(pedido_id):
    conn = get_connection("ecommerce_letraviva")
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            p.id AS pedido_id,
            p.data AS data_pedido,
            c.nome AS cliente_nome,
            c.email AS cliente_email,
            c.endereco AS cliente_endereco,
            l.titulo AS livro_titulo,
            ip.quantidade,
            ip.preco_unitario,
            p.pagamento_id,
            f.tipo_pagamento,
            p.endereco_entrega
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.id
        JOIN itens_pedido ip ON ip.pedido_id = p.id
        JOIN livros l ON l.id = ip.livro_id
        JOIN formas_pagamento f ON f.id = p.pagamento_id
        WHERE p.id = %s
    """
    cursor.execute(query, (pedido_id,))

    rows = cursor.fetchall()
    if not rows:
        print(f"Nenhum dado encontrado para o pedido {pedido_id}")
        return

    row0 = rows[0]
    documento = {
        "pedido_id": row0["pedido_id"],
        "data_pedido": row0["data_pedido"].isoformat(),
        "cliente": {
            "nome": row0["cliente_nome"],
            "email": row0["cliente_email"],
            "endereco": row0["cliente_endereco"]
        },
        "forma_pagamento": {
            "id": row0["pagamento_id"],
            "descricao": row0["tipo_pagamento"]
        },
        "endereco_entrega": row0["endereco_entrega"],
        "itens": []
    }

    for row in rows:
        documento["itens"].append({
            "livro": row["livro_titulo"],
            "quantidade": row["quantidade"],
            "preco_unitario": float(row["preco_unitario"])
        })

    db = get_mongo_db()
    collection = db["pedidosFaturados"]
    collection.insert_one(documento)

    print(f"Pedido {pedido_id} inserido no MongoDB com sucesso.")
    cursor.close()
    conn.close()
