import getpass
from functools import reduce

# Данные пользователей
users = [
    {'username': 'jo', 'password': '1234', 'role': 'user', 'history': [], 'created_at': '2024-09-01'},
    {'username': 'ad', 'password': '12345', 'role': 'admin', 'history': [], 'created_at': '2024-09-01'}
]

# Данные о товарах на складе
products = [
    {'name': 'Товар 1', 'quantity': 10, 'price': 100},
    {'name': 'Товар 2', 'quantity': 5, 'price': 200},
    {'name': 'Товар 3', 'quantity': 0, 'price': 150},
]

# Функция для авторизации
def authorize():
    username = input("Логин: ")
    password = getpass.getpass("Пароль: ")
    for user in users:
        if user['username'] == username and user['password'] == password:
            return user
    print("Неверный логин или пароль.")
    return None

# Функции для пользователя
def user_menu(user):
    while True:
        print("\n--- Пользовательское меню ---")
        print("1. Просмотреть доступные товары")
        print("2. Купить товар")
        print("3. Посмотреть историю покупок")
        print("4. Обновить профиль")
        print("5. Сортировать товары")
        print("6. Фильтровать товары")
        print("7. Выйти")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            view_products()
        elif choice == '2':
            purchase_product(user)
        elif choice == '3':
            view_history(user)
        elif choice == '4':
            update_profile(user)
        elif choice == '5':
            sort_products()
        elif choice == '6':
            filter_products()
        elif choice == '7':
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

def view_products(products=None):
    if products is None:
        products = products

    print("\n--- Доступные товары ---")
    if not products:
        print("Нет доступных товаров.")
        return
    print(f"{'Название':<15} {'Количество':<10} {'Цена':<10}")
    print("-" * 35)
    for product in products:
        print(f"{product['name']:<15} {product['quantity']:<10} {product['price']:<10}")

def purchase_product(user):
    product_name = input("Введите название товара для покупки: ")
    for product in products:
        if product['name'].lower() == product_name.lower():
            if product['quantity'] > 0:
                product['quantity'] -= 1
                user['history'].append(product_name)
                print(f"Вы купили {product_name}.")
                return
            else:
                print("Товар недоступен.")
                return
    print("Товар не найден.")

def view_history(user):
    print("\n--- Ваша история покупок ---")
    if not user['history']:
        print("Вы еще ничего не купили.")
        return
    for item in user['history']:
        print(item)

def update_profile(user):
    new_password = getpass.getpass("Введите новый пароль: ")
    user['password'] = new_password
    print("Пароль обновлен.")

def sort_products():
    print("\n--- Сортировка товаров ---")
    print("1. По имени")
    print("2. По количеству")
    print("3. По цене")
    choice = input("Выберите способ сортировки: ")

    if choice == '1':
        sorted_products = sorted(products, key=lambda x: x['name'])
    elif choice == '2':
        sorted_products = sorted(products, key=lambda x: x['quantity'])
    elif choice == '3':
        sorted_products = sorted(products, key=lambda x: x['price'])
    else:
        print("Неверный выбор.")
        return

    print("\n--- Отсортированные товары ---")
    view_products(sorted_products)

def filter_products():
    print("\n--- Фильтрация товаров ---")
    min_price = input("Введите минимальную цену (или оставьте пустым для пропуска): ")
    max_price = input("Введите максимальную цену (или оставьте пустым для пропуска): ")

    filtered_products = products

    if min_price:
        try:
            min_price = float(min_price)
            filtered_products = list(filter(lambda product: product['price'] >= min_price, filtered_products))
        except ValueError:
            print("Некорректный ввод для минимальной цены. Пропускаем фильтрацию по минимальной цене.")
    
    if max_price:
        try:
            max_price = float(max_price)
            filtered_products = list(filter(lambda product: product['price'] <= max_price, filtered_products))
        except ValueError:
            print("Некорректный ввод для максимальной цены. Пропускаем фильтрацию по максимальной цене.")
    
    print("\n--- Отфильтрованные товары ---")
    view_products(filtered_products)

# Функции для администратора
def admin_menu():
    while True:
        print("\n--- Административное меню ---")
        print("1. Добавить товар")
        print("2. Удалить товар")
        print("3. Изменить товар")
        print("4. Просмотреть статистику")
        print("5. Выйти")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            add_product()
        elif choice == '2':
            remove_product()
        elif choice == '3':
            edit_product()
        elif choice == '4':
            view_statistics()
        elif choice == '5':
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

def add_product():
    name = input("Введите название товара: ")
    quantity = input("Введите количество: ")
    price = input("Введите цену: ")
    
    try:
        quantity = int(quantity)
        price = float(price)
        products.append({'name': name, 'quantity': quantity, 'price': price})
        print("Товар добавлен.")
    except ValueError:
        print("Некорректный ввод для количества или цены.")

def remove_product():
    name = input("Введите название товара для удаления: ")
    global products
    products = list(filter(lambda product: product['name'].lower() != name.lower(), products))
    print("Товар удален." if any(product['name'].lower() == name.lower() for product in products) else "Товар не найден.")

def edit_product():
    name = input("Введите название товара для редактирования: ")
    for product in products:
        if product['name'].lower() == name.lower():
            new_quantity = input("Введите новое количество: ")
            new_price = input("Введите новую цену: ")
            try:
                product['quantity'] = int(new_quantity)
                product['price'] = float(new_price)
                print("Товар обновлен.")
                return
            except ValueError:
                print("Некорректный ввод для количества или цены.")
                return
    print("Товар не найден.")

def view_statistics():
    total_products = len(products)
    total_quantity = reduce(lambda acc, product: acc + product['quantity'], products, 0)
    total_value = reduce(lambda acc, product: acc + product['price'] * product['quantity'], products, 0)
    print(f"Общее количество товаров: {total_products}")
    print(f"Общее количество на складе: {total_quantity}")
    print(f"Общая стоимость товаров на складе: {total_value}")

# Основной цикл приложения
def main():
    print("Добро пожаловать в складскую систему!")
    user = authorize()
    if user:
        if user['role'] == 'admin':
            admin_menu()
        else:
            user_menu(user)

if __name__ == "__main__":
    main()
