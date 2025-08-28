from django.shortcuts import render
from django.http import JsonResponse
from .models import Category, Product, Store, Cart, Order, OrderDetails, Address, Status
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .serializers import CategorySerializer, ProductSerializer, StoreSerializer, CartSerializer, OrderSerializer, OrderSerializer1, OrderListSerializer, AddressSerializer
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib.auth.decorators import login_required
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import IsAdminUserOrReadOnly, IsOwnerProductOrReadOnly, IsOwnerStoreOrReadOnly, IsStoreOrCustomer, IsCustomer, IsStore
from django.db import transaction
# Create your views here.

@api_view(['GET'])
def category_list(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data)

#@api_view(['GET','POST', 'DELETE'])
@api_view(['POST'])
def category_create(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)
    

@api_view(['PUT'])
def category_update(request, id):
    category = Category.objects.get(pk=id)
    serializer = CategorySerializer(category, data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    

@api_view(['DELETE'])
def category_delete(request, id):
    category = Category.objects.get(pk=id)
    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



########################################################

@api_view(['GET'])
def product_list(request):
    product = Product.objects.all()
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def product_delete(request, id):
    product = Product.objects.get(pk=id)
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['PUT'])
def product_update(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product, data=request.data)
    
    if serializer.is_valid():
        if 'name' in request.data and product.name != request.data['name']:
            product.slug = slugify(request.data['name'])
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def product_create(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)
    
##################################################
@api_view(['GET'])
def store(request, id):
    store = Store.objects.get(pk=id)
    serializer = StoreSerializer(store, context = {'request':request})
    return Response(serializer.data)

@api_view(['GET'])
def category(request, id):
    category = Category.objects.get(pk=id)
    serializer = CategorySerializer(category, context = {'request':request})
    return Response(serializer.data)

@api_view(['GET'])
def product(request, id):
    try:
        product = Product.objects.get(pk=id)
        serializer = ProductSerializer(product, context = {'request':request})
        return Response(serializer.data)
    except ObjectDoesNotExist:
        return Response({"error": "Product not found"}, status=404)
    
##########################################

from rest_framework import generics

#Category
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    #queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    def get_queryset(self):
        queryset = Category.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)
        return queryset

from rest_framework.exceptions import NotFound
from rest_framework import status

class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):#!!!!!!!!!!!!!!!
    #queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'
    
    def get_queryset(self):
        queryset = Category.objects.all()
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        
        if min_price is not None and max_price is not None:
             queryset = queryset.filter(products__price__gte=min_price, products__price__lte=max_price) #price in the model
        elif min_price is not None:
             queryset = queryset.filter(products__price__gte=min_price)
        elif max_price is not None:
             queryset = queryset.filter(products__price__lte=max_price)
        return queryset.distinct()
   
#Product
class ProductListCreateAPIView(generics.ListCreateAPIView):
    #queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = Product.objects.all()
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)

        category = self.request.query_params.get('category', None)

        seller = self.request.query_params.get('seller', None)

        if min_price is not None and max_price is not None:
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price) #price in the model
        elif min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        elif max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        if category is not None:
            queryset = queryset.filter(category__name=category)

        if seller is not None:
            queryset = queryset.filter(seller__name=seller)

        return queryset

    def perform_create(self, serializer):
        slug_value = self.request.POST.get('name')
        slug = slugify(slug_value)
        seller = Store.objects.get(user=self.request.user)
        
        serializer.save(slug = slug, seller = seller) #for now
    

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer    
    #lookup_field = 'pk'
    permission_classes = [IsOwnerProductOrReadOnly]
    
    def perform_update(self, serializer):
        slug_value = self.request.POST.get('name')
        slug = slugify(slug_value)
        
        serializer.save(slug = slug) #for now

#Store
class StoreListCreateAPIView(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

class StoreDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    def get_queryset(self):
        queryset = Store.objects.all()
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)

        if min_price is not None and max_price is not None:
            queryset = queryset.filter(products__price__gte=min_price, products__price__lte=max_price) #price in the model
        elif min_price is not None:
            queryset = queryset.filter(products__price__gte=min_price)
        elif max_price is not None:
            queryset = queryset.filter(products__price__lte=max_price)
        return queryset.distinct()
    

###########################################
#ViewSets
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet, ModelViewSet
from rest_framework import mixins
from django.contrib.auth.mixins import LoginRequiredMixin

# /store/ -> Get all stores
# /store/1 -> Get one store
class StoreViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        GenericViewSet
    ):#No POST
    
    #queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsOwnerStoreOrReadOnly]
    
    def get_queryset(self):
        queryset = Store.objects.all()
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)

        if min_price is not None and max_price is not None:
            queryset = queryset.filter(products__price__gte=min_price, products__price__lte=max_price) #price in the model
        elif min_price is not None:
            queryset = queryset.filter(products__price__gte=min_price)
        elif max_price is not None:
            queryset = queryset.filter(products__price__lte=max_price)
        return queryset.distinct()


# /product/ -> GET all products
# /product/1 -> GET one product and PUT, DELETE can be editable by the owner
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerProductOrReadOnly, IsStoreOrCustomer]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    def perform_create(self, serializer):
        slug_value = self.request.POST.get('name')
        slug = slugify(slug_value)
        seller = Store.objects.get(user=self.request.user)
        
        serializer.save(slug = slug, seller = seller) #for now

# /category/ -> GET all categories and only admin can add a new category
# /category/1 -> GET one category and only admin can update or delete
class CategoryViewSet(ModelViewSet):
    #queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    def get_queryset(self):
        queryset = Category.objects.all()
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        
        if min_price is not None and max_price is not None:
             queryset = queryset.filter(products__price__gte=min_price, products__price__lte=max_price) #price in the model
        elif min_price is not None:
             queryset = queryset.filter(products__price__gte=min_price)
        elif max_price is not None:
             queryset = queryset.filter(products__price__lte=max_price)
        return queryset.distinct()
    


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [ IsCustomer]
    def get_queryset(self):
        # Oturum açmış kullanıcının sepetini döndür
        return Cart.objects.filter(customer__user=self.request.user)
    
    def perform_create(self, serializer):
        user = self.request.user.customer
        product = self.request.POST.get('product')
        quantity = int(self.request.POST.get('quantity'))
   
        # o kullanıcın o üründen sepetinde varmı diye bir sorgu yapıyoruz
        # first() ise bize sadece BİR tane nesne döndürüyor      
        existing_cart = Cart.objects.filter(customer=user, product=product).first()
  

        if existing_cart:
            # Eğer mevcut bir Cart varsa, quantity'yi artırıyoruz.
             existing_cart.quantity += quantity
             existing_cart.save()
        else:
            # Eğer mevcut Cart yoksa, yeni bir Cart oluşturuyoruz.
            serializer.save(customer=user, quantity=quantity)

#self.request.POST.get('name') Formdaki veri

#GET -> Get customer orders
#POST -> Buy items in the cart
class OrderViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    #queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return Order.objects.filter(customer__user=self.request.user)

    def perform_create(self, serializer):
        customer = self.request.user.customer
        cart = Cart.objects.filter(customer=customer)

        #Check if the cart is not empty
        if not cart.exists():
            raise PermissionDenied("Your cart is empty.")

        #Address Control
        address_id = self.request.data.get('address')
        address = Address.objects.get(id=address_id)
        
        if address.customer.user != self.request.user:
            raise PermissionDenied("You do not have permission to use this address.")
        
        #Total Price
        total_price = sum(item.product.price * item.quantity for item in cart)
        with transaction.atomic():
            order = serializer.save(customer=customer, total_price=total_price)

            #Save Order Details
            for item in cart:
                OrderDetails.objects.create(
                    order = order,
                    product = item.product,
                    quantity = item.quantity,
                    unit_price = item.product.price,
                    total_price = item.product.price * item.quantity
                )
            cart.delete()


# /store-orders/ -> GET store's orders list with details
class StoreOrderListApiView(LoginRequiredMixin, generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [IsStore]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['customer__user__username']
    login_url = "/dj-rest-auth/login"
   
 # /store-orders/1 -> GET one order and maybe update status?
class StoreOrderDetailApiView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer1
    permission_classes = [IsStore]

    # Send context to serializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            "product":self.kwargs.get('pk') 
        })
        return context
    


# /address/ -> GET address list of the customer and POST new address
# /address/1 -> GET one address and customer can update and delete
class AddressViewSet(ModelViewSet):
    #queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return Address.objects.filter(customer__user=self.request.user)
    
    def perform_create(self, serializer):
        customer = self.request.user.customer
        serializer.save(customer=customer)


@api_view(['DELETE'])
def delete_all_cart(request):
    customer = request.user
    cart = Cart.objects.filter(customer__user = customer)
    cart.delete()
    return Response({"detail": "Cart successfully cleared."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def delete_one(request, id):
    customer = request.user
    try:
        cart_item = Cart.objects.get(customer__user=customer, product_id=id)
        
        # Miktarı kontrol et ve bir azalt
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            return Response({"detail": "Quantity decreased by one."}, status=status.HTTP_200_OK)
        else:
            cart_item.delete()
            return Response({"detail": "Item removed from cart."}, status=status.HTTP_204_NO_CONTENT)
    
    except Cart.DoesNotExist:
        return Response({"detail": "Item not found in cart."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_order_status(request, order_id):
    seller = request.user
    order_details = OrderDetails.objects.filter(order=order_id, product__seller__user = seller)
    status_id = request.data.get('status')
    new_status = Status.objects.get(id=status_id)
    for detail in order_details:
        detail.status = new_status 
        detail.save()
    return Response({"detail": "Status Updated."}, status=status.HTTP_200_OK)