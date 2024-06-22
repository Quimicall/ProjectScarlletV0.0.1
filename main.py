from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QDialog, QHBoxLayout, QPushButton, QMenu
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QPoint
import sys
import shop  # Importando o módulo shop

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.label = QLabel()
        pixmap = QPixmap("imagens/scarlletTeste.jpg")  # Substitua pelo caminho da sua imagem
        self.label.setPixmap(pixmap)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.label.customContextMenuRequested.connect(self.show_context_menu)

        layout.addWidget(self.label)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.drag_position = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = None

    def show_context_menu(self, position: QPoint):
        context_menu = QMenu(self)
        loja_action = context_menu.addAction("Shop")
        loja_action.triggered.connect(self.show_loja)
        status_action = context_menu.addAction("Status")
        status_action.triggered.connect(self.show_status)
        interagir_action = context_menu.addAction("Interact")
        interagir_action.triggered.connect(self.show_interagir)
        diy_action = context_menu.addAction("DIY")
        diy_action.triggered.connect(self.show_diy)
        sistema_action = context_menu.addAction("System")
        sistema_action.triggered.connect(self.show_sistema)

        context_menu.exec_(self.label.mapToGlobal(position))

    def show_loja(self):
        self.open_dialog("Shop")

    def show_status(self):
        self.open_dialog("Status")

    def show_interagir(self):
        self.open_dialog("Interact")

    def show_diy(self):
        self.open_dialog("DIY")

    def show_sistema(self):
        self.open_dialog("System")

    def open_dialog(self, title):
        if title == "Shop":
            dialog = shop.ShopDialog(self)
        else:
            dialog = QDialog(self)
            dialog.setWindowTitle(title)
            dialog_layout = QVBoxLayout()
            dialog_label = QLabel(f"Content of {title}")
            dialog_layout.addWidget(dialog_label)
            dialog.setLayout(dialog_layout)
        
        dialog.exec()

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    