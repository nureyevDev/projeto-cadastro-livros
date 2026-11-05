def inserir_livro(
    conexao,
    titulo,
    autor,
    ano,
    isbn,
):
    cursor = conexao.execute(
        """
        INSERT INTO livro (
            titulo,
            autor,
            ano,
            isbn
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            titulo,
            autor,
            ano,
            isbn,
        ),
    )

    return cursor.lastrowid


def listar_livros(conexao):
    return conexao.execute(
        """
        SELECT
            id,
            titulo,
            autor,
            ano,
            isbn
        FROM livro
        ORDER BY
            titulo COLLATE NOCASE,
            autor COLLATE NOCASE
        """
    ).fetchall()


def pesquisar_livros(
    conexao,
    termo,
):
    filtro = f"%{termo}%"

    return conexao.execute(
        """
        SELECT
            id,
            titulo,
            autor,
            ano,
            isbn
        FROM livro
        WHERE titulo LIKE ? COLLATE NOCASE
           OR autor LIKE ? COLLATE NOCASE
        ORDER BY titulo COLLATE NOCASE
        """,
        (
            filtro,
            filtro,
        ),
    ).fetchall()


def obter_livro(
    conexao,
    livro_id,
):
    return conexao.execute(
        """
        SELECT
            id,
            titulo,
            autor,
            ano,
            isbn
        FROM livro
        WHERE id = ?
        """,
        (livro_id,),
    ).fetchone()


def atualizar_livro(
    conexao,
    livro_id,
    titulo,
    autor,
    ano,
    isbn,
):
    conexao.execute(
        """
        UPDATE livro
        SET
            titulo = ?,
            autor = ?,
            ano = ?,
            isbn = ?
        WHERE id = ?
        """,
        (
            titulo,
            autor,
            ano,
            isbn,
            livro_id,
        ),
    )


def excluir_livro(
    conexao,
    livro_id,
):
    conexao.execute(
        """
        DELETE FROM livro
        WHERE id = ?
        """,
        (livro_id,),
    )