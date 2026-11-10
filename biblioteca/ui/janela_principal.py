from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtWidgets import QApplication 

from PySide6.QtCore import QDateTime, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDateTimeEdit,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QHeaderView,
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

from biblioteca import repositorio as repo
from biblioteca import servicos


class JanelaBiblioteca(QMainWindow):
    def __init__(self, conexao):
        super().__init__()

        self.conexao = conexao
        self.livro_selecionado_id = None

        self.setWindowTitle(
            "Biblioteca | Cadastro de Livros"
        )
        self.resize(1040, 660)

        self.montar_interface()
        self.montar_menu_temas()
        self.aplicar_tema("escuro")
        self.mostrar_todos()
        
        
    def montar_menu_temas(self):
        menu_exibir = self.menuBar().addMenu("&Exibir")
        menu_temas = menu_exibir.addMenu("&Tema")
        
        self.grupo_temas =QActionGroup(self)
        self.grupo_temas.setExclusive(True)
        
        temas = {
            "claro": "Modo claro",
            "escuro": "Modo escuro",
        }
        
        for nome, titulo in temas.items():
            acao = QAction(titulo, self)
            acao.setCheckable(True)
            acao.setData(nome)
            acao.setChecked(nome == "escuro")
            
            acao.triggered.connect(
                lambda marcado, tema=nome:
                self.aplicar_tema(tema)
            )
            
            self.grupo_temas.addAction(acao)
            menu_temas.addAction(acao)
            
    def aplicar_tema(self, nome_tema):
        if nome_tema == "claro":
            self.aplicar_tema_claro()
        else: 
            self.aplicar_tema_escuro()
            
                            
        def montar_interface(self):
            area_central = QWidget()

        layout_principal = QVBoxLayout(
            area_central
        )
        layout_principal.setContentsMargins(
            24,
            20,
            24,
            20,
        )
        layout_principal.setSpacing(16)

        layout_principal.addWidget(
            self.criar_cabecalho()
        )

        conteudo = QHBoxLayout()
        conteudo.setSpacing(16)

        coluna_acervo = QVBoxLayout()
        coluna_acervo.setSpacing(14)

        coluna_acervo.addWidget(
            self.criar_formulario()
        )
        coluna_acervo.addLayout(
            self.criar_botoes()
        )
        coluna_acervo.addWidget(
            self.criar_tabela(),
            1,
        )

        lateral = self.criar_coluna_lateral()
        lateral.setMinimumWidth(330)
        lateral.setMaximumWidth(390)

        conteudo.addLayout(
            coluna_acervo,
            3,
        )
        conteudo.addWidget(
            lateral,
            1,
        )

        layout_principal.addLayout(
            conteudo,
            1,
        )

        self.mensagem = QLabel(
            "Preencha os dados para iniciar."
        )
        self.mensagem.setObjectName(
            "mensagem"
        )
        self.mensagem.setWordWrap(True)

        layout_principal.addWidget(
            self.mensagem
        )

        self.setCentralWidget(area_central)
        
        
    def criar_cabecalho(self):
        frame = QFrame()
        frame.setObjectName("cabecalho")

        layout = QVBoxLayout(frame)

        titulo = QLabel(
            "Cadastro de Livros"
        )
        titulo.setObjectName("titulo")

        subtitulo = QLabel(
            "Cadastro e manutenção do acervo."
        )
        subtitulo.setObjectName(
            "subtitulo"
        )

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)

        return frame
    
    
    def criar_formulario(self):
        frame = QFrame()
        frame.setObjectName("cartao")

        layout = QVBoxLayout(frame)

        titulo = QLabel(
            "Informações do livro"
        )
        titulo.setObjectName(
            "tituloSecao"
        )

        layout.addWidget(titulo)

        formulario = QFormLayout()
        formulario.setHorizontalSpacing(18)
        formulario.setVerticalSpacing(12)

        formulario.setLabelAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.campo_titulo = QLineEdit()
        self.campo_titulo.setPlaceholderText(
            "Ex.: Beira Rio Beira Vida"
        )

        self.campo_autor = QLineEdit()
        self.campo_autor.setPlaceholderText(
            "Ex.: Assis Brasil"
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

        formulario.addRow(
            "Título *",
            self.campo_titulo,
        )
        formulario.addRow(
            "Autor *",
            self.campo_autor,
        )
        formulario.addRow(
            "Ano",
            self.campo_ano,
        )
        formulario.addRow(
            "ISBN",
            self.campo_isbn,
        )

        layout.addLayout(formulario)

        return frame
    
    
    def criar_botoes(self):
        layout = QHBoxLayout()
        layout.setSpacing(10)

        self.botao_cadastrar = QPushButton(
            "Cadastrar"
        )
        self.botao_cadastrar.setObjectName(
            "botaoPrimario"
        )

        self.botao_pesquisar = QPushButton(
            "Pesquisar"
        )

        self.botao_mostrar_todos = QPushButton(
            "Mostrar todos"
        )

        self.botao_atualizar = QPushButton(
            "Atualizar"
        )

        self.botao_excluir = QPushButton(
            "Excluir"
        )
        self.botao_excluir.setObjectName(
            "botaoPerigo"
        )

        self.botao_limpar = QPushButton(
            "Limpar"
        )

        layout.addWidget(
            self.botao_cadastrar
        )
        layout.addWidget(
            self.botao_pesquisar
        )
        layout.addWidget(
            self.botao_mostrar_todos
        )

        layout.addStretch()

        layout.addWidget(
            self.botao_atualizar
        )
        layout.addWidget(
            self.botao_excluir
        )
        layout.addWidget(
            self.botao_limpar
        )

        self.botao_cadastrar.clicked.connect(
            self.cadastrar_livro
        )
        self.botao_pesquisar.clicked.connect(
            self.pesquisar_livros
        )
        self.botao_mostrar_todos.clicked.connect(
            self.mostrar_todos
        )
        self.botao_atualizar.clicked.connect(
            self.atualizar_livro
        )
        self.botao_excluir.clicked.connect(
            self.excluir_livro
        )
        self.botao_limpar.clicked.connect(
            self.limpar_campos
        )

        return layout
    
    # Cria coluna lateral
        def criar_coluna_lateral(self):
            lateral = QFrame()
            lateral.setObjectName("lateral")

            layout = QVBoxLayout(lateral)
            layout.setSpacing(14)

            layout.addWidget(
                self.criar_painel_leitor()
            )
            layout.addWidget(
                self.criar_painel_emprestimo()
            )
            layout.addWidget(
                self.criar_painel_emprestimos_abertos(),
                1,
            )

            return lateral
        
# Painel de cadastro
        def criar_painel_leitor(self):
            painel = QFrame()
            painel.setObjectName("cartaoLateral")

            layout = QVBoxLayout(painel)

            titulo = QLabel("Cadastro de leitor")
            titulo.setObjectName("tituloSecao")
            layout.addWidget(titulo)

            formulario = QFormLayout()

            self.campo_nome_leitor = QLineEdit()
            self.campo_nome_leitor.setPlaceholderText(
                "Nome completo"
            )

            self.campo_documento_leitor = QLineEdit()
            self.campo_documento_leitor.setPlaceholderText(
                "CPF ou matrícula"
            )

            self.campo_telefone_leitor = QLineEdit()
            self.campo_telefone_leitor.setPlaceholderText(
                "Telefone"
            )

            formulario.addRow(
                "Nome *",
                self.campo_nome_leitor,
            )
            formulario.addRow(
                "Documento *",
                self.campo_documento_leitor,
            )
            formulario.addRow(
                "Telefone",
                self.campo_telefone_leitor,
            )

            self.botao_cadastrar_leitor = QPushButton(
                "Cadastrar leitor"
            )
            self.botao_cadastrar_leitor.clicked.connect(
                self.cadastrar_leitor
            )

            layout.addLayout(formulario)
            layout.addWidget(
                self.botao_cadastrar_leitor
            )

            return painel
    
    def criar_tabela(self):
        frame = QFrame()
        frame.setObjectName("cartao")

        layout = QVBoxLayout(frame)

        topo = QHBoxLayout()

        titulo = QLabel(
            "Livros cadastrados"
        )
        titulo.setObjectName(
            "tituloSecao"
        )

        self.contador = QLabel(
            "0 livro(s)"
        )
        self.contador.setObjectName(
            "contador"
        )

        topo.addWidget(titulo)
        topo.addStretch()
        topo.addWidget(self.contador)

        self.tabela = QTableWidget(0, 5)

        self.tabela.setHorizontalHeaderLabels(
            [
                "ID",
                "Título",
                "Autor",
                "Ano",
                "ISBN",
            ]
        )

        self.tabela.setAlternatingRowColors(
            True
        )

        self.tabela.setSelectionBehavior(
            QAbstractItemView
            .SelectionBehavior
            .SelectRows
        )

        self.tabela.setSelectionMode(
            QAbstractItemView
            .SelectionMode
            .SingleSelection
        )

        self.tabela.setEditTriggers(
            QAbstractItemView
            .EditTrigger
            .NoEditTriggers
        )

        self.tabela.verticalHeader().setVisible(
            False
        )

        cabecalho = self.tabela.horizontalHeader()

        cabecalho.setSectionResizeMode(
            0,
            QHeaderView
            .ResizeMode
            .ResizeToContents,
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
            QHeaderView
            .ResizeMode
            .ResizeToContents,
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
    
    
    def dados_formulario(self):
        return (
            self.campo_titulo.text(),
            self.campo_autor.text(),
            self.campo_ano.value(),
            self.campo_isbn.text(),
        )
        
        
    def cadastrar_livro(self):
        try:
            servicos.cadastrar_livro(
                self.conexao,
                *self.dados_formulario(),
            )

        except servicos.ValidacaoErro as erro:
            self.exibir_aviso(str(erro))
            return

        titulo = (
            self.campo_titulo
            .text()
            .strip()
        )

        self.limpar_campos(
            mensagem=False
        )
        self.mostrar_todos(
            mensagem=False
        )

        self.definir_mensagem(
            f'Livro "{titulo}" cadastrado '
            f"com sucesso.",
            "sucesso",
        )
        
        
    def pesquisar_livros(self):
        termo = " ".join(
            self.campo_titulo
            .text()
            .split()
        )

        if not termo:
            termo = " ".join(
                self.campo_autor
                .text()
                .split()
            )

        if not termo:
            self.exibir_aviso(
                "Digite parte do título ou "
                "do autor no formulário."
            )
            return

        livros = repo.pesquisar_livros(
            self.conexao,
            termo,
        )

        self.preencher_tabela(livros)

        if livros:
            self.definir_mensagem(
                f"{len(livros)} livro(s) encontrado(s).",
                "sucesso",
            )
        else:
            self.definir_mensagem(
                "Nenhum livro encontrado.",
                "aviso",
            )
            
            
    def mostrar_todos(
        self,
        mensagem=True,
    ):
        livros = repo.listar_livros(
            self.conexao
        )

        self.preencher_tabela(livros)

        if mensagem:
            self.definir_mensagem(
                "Todos os livros estão sendo exibidos.",
                "normal",
            )
            
            
    def atualizar_livro(self):
        if self.livro_selecionado_id is None:
            self.exibir_aviso(
                "Selecione um livro para atualizar."
            )
            return

        try:
            servicos.editar_livro(
                self.conexao,
                self.livro_selecionado_id,
                *self.dados_formulario(),
            )

        except servicos.ValidacaoErro as erro:
            self.exibir_aviso(str(erro))
            return

        self.mostrar_todos(
            mensagem=False
        )
        self.limpar_campos(
            mensagem=False
        )

        self.definir_mensagem(
            "Livro atualizado com sucesso.",
            "sucesso",
        )
        
        
    def excluir_livro(self):
        if self.livro_selecionado_id is None:
            self.exibir_aviso(
                "Selecione um livro para excluir."
            )
            return

        resposta = QMessageBox.question(
            self,
            "Confirmar exclusão",
            "Deseja realmente excluir "
            "o livro selecionado?",
            (
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No
            ),
            QMessageBox.StandardButton.No,
        )

        if resposta != QMessageBox.StandardButton.Yes:
            return

        try:
            servicos.remover_livro(
                self.conexao,
                self.livro_selecionado_id,
            )

        except servicos.ValidacaoErro as erro:
            self.exibir_aviso(str(erro))
            return

        self.mostrar_todos(
            mensagem=False
        )
        self.limpar_campos(
            mensagem=False
        )

        self.definir_mensagem(
            "Livro excluído com sucesso.",
            "sucesso",
        )
        
        
    def preencher_tabela(self, livros):
        self.tabela.setRowCount(
            len(livros)
        )

        for linha, livro in enumerate(livros):
            valores = [
                livro["id"],
                livro["titulo"],
                livro["autor"],
                livro["ano"] or "",
                livro["isbn"],
            ]

            for coluna, valor in enumerate(valores):
                item = QTableWidgetItem(
                    str(valor)
                )

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

        self.livro_selecionado_id = int(
            self.tabela.item(
                linha,
                0,
            ).text()
        )

        self.campo_titulo.setText(
            self.tabela.item(
                linha,
                1,
            ).text()
        )

        self.campo_autor.setText(
            self.tabela.item(
                linha,
                2,
            ).text()
        )

        texto_ano = self.tabela.item(
            linha,
            3,
        ).text()

        self.campo_ano.setValue(
            int(texto_ano)
            if texto_ano
            else 0
        )

        self.campo_isbn.setText(
            self.tabela.item(
                linha,
                4,
            ).text()
        )

        self.definir_mensagem(
            "Livro selecionado. "
            "Você pode atualizar ou excluir.",
            "normal",
        )
        
        
    def limpar_campos(
        self,
        mensagem=True,
    ):
        self.livro_selecionado_id = None

        self.campo_titulo.clear()
        self.campo_autor.clear()
        self.campo_ano.setValue(0)
        self.campo_isbn.clear()

        self.tabela.clearSelection()
        self.campo_titulo.setFocus()

        if mensagem:
            self.definir_mensagem(
                "Campos limpos.",
                "normal",
            )

    def exibir_aviso(self, texto):
        self.definir_mensagem(
            texto,
            "aviso",
        )

        QMessageBox.warning(
            self,
            "Cadastro de livros",
            texto,
        )

    def definir_mensagem(
        self,
        texto,
        tipo,
    ):
        self.mensagem.setText(texto)
        self.mensagem.setProperty(
            "tipo",
            tipo,
        )

        self.mensagem.style().unpolish(
            self.mensagem
        )
        self.mensagem.style().polish(
            self.mensagem
        )
        
        
    def aplicar_tema_escuro(self):
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

            QFrame#cabecalho,
            QFrame#cartao {
                background-color: #182338;
                border: 1px solid #34435e;
                border-radius: 11px;
                padding: 12px;
            }

            QLabel#titulo {
                font-family: "Segoe UI Semibold";
                font-size: 22pt;
                color: #ffffff;
            }

            QLabel#subtitulo,
            QLabel#contador {
                color: #b4c0d4;
            }

            QLabel#tituloSecao {
                font-family: "Segoe UI Semibold";
                font-size: 12pt;
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

            QPushButton#botaoPrimario {
                background-color: #3867d6;
                border-color: #4b7bec;
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
    
    def aplicar_tema_claro(self):
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #F0FFF0;
            }

            QWidget {
                color: #1F2D24;
                font-family: "Segoe UI";
                font-size: 10pt;
            }

            QFrame#cabecalho {
                background-color: #DDF5E3;
                border: 1px solid #A9CEB3;
                border-radius: 12px;
                padding: 12px;
            }

            QFrame#cartao {
                background-color: #FFFFFF;
                border: 1px solid #BED8C5;
                border-radius: 10px;
                padding: 12px;
            }

            QLabel#titulo {
                color: #183F2B;
                font-family: "Segoe UI Semibold";
                font-size: 22pt;
            }

            QLabel#subtitulo,
            QLabel#contador {
                color: #587060;
            }

            QLabel#tituloSecao {
                color: #244D35;
                font-family: "Segoe UI Semibold";
                font-size: 12pt;
            }

            QLabel#mensagem {
                background-color: #E2F4E6;
                color: #244D35;
                border: 1px solid #9CC8A7;
                border-radius: 6px;
                padding: 9px;
            }

            QLabel#mensagem[tipo="sucesso"] {
                background-color: #D9F2E1;
                color: #185C32;
                border-color: #73B987;
            }

            QLabel#mensagem[tipo="aviso"] {
                background-color: #FFF0EA;
                color: #843C2E;
                border-color: #D79586;
            }

            QLineEdit,
            QSpinBox {
                background-color: #FFFFFF;
                color: #1F2D24;
                border: 1px solid #A9C9B1;
                border-radius: 7px;
                padding: 8px;
                min-height: 22px;
                selection-background-color: #347A4C;
                selection-color: #FFFFFF;
            }

            QLineEdit:focus,
            QSpinBox:focus {
                border: 2px solid #438A5E;
            }

            QPushButton {
                background-color: #E1F1E5;
                color: #244D35;
                border: 1px solid #9EC7A8;
                border-radius: 7px;
                padding: 8px 14px;
                min-height: 24px;
            }

            QPushButton:hover {
                background-color: #CBE6D2;
                border-color: #73B987;
            }

            QPushButton:pressed {
                background-color: #B8DAC1;
            }

            QPushButton#botaoPrimario {
                background-color: #347A4C;
                color: #FFFFFF;
                border-color: #2C6941;
                font-family: "Segoe UI Semibold";
            }

            QPushButton#botaoPrimario:hover {
                background-color: #28653D;
            }

            QPushButton#botaoPerigo {
                background-color: #A94442;
                color: #FFFFFF;
                border-color: #8F3634;
            }

            QPushButton#botaoPerigo:hover {
                background-color: #8F3634;
            }

            QTableWidget {
                background-color: #FFFFFF;
                alternate-background-color: #EDF8EF;
                color: #1F2D24;
                gridline-color: #C4DDCA;
                border: 1px solid #A9C9B1;
                border-radius: 7px;
            }

            QTableWidget::item {
                padding: 7px;
            }

            QTableWidget::item:selected {
                background-color: #70A980;
                color: #FFFFFF;
            }

            QHeaderView::section {
                background-color: #347A4C;
                color: #FFFFFF;
                border: none;
                border-right: 1px solid #5A956C;
                padding: 8px;
                font-family: "Segoe UI Semibold";
            }

            QMenuBar {
                background-color: #DDF5E3;
                color: #1F2D24;
            }

            QMenuBar::item:selected {
                background-color: #CBE6D2;
            }

            QMenu {
                background-color: #FFFFFF;
                color: #1F2D24;
                border: 1px solid #A9C9B1;
            }

            QMenu::item:selected {
                background-color: #CBE6D2;
            }
            """
        )