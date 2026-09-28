import json
import os

DATA_DIR = "data"
ITEMS_PATH = os.path.join(DATA_DIR, "shop_items.json")
SAVE_PATH = os.path.join(DATA_DIR, "hero_save.json")

# Начальный список предметов, если файла еще нет
DEFAULT_ITEMS = [
    {"name": "Iron Branch", "cost": 50, "bonus": "+1 ко всем атрибутам"},
    {"name": "Blight Stone", "cost": 300, "bonus": "-2 брони врагу при атаке"},
    {"name": "Boots of Speed", "cost": 500, "bonus": "+45 к скорости передвижения"},
    {"name": "Morbid Mask", "cost": 900, "bonus": "+15% к вампиризму"},
    {"name": "Shadow Blade", "cost": 3000, "bonus": "+20 к урону, невидимость"},
    {"name": "Sacred Relic", "cost": 3400, "bonus": "+55 к урону"},
    {"name": "Divine Rapier", "cost": 5600, "bonus": "+350 к урону (выпадает при смерти)"}
]

def init_db():
    """Создает базовые файлы данных, если их нет."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    if not os.path.exists(ITEMS_PATH):
        with open(ITEMS_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_ITEMS, f, indent=4, ensure_ascii=False)

def load_shop_items():
    """Загружает товары магазина."""
    init_db()
    with open(ITEMS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def load_hero_progress():
    """Загружает золото и инвентарь игрока."""
    init_db()
    if not os.path.exists(SAVE_PATH):
        return {"gold": 1000, "inventory": []}  # Стартовый капитал 1000 золота
    
    try:
        with open(SAVE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"gold": 1000, "inventory": []}

def save_hero_progress(gold, inventory):
    """Сохраняет текущий прогресс игрока."""
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump({"gold": gold, "inventory": inventory}, f, indent=4, ensure_ascii=False)
