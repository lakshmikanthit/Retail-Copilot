import os
import warnings
import google.generativeai as genai
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from .models import Store, Product, Stock, SalesTransaction
import json

# Suppress deprecation warning for the hackathon (using deprecated but stable API)
warnings.filterwarnings('ignore', message='.*google.generativeai.*')


class RetailCopilotAI:
    def __init__(self):
        # Get API key from environment variable
        self.api_key = os.environ.get('GEMINI_API_KEY')
        self.model = None

        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
            except Exception as e:
                print(f"Warning: Could not initialize Gemini AI: {e}")
                self.model = None

    def get_inventory_data(self, store_id=None):
        """Fetch relevant inventory data for AI context"""
        products = Product.objects.all().select_related('category')

        data = {
            'products': [],
            'stores': [],
            'stocks': [],
            'recent_sales': []
        }

        # Get stores
        stores = Store.objects.all()
        for store in stores:
            data['stores'].append({
                'id': store.id,
                'name': store.name,
                'location': store.location,
                'manager': store.manager_name
            })

        # Get products
        for product in products:
            data['products'].append({
                'id': product.id,
                'name': product.name,
                'sku': product.sku,
                'category': product.category.name,
                'cost_price': float(product.cost_price),
                'selling_price': float(product.selling_price),
                'supplier': product.supplier
            })

        # Get stock levels
        stocks = Stock.objects.all().select_related('store', 'product')
        for stock in stocks:
            if store_id and stock.store_id != store_id:
                continue

            data['stocks'].append({
                'store_id': stock.store_id,
                'store_name': stock.store.name,
                'product_id': stock.product_id,
                'product_name': stock.product.name,
                'quantity': stock.quantity,
                'reorder_level': stock.reorder_level,
                'max_stock_level': stock.max_stock_level
            })

        # Get recent sales (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_sales = SalesTransaction.objects.filter(
            transaction_date__gte=thirty_days_ago
        ).select_related('store', 'product')

        if store_id:
            recent_sales = recent_sales.filter(store_id=store_id)

        for sale in recent_sales[:100]:  # Limit to last 100 sales
            data['recent_sales'].append({
                'store_id': sale.store_id,
                'store_name': sale.store.name,
                'product_id': sale.product_id,
                'product_name': sale.product.name,
                'quantity': sale.quantity,
                'unit_price': float(sale.unit_price),
                'total_amount': float(sale.total_amount),
                'date': sale.transaction_date.strftime('%Y-%m-%d'),
                'payment_method': sale.payment_method
            })

        return data

    def analyze_question(self, question, store_id=None):
        """Analyze a manager's question and provide data-driven answers"""
        # Get relevant data first
        inventory_data = self.get_inventory_data(store_id)

        try:
            # Check if AI model is available
            if not self.model:
                return self._fallback_analysis(question, inventory_data, "Gemini API not configured")

            # Create context for the AI
            context = f"""
You are a retail inventory copilot helping store managers make data-driven decisions.
You have access to the following real data:

STORES: {len(inventory_data['stores'])} stores
PRODUCTS: {len(inventory_data['products'])} products across {len(set(p['category'] for p in inventory_data['products']))} categories
STOCK LEVELS: {len(inventory_data['stocks'])} stock entries
RECENT SALES: {len(inventory_data['recent_sales'])} transactions in the last 30 days

IMPORTANT RULES:
1. NEVER make up numbers. Always use the actual data provided.
2. When answering, always cite the specific numbers behind your answer.
3. If the data cannot answer the question, say so clearly rather than guessing.
4. Focus on actionable insights and recommendations.
5. Flag items that need attention: stock-outs, overstock, slow-moving items, sales spikes/drops.
6. Always provide the reasoning behind your recommendations.

RETAIL DATA:
{json.dumps(inventory_data, indent=2)}

Question: {question}

Provide a comprehensive answer with:
1. Direct answer to the question
2. Specific numbers and data supporting your answer
3. Actionable recommendations
4. Items that need attention
5. Any relevant trends or patterns
"""

            # Generate response
            response = self.model.generate_content(context)
            return {
                'success': True,
                'answer': response.text,
                'data_used': {
                    'stores_count': len(inventory_data['stores']),
                    'products_count': len(inventory_data['products']),
                    'stocks_count': len(inventory_data['stocks']),
                    'sales_count': len(inventory_data['recent_sales'])
                }
            }

        except Exception as e:
            # Fallback to basic analysis if AI fails
            return self._fallback_analysis(question, inventory_data, str(e))

    def _fallback_analysis(self, question, inventory_data, error):
        """Fallback analysis when AI is unavailable"""
        question_lower = question.lower()

        # Basic pattern matching for common questions
        if 'stock out' in question_lower or 'running out' in question_lower:
            stock_outs = [item for item in inventory_data['stocks'] if item['quantity'] == 0]
            low_stock = [item for item in inventory_data['stocks'] if item['quantity'] <= item['reorder_level'] and item['quantity'] > 0]

            answer = f"Based on current inventory data:\n\n"
            answer += f"**Stock Outs ({len(stock_outs)} items):**\n"
            for item in stock_outs[:5]:
                answer += f"- {item['product_name']} at {item['store_name']}: {item['quantity']} units\n"

            answer += f"\n**Low Stock ({len(low_stock)} items):**\n"
            for item in low_stock[:5]:
                answer += f"- {item['product_name']} at {item['store_name']}: {item['quantity']} units (reorder level: {item['reorder_level']})\n"

            answer += f"\n**Recommendation:** Immediate restock is required for stock-out items. Place orders for low-stock items soon."

        elif 'overstock' in question_lower:
            overstock = [item for item in inventory_data['stocks'] if item['quantity'] >= item['max_stock_level']]

            answer = f"Based on current inventory data:\n\n"
            answer += f"**Overstock Items ({len(overstock)} items):**\n"
            for item in overstock[:5]:
                excess = item['quantity'] - item['max_stock_level']
                answer += f"- {item['product_name']} at {item['store_name']}: {item['quantity']} units ({excess} above max)\n"

            answer += f"\n**Recommendation:** Consider reducing future orders or running promotions to clear excess inventory."

        else:
            answer = f"I analyzed your question: '{question}'\n\n"
            answer += f"**Current Data Overview:**\n"
            answer += f"- Stores: {len(inventory_data['stores'])}\n"
            answer += f"- Products: {len(inventory_data['products'])}\n"
            answer += f"- Stock entries: {len(inventory_data['stocks'])}\n"
            answer += f"- Recent sales: {len(inventory_data['recent_sales'])}\n\n"
            answer += f"**Note:** AI analysis is currently unavailable. Using basic data analysis instead.\n"
            answer += "For detailed analysis, please try specific questions about stock-outs, overstock, or check the alerts page."

        return {
            'success': True,
            'answer': answer,
            'data_used': {
                'stores_count': len(inventory_data['stores']),
                'products_count': len(inventory_data['products']),
                'stocks_count': len(inventory_data['stocks']),
                'sales_count': len(inventory_data['recent_sales'])
            }
        }

    def generate_inventory_alerts(self):
        """Generate intelligent inventory alerts based on data analysis"""
        try:
            inventory_data = self.get_inventory_data()

            context = f"""
You are a retail inventory alert system. Analyze the following data and generate alerts for items that need attention.

RETAIL DATA:
{json.dumps(inventory_data, indent=2)}

Generate alerts for:
1. STOCK OUTS: Products with quantity = 0
2. LOW STOCK: Products below reorder level
3. OVERSTOCK: Products above max stock level
4. SLOW MOVING: Products with low sales velocity
5. SALES SPIKES: Unusual increases in sales
6. SALES DROPS: Unusual decreases in sales

For each alert, provide:
- Alert type
- Product name and store
- Severity level (low, medium, high, critical)
- Specific numbers and data
- Recommended action
- Reasoning behind the recommendation

Return the response as a JSON array of alert objects.
"""

            response = self.model.generate_content(context)

            # Try to parse the response as JSON
            try:
                alerts = json.loads(response.text)
                return {'success': True, 'alerts': alerts}
            except json.JSONDecodeError:
                # If not valid JSON, return as text
                return {'success': True, 'alerts_text': response.text}

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'alerts': []
            }

    def get_product_performance(self, product_id, days=30):
        """Get detailed performance analysis for a specific product"""
        try:
            product = Product.objects.get(id=product_id)
            cutoff_date = timezone.now() - timedelta(days=days)

            sales = SalesTransaction.objects.filter(
                product=product,
                transaction_date__gte=cutoff_date
            ).select_related('store')

            total_quantity = sum(sale.quantity for sale in sales)
            total_revenue = sum(sale.total_amount for sale in sales)
            avg_daily_sales = total_quantity / days if days > 0 else 0

            sales_by_store = {}
            for sale in sales:
                store_name = sale.store.name
                if store_name not in sales_by_store:
                    sales_by_store[store_name] = {'quantity': 0, 'revenue': 0}
                sales_by_store[store_name]['quantity'] += sale.quantity
                sales_by_store[store_name]['revenue'] += float(sale.total_amount)

            stock_levels = Stock.objects.filter(product=product).select_related('store')
            stock_info = []
            for stock in stock_levels:
                stock_info.append({
                    'store': stock.store.name,
                    'quantity': stock.quantity,
                    'reorder_level': stock.reorder_level,
                    'status': 'low' if stock.quantity < stock.reorder_level else 'normal'
                })

            context = f"""
Analyze the performance of this product:

PRODUCT: {product.name} (SKU: {product.sku})
CATEGORY: {product.category.name}
COST PRICE: ${product.cost_price}
SELLING PRICE: ${product.selling_price}
SUPPLIER: {product.supplier}

PERFORMANCE OVER LAST {days} DAYS:
- Total Sales: {total_quantity} units
- Total Revenue: ${total_revenue:.2f}
- Average Daily Sales: {avg_daily_sales:.2f} units/day

SALES BY STORE:
{json.dumps(sales_by_store, indent=2)}

CURRENT STOCK LEVELS:
{json.dumps(stock_info, indent=2)}

Provide analysis covering:
1. Sales performance summary
2. Stock status across stores
3. Trends and patterns
4. Recommendations for inventory management
5. Any concerns or opportunities
"""

            response = self.model.generate_content(context)

            return {
                'success': True,
                'product': product.name,
                'analysis': response.text,
                'metrics': {
                    'total_quantity': total_quantity,
                    'total_revenue': float(total_revenue),
                    'avg_daily_sales': avg_daily_sales,
                    'sales_by_store': sales_by_store,
                    'stock_levels': stock_info
                }
            }

        except Product.DoesNotExist:
            return {
                'success': False,
                'error': 'Product not found'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }