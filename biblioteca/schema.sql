CREATE TABLE IF NOT EXISTS leitor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    documento TEXT NOT NULL UNIQUE,
    telefone TEXT NOT NULL DEFAULT '',
    ativo INTEGER NOT NULL DEFAULT 1,
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS exemplar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    livro_id INTEGER NOT NULL,
    codigo TEXT NOT NULL UNIQUE,
    situacao TEXT NOT NULL DEFAULT 'disponivel'
        CHECK (
            situacao IN (
                'disponivel',
                'emprestado',
                'manutencao'
            )
        ),
    FOREIGN KEY (livro_id)
        REFERENCES livro(id)
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS emprestimo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    leitor_id INTEGER NOT NULL,
    exemplar_id INTEGER NOT NULL,
    retirada TEXT NOT NULL,
    devolucao_prevista TEXT NOT NULL,
    devolucao_real TEXT,
    FOREIGN KEY (leitor_id)
        REFERENCES leitor(id)
        ON DELETE RESTRICT,
    FOREIGN KEY (exemplar_id)
        REFERENCES exemplar(id)
        ON DELETE RESTRICT
);

CREATE UNIQUE INDEX IF NOT EXISTS
idx_emprestimo_exemplar_aberto
ON emprestimo(exemplar_id)
WHERE devolucao_real IS NULL;

CREATE INDEX IF NOT EXISTS
idx_leitor_nome
ON leitor(nome);

CREATE INDEX IF NOT EXISTS
idx_emprestimo_leitor
ON emprestimo(leitor_id);

CREATE TABLE IF NOT EXISTS livro (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    ano INTEGER,
    isbn TEXT NOT NULL DEFAULT '',
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_livro_titulo
ON livro(titulo);

CREATE INDEX IF NOT EXISTS idx_livro_autor
ON livro(autor);

CREATE INDEX IF NOT EXISTS idx_livro_isbn
ON livro(isbn);