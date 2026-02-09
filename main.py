"""
Point d'entrée de l'application Bélote
"""
import sys
from PySide6.QtWidgets import QApplication
from views.main_window import MainWindow


def main():
    """Fonction principale pour lancer l'application"""
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
