import random
from openpyxl import Workbook

def generate_product_data(count=100):
    products = []
    for i in range(1, count + 1):
        product_id = f"P{i:04d}"                # P0001, P0002 ...
        product_name = f"전자제품_{i:03d}"     # 전자제품_001 ...
        price = random.randint(20000, 1000000)  # 20,000 ~ 1,000,000
        quantity = random.randint(1, 200)       # 1 ~ 200
        products.append((product_id, product_name, price, quantity))
    return products

def save_to_excel(products, filename="ProductList.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "Products"
    ws.append(["제품ID", "제품명", "가격", "수량"])

    for product in products:
        ws.append(product)

    wb.save(filename)
    print(f"저장 완료: {filename} (총 {len(products)}개)")

if __name__ == "__main__":
    data = generate_product_data(100)
    save_to_excel(data, "ProductList.xlsx")