from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtWidgets import QApplication

from PySide6.QtCore import QDateTime, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QAbstractSpinBox,
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
    QScrollArea,
    QSizePolicy,
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
        self.resize(1450, 850)
        self.setMinimumSize(1180, 760)

        self.montar_interface()
        self.montar_menu_temas()
        self.aplicar_tema("escuro")
        self.mostrar_todos()
        self.atualizar_coluna_lateral()
        
        
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

        layout_principal = QVBoxLayout(area_central)
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
        lateral.setMinimumWidth(400)

        rolagem_lateral = QScrollArea()
        rolagem_lateral.setObjectName("rolagemLateral")
        rolagem_lateral.setWidget(lateral)
        rolagem_lateral.setWidgetResizable(True)
        rolagem_lateral.setFrameShape(QFrame.Shape.NoFrame)
        rolagem_lateral.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        conteudo.addLayout(
            coluna_acervo,
            5,
        )

        conteudo.addWidget(rolagem_lateral, 2)

        layout_principal.addLayout(
            conteudo,
            1,
        )

        self.mensagem = QLabel(
            "Preencha os dados para iniciar."
        )
        self.mensagem.setObjectName("mensagem")
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
        self.campo_ano.setButtonSymbols(
            QAbstractSpinBox.ButtonSymbols.NoButtons
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

        self.botao_atualizar.setEnabled(False)
        self.botao_excluir.setEnabled(False)

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
        painel.setMinimumHeight(260)
        painel.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Fixed,
        )

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
        
    def criar_painel_emprestimo(self):
        painel = QFrame()
        painel.setObjectName("cartaoLateral")
        painel.setMinimumHeight(300)
        painel.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Fixed,
        )

        layout = QVBoxLayout(painel)

        titulo = QLabel("Novo empréstimo")
        titulo.setObjectName("tituloSecao")
        layout.addWidget(titulo)

        formulario = QFormLayout()

        self.combo_leitor = QComboBox()
        self.combo_exemplar = QComboBox()

        self.data_retirada = QDateTimeEdit(
            QDateTime.currentDateTime()
        )
        self.data_retirada.setDisplayFormat(
            "dd/MM/yyyy HH:mm"
        )
        self.data_retirada.setReadOnly(True)
        self.data_retirada.setButtonSymbols(
            QAbstractSpinBox.ButtonSymbols.NoButtons
        )

        self.data_devolucao = QDateTimeEdit(
            QDateTime.currentDateTime().addDays(7)
        )
        self.data_devolucao.setDisplayFormat(
            "dd/MM/yyyy HH:mm"
        )
        self.data_devolucao.setReadOnly(True)
        self.data_devolucao.setButtonSymbols(
            QAbstractSpinBox.ButtonSymbols.NoButtons
        )

        formulario.addRow(
            "Leitor",
            self.combo_leitor,
        )
        formulario.addRow(
            "Exemplar",
            self.combo_exemplar,
        )
        formulario.addRow(
            "Retirada",
            self.data_retirada,
        )
        formulario.addRow(
            "Previsão",
            self.data_devolucao,
        )

        self.botao_emprestar = QPushButton(
            "Registrar empréstimo"
        )
        self.botao_emprestar.setObjectName(
            "botaoPrimario"
        )
        self.botao_emprestar.clicked.connect(
            self.registrar_emprestimo
        )

        layout.addLayout(formulario)
        layout.addWidget(self.botao_emprestar)

        return painel
    
    def atualizar_coluna_lateral(self):
        leitores = repo.listar_leitores(
            self.conexao
        )

        self.combo_leitor.clear()
        self.combo_leitor.addItem(
            "Selecione um leitor",
            None,
        )

        for leitor in leitores:
            self.combo_leitor.addItem(
                (
                    f"{leitor['nome']} "
                    f"({leitor['documento']})"
                ),
                leitor["id"],
            )

        exemplares = (
            repo.listar_exemplares_disponiveis(
                self.conexao
            )
        )

        self.combo_exemplar.clear()
        self.combo_exemplar.addItem(
            "Selecione um exemplar",
            None,
        )

        for exemplar in exemplares:
            self.combo_exemplar.addItem(
                (
                    f"{exemplar['titulo']} | "
                    f"{exemplar['codigo']}"
                ),
                exemplar["id"],
            )

        emprestimos = (
            repo.listar_emprestimos_abertos(
                self.conexao
            )
        )

        self.tabela_emprestimos.setRowCount(
            len(emprestimos)
        )

        for linha, emprestimo in enumerate(
            emprestimos
        ):
            valores = [
                emprestimo["id"],
                emprestimo["leitor"],
                (
                    f"{emprestimo['titulo']} "
                    f"({emprestimo['exemplar']})"
                ),
            ]

            for coluna, valor in enumerate(valores):
                self.tabela_emprestimos.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(str(valor)),
                )

        agora = QDateTime.currentDateTime()

        self.data_retirada.setDateTime(agora)
        self.data_devolucao.setDateTime(
            agora.addDays(7)
        )
        

    
    def criar_painel_emprestimos_abertos(self):
        painel = QFrame()
        painel.setObjectName("cartaoLateral")
        painel.setMinimumHeight(240)
        painel.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding,
        )

        layout = QVBoxLayout(painel)

        titulo = QLabel("Empréstimos em aberto")
        titulo.setObjectName("tituloSecao")
        layout.addWidget(titulo)

        self.tabela_emprestimos = QTableWidget(
            0,
            3,
        )
        self.tabela_emprestimos.setHorizontalHeaderLabels(
            [
                "ID",
                "Leitor",
                "Livro",
            ]
        )
        self.tabela_emprestimos.setSelectionBehavior(
            QAbstractItemView
            .SelectionBehavior
            .SelectRows
        )
        self.tabela_emprestimos.setSelectionMode(
            QAbstractItemView
            .SelectionMode
            .SingleSelection
        )
        self.tabela_emprestimos.setEditTriggers(
            QAbstractItemView
            .EditTrigger
            .NoEditTriggers
        )
        self.tabela_emprestimos.verticalHeader().setVisible(
            False
        )

        cabecalho = (
            self.tabela_emprestimos
            .horizontalHeader()
        )
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

        self.botao_devolver = QPushButton(
            "Registrar devolução"
        )
        self.botao_devolver.setObjectName(
            "botaoPerigo"
        )
        self.botao_devolver.clicked.connect(
            self.registrar_devolucao
        )

        layout.addWidget(
            self.tabela_emprestimos
        )
        layout.addWidget(
            self.botao_devolver
        )

        return painel
    
    def cadastrar_leitor(self):
        try:
            servicos.cadastrar_leitor(
                self.conexao,
                self.campo_nome_leitor.text(),
                self.campo_documento_leitor.text(),
                self.campo_telefone_leitor.text(),
            )

        except servicos.ValidacaoErro as erro:
            self.exibir_aviso(str(erro))
            return

        self.campo_nome_leitor.clear()
        self.campo_documento_leitor.clear()
        self.campo_telefone_leitor.clear()

        self.atualizar_coluna_lateral()

        self.definir_mensagem(
            "Leitor cadastrado com sucesso.",
            "sucesso",
        )
        
    def registrar_emprestimo(self):
        leitor_id = self.combo_leitor.currentData()
        exemplar_id = (
            self.combo_exemplar.currentData()
        )

        try:
            servicos.registrar_emprestimo(
                self.conexao,
                leitor_id,
                exemplar_id,
            )

        except servicos.ValidacaoErro as erro:
            self.exibir_aviso(str(erro))
            return

        self.atualizar_coluna_lateral()

        self.definir_mensagem(
            "Empréstimo registrado com sucesso.",
            "sucesso",
        )
    
    def registrar_devolucao(self):
        linha = self.tabela_emprestimos.currentRow()

        if linha < 0:
            self.exibir_aviso(
                "Selecione um empréstimo."
            )
            return

        emprestimo_id = int(
            self.tabela_emprestimos.item(
                linha,
                0,
            ).text()
        )

        resposta = QMessageBox.question(
            self,
            "Confirmar devolução",
            "Confirmar a devolução do exemplar?",
            (
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No
            ),
            QMessageBox.StandardButton.No,
        )

        if resposta != QMessageBox.StandardButton.Yes:
            return

        try:
            servicos.registrar_devolucao(
                self.conexao,
                emprestimo_id,
            )

        except servicos.ValidacaoErro as erro:
            self.exibir_aviso(str(erro))
            return

        self.atualizar_coluna_lateral()

        self.definir_mensagem(
            "Devolução registrada com sucesso.",
            "sucesso",
        )
    
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
        self.livro_selecionado_id = None
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

        self.botao_atualizar.setEnabled(False)
        self.botao_excluir.setEnabled(False)

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

        self.botao_atualizar.setEnabled(True)
        self.botao_excluir.setEnabled(True)

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
        self.botao_atualizar.setEnabled(False)
        self.botao_excluir.setEnabled(False)

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
            
            QFrame#lateral {
                background-color: transparent;
                border: none;
            }

            QScrollArea#rolagemLateral {
                background-color: transparent;
                border: none;
            }

            QScrollArea#rolagemLateral > QWidget > QWidget {
                background-color: transparent;
            }

            QMenuBar {
                background-color: #182338;
                color: #f1f5fb;
                border-bottom: 1px solid #34435e;
            }

            QMenuBar::item {
                background-color: transparent;
                padding: 7px 12px;
            }

            QMenuBar::item:selected {
                background-color: #263550;
            }

            QMenu {
                background-color: #182338;
                color: #f1f5fb;
                border: 1px solid #34435e;
                padding: 5px;
            }

            QMenu::item {
                padding: 7px 28px 7px 12px;
            }

            QMenu::item:selected {
                background-color: #344764;
            }

            QFrame#cartaoLateral {
                background-color: #182338;
                border: 1px solid #34435e;
                border-radius: 10px;
                padding: 10px;
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
            QSpinBox,
            QComboBox,
            QDateTimeEdit {
                background-color: #111b2c;
                color: #f1f5fb;
                border: 1px solid #34435e;
                border-radius: 7px;
                padding: 7px 8px;
                min-height: 28px;
            }


            QLineEdit:focus,
            QSpinBox:focus,
            QComboBox:focus,
            QDateTimeEdit:focus {
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

            QPushButton:disabled {
                background-color: #1b263a;
                color: #71809a;
                border-color: #2d3a52;
            }

            QComboBox QAbstractItemView {
                background-color: #111b2c;
                color: #f1f5fb;
                border: 1px solid #34435e;
                selection-background-color: #294b7a;
                selection-color: #ffffff;
                outline: none;
            }

            QAbstractSpinBox::up-button,
            QAbstractSpinBox::down-button {
                width: 0px;
                height: 0px;
                border: none;
            }

            QAbstractSpinBox::up-arrow,
            QAbstractSpinBox::down-arrow {
                image: none;
                width: 0px;
                height: 0px;
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
                background-color: #EEEEE0;
            }

            QWidget {
                color: #292C26;
                font-family: "Segoe UI";
                font-size: 10pt;
            }

            QMenuBar {
                background-color: #DDDCCF;
                color: #292C26;
                border-bottom: 1px solid #AAA99C;
            }

            QMenuBar::item {
                background-color: transparent;
                padding: 7px 12px;
            }

            QMenuBar::item:selected {
                background-color: #CCCBBE;
            }

            QMenu {
                background-color: #FFFFFF;
                color: #292C26;
                border: 1px solid #AAA99C;
                padding: 5px;
            }

            QMenu::item {
                padding: 7px 28px 7px 12px;
            }

            QMenu::item:selected {
                background-color: #D8D8C9;
                color: #30392B;
            }

            QFrame#cabecalho {
                background-color: #DDDCCF;
                border: 1px solid #AAA99C;
                border-radius: 12px;
                padding: 14px;
            }

            QFrame#cartao {
                background-color: #FFFFFF;
                border: 1px solid #B9B8AA;
                border-radius: 10px;
                padding: 12px;
            }

            QFrame#lateral {
                background-color: transparent;
                border: none;
            }

            QFrame#cartaoLateral {
                background-color: #FAFAF4;
                border: 1px solid #B9B8AA;
                border-radius: 10px;
                padding: 12px;
            }

            QLabel {
                background-color: transparent;
            }

            QLabel#titulo {
                color: #30392B;
                font-family: "Segoe UI Semibold";
                font-size: 22pt;
            }

            QLabel#subtitulo {
                color: #62665B;
                font-size: 10pt;
            }

            QLabel#tituloSecao {
                color: #3F5038;
                font-family: "Segoe UI Semibold";
                font-size: 12pt;
                padding-bottom: 5px;
            }

            QLabel#contador {
                color: #62665B;
                font-family: "Segoe UI Semibold";
            }

            QLabel#mensagem {
                background-color: #E1E4D5;
                color: #30392B;
                border: 1px solid #AAA99C;
                border-radius: 7px;
                padding: 10px;
            }

            QLabel#mensagem[tipo="sucesso"] {
                background-color: #DCE9D5;
                color: #294522;
                border-color: #809A72;
            }

            QLabel#mensagem[tipo="aviso"] {
                background-color: #F5DDD4;
                color: #7A2D22;
                border-color: #C98272;
            }

            QLineEdit,
            QSpinBox,
            QComboBox,
            QDateTimeEdit {
                background-color: #FFFFFF;
                color: #292C26;
                border: 1px solid #AAA99C;
                border-radius: 7px;
                padding: 7px 9px;
                min-height: 28px;
                selection-background-color: #617653;
                selection-color: #FFFFFF;
            }

            QLineEdit:hover,
            QSpinBox:hover,
            QComboBox:hover,
            QDateTimeEdit:hover {
                border-color: #75816B;
            }

            QLineEdit:focus,
            QSpinBox:focus,
            QComboBox:focus,
            QDateTimeEdit:focus {
                border: 2px solid #617653;
            }

            QLineEdit:disabled,
            QSpinBox:disabled,
            QComboBox:disabled,
            QDateTimeEdit:disabled {
                background-color: #E8E8DD;
                color: #85877E;
                border-color: #C5C5BA;
            }

            QComboBox::drop-down {
                width: 28px;
                border: none;
                border-left: 1px solid #B3B2A6;
                background-color: #E3E3D6;
            }

            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                color: #292C26;
                border: 1px solid #AAA99C;
                selection-background-color: #D5DDCF;
                selection-color: #30392B;
                outline: none;
            }

            QAbstractSpinBox::up-button,
            QAbstractSpinBox::down-button {
                width: 24px;
                background-color: #E3E3D6;
                border: none;
                border-left: 1px solid #B3B2A6;
            }

            QAbstractSpinBox::up-button:hover,
            QAbstractSpinBox::down-button:hover {
                background-color: #D2D2C4;
            }

            QPushButton {
                background-color: #DFE2D7;
                color: #394331;
                border: 1px solid #AAAEA0;
                border-radius: 7px;
                padding: 8px 14px;
                min-height: 27px;
                font-family: "Segoe UI Semibold";
            }

            QPushButton:hover {
                background-color: #CED4C5;
                border-color: #7B8871;
            }

            QPushButton:pressed {
                background-color: #BBC4B2;
            }

            QPushButton:disabled {
                background-color: #E8E8DE;
                color: #92948C;
                border-color: #CECEC4;
            }

            QPushButton#botaoPrimario {
                background-color: #526746;
                color: #FFFFFF;
                border-color: #405137;
            }

            QPushButton#botaoPrimario:hover {
                background-color: #657D57;
                border-color: #526746;
            }

            QPushButton#botaoPrimario:pressed {
                background-color: #405137;
            }

            QPushButton#botaoPerigo {
                background-color: #98433E;
                color: #FFFFFF;
                border-color: #7E3733;
            }

            QPushButton#botaoPerigo:hover {
                background-color: #B0524C;
            }

            QPushButton#botaoPerigo:pressed {
                background-color: #79332F;
            }

            QTableWidget {
                background-color: #FFFFFF;
                alternate-background-color: #F5F4EA;
                color: #292C26;
                gridline-color: #D1D0C3;
                border: 1px solid #AAA99C;
                border-radius: 7px;
                outline: none;
            }

            QTableWidget::item {
                padding: 7px;
                border-bottom: 1px solid #E2E1D7;
            }

            QTableWidget::item:hover {
                background-color: #E7E8DC;
            }

            QTableWidget::item:selected {
                background-color: #708461;
                color: #FFFFFF;
            }

            QHeaderView::section {
                background-color: #526746;
                color: #FFFFFF;
                border: none;
                border-right: 1px solid #718466;
                border-bottom: 1px solid #405137;
                padding: 9px;
                font-family: "Segoe UI Semibold";
            }

            QScrollBar:vertical {
                background-color: #E7E7DB;
                width: 12px;
                margin: 0;
            }

            QScrollBar::handle:vertical {
                background-color: #A5AA9C;
                border-radius: 6px;
                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #7D8773;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0;
            }

            QScrollBar:horizontal {
                background-color: #E7E7DB;
                height: 12px;
                margin: 0;
            }

            QScrollBar::handle:horizontal {
                background-color: #A5AA9C;
                border-radius: 6px;
                min-width: 30px;
            }

            QScrollBar::handle:horizontal:hover {
                background-color: #7D8773;
            }

            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0;
            }

            QToolTip {
                background-color: #3F5038;
                color: #FFFFFF;
                border: 1px solid #30392B;
                padding: 5px;
            }
            """
        )
