from orders.models import Order, OrderItem
from product.models import Product
from account.models import CustomUser
from product.models import Discount, Product,Like,Comment, Image, Category
from model_bakery import baker
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta


class TestDiscount(TestCase):
    def setUp(self):
        self.discount = baker.make(Discount, type="percent", amount= 2000)
        self.discount_max_dis = baker.make(Discount, type="number", amount = 30, max_dis = 2000)
        self.discount_code= baker.make(Discount, type="percent",discount_code = "kjdandjad")
        self.discount_expire = baker.make(Discount, type="number", amount= 2000, expire = timezone.now())
        # self.discount_expire = baker.make(Discount, type="number", amount= 2000, expire = timezone.now()+ timedelta(days=2))
    def test_model_str(self):
        self.assertEqual(str(self.discount), 'type --> percent amount --> 2000')

    def test_clean(self):
        with self.assertRaises(ValidationError):
             self.discount.clean()
        with self.assertRaises(ValidationError):
             self.discount_max_dis.clean()
        with self.assertRaises(ValidationError):
             self.discount_code.clean()
        with self.assertRaises(ValidationError):
             self.discount_expire.clean()
            

class TestImage(TestCase):
    def setUp(self):
        self.product = baker.make(Product, name="iphone")
        self.image = baker.make(Image, product=self.product)

    def test_model_str(self):
        self.assertEqual(str(self.image),'iphone')


class TestComment(TestCase):
    def setUp(self):
        self.user = baker.make(CustomUser, username="mamad", email="mamad@gmail.com")
        self.product = baker.make(Product, name="iphone")
        self.comment = baker.make(Comment, product=self.product, user = self.user)

    def test_model_str(self):
        self.assertEqual(str(self.comment),'mamad@gmail.com comment for iphone')

class TestLike(TestCase):
    def setUp(self):
        self.user = baker.make(CustomUser, username="mamad", email="mamad@gmail.com")
        self.product = baker.make(Product, name="iphone")
        self.like = baker.make(Like, product=self.product, user = self.user)
        # self.like2 = baker.make(Like, product=self.product, user = self.user)

    def test_model_str(self):
        self.assertEqual(str(self.like),'mamad@gmail.com liked iphone')
    
    def test_clean(self):
        with self.assertRaises(ValidationError):
             self.like.clean()

class TestCategory(TestCase):
    def setUp(self):
        self.category = baker.make(Category, name = "laptop", id=1)

    def test_model_str(self):
        self.assertEqual(str(self.category),'laptop')
    
    def test_save(self):
        self.assertEqual(self.category.slug,'laptop-1')
    
class Testproduct(TestCase):
    def setUp(self):
        self.user_mamad = baker.make(CustomUser, username="mamad", email="mamad@gmail.com")
        self.user_meysam = baker.make(CustomUser, username="meysam", email="meysam@gmail.com")
        self.product = baker.make(Product,id=5, name="iphone", inventory=30)
        self.like = baker.make(Like, product=self.product, user = self.user_mamad)
        self.like2 = baker.make(Like, product=self.product, user = self.user_meysam)
        self.discount = baker.make(Discount, type="number", amount = 30000)
        self.product_laptop = baker.make(Product, name="laptop", inventory=50,price= 20000 , discount=self.discount )


    def test_model_str(self):
        self.assertEqual(str(self.product),'name : iphone | inventory : 30 ')
    
    def test_like_count(self):
        self.assertEqual(self.product.like_count(),2)

    def test_is_like(self):
        self.assertTrue(self.product.is_like(self.user_meysam))
    
    def test_save(self):
        self.assertEqual(self.product.slug,'iphone-5')
    
    def test_clean(self):
        with self.assertRaises(ValidationError):
            self.product_laptop.clean()
    