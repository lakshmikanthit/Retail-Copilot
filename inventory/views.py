from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum, Count, Q
from .models import Store, Product, Stock, SalesTransaction, InventoryAlert, UserProfile
from .genai_service import RetailCopilotAI
from django.utils import timezone
from datetime import timedelta
import json


@login_required
def dashboard(request):
    """Main dashboard view with user-specific data"""
    # Get user's accessible stores
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_stores = user_profile.user.stores.all() if hasattr(user_profile.user, 'stores') else Store.objects.all()

    # If user has no stores assigned, show all stores (for demo purposes)
    if not user_stores.exists():
        user_stores = Store.objects.all()

    stores = user_stores
    products = Product.objects.all()
    total_stocks = Stock.objects.filter(store__in=stores).count()
    recent_sales = SalesTransaction.objects.filter(
        store__in=stores,
        transaction_date__gte=timezone.now() - timedelta(days=7)
    ).count()

    # Get basic metrics (user-specific)
    low_stock_count = Stock.objects.filter(store__in=stores, quantity__lte=F('reorder_level')).count()
    stock_out_count = Stock.objects.filter(store__in=stores, quantity=0).count()

    # Chart data: Inventory by category
    category_data = products.values('category__name').annotate(
        count=Count('id')
    ).order_by('-count')

    # Chart data: Sales by store (last 7 days) - user-specific
    seven_days_ago = timezone.now() - timedelta(days=7)
    sales_by_store = SalesTransaction.objects.filter(
        store__in=stores,
        transaction_date__gte=seven_days_ago
    ).values('store__name').annotate(
        total_amount=Sum('total_amount'),
        total_quantity=Sum('quantity')
    ).order_by('store__name')

    # Convert Decimal to float for JSON serialization
    sales_by_store_list = []
    for item in sales_by_store:
        sales_by_store_list.append({
            'store__name': item['store__name'],
            'total_amount': float(item['total_amount']) if item['total_amount'] else 0,
            'total_quantity': item['total_quantity'] or 0
        })

    context = {
        'stores': stores,
        'products': products,
        'total_stocks': total_stocks,
        'recent_sales': recent_sales,
        'low_stock_count': low_stock_count,
        'stock_out_count': stock_out_count,
        'category_data': json.dumps(list(category_data)),
        'sales_by_store': json.dumps(sales_by_store_list),
        'user_profile': user_profile,
    }
    return render(request, 'inventory/dashboard.html', context)


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def copilot_chat(request):
    """Handle copilot chat requests"""
    try:
        data = json.loads(request.body)
        question = data.get('question', '')
        store_id = data.get('store_id', None)

        if not question:
            return JsonResponse({
                'success': False,
                'error': 'Question is required'
            }, status=400)

        # Get user's accessible stores
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_stores = user_profile.user.stores.all() if hasattr(user_profile.user, 'stores') else Store.objects.all()

        # Filter store_id to user's accessible stores
        if store_id and not user_stores.filter(id=store_id).exists():
            return JsonResponse({
                'success': False,
                'error': 'You do not have access to this store'
            }, status=403)

        # Initialize AI service
        ai_service = RetailCopilotAI()
        result = ai_service.analyze_question(question, store_id)

        return JsonResponse(result)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
def inventory_alerts(request):
    """View for inventory alerts - user-specific"""
    # Get user's accessible stores
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_stores = user_profile.user.stores.all() if hasattr(user_profile.user, 'stores') else Store.objects.all()

    # If user has no stores assigned, show all stores (for demo purposes)
    if not user_stores.exists():
        user_stores = Store.objects.all()

    alerts = InventoryAlert.objects.filter(
        is_resolved=False,
        store__in=user_stores
    ).select_related('store', 'product').order_by('-created_at')[:50]  # Limit to 50 most recent

    # Calculate alert counts by severity (user-specific)
    critical_count = InventoryAlert.objects.filter(
        is_resolved=False,
        severity='critical',
        store__in=user_stores
    ).count()
    high_count = InventoryAlert.objects.filter(
        is_resolved=False,
        severity='high',
        store__in=user_stores
    ).count()
    medium_count = InventoryAlert.objects.filter(
        is_resolved=False,
        severity='medium',
        store__in=user_stores
    ).count()
    low_count = InventoryAlert.objects.filter(
        is_resolved=False,
        severity='low',
        store__in=user_stores
    ).count()

    context = {
        'alerts': alerts,
        'critical_count': critical_count,
        'high_count': high_count,
        'medium_count': medium_count,
        'low_count': low_count,
        'user_stores': user_stores,
    }
    return render(request, 'inventory/alerts.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def generate_alerts(request):
    """Generate new inventory alerts using the management command logic"""
    try:
        from django.core.management import call_command
        from io import StringIO
        import sys

        # Capture output
        out = StringIO()
        call_command('generate_alerts', stdout=out)

        # Get the new alert count
        new_alerts_count = InventoryAlert.objects.filter(is_resolved=False).count()

        return JsonResponse({
            'success': True,
            'message': f'Successfully generated {new_alerts_count} alerts',
            'alerts_count': new_alerts_count
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def product_analysis(request, product_id):
    """Detailed analysis for a specific product"""
    try:
        ai_service = RetailCopilotAI()
        result = ai_service.get_product_performance(product_id)

        if result['success']:
            product = Product.objects.get(id=product_id)
            context = {
                'product': product,
                'analysis': result['analysis'],
                'metrics': result['metrics'],
            }
            return render(request, 'inventory/product_analysis.html', context)
        else:
            return JsonResponse(result, status=404)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def get_store_data(request):
    """API endpoint to get store data for dropdowns"""
    stores = Store.objects.all().values('id', 'name', 'location')
    return JsonResponse({'stores': list(stores)})


def get_product_data(request):
    """API endpoint to get product data for dropdowns"""
    products = Product.objects.all().values('id', 'name', 'sku', 'category__name')
    return JsonResponse({'products': list(products)})
