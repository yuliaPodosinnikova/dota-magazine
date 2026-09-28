from src.database import load_shop_items, load_hero_progress, save_hero_progress

class DotaShop:
    def __init__(self):
        self.shop_items = load_shop_items()
        progress = load_hero_progress()
        self.gold = progress["gold"]
        self.inventory = progress["inventory"]

    def show_items(self):
        """Выводит список товаров в лавке."""
        print("\n⚔️ --- АССОРТИМЕНТ ПОТАЙНОЙ ЛАВКИ ---")
        for idx, item in enumerate(self.shop_items, 1):
            print(f"{idx}. {item['name']} —  {item['cost']} gold | Эффект: {item['bonus']}")

    def buy_item(self, item_index):
        """Логика покупки предмета."""
        if item_index < 0 or item_index >= len(self.shop_items):
            print("Ошибка: Предмета с таким номером не существует в лавке!")
            return

        selected_item = self.shop_items[item_index]
        
        if self.gold >= selected_item["cost"]:
            self.gold -= selected_item["cost"]
            self.inventory.append(selected_item["name"])
            save_hero_progress(self.gold, self.inventory)
            print(f"Вы купили {selected_item['name']}! Нажмите TAB в игре (шутка).")
        else:
            print(f"Недостаточно золота! Вам не хватает {selected_item['cost'] - self.gold} золота для покупки {selected_item['name']}.")

    def farm_gold(self):
        """Симуляция убийства крипов (фарм)."""
        earned = 150  # Золото за пачку крипов
        self.gold += earned
        save_hero_progress(self.gold, self.inventory)
        print(f"Вы отфармили пачку крипов на линии! Получено +{earned} ")

    def show_inventory(self):
        """Показывает золото и вещи героя."""
        print("\n --- ИНВЕНТАРЬ ГЕРОЯ ---")
        print(f"Текущее золото: {self.gold}")
        if not self.inventory:
            print("Инвентарь пуст. Вы бегаете «голым»!")
        else:
            for item in self.inventory:
                print(f" - [{item}]")
