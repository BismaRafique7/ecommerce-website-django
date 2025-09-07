from .models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.session_key = 'cart'
        cart = self.session.get(self.session_key)
        if not cart:
            cart = self.session[self.session_key] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 1,
                'price': str(product.price)  
            }

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        if self.cart[product_id]['quantity'] <= 0:
            self.remove(product)

        self.save()

    def save(self):
        self.session[self.session_key] = self.cart
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        product_map = {str(product.id): product for product in products}

        for product_id, item in self.cart.items():
            item_copy = item.copy() 
            item_copy['product'] = product_map.get(product_id)
            item_copy['price'] = float(item_copy['price'])
            item_copy['total_price'] = item_copy['price'] * item_copy['quantity']
            yield item_copy

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())
