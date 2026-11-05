import sys

from PySide6.QtWidgets import QApplication

from biblioteca.db import (
    conectar,
    preparar_banco,
)
from biblioteca.ui.janela_principal import (
    JanelaBiblioteca,
)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    conexao = conectar()
    preparar_banco(conexao)

    janela = JanelaBiblioteca(conexao)
    janela.show()

    codigo = app.exec()

    conexao.close()

    return codigo


if __name__ == "__main__":
    sys.exit(main())