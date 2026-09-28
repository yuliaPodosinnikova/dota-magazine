import random
import time
from src.database import load_shop_items, load_hero_progress, save_hero_progress

class DotaShop:
    def __init__(self):
        self.shop_items = load_shop_items()
        progress = load_hero_progress()
        self.gold = progress["gold"]
        self.inventory = progress["inventory"]
        self.hp = progress.get("hp", 500)
        self.max_slots = 6

    def get_hero_stats(self):
        stats = {
            "max_hp": 500,
            "damage": 50,
            "lifesteal": 0.0,
            "evasion": 0.0
        }
        for item in self.inventory:
            if item == "Iron Branch":
                stats["max_hp"] += 10
                stats["damage"] += 1
            elif item == "Blight Stone":
                stats["damage"] += 5
            elif item == "Boots of Speed":
                stats["evasion"] += 0.15
            elif item == "Morbid Mask":
                stats["lifesteal"] += 0.15
            elif item == "Quarterstaff":
                stats["damage"] += 10
            elif item == "Sacred Relic":
                stats["damage"] += 55
            elif item == "Power Treads":
                stats["max_hp"] += 100
                stats["damage"] += 15
            elif item == "Mask of Madness":
                stats["lifesteal"] += 0.20
                stats["damage"] += 30
            elif item == "Divine Rapier":
                stats["damage"] += 350
        return stats

    def show_items(self):
        print("\n--- АССОРТИМЕНТ ПОТАЙНОЙ ЛАВКИ ---")
        for idx, item in enumerate(self.shop_items, 1):
            if item["cost"] == 0:
                continue
            type_label = "[СБОРНЫЙ]" if item.get("components") else "[БАЗОВЫЙ]"
            print(f"{idx}. {type_label} {item['name']} — {item['cost']} gold | {item['bonus']}")

    def check_crafting(self):
        for item in self.shop_items:
            components = item.get("components")
            if components:
                temp_inv = self.inventory.copy()
                has_all = True
                for comp in components:
                    if comp in temp_inv:
                        temp_inv.remove(comp)
                    else:
                        has_all = False
                        break
                
                if has_all:
                    self.inventory = temp_inv
                    self.inventory.append(item["name"])
                    print(f"Успех! Ваши предметы объединились в: {item['name']}!")
                    save_hero_progress(self.gold, self.inventory, self.hp)
                    self.check_crafting()
                    break

    def buy_item(self, item_index):
        if item_index < 0 or item_index >= len(self.shop_items):
            print("Ошибка: Предмета с таким номером нет в лавке!")
            return

        selected_item = self.shop_items[item_index]
        if selected_item["cost"] == 0:
            print("Ошибка: Этот предмет нельзя купить!")
            return
        
        if not selected_item.get("components") and len(self.inventory) >= self.max_slots:
            print("Ошибка: Рюкзак забит! У вас уже 6 предметов. Продайте что-нибудь.")
            return

        if self.gold >= selected_item["cost"]:
            self.gold -= selected_item["cost"]
            if selected_item["name"] == "Tango":
                stats = self.get_hero_stats()
                self.hp = min(stats["max_hp"], self.hp + 100)
                print("Вы купили и сразу использовали Tango. Восстановлено 100 HP.")
            else:
                self.inventory.append(selected_item["name"])
                print(f"Вы купили {selected_item['name']}!")
            
            self.check_crafting()
            save_hero_progress(self.gold, self.inventory, self.hp)
        else:
            print(f"Ошибка: Недостаточно золота! Не хватает {selected_item['cost'] - self.gold} золота.")

    def sell_item(self, inv_index):
        if inv_index < 0 or inv_index >= len(self.inventory):
            print("Ошибка: Нет предмета с таким номером в инвентаре!")
            return
        
        item_name = self.inventory[inv_index]
        item_cost = next((item["cost"] for item in self.shop_items if item["name"] == item_name), 0)
        sell_price = item_cost // 2

        self.gold += sell_price
        self.inventory.pop(inv_index)
        save_hero_progress(self.gold, self.inventory, self.hp)
        print(f"Вы продали {item_name} торговцу за {sell_price} золота.")

    def handle_death(self):
        if "Aegis of the Immortal" in self.inventory:
            self.inventory.remove("Aegis of the Immortal")
            stats = self.get_hero_stats()
            self.hp = stats["max_hp"]
            print("Вы погибли! Но Aegis of the Immortal возвращает вас к жизни с полным HP!")
            save_hero_progress(self.gold, self.inventory, self.hp)
            return False
        
        print("Вы погибли! Возрождение в фонтане. Вы потеряли 200 золота.")
        if "Divine Rapier" in self.inventory:
            self.inventory.remove("Divine Rapier")
            print("Внимание: Вы потеряли Divine Rapier при смерти!")
        
        self.gold = max(0, self.gold - 200)
        stats = self.get_hero_stats()
        self.hp = stats["max_hp"]
        save_hero_progress(self.gold, self.inventory, self.hp)
        return True

    def farm_gold(self):
        stats = self.get_hero_stats()
        if self.hp <= 50:
            print("У вас слишком мало HP для выхода на линию! Купите Tango или посетите фонтан.")
            return

        print(f"\n--- ВЫШЛИ НА ЛИНИЮ | Ваш HP: {self.hp}/{stats['max_hp']} | Урон: {stats['damage']} ---")
        creeps = 4
        total_earned = 0

        for i in range(1, creeps + 1):
            creep_hp = random.randint(30, 90)
            enemy_deny_chance = 0.35
            
            print(f"\nКрип #{i} выползает на линию. Его HP: {creep_hp}")
            
            if random.random() < 0.40:
                enemy_dmg = random.randint(25, 45)
                if random.random() < stats["evasion"]:
                    print("Вражеский хардлейнер пытался вас ударить, но вы уклонились!")
                else:
                    self.hp -= enemy_dmg
                    print(f"Вражеский хардлейнер ударил вас! Вы потеряли {enemy_dmg} HP. Осталось: {self.hp}")
                    if self.hp <= 0:
                        if self.handle_death():
                            return

            print("1. Ударить крипа")
            print("2. Подождать просадки HP")
            choice = input("Действие: ").strip()

            if choice == "2":
                creep_hp -= random.randint(20, 40)
                if creep_hp <= 0:
                    print("Союзные крипы добили цель. Вы упустили золото.")
                    continue
                if random.random() < enemy_deny_chance:
                    print("Враг воспользовался вашим промедлением и заденаил крипа!")
                    continue
                print(f"HP крипа опустилось до {creep_hp}. Вы бьете!")

            if stats["damage"] >= creep_hp:
                gold_reward = 45
                total_earned += gold_reward
                print(f"Ластхит! Вы получили +{gold_reward} золота.")
                if stats["lifesteal"] > 0:
                    healed = int(stats["damage"] * stats["lifesteal"])
                    self.hp = min(stats["max_hp"], self.hp + healed)
                    print(f"Вампиризм восстановил вам {healed} HP.")
            else:
                print(f"Не добил! У крипа осталось {creep_hp - stats['damage']} HP, его заденаил ваш оппонент.")
            
            time.sleep(0.4)

        self.gold += total_earned
        save_hero_progress(self.gold, self.inventory, self.hp)
        print(f"\nПачка зачищена. Получено золота: {total_earned}")

    def fight_roshan(self):
        stats = self.get_hero_stats()
        print("\n--- ЛОГОВО РОШАНА ---")
        print(f"Ваш HP: {self.hp}/{stats['max_hp']} | Урон: {stats['damage']}")
        print("Рошан невероятно силен. Вы уверены, что хотите напасть? (да/нет)")
        
        if input().strip().lower() != "да":
            print("Вы испугались грозного рыка и убежали.")
            return

        roshan_hp = 1200
        roshan_dmg = 75

        print("Битва началась!")
        while roshan_hp > 0 and self.hp > 0:
            roshan_hp -= stats["damage"]
            print(f"Вы нанесли Рошану {stats['damage']} урона. У него осталось {max(0, roshan_hp)} HP.")
            if stats["lifesteal"] > 0:
                healed = int(stats["damage"] * stats["lifesteal"])
                self.hp = min(stats["max_hp"], self.hp + healed)
                print(f"Вампиризм восстановил вам {healed} HP.")
            
            if roshan_hp <= 0:
                break
                
            time.sleep(0.5)
            if random.random() < stats["evasion"]:
                print("Рошан замахнулся, но вы уклонились от его удара!")
            else:
                self.hp -= roshan_dmg
                print(f"Рошан бьет в ответ: -{roshan_dmg} HP. Ваше здоровье: {max(0, self.hp)}")

        if self.hp <= 0:
            self.handle_death()
        else:
            print("\nПобеда! Вы повергли Рошана!")
            if len(self.inventory) < self.max_slots:
                self.inventory.append("Aegis of the Immortal")
                print("Вы подобрали Aegis of the Immortal! Теперь у вас есть одна бесплатная жизнь.")
            else:
                print("Ваш инвентарь был полон, Aegis упал на землю и растворился!")
            
            self.gold += 500
            print("Вы получили бонусные +500 золота за убийство босса.")
            save_hero_progress(self.gold, self.inventory, self.hp)

    def show_inventory(self):
        stats = self.get_hero_stats()
        print("\n--- ИНВЕНТАРЬ ГЕРОЯ ---")
        print(f"Слоты: {len(self.inventory)} / {self.max_slots}")
        print(f"Текущий баланс: {self.gold} gold")
        print(f"Характеристики: HP: {self.hp}/{stats['max_hp']} | Урон: {stats['damage']} | Вампиризм: {int(stats['lifesteal']*100)}% | Уклонение: {int(stats['evasion']*100)}%")
        
        if not self.inventory:
            print("Инвентарь пуст.")
        else:
            for idx, item in enumerate(self.inventory, 1):
                bonus = next((i["bonus"] for i in self.shop_items if i["name"] == item), "Нет описания")
                print(f" {idx}. [{item}] — {bonus}")
