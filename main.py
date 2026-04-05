import sqlite3


conn = sqlite3.connect("shop.db")
cursor = conn.cursor()


def show_menu():
   print("\n=== МЕНЮ ===")
   print("1. Додати товар")
   print("2. Додати клієнта")
   print("3. Додати замовлення")
   print("4. Показати всі товари")
   print("5. Показати клієнтів")
   print("6. Загальний дохід")
   print("7. Замовлення по клієнтах")
   print("8. Середній чек")
   print("9. Популярна категорія")
   print("10. Товари по категоріях")
   print("11. Підвищити ціни")
   print("0. Вихід")




def add_product():
   try:
       name = input("Назва товару: ")
       category = input("Категорія: ")
       price = float(input("Ціна: "))


       cursor.execute("""
       INSERT INTO products (name, category, price)
       VALUES (?, ?, ?)
       """, (name, category, price))


       print("✅ Товар додано")


   except ValueError:
       print("❌ Ціна має бути числом!")




def add_customer():
   first_name = input("Ім'я: ")
   last_name = input("Прізвище: ")
   email = input("Email: ")


   cursor.execute("""
   INSERT INTO customers (first_name, last_name, email)
   VALUES (?, ?, ?)
   """, (first_name, last_name, email))


   print("✅ Клієнта додано")




def add_order():
   try:
       show_customers()
       customer_id = int(input("ID клієнта: "))


       show_products()
       product_id = int(input("ID товару: "))


       quantity = int(input("Кількість: "))
       date = input("Дата (YYYY-MM-DD): ")


       cursor.execute("""
       INSERT INTO orders (customer_id, product_id, quantity, order_date)
       VALUES (?, ?, ?, ?)
       """, (customer_id, product_id, quantity, date))


       print("✅ Замовлення додано")


   except ValueError:
       print("❌ Помилка: введіть правильні числа!")
   except Exception as e:
       print("❌ Помилка:", e)


def show_products():
   cursor.execute("SELECT * FROM products")
   print("\n📦 Товари:")
   for row in cursor.fetchall():
       print(row)




def show_customers():
   cursor.execute("SELECT * FROM customers")
   print("\n👤 Клієнти:")
   for row in cursor.fetchall():
       print(row)


def total_sales():
  cursor.execute("""
  SELECT SUM(p.price * o.quantity)
  FROM orders o
  JOIN products p ON o.product_id = p.product_id
  """)
  print("Загальний дохід:", cursor.fetchone()[0])


def orders_per_customer():
  cursor.execute("""
  SELECT c.first_name, c.last_name, COUNT(o.order_id)
  FROM customers c
  JOIN orders o ON c.customer_id = o.customer_id
  GROUP BY c.customer_id
  """)
  for row in cursor.fetchall():
      print(row)


def avg_check():
  cursor.execute("""
  SELECT AVG(total) FROM (
      SELECT SUM(p.price * o.quantity) AS total
      FROM orders o
      JOIN products p ON o.product_id = p.product_id
      GROUP BY o.order_id
  )
  """)
  print("Середній чек:", cursor.fetchone()[0])


def popular_category():
  cursor.execute("""
  SELECT p.category, COUNT(*)
  FROM orders o
  JOIN products p ON o.product_id = p.product_id
  GROUP BY p.category
  ORDER BY COUNT(*) DESC
  LIMIT 1
  """)
  print("Популярна категорія:", cursor.fetchone())


def products_per_category():
  cursor.execute("""
  SELECT category, COUNT(*)
  FROM products
  GROUP BY category
  """)
  for row in cursor.fetchall():
      print(row)


def update_prices():
  cursor.execute("""
  UPDATE products
  SET price = price * 1.10
  WHERE category = 'смартфони'
  """)
  print("Ціни оновлено!")


while True:
   show_menu()
   choice = input("Вибір: ")


   if choice == "1":
       add_product()
   elif choice == "2":
       add_customer()
   elif choice == "3":
       add_order()
   elif choice == "4":
       show_products()
   elif choice == "5":
       show_customers()
   elif choice == "6":
       total_sales()
   elif choice == "7":
       orders_per_customer()
   elif choice == "8":
       avg_check()
   elif choice == "9":
       popular_category()
   elif choice == "10":
       products_per_category()
   elif choice == "11":
       update_prices()
   elif choice == "0":
       save = input("Зберегти зміни? (y/n): ")
       if save.lower() == "y":
           conn.commit()
       break


conn.close()
