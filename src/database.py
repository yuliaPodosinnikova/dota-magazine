import json
import os

DATA_DIR = "data"
ITEMS_PATH = os.path.join(DATA_DIR, "shop_items.json")
SAVE_PATH = os.path.join(DATA_DIR, "hero_save.json")

DEFAULT_ITEMS = [
    {"name": "Tango", "cost": 90, "bonus": "Восстанавливает 100 HP на линии", "components": None},
    {"name": "Iron Branch", "cost": 50, "bonus": "+1 ко всем атрибутам (+10 HP, +1 урон)", "components": None},
    {"name": "Blight Stone", "cost": 300, "bonus": "-2 брони врагу (увеличивает ваш урон на +5)", "components": None},
    {"name": "Boots of Speed", "cost": 500, "bonus": "+45 к скорости передвижения (шанс уклониться от удара врага)", "components": None},
    {"name": "Gloves of Haste", "cost": 450, "bonus": "+20 к скорости атаки", "components": None},
    {"name": "Morbid Mask", "cost": 900, "bonus": "+15% к вампиризму (лечит при атаке)", "components": None},
    {"name": "Quarterstaff", "cost": 875, "bonus": "+10 к урону, +10 к скорости атаки", "components": None},
    {"name": "Sacred Relic", "cost": 3400, "bonus": "+55 к урону", "components": None},
    
    {"name": "Power Treads", "cost": 1000, "bonus": "+15 урон, +25 скор. атаки, +100 HP", "components": ["Boots of Speed", "Gloves of Haste", "Iron Branch"]},
    {"name": "Mask of Madness", "cost": 1775, "bonus": "+20% к вампиризму, +30 к урону", "components": ["Morbid Mask", "Quarterstaff"]},
    {"name": "Divine Rapier", "cost": 5600, "bonus": "+350 к урону (выпадает при смерти)", "components": ["Sacred Relic"]},
    {"name": "Aegis of the Immortal", "cost": 0, "bonus": "Защищает от одной смерти", "components": None}
]

def init_db():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    if not os.path.exists(ITEMS_PATH):
        with open(ITEMS_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_ITEMS, f, indent=4, ensure_ascii=False)

def load_shop_items():
    init_db()
    with open(ITEMS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def load_hero_progress():
    init_db()
    if not os.path.exists(SAVE_PATH):
        return {"gold": 600, "inventory": [], "hp": 500}
    
    try:
        with open(SAVE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "hp" not in data:
                data["hp"] = 500
            return data
    except json.JSONDecodeError:
        return {"gold": 600, "inventory": [], "hp": 500}

def save_hero_progress(gold, inventory, hp=500):
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump({"gold": gold, "inventory": inventory, "hp": hp}, f, indent=4, ensure_ascii=False)
