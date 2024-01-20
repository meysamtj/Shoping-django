from orders.models import Order, OrderItem
from product.models import Product
from account.models import CustomUser
from model_bakery import baker
from django.test import TestCase
from django.core.exceptions import ValidationError


class TestOrder(TestCase):
    def setUp(self):
        self.user = baker.make(CustomUser, email="mamad@gmail.com")
        self.order = baker.make(Order, user=self.user)

    def test_model_str(self):
        self.assertEqual(str(self.order), 'user -->mamad@gmail.com total--> 0')


class TestOrderItem(TestCase):
    def setUp(self):
        self.product = baker.make(Product, name="iphone", price_discount=10, inventory=30)
        self.order_item = baker.make(OrderItem, product=self.product, quantity=2)
        # self.order_item_clean = baker.make(OrderItem,  product=self.product, quantity=50)

        self.product2 = baker.make(Product, name='product',price=500,inventory=10)
        self.orderitem=baker.make(OrderItem,product=self.product2,quantity=2)
        self.orderitem2=baker.make(OrderItem,product=self.product,quantity=3)

    def test_model_str(self):
        self.assertEqual(str(self.orderitem),
                         'product X 2')

    def test_model_get_cost(self):
        self.assertEqual(self.orderitem.get_cost(), 1000)

    def test_clean(self):
        with self.assertRaises(ValidationError):
            order_item = baker.prepare(OrderItem, product=self.product, quantity=31)
            order_item.full_clean()
        # with self.assertRaises(ValidationError):
        #     self.order_item_clean.clean()

    def test_counter_cell_product(self):
        print(OrderItem.counter_cell_product(self.product2))
        self.assertEqual(OrderItem.counter_cell_product(self.product2), 2)

    def test_top_cell_productt(self):
        print(OrderItem.top_cell_product()) 
        self.assertEqual(OrderItem.top_cell_product()[0], (5, 'iphone'))