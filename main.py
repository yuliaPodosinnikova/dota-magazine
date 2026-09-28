from src.shop import DotaShop

def main():
    shop = DotaShop()
    
    while True:
        stats = shop.get_hero_stats()
        print("\n=== DOTA 2 RPG SIMULATOR ===")
        print(f"Здоровье: {shop.hp}/{stats['max_hp']} | Золото: {shop.gold} | Урон: {stats['damage']} | Слоты: {len(shop.inventory)}/6")
        print("1. Посмотреть товары в лавке")
        print("2. Купить предмет / Расходники")
        print("3. Продать предмет")
        print("4. Отправиться на фарм линии (Опасная зона)")
        print("5. Открыть инвентарь")
        print("6. Посетить фонтан (Восстановить HP)")
        print("7. Пойти на Рошана (Битва за Aegis)")
        print("8. Выйти из игры")
        
        choice = input("Выберите действие (1-8): ").strip()
        
        if choice == "1":
            shop.show_items()
        elif choice == "2":
            shop.show_items()
            try:
                item_idx = int(input("\nВведите номер предмета для покупки: ")) - 1
                shop.buy_item(item_idx)
            except ValueError:
                print("Ошибка: введите корректное число!")
        elif choice == "3":
            if not shop.inventory:
                print("Вам нечего продавать, инвентарь пуст!")
                continue
            shop.show_inventory()
            try:
                inv_idx = int(input("\nКакой предмет хотите продать (номер): ")) - 1
                shop.sell_item(inv_idx)
            except ValueError:
                print("Ошибка: введите корректное число!")
        elif choice == "4":
            shop.farm_gold()
        elif choice == "5":
            shop.show_inventory()
        elif choice == "6":
            print("Вы вернулись на базу. Источник полностью восстановил ваше здоровье.")
            shop.hp = stats["max_hp"]
        elif choice == "7":
            shop.fight_roshan()
        elif choice == "8":
            print("GG WP! Данные сохранены. Удачи в следующих матчах!")
            break
        else:
            print("Неверный выбор меню. Попробуйте еще раз.")

if __name__ == "__main__":
    main()
