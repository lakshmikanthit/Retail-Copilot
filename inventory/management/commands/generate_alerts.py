from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Avg, F, Q, Count
from decimal import Decimal
from inventory.models import Store, Product, Stock, SalesTransaction, InventoryAlert
import random


class Command(BaseCommand):
    help = 'Generate intelligent inventory alerts based on data analysis'

    def handle(self, *args, **options):
        self.stdout.write('Generating intelligent inventory alerts...')

        # Clear existing unresolved alerts
        InventoryAlert.objects.filter(is_resolved=False).delete()

        # Get all stocks
        stocks = Stock.objects.all().select_related('store', 'product')

        for stock in stocks:
            self._analyze_stock(stock)

        # Analyze sales patterns
        self._analyze_sales_patterns()

        self.stdout.write(self.style.SUCCESS('Inventory alerts generated successfully!'))

    def _analyze_stock(self, stock):
        """Analyze individual stock levels and generate alerts"""

        # Stock out alert
        if stock.quantity == 0:
            self._create_alert(
                stock.store,
                stock.product,
                'stock_out',
                'critical',
                f'{stock.product.name} is completely out of stock at {stock.store.name}. Current stock: {stock.quantity} units.',
                f'Immediate restock required. This product has 0 units available. Historical data shows this product typically sells at an average rate.',
                {'current_stock': stock.quantity, 'reorder_level': stock.reorder_level}
            )

        # Low stock alert
        elif stock.quantity <= stock.reorder_level:
            severity = 'high' if stock.quantity <= stock.reorder_level / 2 else 'medium'
            self._create_alert(
                stock.store,
                stock.product,
                'low_stock',
                severity,
                f'{stock.product.name} is running low at {stock.store.name}. Current stock: {stock.quantity} units (Reorder level: {stock.reorder_level}).',
                f'Place reorder soon. At current sales rate, stock may run out soon. Recommended order quantity: {stock.max_stock_level - stock.quantity} units.',
                {'current_stock': stock.quantity, 'reorder_level': stock.reorder_level, 'suggested_order': stock.max_stock_level - stock.quantity}
            )

        # Overstock alert
        elif stock.quantity >= stock.max_stock_level:
            self._create_alert(
                stock.store,
                stock.product,
                'overstock',
                'medium',
                f'{stock.product.name} is overstocked at {stock.store.name}. Current stock: {stock.quantity} units (Max level: {stock.max_stock_level}).',
                f'Consider reducing future orders or running promotions to clear excess inventory. Current stock is {((stock.quantity - stock.max_stock_level) / stock.max_stock_level * 100):.1f}% above maximum level.',
                {'current_stock': stock.quantity, 'max_stock_level': stock.max_stock_level, 'excess_percentage': round((stock.quantity - stock.max_stock_level) / stock.max_stock_level * 100, 1)}
            )

    def _analyze_sales_patterns(self):
        """Analyze sales patterns to detect spikes, drops, and slow-moving items"""

        # Get last 30 days and previous 30 days for comparison
        now = timezone.now()
        current_period_start = now - timedelta(days=30)
        previous_period_start = now - timedelta(days=60)
        previous_period_end = current_period_start

        # Analyze each product
        products = Product.objects.all()

        for product in products:
            # Get sales data for current and previous periods
            current_sales = SalesTransaction.objects.filter(
                product=product,
                transaction_date__gte=current_period_start
            ).aggregate(
                total_quantity=Sum('quantity'),
                total_revenue=Sum('total_amount'),
                transaction_count=Count('id')
            )

            previous_sales = SalesTransaction.objects.filter(
                product=product,
                transaction_date__gte=previous_period_start,
                transaction_date__lt=previous_period_end
            ).aggregate(
                total_quantity=Sum('quantity'),
                total_revenue=Sum('total_amount'),
                transaction_count=Count('id')
            )

            current_qty = current_sales['total_quantity'] or 0
            previous_qty = previous_sales['total_quantity'] or 0

            # Sales spike detection (more than 50% increase)
            if previous_qty > 0 and current_qty > previous_qty * 1.5:
                percentage_increase = ((current_qty - previous_qty) / previous_qty) * 100
                for store in Store.objects.all():
                    self._create_alert(
                        store,
                        product,
                        'sales_spike',
                        'medium',
                        f'{product.name} shows a sales spike of {percentage_increase:.1f}% compared to previous month. Current: {current_qty} units vs Previous: {previous_qty} units.',
                        f'Investigate cause of spike (promotion, seasonality, or market trend). Ensure sufficient stock to meet demand. Consider capitalizing on momentum with complementary product promotions.',
                        {'current_period_sales': current_qty, 'previous_period_sales': previous_qty, 'percentage_increase': round(percentage_increase, 1)}
                    )

            # Sales drop detection (more than 50% decrease)
            elif previous_qty > 0 and current_qty < previous_qty * 0.5:
                percentage_decrease = ((previous_qty - current_qty) / previous_qty) * 100
                for store in Store.objects.all():
                    self._create_alert(
                        store,
                        product,
                        'sales_drop',
                        'high',
                        f'{product.name} shows a sales drop of {percentage_decrease:.1f}% compared to previous month. Current: {current_qty} units vs Previous: {previous_qty} units.',
                        f'Investigate cause of drop (seasonality, competition, or stock issues). Review pricing, placement, and marketing efforts. Consider promotion to revive sales.',
                        {'current_period_sales': current_qty, 'previous_period_sales': previous_qty, 'percentage_decrease': round(percentage_decrease, 1)}
                    )

            # Slow-moving detection (low sales velocity relative to stock)
            if current_qty < 10:  # Less than 10 units sold in 30 days
                total_stock = Stock.objects.filter(product=product).aggregate(total=Sum('quantity'))['total'] or 0
                if total_stock > 30:  # Has more than 30 units in stock but selling slowly
                    days_of_stock = total_stock / (current_qty / 30) if current_qty > 0 else 999
                    for store in Store.objects.all():
                        stock_at_store = Stock.objects.filter(store=store, product=product).first()
                        if stock_at_store and stock_at_store.quantity > 10:
                            self._create_alert(
                                store,
                                product,
                                'slow_moving',
                                'medium',
                                f'{product.name} is slow-moving. Only {current_qty} units sold in 30 days while {stock_at_store.quantity} units in stock at {store.name}.',
                                f'At current sales rate, stock will last {days_of_stock:.0f} days. Consider promotional pricing, bundling, or display changes to increase turnover. Review if this product should remain in assortment.',
                                {'current_period_sales': current_qty, 'stock_at_store': stock_at_store.quantity, 'estimated_days_of_stock': round(days_of_stock, 0)}
                            )

    def _create_alert(self, store, product, alert_type, severity, message, recommended_action, data_snapshot):
        """Create an inventory alert"""
        InventoryAlert.objects.create(
            store=store,
            product=product,
            alert_type=alert_type,
            severity=severity,
            message=message,
            recommended_action=recommended_action,
            data_snapshot=data_snapshot
        )