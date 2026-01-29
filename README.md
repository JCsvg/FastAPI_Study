
# 🚀 Task Manager - FastAPI do Zero

![Status](https://img.shields.io/badge/STATUS-EM_DESENVOLVIMENTO-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-005571?style=for-the-badge&logo=fastapi)

> 🚧 **Projeto Educacional**: Este projeto segue a trilha do curso "FastAPI do Zero". Atualmente estou focando na implementação do Banco de Dados e Migrações. 🚧

## 📋 Sobre o Projeto

Este é um projeto de estudo para construção de uma API robusta de gerenciamento de tarefas (To-do List). O objetivo é dominar o ecossistema do FastAPI, aplicando boas práticas desde o início, como **TDD (Test Driven Development)**, validação de dados com **Pydantic** e gerenciamento de dependências com **Poetry**.

No estágio atual, a aplicação já possui a estrutura base e testes configurados, e estou iniciando a integração com **Banco de Dados Relacional (SQLAlchemy)** para persistência dos dados.

## 🛠️ Tecnologias e Ferramentas

- **Linguagem:** Python 3.11+
- **Framework:** FastAPI
- **Banco de Dados:** SQLAlchemy (Em implementação)
- **Migrações:** Alembic (Em implementação)

## 📍 Progresso do Desenvolvimento

Abaixo, o status atual das funcionalidades:

- [x] **Configuração do Ambiente** (Poetry, Git, Taskipy)
- [x] **Sistema de Migrações** (Alembic)
- [x] **Integração com Banco de Dados** (Modelos e SQLAlchemy)  
- [ ] **Estrutura básica da API** (Rotas, Schemas e Settings) 🚧 *<-- Foco Atual*
- [x] **Autenticação e Segurança** (JWT) 
- [ ] **Deploy**

## 🚀 Como Rodar o Projeto Localmente

1. **Clone o repositório:**
```bash
git clone [https://github.com/seu-usuario/nome-do-projeto.git](https://github.com/seu-usuario/nome-do-projeto.git)
cd nome-do-projeto
```

2. **Instale as dependências com Poetry:**
```Bash
poetry install
```
   
3. **Ative o ambiente virtual:**   
```Bash
poetry shell
```

4. **Rode o servidor de desenvolvimento:**
```Bash
task run
# ou: fastapi dev fast_zero/app.py
```
---

_Projeto desenvolvido por **João Carlos** com fins educacionais._
