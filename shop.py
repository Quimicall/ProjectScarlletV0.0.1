# shop.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox
import sqlite3

class ShopDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Shop")
        
        layout = QVBoxLayout()
        
        # Itens da loja
        self.items = [
            {"name": "Vodka", "description": "Uma bebida forte", "price": 10},
            {"name": "Arroz com feijão", "description": "Uma refeição excelente", "price": 15},
            {"name": "Suco de uva", "description": "Um suco brasileiro", "price": 5}
        ]
        
        # Conectar ao banco de dados
        self.conn = sqlite3.connect("inventory.db")
        self.cursor = self.conn.cursor()
        
        # Criar tabelas se não existirem
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price INTEGER
            );

            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER,
                FOREIGN KEY (item_id) REFERENCES items(id)
            );
        """)
        
        # Adicionar itens à loja
        for item in self.items:
            item_label = QLabel(f"{item['name']}: {item['description']} - Price: ${item['price']}")
            buy_button = QPushButton("Buy")
            buy_button.clicked.connect(lambda _, i=item: self.buy_item(i))
            layout.addWidget(item_label)
            layout.addWidget(buy_button)
        
        self.setLayout(layout)
    
    def buy_item(self, item):
        try:
            # Verificar se o jogador tem dinheiro suficiente
            money = self.get_money()
            if money < item['price']:
                QMessageBox.warning(self, "Insufficient Funds", "You don't have enough money to buy this item.")
                return
            
            # Deduzir o preço do item do dinheiro do jogador
            new_money = money - item['price']
            self.cursor.execute("UPDATE player SET money = ?", (new_money,))
            
            # Adicionar o item ao inventário do jogador
            self.cursor.execute("INSERT INTO inventory (item_id) VALUES (?)", (item['id'],))
            self.conn.commit()
            
            QMessageBox.information(self, "Purchase Successful", f"You have bought {item['name']}!")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            
    def get_money(self):
        self.cursor.execute("SELECT money FROM player")
        money = self.cursor.fetchone()
        if money:
            return money[0]
        else:
            return 0
    
    def closeEvent(self, event):
        self.conn.close()
        event.accept()

class InventoryManager:
    def __init__(self):
        self.conn = sqlite3.connect("inventory.db")
        self.cursor = self.conn.cursor()
    
    def get_inventory(self):
        self.cursor.execute("""
            SELECT items.name, items.description
            FROM inventory
            JOIN items ON inventory.item_id = items.id
        """)
        return self.cursor.fetchall()
    
    def close(self):
        self.conn.close()
