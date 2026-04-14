# Sistema de Gerenciamento de E-Commerce

Projeto desenvolvido para a atividade de desenvolvimento da **Rocket Lab 2026 / Visagio**, com o objetivo de implementar um módulo de gerenciamento de produtos de um sistema de e-commerce.

A aplicação foi construída em arquitetura **full stack**, com **frontend e backend separados**, permitindo que o gerente da loja consiga visualizar, buscar, cadastrar, editar, remover e analisar produtos do catálogo.

## Objetivo da aplicação

O sistema permite ao usuário:

* navegar em um catálogo de produtos;
* buscar produtos específicos por nome ou categoria;
* visualizar detalhes de cada produto;
* acompanhar medidas, vendas e avaliações;
* visualizar a média das avaliações de um produto;
* adicionar, editar e remover produtos individualmente.

Os dados utilizados no sistema são carregados a partir de arquivos `.csv`, com persistência em banco SQLite.

---

## Stack utilizada

### Frontend

* Vite
* React
* TypeScript
* Tailwind CSS
* Axios
* pnpm

### Backend

* FastAPI
* SQLAlchemy
* Alembic
* SQLite

---

## Estrutura do projeto

```bash
rocketlab2026/
├── backend/
│   ├── alembic/
│   ├── app/
│   ├── data/
│   ├── .env
│   ├── alembic.ini
│   ├── requirements.txt
│   └── database.db
└── frontend/
```

> Observação: a pasta `backend/data` é utilizada para armazenar os arquivos necessários para população inicial do banco.

---

## Funcionalidades implementadas

* listagem de produtos em catálogo;
* busca de produtos por nome ou categoria;
* paginação de produtos;
* visualização de detalhes de cada produto;
* exibição de medidas do produto;
* exibição de quantidade de vendas e valor total vendido;
* exibição de avaliações do produto;
* exibição da média das avaliações;
* cadastro de novos produtos;
* edição de produtos existentes;
* remoção de produtos com confirmação;
* sugestão de categorias no formulário de criação e edição;
* feedback visual para carregamento, erro e estado vazio;
* documentação automática da API com Swagger.

---

## Pré-requisitos

Antes de executar o projeto, é necessário ter instalado:

* Python 3.11 ou superior
* Node.js
* pnpm

---

## Como executar o backend

Acesse a pasta do backend:

```bash
cd backend
```

Crie o ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual no PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie um arquivo `.env` dentro da pasta `backend` com o seguinte conteúdo:

```env
DATABASE_URL=sqlite:///./database.db
```

Execute as migrações:

```bash
alembic upgrade head
```

### Popular o banco de dados

Após executar as migrações, rode o script de seed para popular o banco com os dados dos arquivos `.csv`:

```bash
python -m app.seed
```

### Iniciar o servidor backend

```bash
uvicorn app.main:app --reload
```

O backend ficará disponível em:

* API: `http://localhost:8000`
* Swagger: `http://localhost:8000/docs`

---

## Como executar o frontend

Abra outro terminal e acesse a pasta do frontend:

```bash
cd frontend
```

Instale as dependências:

```bash
pnpm install
```

Inicie o servidor de desenvolvimento:

```bash
pnpm dev
```

O frontend ficará disponível em:

* Interface: `http://localhost:5173`

---

## Ordem recomendada de execução

Para rodar o projeto corretamente:

## Ordem recomendada de execução

Para rodar o projeto corretamente:

1. acessar a pasta `backend`;
2. criar e ativar o ambiente virtual;
3. instalar as dependências do backend;
4. criar o arquivo `.env`;
5. executar as migrações com Alembic;
6. popular o banco com o script de seed;
7. subir o servidor FastAPI;
8. abrir outro terminal e acessar a pasta `frontend`;
9. instalar as dependências do frontend;
10. iniciar o frontend com `pnpm dev`.

---

## Como utilizar o sistema

Com backend e frontend rodando, é possível:

1. acessar o catálogo de produtos;
2. navegar entre as páginas do grid;
3. buscar produtos por nome ou categoria;
4. clicar em um produto para ver seus detalhes;
5. cadastrar um novo produto;
6. editar um produto existente;
7. excluir um produto do catálogo.

---

## Banco de dados

O projeto utiliza **SQLite** como banco local.

O arquivo do banco é armazenado no backend com o nome:

```bash
database.db
```

A estrutura do banco é gerenciada pelo **Alembic**, e a população inicial é feita a partir de arquivos `.csv` por meio do script de seed.

---

## Documentação da API

A documentação interativa da API pode ser acessada em:

```bash
http://localhost:8000/docs
```

---

## Observações importantes

* o backend deve estar em execução para que o frontend consiga consumir a API;
* o arquivo `.env` deve existir dentro da pasta `backend`;
* as migrações devem ser executadas antes do primeiro uso;
* o banco precisa ser populado com o script de seed para que o catálogo inicial apareça;
* o frontend utiliza `pnpm` como gerenciador de pacotes;
* o projeto utiliza frontend e backend separados, executados em terminais diferentes.