from django.urls import path, include
from . import views
from .views import StoreViewSet, ProductViewSet, CategoryViewSet, CartViewSet, OrderViewSet, AddressViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'store', StoreViewSet, basename='store')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'address', AddressViewSet, basename='address')

#status değerini güncelleme
#cart item silme ve delete all
# {customer}/delete-all || {customer}/delete-one/{product} (no need) || {customer}/delete-product/{product}   
urlpatterns = [
    path('', include(router.urls)),
    path('store-orders', views.StoreOrderListApiView.as_view()),
    path('store-orders/<int:pk>',views.StoreOrderDetailApiView.as_view(), name='store-order-detail'),
    path('cart/delete-all', views.delete_all_cart),
    path('cart/<int:id>/delete-one', views.delete_one),
    path('store-orders/<int:order_id>/update', views.update_order_status)
    #!path("category", views.CategoryListCreateAPIView.as_view()),
    #!path("category/<int:pk>", views.CategoryDetailAPIView.as_view(), name="category-detail"),
    #path("update/<int:pk>",views.category_update),
    #path("delete/<int:pk>", views.category_delete),
    #!path("product",views.ProductListCreateAPIView.as_view()),
    #path("product/delete/<int:pk>",views.product_delete),
    #!path("product/<int:pk>", views.ProductDetailAPIView.as_view(), name="product-detail"),
    #!path("product/update/<int:pk>",views.ProductDetailAPIView.as_view()),
    #!path("product/create",views.ProductListCreateAPIView.as_view()),
    #!path("store/<int:pk>", views.StoreDetailAPIView.as_view(), name="store-detail"),
    #!path("store",views.StoreListCreateAPIView.as_view())
]

# urlpatterns = [
#     path("", views.CategoryListCreateAPIView.as_view()),
#     path("category/<int:id>", views.category, name="category-detail"),
#     path("update/<int:id>",views.category_update),
#     path("delete/<int:id>", views.category_delete),
#     path("product",views.product_list),
#     path("product/delete/<int:id>",views.product_delete),
#     path("product/<int:id>", views.product, name="product-detail"),
#     path("product/update/<int:id>",views.product_update),
#     path("product/create",views.product_create),
#     path("store/<int:id>", views.store, name="store-detail")
# ]
