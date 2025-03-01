from api.services.implement.userService import UserService
from api.services.implement.marketService import MarketService
from api.services.implement.productService import ProductService
from api.services.interface.userServiceInterface import UserServiceInterface
from api.services.interface.marketServiceInterface import MarketServiceInterface
from api.services.interface.productServiceInterface import ProductServiceInterface
from api.repositories.interface.productRepositoryInterface import (
    ProductRepositoryInterface,
)
from api.services.interface.SupplierServiceInterface import SupplierServiceInterface
from api.services.implement.SupplierService import SupplierService

from api.factories.repository_factory import create_market_repository
from api.factories.repository_factory import create_product_repository
from api.factories.repository_factory import create_supplier_repository
from api.factories.repository_factory import create_User_repository


###################################################################
market_service_instance = None


def create_market_service(singleton: bool = False) -> MarketServiceInterface:

    global market_service_instance

    if singleton:
        if market_service_instance is None:
            market_repository = create_market_repository(
                singleton=True
            )  # Get the singleton repository instance
            market_service_instance = MarketService(
                market_repository
            )  # Create singleton service
        return market_service_instance
    else:
        market_repository = create_market_repository(
            singleton=False
        )  # Get a new repository instance
        return MarketService(
            market_repository
        )  # Return a new service instance with the injected repository


###################################################################################################


#####################################################################################
def create_product_service() -> ProductServiceInterface:
    product_repository: ProductRepositoryInterface = create_product_repository()
    return ProductService(product_repository)


#####################################################################################
supplier_service_instance = None


def create_supplier_service(singleton: bool = False) -> SupplierServiceInterface:

    global supplier_service_instance

    if singleton:
        if supplier_service_instance is None:
            supplier_repository = create_supplier_repository(
                singleton=True
            )  # Get the singleton repository instance
            supplier_service_instance = SupplierService(
                supplier_repository
            )  # Create singleton service
        return supplier_service_instance
    else:
        supplier_repository = create_market_repository(
            singleton=False
        )  # Get a new repository instance
        return SupplierService(
            supplier_repository
        )  # Return a new service instance with the injected repository
    #######################################################################################

    #######################################################################################

user_service_instance = None

def create_user_service(singleton: bool = False) -> UserServiceInterface:

    global user_service_instance

    if singleton:
        if supplier_service_instance is None:
            user_repository = create_User_repository(
                singleton=True
            )  # Get the singleton repository instance
            user_service_instance = UserService(
                user_repository
            )  # Create singleton service
        return user_service_instance
    else:
        user_repository = create_User_repository(
            singleton=False
        )  # Get a new repository instance
        return UserService(
            user_repository
        )  # Return a new service instance with the injected repository
