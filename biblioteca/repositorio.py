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

# Funçao leitores
def inserir_leitor(
    conexao,
    nome,
    documento,
    telefone,
):
    cursor = conexao.execute(
        """
        INSERT INTO leitor (
            nome,
            documento,
            telefone
        )
        VALUES (?, ?, ?)
        """,
        (
            nome,
            documento,
            telefone,
        ),
    )  
    
    return cursor.lastrowid

def buscar_leitor_por_documento(
    conexao,
    documento,
):
    return conexao.execute(
        """
        SELECT
            id,
            nome,
            documento,
            telefone,
            ativo
        FROM leitor
        WHERE documento = ?
        """,
        (documento,),
    ).fetchone()
    
def listar_leitores(conexao):
    return conexao.execute(
        """
        SELECT
        id,
        nome,
        documento,
        telefone
    FROM leitor
    WHERE ativo = 1
    ORDER BY nome COLLATE NOCASE
        """
    ).fetchall()
    
# Funçao Exemplares
def inserir_exemplar(
    conexao,
    livro_id,
    codigo,
):
    cursor = conexao.execute(
        """
        INSERT INTO exemplar (
            livro_id,
            codigo
        )
        VALUES (?, ?)
        """,
        (
            livro_id,
            codigo,
        ),
    )
    
    return cursor.lastrowid

def listar_exemplares_disponiveis(conexao):
    return conexao.execute(
        """
        SELECT
            e.id,
            e.codigo,
            l.titulo,
            l.autor
        FROM exemplar e
        JOIN livro l
            ON l.id = e.livro_id
        WHERE e.situacao = 'disponivel'
        ORDER BY l.titulo, e.codigo
        """
    ).fetchall()
    
def atualizar_situacao_exemplar(
    conexao,
    exemplar_id,
    situacao
):
    conexao.execute(
        """
        UPDATE exemplar
        SET situacao = ?
        WHERE id = ?
        """,
        (
            situacao,
            exemplar_id,
        ),
    )
    
# Funçao Emprestimo
def inserir_emprestimo(
    conexao,
    leitor_id,
    exemplar_id,
    retirada,
    devolucao_prevista,
):
    cursor = conexao.execute(
        """
        INSERT INTO emprestimo (
            leitor_id, 
            exemplar_id,
            retirada,
            devolucao_prevista
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            leitor_id,
            exemplar_id,
            retirada,
            devolucao_prevista,
        ),
    )
    
    return cursor.lastrowid

def listar_emprestimos_abertos(conexao):
    return conexao.execute(
        """
        SELECT
            emp.id,
            lei.nome AS leitor,
            liv.titulo,
            ex.codigo AS exemplar,
            emp.retirada,
            emp.devolucao_prevista
        FROM emprestimo emp
        JOIN leitor lei
            ON lei.id = emp.leitor_id
        JOIN exemplar ex
            ON ex.id = emp.exemplar_id
        JOIN livro liv
            ON liv.id = ex.livro_id
        WHERE emp.devolucao_real IS NULL
        ORDER BY emp.retirada DESC
        """
    ).fetchall()
    
def obter_emprestimo_aberto(
    conexao,
    emprestimo_id
):
    return conexao.execute(
        """
        SELECT
            id,
            leitor_id,
            exemplar_id,
            retirada,
            devolucao_prevista
        FROM emprestimo
        WHERE id = ?
          AND devolucao_real IS NULL
          """,
          (emprestimo_id,),
    ).fetchone()
    
def encerrar_emprestimo(
    conexao,
    emprestimo_id,
    devolucao_real,
):
    conexao.execute(
        """
        UPDATE emprestimo
        SET devolucao_real = ?
        WHERE id = ?
        """,
        (
            devolucao_real,
            emprestimo_id
        ),
    )
    
def contar_exemplares_do_livro(
    conexao,
    livro_id,
):
    return conexao.execute(
        """
        SELECT COUNT(*)
        FROM exemplar
        WHERE livro_id = ?
        """,
        (livro_id,),
    ).fetchone()[0]
