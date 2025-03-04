from api.repositories.implement.userRepository import UserRepository
from api.repositories.implement.marketRepository import MarketRepository
from api.repositories.interface.userRepositoryInterface import UserRepositoryInterface
from api.repositories.interface.marketRepositoryInterface import MarketRepositoryInterface
from api.repositories.interface.supplierRepositoryInterface import SupplierRepositoryInterface
from api.repositories.implement.SupplierRepository import SupplierRepository
from api.repositories.interface.customerRepositoryInterface import CustomerRepositoryInterface
from api.repositories.implement.customerRepository import CustomerRepository
from api.repositories.interface.productRepositoryInterface import ProductRepositoryInterface
from api.repositories.implement.productRepository import ProductRepository
from api.repositories.interface.orderRepositoryInterface import OrderRepositoryInterface
from api.repositories.implement.orderRepository import OrderRepository
from api.repositories.interface.percentageRepositoryInterface import PercentageRepositoryInterface
from api.repositories.implement.percentageRepository import PercentageRepository



user_repository_instance = None

def create_User_repository(singleton: bool = False) -> UserRepositoryInterface:
    global user_repository_instance
    
    
    if singleton:
        if user_repository_instance is None:
            user_repository_instance = UserRepository()  # Create the singleton instance
        return user_repository_instance
    else:
        return UserRepository()  # Create a new instance each time
#########################################################################
market_repository_instance = None

def create_market_repository(singleton: bool = False) -> MarketRepositoryInterface:
   
    global market_repository_instance
    
    
    if singleton:
        if market_repository_instance is None:
            market_repository_instance = MarketRepository()  # Create the singleton instance
        return market_repository_instance
    else:
        return MarketRepository()  # Create a new instance each time
    
####################################################################################


    
####################################################################################
supplier_repository_instance = None

def create_supplier_repository(singleton: bool = False) -> SupplierRepositoryInterface:
    global supplier_repository_instance
    
    
    if singleton:
        if supplier_repository_instance is None:
            supplier_repository_instance = SupplierRepository()  # Create the singleton instance
        return supplier_repository_instance
    else:
        return SupplierRepository()  # Create a new instance each time
#####################################################################################################################
####################################################################################
customer_repository_instance = None

def create_customer_repository(singleton: bool = False) -> CustomerRepositoryInterface:
    global customer_repository_instance
    
    
    if singleton:
        if customer_repository_instance is None:
            customer_repository_instance = CustomerRepository()  # Create the singleton instance
        return customer_repository_instance
    else:
        return CustomerRepository()  # Create a new instance each time
#####################################################################################################################
####################################################################################
product_repository_instance = None

def create_product_repository(singleton: bool = False) -> ProductRepositoryInterface:
    global product_repository_instance
    
    
    if singleton:
        if product_repository_instance is None:
            product_repository_instance = ProductRepository()  # Create the singleton instance
        return product_repository_instance
    else:
        return ProductRepository()  # Create a new instance each time
#####################################################################################################################
####################################################################################
order_repository_instance = None

def create_order_repository(singleton: bool = False) -> OrderRepositoryInterface:
    global order_repository_instance
    
    
    if singleton:
        if order_repository_instance is None:
            order_repository_instance = OrderRepository()  # Create the singleton instance
        return order_repository_instance
    else:
        return OrderRepository()  # Create a new instance each time
#####################################################################################################################

Percentage_repository_instance = None

def create_Percentage_repository(singleton: bool = False) -> PercentageRepositoryInterface:
    global Percentage_repository_instance
    
    
    if singleton:
        if Percentage_repository_instance is None:
            Percentage_repository_instance = PercentageRepository()  # Create the singleton instance
        return Percentage_repository_instance
    else:
        return PercentageRepository()  # Create a new instance each time
#####################################################################################################################




