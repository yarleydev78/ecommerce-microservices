import unittest
import json
from product_service import app, products_db

class TestProductService(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        # Restaurar stock para prueba
        products_db[1]['stock'] = 10

    def test_get_product(self):
        response = self.app.get('/products/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Laptop', response.data)

    def test_reduce_stock_success(self):
        payload = {"product_id": 1, "quantity": 2}
        response = self.app.post('/products/reduce_stock', 
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(products_db[1]['stock'], 8)

if __name__ == '__main__':
    unittest.main()
