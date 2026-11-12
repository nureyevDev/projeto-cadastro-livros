# Cadastro de Livros

Aplicação desktop desenvolvida em Python e PySide6 para cadastro e consulta de livros, leitores e empréstimos de uma pequena biblioteca.

## Funcionalidades

- Cadastro, pesquisa, atualização e exclusão de livros;
- Cadastro de leitores;
- Registro de empréstimos e devoluções;
- Validação dos campos obrigatórios;
- Exibição dos livros em tabela;
- Pesquisa por título ou autor;
- Dados persistidos em SQLite;
- Tema claro e escuro;
- Coluna lateral com rolagem para evitar corte dos botões em telas menores.

## Como executar

Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

Execute a aplicação:

```powershell
python main.py
```

O banco `biblioteca.db` será criado automaticamente na pasta do projeto.
