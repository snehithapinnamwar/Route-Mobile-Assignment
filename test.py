from app import app
from models import Item


with app.app_context():


    items = Item.query.all()

    if not items:
        print("No records found.")
    else:
        print("-" * 40)
        print(f"{'ID':<5}{'ITEM':<15}{'STATUS':<15}")
        print("-" * 40)

        for item in items:
            print(f"{item.id:<5}{item.item:<15}{item.status:<15}")

        print("-" * 40)