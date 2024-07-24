import pytest
from user import User

class TestUser:
    # Test for the get_username() method
    def test_get_username(self):
        user = User("testu", "AA", 0.0)
        assert user.get_username() == "testu"

    # Test for the get_user_type() method
    def test_get_user_type(self):
        user = User("testu", "AA", 0.0)
        assert user.get_user_type() == "AA"

    # Test for the get_credit() method
    def test_get_credit(self):
        user = User("testu", "AA", 0.0)
        assert user.get_credit() == 0.0

    # Test for the add_credit() method
    def test_add_credit(self):
        user = User("testu", "AA", 0.0)
        user.add_credit(1.0)
        assert user.get_credit() == 1.0

    # Test for the remove_credit() method
    def test_remove_credit(self):
        user = User("testu", "AA", 1.0)
        user.remove_credit(1.0)
        assert user.get_credit() == 0.0

    # Test for the set_username() method
    def test_set_username(self):
        user = User("testu", "AA", 0.0)
        user.set_username("testu")
        assert user.get_username() == "testu"

    # Test for the set_user_type() method
    def test_set_user_type(self):
        user = User("testu", "AA", 0.0)
        user.set_user_type("FS")
        assert user.get_user_type() == "FS"

    # Test for the to_string() method
    def test_to_string(self):
        user = User("testu", "AA", 0.0)
        assert user.to_string() == "testu_AA_0.00"
