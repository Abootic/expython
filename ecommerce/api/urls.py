from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views.user_views import UserViewSet
from api.views.market_views import MarketViewSet
from api.views.product_views import ProductViewSet
from api.views.Supplier_views import SupplierViewSet
from api.views.login_view import LoginViewSet
from api.views.customer_view import CustomerViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'markets', MarketViewSet, basename='market')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r'customers', CustomerViewSet, basename='customer')

# Register LoginViewSet for useraccess/login
router.register(r'useraccess', LoginViewSet, basename='login')

urlpatterns = [
    path('', include(router.urls)),  # Include router URLs (don't add 'api/' here)
]
