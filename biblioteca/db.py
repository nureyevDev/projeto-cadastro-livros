import sqlite3
from pathlib import Path


PASTA_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_BANCO = PASTA_PROJETO / "biblioteca.db"
CAMINHO_ESQUEMA = Path(__file__).with_name("schema.sql")


def conectar(caminho=None):
    caminho_banco = caminho or CAMINHO_BANCO

    conexao = sqlite3.connect(
        str(caminho_banco)
    )

    conexao.row_factory = sqlite3.Row

    conexao.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conexao


def preparar_banco(conexao):
    esquema = CAMINHO_ESQUEMA.read_text(
        encoding="utf-8"
    )

    conexao.executescript(esquema)
    conexao.commit()