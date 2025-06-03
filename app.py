from flask import Flask, request, jsonify
from db_config import get_connection
from etl import etl_criar_livro
from etl import etl_criar_cliente, etl_login, etl_faturar_pedido

app = Flask(__name__)

@app.route("/criarConta", methods=["POST"])
def criar_conta():
    data = request.json
    conn = get_connection("ecommerce_letraviva")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO clientes (nome, email, senha, endereco)
        VALUES (%s, %s, %s, %s)
    """, (data['nome'], data['email'], data['senha'], data['endereco']))
    conn.commit()
    cliente_id = cur.lastrowid
    cur.close()
    conn.close()

    data['id'] = cliente_id
    etl_criar_cliente(data)
    return jsonify({"status": "conta criada", "id": cliente_id})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = get_connection("ecommerce_letraviva")
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM clientes WHERE email = %s AND senha = %s", (data['email'], data['senha']))
    cliente = cur.fetchone()
    if cliente:
        etl_login(cliente['id'])
        return jsonify({"status": "login efetuado"})
    return jsonify({"status": "erro"}), 401

@app.route("/adicionarLivro", methods=["POST"])
def adicionar_livro():
    try:
        data = request.json
        conn = get_connection("ecommerce_letraviva")
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO livros (titulo, genero, preco, autor_id)
            VALUES (%s, %s, %s, %s)
        """, (data['titulo'], data['genero'], data['preco'], data['autor_id']))
        conn.commit()
        livro_id = cur.lastrowid

        cur.execute("SELECT nome FROM autores WHERE id = %s", (data['autor_id'],))
        autor = cur.fetchone()
        autor_nome = autor[0] if autor else None

        cur.close()
        conn.close()

        livro = {
            'id': livro_id,
            'titulo': data['titulo'],
            'genero': data['genero'],
            'preco': data['preco'],
            'autor_nome': autor_nome
        }
        etl_criar_livro(livro)

        return jsonify({"status": "livro cadastrado", "id": livro_id})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/faturarPedido", methods=["POST"])
def faturar_pedido():
    data = request.json
    conn = get_connection("ecommerce_letraviva")
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO pedidos (cliente_id, data, pagamento_id, endereco_entrega)
        VALUES (%s, NOW(), %s, %s)
    """, (data['cliente_id'], data['pagamento_id'], data['endereco_entrega']))
    pedido_id = cur.lastrowid

    for item in data['itens']:
        cur.execute("""
            INSERT INTO itens_pedido (pedido_id, livro_id, quantidade, preco_unitario)
            VALUES (%s, %s, %s, %s)
        """, (pedido_id, item['livro_id'], item['quantidade'], item['preco_unitario']))

    conn.commit()
    cur.close()
    conn.close()

    etl_faturar_pedido(pedido_id)
    return jsonify({"status": "pedido faturado", "id": pedido_id})

if __name__ == "__main__":
    app.run(debug=True)
