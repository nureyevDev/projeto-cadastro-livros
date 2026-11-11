from biblioteca import repositorio as repo
from datetime import datetime, timedelta


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
        livro_id = repo.inserir_livro(
            conexao,
            *dados,
        )

        codigo = f"EX-{livro_id:04d}-01"

        repo.inserir_exemplar(
            conexao,
            livro_id,
            codigo,
        )

        return livro_id
        


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

# Cadastrar leitor
def cadastrar_leitor(
    conexao,
    nome,
    documento,
    telefone="",
):
    nome = normalizar_texto(nome)
    documento = "".join(
        caractere
        for caractere in (documento or "")
        if caractere.isalnum()
    )

    telefone = (telefone or "").strip()

    if not nome:
        raise ValidacaoErro(
            "Informe o nome do leitor."
        )

    if not documento:
        raise ValidacaoErro(
            "Informe o CPF ou a matrícula do leitor."
        )

    existente = repo.buscar_leitor_por_documento(
        conexao,
        documento,
    )

    if existente:
        raise ValidacaoErro(
            "Já existe um leitor com esse documento."
        )

    with conexao:
        return repo.inserir_leitor(
            conexao,
            nome,
            documento,
            telefone,
        )
        
# Registrar emprestimo
def registrar_emprestimo(
    conexao,
    leitor_id,
    exemplar_id,
    dias=7,
):
    if leitor_id is None:
        raise ValidacaoErro(
            "Selecione um leitor."
        )

    if exemplar_id is None:
        raise ValidacaoErro(
            "Selecione um exemplar disponível."
        )

    retirada = datetime.now()
    devolucao_prevista = retirada + timedelta(
        days=dias
    )

    with conexao:
        emprestimo_id = repo.inserir_emprestimo(
            conexao,
            leitor_id,
            exemplar_id,
            retirada.isoformat(
                sep=" ",
                timespec="seconds",
            ),
            devolucao_prevista.isoformat(
                sep=" ",
                timespec="seconds",
            ),
        )

        repo.atualizar_situacao_exemplar(
            conexao,
            exemplar_id,
            "emprestado",
        )

    return emprestimo_id

# Registrar devoluçao
def registrar_devolucao(
    conexao,
    emprestimo_id,
):
    emprestimo = repo.obter_emprestimo_aberto(
        conexao,
        emprestimo_id,
    )

    if emprestimo is None:
        raise ValidacaoErro(
            "O empréstimo não existe ou já foi encerrado."
        )

    devolucao = datetime.now().isoformat(
        sep=" ",
        timespec="seconds",
    )

    with conexao:
        repo.encerrar_emprestimo(
            conexao,
            emprestimo_id,
            devolucao,
        )

        repo.atualizar_situacao_exemplar(
            conexao,
            emprestimo["exemplar_id"],
            "disponivel",
        )
