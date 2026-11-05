from biblioteca import repositorio as repo


class ValidacaoErro(Exception):
    pass


def normalizar_texto(valor):
    return " ".join(
        (valor or "").split()
    )


def validar_dados(
    titulo,
    autor,
    ano,
    isbn,
):
    titulo = normalizar_texto(titulo)
    autor = normalizar_texto(autor)
    isbn = (isbn or "").strip()

    if not titulo:
        raise ValidacaoErro(
            "Informe o título do livro."
        )

    if not autor:
        raise ValidacaoErro(
            "Informe o autor do livro."
        )

    if ano in (None, 0, ""):
        ano = None
    else:
        ano = int(ano)

        if ano < 0 or ano > 2100:
            raise ValidacaoErro(
                "Informe um ano válido."
            )

    return titulo, autor, ano, isbn


def cadastrar_livro(
    conexao,
    titulo,
    autor,
    ano,
    isbn,
):
    dados = validar_dados(
        titulo,
        autor,
        ano,
        isbn,
    )

    with conexao:
        return repo.inserir_livro(
            conexao,
            *dados,
        )


def editar_livro(
    conexao,
    livro_id,
    titulo,
    autor,
    ano,
    isbn,
):
    livro = repo.obter_livro(
        conexao,
        livro_id,
    )

    if livro is None:
        raise ValidacaoErro(
            "O livro selecionado não existe mais."
        )

    dados = validar_dados(
        titulo,
        autor,
        ano,
        isbn,
    )

    with conexao:
        repo.atualizar_livro(
            conexao,
            livro_id,
            *dados,
        )


def remover_livro(
    conexao,
    livro_id,
):
    livro = repo.obter_livro(
        conexao,
        livro_id,
    )

    if livro is None:
        raise ValidacaoErro(
            "O livro selecionado não existe mais."
        )

    with conexao:
        repo.excluir_livro(
            conexao,
            livro_id,
        )
