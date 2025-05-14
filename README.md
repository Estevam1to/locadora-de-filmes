# Trabalho Prático 01 - Sistema de Locadora de Filmes

Sistema de gerenciamento para locadora de filmes com funcionalidades de conversão de arquivos de dados, desenvolvido como atividade acadêmica.

## Sobre o Projeto

Este projeto implementa uma API RESTful para gerenciar uma locadora de filmes, permitindo o cadastro e consulta de clientes, filmes e aluguéis. Além disso, oferece funcionalidades de conversão de arquivos entre diferentes formatos (CSV, XML, ZIP) e cálculo de hash para verificação de integridade.

## Equipe

Projeto desenvolvido por:
- **Luís Estevam**: Endpoints de conversão de arquivos, gerenciamento de clientes e estruturação do repositório.
- **Luís Fernando**: Endpoints e lógica de filmes, sistema de aluguéis e logs.

> **Nota**: O repositório contém commits principalmente de um integrante pois ele foi responsável pela estruturação do código. O desenvolvimento foi realizado em conjunto utilizando compartilhamento de arquivos.

## Funcionalidades

### Sistema de Locadora
- Cadastro e gerenciamento de clientes
- Catalogação de filmes com informações como título, gênero e ano de lançamento
- Sistema de aluguéis com controle de status e datas de devolução
- Consultas e filtros para clientes, filmes e aluguéis

### Conversão de Arquivos
- Conversão de CSV para XML
- Compactação de arquivos CSV para ZIP
- Cálculo de hash SHA-256 para verificação de integridade dos arquivos

## Pré-requisitos

- Python 3.8 ou superior (recomendado: Python 3.10)
- UV (gerenciador de pacotes Python)

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/convert-files.git
cd convert-files
```

2. Crie um ambiente virtual e instale as dependências com UV:

```bash
# Crie o ambiente virtual com Python 3.10
uv venv --python 3.10

# Instale as dependências do projeto
uv sync
```

## Execução

1. Ative o ambiente virtual:

```bash
# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

2. Execute a aplicação:

```bash
cd src
uv run app.py
```

## Estrutura do Projeto

```
convert-files/
├── src/                # Diretório principal do código-fonte
│   ├── app.py          # Ponto de entrada da aplicação
│   ├── config/         # Configurações (logs, etc.)
│   ├── data/           # Arquivos CSV de dados
│   │   ├── alugueis.csv
│   │   ├── clientes.csv
│   │   └── filmes.csv
│   ├── routes/         # Endpoints da API (controllers)
│   │   ├── aluguel.py
│   │   ├── cliente.py
│   │   ├── convert_files.py
│   │   └── filme.py
│   ├── schemas/        # Modelos de dados (Pydantic)
│   │   ├── aluguel.py
│   │   ├── cliente.py
│   │   └── filme.py
│   └── utils/          # Utilitários e funções auxiliares
│       ├── csv_utils.py
│       └── xml_utils.py
├── pyproject.toml      # Configuração do projeto e dependências
└── README.md           # Este arquivo
```

## API Endpoints

A API oferece os seguintes endpoints principais:

### Filmes
- `GET /filmes`: Lista todos os filmes
- `GET /filmes/{id}`: Obtém detalhes de um filme específico
- `POST /filmes`: Cadastra um novo filme
- `PUT /filmes/{id}`: Atualiza informações de um filme
- `DELETE /filmes/{id}`: Remove um filme

### Clientes
- `GET /clientes`: Lista todos os clientes
- `GET /clientes/{id}`: Obtém detalhes de um cliente específico
- `POST /clientes`: Cadastra um novo cliente
- `PUT /clientes/{id}`: Atualiza informações de um cliente
- `DELETE /clientes/{id}`: Remove um cliente

### Aluguéis
- `GET /alugueis`: Lista todos os aluguéis
- `GET /alugueis/{id}`: Obtém detalhes de um aluguel específico
- `POST /alugueis`: Registra um novo aluguel
- `PUT /alugueis/{id}`: Atualiza informações de um aluguel
- `DELETE /alugueis/{id}`: Remove um aluguel

### Conversão de Arquivos
- `GET /converter/compactar/{entidade}`: Compacta um arquivo CSV para ZIP
- `GET /converter/hash/{entidade}`: Calcula o hash SHA-256 de um arquivo CSV
- `GET /converter/converter/{entidade}/xml`: Converte um arquivo CSV para XML

## Documentação da API

A documentação completa da API está disponível em `/docs` após iniciar o servidor (http://localhost:5000/docs).