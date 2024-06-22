from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QDialog, QHBoxLayout, QPushButton, QSizePolicy
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
        context_menu_widget = QWidget()
        context_menu_layout = QHBoxLayout()

        loja_button = QPushButton("Shop")
        loja_button.clicked.connect(self.show_loja)
        status_button = QPushButton("Status")
        status_button.clicked.connect(self.show_status)
        interagir_button = QPushButton("Interact")
        interagir_button.clicked.connect(self.show_interagir)
        diy_button = QPushButton("DIY")
        diy_button.clicked.connect(self.show_diy)
        sistema_button = QPushButton("System")
        sistema_button.clicked.connect(self.show_sistema)

        context_menu_layout.addWidget(loja_button)
        context_menu_layout.addWidget(status_button)
        context_menu_layout.addWidget(interagir_button)
        context_menu_layout.addWidget(diy_button)
        context_menu_layout.addWidget(sistema_button)

        context_menu_widget.setLayout(context_menu_layout)
        context_menu_widget.setWindowFlags(Qt.Popup)

        # Calcula a posição para centralizar o menu na parte inferior da imagem
        label_rect = self.label.rect()
        global_position = self.label.mapToGlobal(label_rect.bottomLeft())
        global_position.setX(global_position.x() + label_rect.width() / 2 - context_menu_widget.sizeHint().width() / 2)
        global_position.setY(global_position.y())

        context_menu_widget.move(global_position)
        context_menu_widget.show()

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
