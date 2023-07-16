from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from user.models import User
from rest_framework_simplejwt.tokens import AccessToken
from .models import Order, Product


class OrderCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@test.com',
            first_name='test',
            last_name='test',
            password='testpassword'
        )
        self.product = Product.objects.create(name='Test Product', price=10)
        self.access_token = AccessToken.for_user(self.user)

    def test_create_order_with_api_key_and_token(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            HTTP_X_API_KEY='api_key'
        )

        url = '/api/orders/'

        order_post = {
            'shipment_method': 'P',
            'products': [{'id': self.product.id, 'quantity': 2}]
        }

        response = self.client.post(url, order_post, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'orden creada con exito')

    def test_create_order_without_api_key(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
        )

        url = '/api/orders/'

        order_post = {
            'shipment_method': 'P',
            'products': [{'id': self.product.id, 'quantity': 2}]
        }

        response = self.client.post(url, order_post, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_create_order_without_token(self):
        self.client.credentials(
            HTTP_X_API_KEY='api_key'
        )

        url = '/api/orders/'

        order_post = {
            'shipment_method': 'P',
            'products': [{'id': self.product.id, 'quantity': 2}]
        }

        response = self.client.post(url, order_post, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_order_invalid_product(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
        HTTP_X_API_KEY = 'api_key'
        )

        url = '/api/orders/'
        order_post = {
            'shipment_method': 'P',
            'products': [{'id': 999, 'quantity': 2}]
        }

        response = self.client.post(url, order_post, format='json')

        self.assertEqual(response.data['error'], 'el producto id 999 no existe')


    def test_order_price_include_shipment_cost(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            HTTP_X_API_KEY='api_key'
        )

        url = '/api/orders/'
        order_json = {
            'shipment_method': 'E',
            'products': [{'id': self.product.id, 'quantity': 2}]
        }

        response = self.client.post(url, order_json, format='json')

        correct_total_price = self.product.price * 2 + Order.SHIPMENT_METHODS_PRICES.get('E')

        self.assertEqual(response.data['order']['total_price'], correct_total_price)


    def test_order_price_include_shipment_cost2(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            HTTP_X_API_KEY='api_key'
        )

        url = '/api/orders/'
        order_json = {
            'shipment_method': 'S',
            'products': [{'id': self.product.id, 'quantity': 2}]
        }

        response = self.client.post(url, order_json, format='json')

        correct_total_price = self.product.price * 2 + Order.SHIPMENT_METHODS_PRICES.get('S')

        self.assertEqual(response.data['order']['total_price'], correct_total_price)