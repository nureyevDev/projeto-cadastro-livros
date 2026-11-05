import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class JanelaBiblioteca(QMainWindow):
    def __init__(self):
        super().__init__()

        self.livros = []
        self.proximo_id = 1

        self.setWindowTitle("Biblioteca | Cadastro de Livros")
        self.resize(980, 620)

        self.montar_interface()
        self.aplicar_estilo()

    def montar_interface(self):
        area_central = QWidget()
        layout_principal = QVBoxLayout(area_central)
        layout_principal.setContentsMargins(24, 20, 24, 20)
        layout_principal.setSpacing(16)

        cabecalho = self.criar_cabecalho()
        formulario = self.criar_formulario()
        botoes = self.criar_botoes()
        tabela = self.criar_tabela()

        layout_principal.addWidget(cabecalho)
        layout_principal.addWidget(formulario)
        layout_principal.addLayout(botoes)
        layout_principal.addWidget(tabela, 1)

        self.mensagem = QLabel(
            "Preencha os dados do livro para iniciar."
        )
        self.mensagem.setObjectName("mensagem")
        self.mensagem.setWordWrap(True)

        layout_principal.addWidget(self.mensagem)

        self.setCentralWidget(area_central)

    def criar_cabecalho(self):
        frame = QFrame()
        frame.setObjectName("cabecalho")

        layout = QVBoxLayout(frame)

        titulo = QLabel("Cadastro de Livros")
        titulo.setObjectName("titulo")

        subtitulo = QLabel(
            "Gerencie o acervo da biblioteca de forma simples e organizada."
        )
        subtitulo.setObjectName("subtitulo")

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)

        return frame

    def criar_formulario(self):
        frame = QFrame()
        frame.setObjectName("cartao")

        layout = QVBoxLayout(frame)

        titulo_formulario = QLabel("Informações do livro")
        titulo_formulario.setObjectName("tituloSecao")
        layout.addWidget(titulo_formulario)

        formulario = QFormLayout()
        formulario.setLabelAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )
        formulario.setHorizontalSpacing(18)
        formulario.setVerticalSpacing(12)

        self.campo_titulo = QLineEdit()
        self.campo_titulo.setPlaceholderText(
            "Ex.: Dom Casmurro"
        )

        self.campo_autor = QLineEdit()
        self.campo_autor.setPlaceholderText(
            "Ex.: Machado de Assis"
        )

        self.campo_ano = QSpinBox()
        self.campo_ano.setRange(0, 2100)
        self.campo_ano.setSpecialValueText(
            "Não informado"
        )

        self.campo_isbn = QLineEdit()
        self.campo_isbn.setPlaceholderText(
            "Ex.: 9788535910663"
        )
        self.campo_isbn.setMaxLength(30)

        formulario.addRow("Título *", self.campo_titulo)
        formulario.addRow("Autor *", self.campo_autor)
        formulario.addRow("Ano", self.campo_ano)
        formulario.addRow("ISBN", self.campo_isbn)

        layout.addLayout(formulario)

        return frame

    def criar_botoes(self):
        layout = QHBoxLayout()
        layout.setSpacing(10)

        self.botao_cadastrar = QPushButton("Cadastrar")
        self.botao_cadastrar.setObjectName("botaoPrimario")

        self.botao_pesquisar = QPushButton("Pesquisar")
        self.botao_mostrar_todos = QPushButton("Mostrar todos")

        self.botao_atualizar = QPushButton("Atualizar")
        self.botao_atualizar.setEnabled(False)
        self.botao_atualizar.setToolTip(
            "Será implementado em uma etapa posterior."
        )

        self.botao_excluir = QPushButton("Excluir")
        self.botao_excluir.setObjectName("botaoPerigo")
        self.botao_excluir.setEnabled(False)
        self.botao_excluir.setToolTip(
            "Será implementado em uma etapa posterior."
        )

        self.botao_limpar = QPushButton("Limpar")

        layout.addWidget(self.botao_cadastrar)
        layout.addWidget(self.botao_pesquisar)
        layout.addWidget(self.botao_mostrar_todos)
        layout.addStretch()
        layout.addWidget(self.botao_atualizar)
        layout.addWidget(self.botao_excluir)
        layout.addWidget(self.botao_limpar)

        self.botao_cadastrar.clicked.connect(
            self.cadastrar_livro
        )
        self.botao_pesquisar.clicked.connect(
            self.pesquisar_livro
        )
        self.botao_mostrar_todos.clicked.connect(
            self.mostrar_todos
        )
        self.botao_limpar.clicked.connect(
            self.limpar_campos
        )

        return layout

    def criar_tabela(self):
        frame = QFrame()
        frame.setObjectName("cartao")

        layout = QVBoxLayout(frame)

        topo = QHBoxLayout()

        titulo_tabela = QLabel("Livros cadastrados")
        titulo_tabela.setObjectName("tituloSecao")

        self.contador = QLabel("0 livro(s)")
        self.contador.setObjectName("contador")

        topo.addWidget(titulo_tabela)
        topo.addStretch()
        topo.addWidget(self.contador)

        self.tabela = QTableWidget(0, 5)
        self.tabela.setHorizontalHeaderLabels(
            ["ID", "Título", "Autor", "Ano", "ISBN"]
        )
        self.tabela.setAlternatingRowColors(True)
        self.tabela.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.tabela.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.tabela.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.tabela.verticalHeader().setVisible(False)

        cabecalho = self.tabela.horizontalHeader()
        cabecalho.setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.ResizeToContents,
        )
        cabecalho.setSectionResizeMode(
            1,
            QHeaderView.ResizeMode.Stretch,
        )
        cabecalho.setSectionResizeMode(
            2,
            QHeaderView.ResizeMode.Stretch,
        )
        cabecalho.setSectionResizeMode(
            3,
            QHeaderView.ResizeMode.ResizeToContents,
        )
        cabecalho.setSectionResizeMode(
            4,
            QHeaderView.ResizeMode.Stretch,
        )

        self.tabela.itemSelectionChanged.connect(
            self.carregar_livro_selecionado
        )

        layout.addLayout(topo)
        layout.addWidget(self.tabela)

        return frame

    def cadastrar_livro(self):
        titulo = self.campo_titulo.text().strip()
        autor = self.campo_autor.text().strip()
        ano = self.campo_ano.value()
        isbn = self.campo_isbn.text().strip()

        if not titulo:
            self.exibir_aviso(
                "Informe o título do livro."
            )
            self.campo_titulo.setFocus()
            return

        if not autor:
            self.exibir_aviso(
                "Informe o autor do livro."
            )
            self.campo_autor.setFocus()
            return

        livro = {
            "id": self.proximo_id,
            "titulo": titulo,
            "autor": autor,
            "ano": ano if ano > 0 else "",
            "isbn": isbn,
        }

        self.livros.append(livro)
        self.proximo_id += 1

        self.preencher_tabela(self.livros)
        self.limpar_campos(
            mensagem=False
        )

        self.mensagem.setText(
            f'Livro "{titulo}" cadastrado com sucesso.'
        )
        self.mensagem.setProperty(
            "tipo",
            "sucesso",
        )
        self.atualizar_estilo_mensagem()

    def pesquisar_livro(self):
        termo, confirmado = QInputDialog.getText(
            self,
            "Pesquisar livros",
            "Digite parte do título ou do autor:",
        )

        if not confirmado:
            return

        termo = termo.strip().lower()

        if not termo:
            self.exibir_aviso(
                "Informe um título ou autor para pesquisar."
            )
            return

        encontrados = [
            livro
            for livro in self.livros
            if termo in livro["titulo"].lower()
            or termo in livro["autor"].lower()
        ]

        self.preencher_tabela(encontrados)

        if encontrados:
            self.mensagem.setText(
                f"{len(encontrados)} livro(s) encontrado(s)."
            )
            self.mensagem.setProperty(
                "tipo",
                "sucesso",
            )
        else:
            self.mensagem.setText(
                "Nenhum livro encontrado."
            )
            self.mensagem.setProperty(
                "tipo",
                "aviso",
            )

        self.atualizar_estilo_mensagem()

    def mostrar_todos(self):
        self.preencher_tabela(self.livros)

        self.mensagem.setText(
            "Todos os livros cadastrados estão sendo exibidos."
        )
        self.mensagem.setProperty(
            "tipo",
            "normal",
        )
        self.atualizar_estilo_mensagem()

    def preencher_tabela(self, livros):
        self.tabela.setRowCount(len(livros))

        for linha, livro in enumerate(livros):
            valores = [
                livro["id"],
                livro["titulo"],
                livro["autor"],
                livro["ano"],
                livro["isbn"],
            ]

            for coluna, valor in enumerate(valores):
                item = QTableWidgetItem(str(valor))

                if coluna in (0, 3):
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignCenter
                    )

                self.tabela.setItem(
                    linha,
                    coluna,
                    item,
                )

        self.tabela.clearSelection()
        self.contador.setText(
            f"{len(livros)} livro(s)"
        )

    def carregar_livro_selecionado(self):
        linha = self.tabela.currentRow()

        if linha < 0:
            return

        self.campo_titulo.setText(
            self.tabela.item(linha, 1).text()
        )
        self.campo_autor.setText(
            self.tabela.item(linha, 2).text()
        )

        texto_ano = self.tabela.item(
            linha,
            3,
        ).text()

        self.campo_ano.setValue(
            int(texto_ano) if texto_ano else 0
        )

        self.campo_isbn.setText(
            self.tabela.item(linha, 4).text()
        )

        self.mensagem.setText(
            "Livro selecionado. "
            "Atualização e exclusão serão implementadas posteriormente."
        )
        self.mensagem.setProperty(
            "tipo",
            "normal",
        )
        self.atualizar_estilo_mensagem()

    def limpar_campos(self, mensagem=True):
        self.campo_titulo.clear()
        self.campo_autor.clear()
        self.campo_ano.setValue(0)
        self.campo_isbn.clear()
        self.tabela.clearSelection()
        self.campo_titulo.setFocus()

        if mensagem:
            self.mensagem.setText(
                "Campos limpos."
            )
            self.mensagem.setProperty(
                "tipo",
                "normal",
            )
            self.atualizar_estilo_mensagem()

    def exibir_aviso(self, texto):
        self.mensagem.setText(texto)
        self.mensagem.setProperty(
            "tipo",
            "aviso",
        )
        self.atualizar_estilo_mensagem()

        QMessageBox.warning(
            self,
            "Cadastro de livros",
            texto,
        )

    def atualizar_estilo_mensagem(self):
        self.mensagem.style().unpolish(
            self.mensagem
        )
        self.mensagem.style().polish(
            self.mensagem
        )

    def aplicar_estilo(self):
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #101827;
            }

            QWidget {
                color: #f1f5fb;
                font-family: "Segoe UI";
                font-size: 10pt;
            }

            QFrame#cabecalho {
                background-color: #182338;
                border: 1px solid #34435e;
                border-radius: 12px;
                padding: 12px;
            }

            QFrame#cartao {
                background-color: #182338;
                border: 1px solid #34435e;
                border-radius: 10px;
                padding: 12px;
            }

            QLabel#titulo {
                font-family: "Segoe UI Semibold";
                font-size: 22pt;
                color: #ffffff;
            }

            QLabel#subtitulo {
                color: #b4c0d4;
                font-size: 10pt;
            }

            QLabel#tituloSecao {
                font-family: "Segoe UI Semibold";
                font-size: 12pt;
                color: #f1f5fb;
                padding-bottom: 6px;
            }

            QLabel#contador {
                color: #b4c0d4;
            }

            QLabel#mensagem {
                background-color: #1c3155;
                color: #dce9ff;
                border: 1px solid #466ca6;
                border-radius: 6px;
                padding: 9px;
            }

            QLabel#mensagem[tipo="sucesso"] {
                background-color: #143b32;
                color: #d7f4e8;
                border-color: #287c6d;
            }

            QLabel#mensagem[tipo="aviso"] {
                background-color: #4b2d24;
                color: #ffe4dc;
                border-color: #dc5a64;
            }

            QLineEdit,
            QSpinBox {
                background-color: #111b2c;
                color: #f1f5fb;
                border: 1px solid #34435e;
                border-radius: 7px;
                padding: 8px;
                min-height: 22px;
            }

            QLineEdit:focus,
            QSpinBox:focus {
                border: 2px solid #82aaff;
            }

            QPushButton {
                background-color: #263550;
                color: #f1f5fb;
                border: 1px solid #465878;
                border-radius: 7px;
                padding: 8px 14px;
                min-height: 24px;
            }

            QPushButton:hover {
                background-color: #344764;
            }

            QPushButton:disabled {
                background-color: #202b3d;
                color: #76839a;
                border-color: #303d52;
            }

            QPushButton#botaoPrimario {
                background-color: #3867d6;
                color: #ffffff;
                border: 1px solid #4b7bec;
                font-family: "Segoe UI Semibold";
            }

            QPushButton#botaoPrimario:hover {
                background-color: #4b7bec;
            }

            QPushButton#botaoPerigo {
                background-color: #5b2a32;
                color: #ffdce0;
                border-color: #8c3e49;
            }

            QTableWidget {
                background-color: #111b2c;
                alternate-background-color: #1d2a42;
                color: #f1f5fb;
                gridline-color: #34435e;
                border: 1px solid #34435e;
                border-radius: 7px;
            }

            QTableWidget::item {
                padding: 7px;
            }

            QTableWidget::item:selected {
                background-color: #294b7a;
                color: #ffffff;
            }

            QHeaderView::section {
                background-color: #263550;
                color: #ffffff;
                border: none;
                border-right: 1px solid #34435e;
                padding: 8px;
                font-family: "Segoe UI Semibold";
            }
            """
        )


def main():
    app = QApplication(sys.argv)

    janela = JanelaBiblioteca()
    janela.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()