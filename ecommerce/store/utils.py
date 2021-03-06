import json
from django.shortcuts import get_object_or_404
from .models import Product,Order,OrderItem,ShippingAddress, ProductImage
from .recommandation import makeRecommandation
from utilisateurs.models import Account

def cookieCart(request):
	#Create empty cart for now for non-logged in user
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
		print('CART:', cart)

	items = []
	order = {'get_cart_total':0, 'get_cart_items':0}
	cartItems = order['get_cart_items']

	for i in cart:
		#We use try block to prevent items in cart that may have been removed from causing error
		try:
			cartItems += cart[i]['quantity']

			product = Product.objects.get(id=i)
			total = (product.price * cart[i]['quantity'])

			order['get_cart_total'] += total
			order['get_cart_items'] += cart[i]['quantity']

			item = {
				'id':product.id,
				'product':{'id':product.id,'title':product.title, 'price':product.price,'get_image':{'imageURL':product.get_image.imageURL} },
				'quantity':cart[i]['quantity'],
				'get_total':total,
				}
			items.append(item)
		except:
			pass
		
	return {'cartItems':cartItems ,'order':order, 'items':items}

def cartData(request):
	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']

	return {'cartItems':cartItems ,'order':order, 'items':items}

	
def guestOrder(request, data):
	name = data['form']['name']
	email = data['form']['email']

	cookieData = cookieCart(request)
	items = cookieData['items']

	customer, created = Account.objects.get_or_create(
			email=email,
			)
	customer.username = name
	customer.save()

	order = Order.objects.create(
		customer=customer,
		complete=False,
		)

	for item in items:
		product = Product.objects.get(id=item['id'])
		orderItem = OrderItem.objects.create(
			product=product,
			order=order,
			quantity=item['quantity'],
		)
	return customer, order

def cartItems(request):
	data = cartData(request)
	cartItems = data['cartItems']
	return {'cartItems':cartItems}

def similarProduct(request, nbPrdt):
	S=[]
	userId = request.user.id
	for prdtId in makeRecommandation(n_rec=nbPrdt, userId=userId):
		product = get_object_or_404(Product, id=prdtId[0])
		S.append(product)

	return S