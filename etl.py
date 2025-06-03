from db_config import get_connection

def etl_criar_cliente(cliente):
    dw = get_connection("DW_LetraViva")
    cursor = dw.cursor()
    cursor.execute("""
        INSERT INTO dim_cliente (id, nome, email, endereco)
        VALUES (%s, %s, %s, %s)
    """, (cliente['id'], cliente['nome'], cliente['email'], cliente['endereco']))
    dw.commit()
    cursor.close()
    dw.close()

def etl_login(cliente_id):
    dw = get_connection("DW_LetraViva")
    cursor = dw.cursor()
    cursor.execute("REPLACE INTO dim_login (cliente_id, ultimo_login) VALUES (%s, NOW())", (cliente_id,))
    dw.commit()
    cursor.close()
    dw.close()

def etl_criar_livro(livro):
    dw = get_connection("DW_LetraViva")
    cursor = dw.cursor()
    cursor.execute("""
        INSERT INTO dim_livro (id, autor, titulo, preco, genero, ano_publicacao)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        livro['id'],
        livro['autor_nome'],  # corresponde à coluna 'autor'
        livro['titulo'],
        livro['preco'],
        livro['genero'],
        livro.get('ano_publicacao')  # pode ser None, se não enviado
    ))
    dw.commit()
    cursor.close()
    dw.close()
    
def etl_faturar_pedido(pedido_id):
    ecommerce = get_connection("ecommerce_letraviva")
    dw = get_connection("DW_LetraViva")
    cur = ecommerce.cursor(dictionary=True)
    
    # Pega info do pedido
    cur.execute("""
        SELECT p.*, c.nome AS cliente_nome, c.email, c.endereco, f.tipo_pagamento
        FROM pedidos p
        JOIN clientes c ON c.id = p.cliente_id
        JOIN formas_pagamento f ON f.id = p.pagamento_id
        WHERE p.id = %s
    """, (pedido_id,))
    pedido = cur.fetchone()

    # Pega itens do pedido
    cur.execute("""
        SELECT i.*, l.titulo, l.genero, l.preco, a.nome AS autor_nome
        FROM itens_pedido i
        JOIN livros l ON l.id = i.livro_id
        JOIN autores a ON a.id = l.autor_id
        WHERE i.pedido_id = %s
    """, (pedido_id,))
    itens = cur.fetchall()

    cur_dw = dw.cursor()
    for item in itens:
        total = item['quantidade'] * item['preco_unitario']
        cur_dw.execute("""
            INSERT INTO fato_pedido_completo (
                cliente_id, cliente_nome, livro_titulo, genero,
                autor_nome, quantidade, preco_unitario, total,
                forma_pagamento, endereco_entrega, data_pedido
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            pedido['cliente_id'], pedido['cliente_nome'], item['titulo'], item['genero'],
            item['autor_nome'], item['quantidade'], item['preco_unitario'], total,
            pedido['tipo_pagamento'], pedido['endereco_entrega'], pedido['data']
        ))

    dw.commit()
    cur.close()
    cur_dw.close()
    ecommerce.close()
    dw.close()
