API de Controle de Vendas
Uma API RESTful para gerenciar o controle de vendas, construída com Python, Flask e SQLite.

Visão Geral
Este projeto é uma API de Controle de Vendas que permite o gerenciamento completo de usuários, clientes, produtos e registros de vendas. Ele é projetado para ser flexível, escalável e fácil de integrar com outras aplicações, fornecendo endpoints e uma estrutura de banco de dados

Funcionalidades
Gerenciamento de Usuários:

Criação, leitura, atualização e exclusão de usuários para acesso à API.

Gerenciamento de Clientes:

Registro e manutenção de informações de clientes.

Gerenciamento de Produtos:

Cadastro de produtos com suas propriedades (nome, ponderador, meta_flot).

Gerenciamento de Vendas:

Registro de novas vendas, incluindo associação a clientes e produtos.

Consulta, atualização e exclusão de vendas existentes.

Modelos de Dados:

Estruturas de dados bem definidas para User, Cliente, Produto e Venda, refletindo o esquema do banco de dados.

Rotas de API:

Endpoints para interagir com as entidades do sistema.

Banco de Dados SQLite:

Persistência de dados leve e eficiente utilizando SQLite.

Tecnologias Utilizadas
Python 3.11

Flask (Framework Web)

SQLAlchemy (ORM para interação com o banco de dados, via Flask-SQLAlchemy)

SQLite3 (para o banco de dados app.db)

Flask-CORS (para lidar com requisições de diferentes origens)

Estrutura do Banco de Dados (database/app.db)
O banco de dados SQLite (app.db) contém as seguintes tabelas:

> User: Gerencia os usuários do sistema.

> Cliente: Armazena informações dos clientes.

> Produto: Cadastra os produtos disponíveis.

> Venda: Registra cada transação de venda.
