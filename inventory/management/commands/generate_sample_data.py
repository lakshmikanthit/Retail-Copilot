from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date
import random
from decimal import Decimal
from inventory.models import Store, Category, Product, Stock, SalesTransaction


class Command(BaseCommand):
    help = 'Generate sample retail data for the hackathon'

    def handle(self, *args, **options):
        self.stdout.write('Generating sample retail data...')

        # Create Categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Electronic devices and accessories'},
            {'name': 'Clothing', 'description': 'Apparel and fashion items'},
            {'name': 'Groceries', 'description': 'Food and household items'},
            {'name': 'Home & Garden', 'description': 'Home improvement and garden supplies'},
            {'name': 'Sports', 'description': 'Sports equipment and accessories'},
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create Stores
        stores_data = [
            {
                'name': 'Downtown Store',
                'location': '123 Main Street, Downtown',
                'manager_name': 'John Smith',
                'contact_email': 'john.downtown@retail.com',
                'contact_phone': '+1-555-0101'
            },
            {
                'name': 'Mall Branch',
                'location': '456 Shopping Mall, West Wing',
                'manager_name': 'Sarah Johnson',
                'contact_email': 'sarah.mall@retail.com',
                'contact_phone': '+1-555-0102'
            },
            {
                'name': 'Suburban Outlet',
                'location': '789 Suburban Plaza',
                'manager_name': 'Mike Williams',
                'contact_email': 'mike.suburban@retail.com',
                'contact_phone': '+1-555-0103'
            },
        ]

        stores = []
        for store_data in stores_data:
            store, created = Store.objects.get_or_create(
                name=store_data['name'],
                defaults=store_data
            )
            stores.append(store)
            if created:
                self.stdout.write(f'Created store: {store.name}')

        # Create Products
        products_data = [
            # Electronics
            {'name': 'Wireless Headphones', 'sku': 'ELEC-001', 'category': categories[0], 'cost_price': Decimal('45.00'), 'selling_price': Decimal('79.99'), 'supplier': 'TechSupply Co'},
            {'name': 'Bluetooth Speaker', 'sku': 'ELEC-002', 'category': categories[0], 'cost_price': Decimal('25.00'), 'selling_price': Decimal('49.99'), 'supplier': 'TechSupply Co'},
            {'name': 'USB-C Cable', 'sku': 'ELEC-003', 'category': categories[0], 'cost_price': Decimal('3.00'), 'selling_price': Decimal('9.99'), 'supplier': 'CableKing'},
            {'name': 'Phone Case', 'sku': 'ELEC-004', 'category': categories[0], 'cost_price': Decimal('5.00'), 'selling_price': Decimal('14.99'), 'supplier': 'AccessoriesPlus'},
            {'name': 'Laptop Stand', 'sku': 'ELEC-005', 'category': categories[0], 'cost_price': Decimal('20.00'), 'selling_price': Decimal('39.99'), 'supplier': 'OfficeTech'},
            {'name': 'Wireless Mouse', 'sku': 'ELEC-006', 'category': categories[0], 'cost_price': Decimal('12.00'), 'selling_price': Decimal('24.99'), 'supplier': 'TechSupply Co'},
            {'name': 'Keyboard', 'sku': 'ELEC-007', 'category': categories[0], 'cost_price': Decimal('15.00'), 'selling_price': Decimal('29.99'), 'supplier': 'OfficeTech'},
            {'name': 'Webcam', 'sku': 'ELEC-008', 'category': categories[0], 'cost_price': Decimal('30.00'), 'selling_price': Decimal('59.99'), 'supplier': 'TechSupply Co'},

            # Clothing
            {'name': 'Cotton T-Shirt', 'sku': 'CLTH-001', 'category': categories[1], 'cost_price': Decimal('8.00'), 'selling_price': Decimal('19.99'), 'supplier': 'FashionHub'},
            {'name': 'Jeans', 'sku': 'CLTH-002', 'category': categories[1], 'cost_price': Decimal('25.00'), 'selling_price': Decimal('49.99'), 'supplier': 'FashionHub'},
            {'name': 'Sneakers', 'sku': 'CLTH-003', 'category': categories[1], 'cost_price': Decimal('35.00'), 'selling_price': Decimal('69.99'), 'supplier': 'ShoeWorld'},
            {'name': 'Winter Jacket', 'sku': 'CLTH-004', 'category': categories[1], 'cost_price': Decimal('45.00'), 'selling_price': Decimal('89.99'), 'supplier': 'FashionHub'},
            {'name': 'Baseball Cap', 'sku': 'CLTH-005', 'category': categories[1], 'cost_price': Decimal('5.00'), 'selling_price': Decimal('14.99'), 'supplier': 'AccessoriesPlus'},
            {'name': 'Socks (3-pack)', 'sku': 'CLTH-006', 'category': categories[1], 'cost_price': Decimal('4.00'), 'selling_price': Decimal('9.99'), 'supplier': 'FashionHub'},

            # Groceries
            {'name': 'Organic Coffee', 'sku': 'GROC-001', 'category': categories[2], 'cost_price': Decimal('8.00'), 'selling_price': Decimal('14.99'), 'supplier': 'WholeFoods Supplier'},
            {'name': 'Green Tea', 'sku': 'GROC-002', 'category': categories[2], 'cost_price': Decimal('6.00'), 'selling_price': Decimal('11.99'), 'supplier': 'WholeFoods Supplier'},
            {'name': 'Almonds (1lb)', 'sku': 'GROC-003', 'category': categories[2], 'cost_price': Decimal('7.00'), 'selling_price': Decimal('12.99'), 'supplier': 'NutCo'},
            {'name': 'Olive Oil', 'sku': 'GROC-004', 'category': categories[2], 'cost_price': Decimal('10.00'), 'selling_price': Decimal('18.99'), 'supplier': 'WholeFoods Supplier'},
            {'name': 'Pasta Sauce', 'sku': 'GROC-005', 'category': categories[2], 'cost_price': Decimal('3.00'), 'selling_price': Decimal('6.99'), 'supplier': 'FoodDistributors'},
            {'name': 'Rice (2kg)', 'sku': 'GROC-006', 'category': categories[2], 'cost_price': Decimal('4.00'), 'selling_price': Decimal('8.99'), 'supplier': 'FoodDistributors'},

            # Home & Garden
            {'name': 'Plant Pot', 'sku': 'HOME-001', 'category': categories[3], 'cost_price': Decimal('8.00'), 'selling_price': Decimal('15.99'), 'supplier': 'GardenPro'},
            {'name': 'Garden Tool Set', 'sku': 'HOME-002', 'category': categories[3], 'cost_price': Decimal('25.00'), 'selling_price': Decimal('49.99'), 'supplier': 'GardenPro'},
            {'name': 'LED Light Bulb', 'sku': 'HOME-003', 'category': categories[3], 'cost_price': Decimal('2.00'), 'selling_price': Decimal('5.99'), 'supplier': 'HomeEssentials'},
            {'name': 'Picture Frame', 'sku': 'HOME-004', 'category': categories[3], 'cost_price': Decimal('7.00'), 'selling_price': Decimal('14.99'), 'supplier': 'HomeDecor'},
            {'name': 'Throw Pillow', 'sku': 'HOME-005', 'category': categories[3], 'cost_price': Decimal('10.00'), 'selling_price': Decimal('19.99'), 'supplier': 'HomeDecor'},

            # Sports
            {'name': 'Yoga Mat', 'sku': 'SPRT-001', 'category': categories[4], 'cost_price': Decimal('15.00'), 'selling_price': Decimal('29.99'), 'supplier': 'FitnessGear'},
            {'name': 'Dumbbells (5kg)', 'sku': 'SPRT-002', 'category': categories[4], 'cost_price': Decimal('20.00'), 'selling_price': Decimal('39.99'), 'supplier': 'FitnessGear'},
            {'name': 'Water Bottle', 'sku': 'SPRT-003', 'category': categories[4], 'cost_price': Decimal('5.00'), 'selling_price': Decimal('12.99'), 'supplier': 'SportsCo'},
            {'name': 'Jump Rope', 'sku': 'SPRT-004', 'category': categories[4], 'cost_price': Decimal('4.00'), 'selling_price': Decimal('9.99'), 'supplier': 'SportsCo'},
            {'name': 'Tennis Balls (3-pack)', 'sku': 'SPRT-005', 'category': categories[4], 'cost_price': Decimal('6.00'), 'selling_price': Decimal('11.99'), 'supplier': 'SportsCo'},
        ]

        products = []
        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                sku=prod_data['sku'],
                defaults=prod_data
            )
            products.append(product)
            if created:
                self.stdout.write(f'Created product: {product.name}')

        # Create Stock entries for each store-product combination
        stock_entries = []
        for store in stores:
            for product in products:
                # Random stock levels with some products being low or high
                rand_num = random.random()
                if rand_num < 0.1:  # 10% chance of stock out
                    quantity = 0
                elif rand_num < 0.25:  # 15% chance of low stock
                    quantity = random.randint(1, 9)
                elif rand_num < 0.35:  # 10% chance of overstock
                    quantity = random.randint(101, 150)
                else:  # normal stock
                    quantity = random.randint(10, 100)

                stock, created = Stock.objects.get_or_create(
                    store=store,
                    product=product,
                    defaults={
                        'quantity': quantity,
                        'reorder_level': random.randint(5, 15),
                        'max_stock_level': random.randint(80, 120)
                    }
                )
                stock_entries.append(stock)
                if created:
                    self.stdout.write(f'Created stock: {product.name} at {store.name} - {quantity} units')

        # Generate sales transactions for the last 90 days
        payment_methods = ['cash', 'card', 'upi', 'other']
        sales_count = 0

        for days_ago in range(90, 0, -1):
            transaction_date = timezone.now() - timedelta(days=days_ago)

            # Generate 5-15 transactions per day
            daily_transactions = random.randint(5, 15)

            for _ in range(daily_transactions):
                store = random.choice(stores)
                product = random.choice(products)

                # Get current stock for this product at this store
                try:
                    stock = Stock.objects.get(store=store, product=product)
                except Stock.DoesNotExist:
                    continue

                # Random quantity (1-5)
                quantity = random.randint(1, min(5, stock.quantity + 10))  # Allow negative stock for testing

                unit_price = product.selling_price
                total_amount = unit_price * quantity

                SalesTransaction.objects.create(
                    store=store,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_amount=total_amount,
                    transaction_date=transaction_date,
                    payment_method=random.choice(payment_methods)
                )
                sales_count += 1

        self.stdout.write(f'Generated {sales_count} sales transactions')

        self.stdout.write(self.style.SUCCESS('Sample data generation completed successfully!'))