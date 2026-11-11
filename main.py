import sys

from PySide6.QtWidgets import QApplication

from biblioteca.db import conectar, preparar_banco


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")


    from biblioteca.ui.janela_principal import JanelaBiblioteca

    conexao = conectar()
    preparar_banco(conexao)

    janela = JanelaBiblioteca(conexao)
    janela.show()

    codigo = app.exec()

    conexao.close()

    return codigo


if __name__ == "__main__":
    sys.exit(main())