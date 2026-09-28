from src.shop import DotaShop

def main():
    shop = DotaShop()
    
    while True:
        print("\n--- DOTA 2 SHOP SIMULATOR ---")
        print(f"Ваше золото: {shop.gold}")
        print("1. Посмотреть товары в лавке")
        print("2. Купить предмет")
        print("3. Отправиться на фарм (+золото)")
        print("4. Открыть инвентарь")
        print("5. Выйти из игры")
        
        choice = input("Выберите действие (1-5): ").strip()
        
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
            shop.farm_gold()
        elif choice == "4":
            shop.show_inventory()
        elif choice == "5":
            print("GG WP! Данные сохранены. Возвращайтесь в лавку снова.")
            break
        else:
            print("Неверный выбор меню. Попробуйте еще раз.")

if __name__ == "__main__":
    main()