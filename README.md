# 📚 Ecommerce Livraria

Projeto de backend para uma livraria online, desenvolvido com Flask, MySQL e MongoDB. Este sistema gerencia clientes, livros, pedidos e integra um processo ETL para armazenar dados em um Data Warehouse (MongoDB).

## 🚀 Tecnologias Utilizadas

* [Python 3.x](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/)
* [MySQL](https://www.mysql.com/)
* [MongoDB](https://www.mongodb.com/)
* [PyMySQL](https://pymysql.readthedocs.io/)
* [PyMongo](https://pymongo.readthedocs.io/)

## 📁 Estrutura do Projeto

```
ecommerce_livraria/
├── app.py
├── etl.py
├── mongo_config.py
├── mysql_config.py
├── .gitignore
├── teste/
└── videos/
```

* `app.py`: Arquivo principal com os endpoints da aplicação.
* `etl.py`: Processos ETL para transferência de dados entre MySQL e MongoDB.
* `mongo_config.py`: Configurações de conexão com o MongoDB.
* `mysql_config.py`: Configurações de conexão com o MySQL.
* `teste/`: Pasta para testes da aplicação.
* `videos/`: Pasta para armazenar vídeos relacionados ao projeto.

## ⚙️ Configuração e Execução

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/AgathaAssis/ecommerce_livraria.git
   cd ecommerce_livraria
   ```

2. **Crie e ative um ambiente virtual:**

   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No macOS/Linux:
   source venv/bin/activate
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as conexões com os bancos de dados:**

   * **MySQL:** Edite o arquivo `mysql_config.py` com as credenciais do seu banco de dados MySQL.
   * **MongoDB:** Edite o arquivo `mongo_config.py` com as credenciais do seu banco de dados MongoDB.

5. **Execute a aplicação:**

   ```bash
   python app.py
   ```

   A aplicação estará disponível em `http://localhost:5000`.

## 📌 Endpoints Disponíveis

* `POST /criarConta`: Cria uma nova conta de cliente.
* `POST /login`: Realiza o login de um cliente.
* `POST /adicionarLivro`: Adiciona um novo livro ao catálogo.
* `POST /faturarPedido`: Fatura um pedido realizado por um cliente.

## 🛠️ Funcionalidades

* **Cadastro de Clientes:** Armazena informações como nome, email, senha e endereço.
* **Login de Clientes:** Verifica as credenciais e registra o login no MongoDB.
* **Cadastro de Livros:** Armazena detalhes dos livros, incluindo título, gênero, preço e autor.
* **Faturamento de Pedidos:** Registra pedidos com informações detalhadas e realiza ETL para o MongoDB.
