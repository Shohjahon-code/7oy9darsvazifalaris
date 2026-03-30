from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Order, OrderProduct, ShippingAddress

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required



def index(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True).select_related('category')
    return render(request, 'shop/index.html', {
        'categories': categories,
        'products': products,
    })


@login_required(login_url='login')
def add_to_cart(request, product_slug, action):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'invalid request'}, status=400)

    product = get_object_or_404(Product, slug=product_slug)

    # Foydalanuvchining aktiv (default) orderini olamiz yoki yaratamiz
    order, _ = Order.objects.get_or_create(user=request.user, is_default=True)

    order_product, created = OrderProduct.objects.get_or_create(
        order=order,
        product=product
    )

    if action == 'add':
        order_product.quantity += 1
        order_product.save()

    elif action == 'remove':
        if order_product.quantity > 1:
            order_product.quantity -= 1
            order_product.save()
        else:
            order_product.delete()

    return JsonResponse({'success': True})