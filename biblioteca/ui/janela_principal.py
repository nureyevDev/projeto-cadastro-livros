from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
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
        self.aplicar_estilo()
        self.mostrar_todos()
        
        
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
        layout_principal.addWidget(
            self.criar_formulario()
        )
        layout_principal.addLayout(
            self.criar_botoes()
        )
        layout_principal.addWidget(
            self.criar_tabela(),
            1,
        )

        self.mensagem = QLabel(
            "Preencha os dados do livro para iniciar."
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
            "Cadastro e manutenção do acervo "
            "da biblioteca com SQLite."
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
    
    
    