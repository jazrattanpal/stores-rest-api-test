import json
from models.store import  StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest

class ItemTest(BaseTest):


    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp =client.get('/item/test')
                self.assertEqual(resp.status_code,401)

    def test_get_item_not_found(self):
       pass
    #not working chapter 7 writing our system tests

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99,1).save_to_db()

                resp = client.delete('/item/test')
                self.assertEqual(resp.status_code,200)
                self.assertDictEqual({'message': 'Item deleted'},json.loads(resp.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                resp = client.post('/item/test',
                                   data=json.dumps({'price': 17.99, 'store_id': 1}),
                                   headers = {'Content-Type': 'application/json'})  # Correct Content-Type header

                self.assertDictEqual({'name': 'test', 'price': 17.99},
                                        json.loads(resp.data))
                self.assertEqual(resp.status_code,201)

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                resp = client.post('/item/test',
                                   data=json.dumps({'price': 17.99, 'store_id': 1}),
                                   headers={'Content-Type': 'application/json'})
                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual({'message': 'An item with name \'test\' already exists.'},json.loads(resp.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.put('/item/test',
                                   data=json.dumps({'price': 17.99, 'store_id': 1}),
                                   headers={'Content-Type': 'application/json'})
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price,17.99)
                self.assertDictEqual({'name': 'test', 'price': 17.99},
                                    json.loads(resp.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test',5.99,1).save_to_db()
                self.assertEqual(ItemModel.find_by_name('test').price, 5.99)
                resp = client.put('/item/test',
                                  data=json.dumps({'price': 17.99, 'store_id': 1}),
                                  headers={'Content-Type': 'application/json'})
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual({'name': 'test', 'price': 17.99},
                                     json.loads(resp.data))

    def test_item_listy(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 5.99, 1).save_to_db()

                resp = client.get('/items')

                self.assertDictEqual({'items': [{'name': 'test', 'price': 5.99}]},
                                     json.loads(resp.data))
