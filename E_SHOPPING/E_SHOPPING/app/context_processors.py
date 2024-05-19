from app.models import Product

def recent_update(request):
    product = Product.objects.filter(status=False).order_by('-updation')
    return {
        'updated_products':product
    }
