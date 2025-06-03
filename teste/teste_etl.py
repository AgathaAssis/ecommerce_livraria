from etl import etl_criar_livro  # ou ajuste o nome do seu arquivo onde está a função

livro_teste = {
    'id': 9999,
    'titulo': "Livro de Teste",
    'genero': "Fantasia",
    'preco': 45.90,
    'autor_nome': "Autor Teste"
}

try:
    etl_criar_livro(livro_teste)
    print("ETL criado com sucesso!")
except Exception as e:
    print("Erro ao criar ETL:", e)
