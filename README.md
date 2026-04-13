# Sistema de Gerenciamento de E-Commerce

Aplicação full stack para gerenciamento de produtos em um sistema de e-commerce. O sistema foi desenvolvido com frontend e backend separados, permitindo listar, buscar, visualizar detalhes, cadastrar, editar e remover produtos, além de exibir informações relacionadas a vendas e avaliações.

## Tecnologias utilizadas

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

## Estrutura do projeto

```bash
rocketlab2026/
├── backend/
│   ├── alembic/
│   ├── app/
│   ├── .env
│   ├── alembic.ini
│   ├── requirements.txt
│   └── database.db
└── frontend/
```

## Pré-requisitos

Antes de executar o projeto, é necessário ter instalado:

* Python 3.11 ou superior
* Node.js
* pnpm

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

Crie um arquivo `.env` com o seguinte conteúdo:

```env
DATABASE_URL=sqlite:///./database.db
```

Execute as migrações do banco de dados:

```bash
alembic upgrade head
```

Inicie a aplicação:

```bash
uvicorn app.main:app --reload
```

O backend ficará disponível em:

* API: `http://localhost:8000`
* Swagger: `http://localhost:8000/docs`

## Como executar o frontend

Acesse a pasta do frontend:

```bash
cd frontend
```

Instale as dependências:

```bash
pnpm install
```

Execute o servidor de desenvolvimento:

```bash
pnpm dev
```

O frontend ficará disponível em:

* Interface: `http://localhost:5173`

## Banco de dados

O projeto utiliza SQLite como banco de dados local. O arquivo do banco é criado automaticamente no backend com o nome:

```bash
database.db
```

A estrutura do banco é controlada por migrações do Alembic.

## Observações importantes

* O backend deve estar rodando para que o frontend consiga consumir a API.
* O arquivo `.env` precisa existir dentro da pasta `backend`.
* As migrações devem ser executadas antes de iniciar a aplicação pela primeira vez.
* O frontend utiliza `pnpm` como gerenciador de pacotes.
* O banco de dados é local e persistido em arquivo SQLite.

## Funcionalidades

As funcionalidades implementadas e/ou planejadas para o sistema incluem:

* listagem de produtos;
* busca de produtos;
* visualização de detalhes do produto;
* cadastro de produtos;
* edição de produtos;
* remoção de produtos;
* exibição de informações de vendas;
* exibição de avaliações;
* cálculo da média das avaliações.

## Documentação da API

A documentação interativa da API pode ser acessada via Swagger em:

```bash
http://localhost:8000/docs
```
