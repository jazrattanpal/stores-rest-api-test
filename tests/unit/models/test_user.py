from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest

class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('test','abcd')

        self.assertEqual(user.username,'test', "Invalid user name")
        self.assertEqual(user.password, 'abcd',"invalid password")

