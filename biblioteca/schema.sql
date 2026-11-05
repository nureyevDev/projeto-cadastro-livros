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