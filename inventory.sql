-- inventory.sql
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

CREATE TABLE IF NOT EXISTS player (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    money INTEGER
);

-- Inicializa o jogador com $100 se ele ainda não existir
INSERT INTO player (money)
SELECT 100
WHERE NOT EXISTS (SELECT 1 FROM player);

-- Adiciona os itens à tabela items se ainda não existirem
INSERT INTO items (name, description, price)
SELECT 'Vodka', 'Uma bebida forte', 10
WHERE NOT EXISTS (SELECT 1 FROM items WHERE name = 'Vodka');

INSERT INTO items (name, description, price)
SELECT 'Arroz com feijão', 'Uma refeição excelente', 15
WHERE NOT EXISTS (SELECT 1 FROM items WHERE name = 'Arroz com feijão');

INSERT INTO items (name, description, price)
SELECT 'Suco de uva', 'Um suco brasileiro', 5
WHERE NOT EXISTS (SELECT 1 FROM items WHERE name = 'Suco de uva');
