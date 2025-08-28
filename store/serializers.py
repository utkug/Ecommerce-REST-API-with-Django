from django.urls import reverse
from rest_framework import serializers
from .models import Category, Product, Store, Customer, Cart, Order, OrderDetails, Address, Status

# It takes pk from url and then it creates a url with product-detail
class CategorySerializer(serializers.ModelSerializer):
    products = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name="product-detail",
        lookup_field = "pk"
    )
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["slug"]
    
    seller = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name="store-detail",
        lookup_field = 'pk'
    )
    # One product can have more than one category??
    category = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),
        many=True,
        view_name="category-detail",
        lookup_field="pk"
    )


class StoreSerializer(serializers.ModelSerializer):
    #products = ProductSerializer(many=True, read_only=True)
    products = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name="product-detail",
        lookup_field = 'pk'
    )
    name = serializers.SerializerMethodField()
    class Meta:
        model = Store
        #fields = '__all__'
        exclude = ['user']
    def get_name(self, obj):
        return obj.user.username if obj.user else None
    
from dj_rest_auth.registration.serializers import RegisterSerializer

# For Registration Page dj-auth
class CustomRegisterSerializer(RegisterSerializer):
    is_store = serializers.BooleanField(default=False)
    is_customer = serializers.BooleanField(default=False)
    phone = serializers.CharField(max_length=15, required=False, allow_blank=True)

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        is_store = self.validated_data.get('is_store', False)
        is_customer = self.validated_data.get('is_customer', False)

        user.is_store = is_store
        user.is_customer = is_customer
        user.phone = self.validated_data.get('phone', '')
        user.save()

        if is_store:
            Store.objects.create(user=user)
        elif is_customer:
            Customer.objects.create(user=user)

        return user


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        #fields = ['id','product', 'quantity', ]

# For Customer
class OrderSerializer(serializers.ModelSerializer):
    order_details = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = '__all__'
        #fields = ['address']   
    # It takes user object and filters the order details
    def get_order_details(self, obj):
        request = self.context.get('request')
        user = request.user
        order_details = OrderDetails.objects.filter(order__customer__user=user, order=obj)
        return OrdersSerializer(order_details, many=True).data
    

# They are serializer to use in this py
class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = '__all__' 


class NormalOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'



class OrderSerializer1(serializers.ModelSerializer):
    order_details = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = '__all__' 
    # It take the context from the view and filters
    def get_order_details(self, obj):
        request = self.context.get('request')
        product_id = self.context.get('product')
        user = request.user
        order_details = OrderDetails.objects.filter(product__seller__user=user, order=product_id)
        return OrdersSerializer(order_details, many=True).data
    
# For Store
class OrderListSerializer(serializers.ModelSerializer):
    order_details = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = '__all__'
    def get_order_details(self, obj):
        request = self.context.get('request')
        user = request.user
        order_details = OrderDetails.objects.filter(product__seller__user=user, order=obj)
        return OrdersSerializer(order_details, many=True).data
    

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'