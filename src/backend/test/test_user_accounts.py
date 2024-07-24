import pytest
from file_manager import UserAccountsFileManager
from user import User
from util import change_to_file_dir

# Define a fixture for the file manager and test users
@pytest.fixture
def setup_data():
    file_manager = UserAccountsFileManager()
    test_users = [User('test1', 'AA', 0.00), User('test2', 'FS', 0.00)]
    change_to_file_dir(__file__)
    test_file = 'test_user_accounts.txt'
    return file_manager, test_users, test_file

def test_read(setup_data):
    file_manager, test_users, test_file = setup_data

    # Write test users to the file
    file_manager.write(test_file, test_users)

    # Read users from the file
    users = file_manager.read(test_file)

    # Check that the correct number of users were read
    assert len(users) == len(test_users)

    # Check that the users have the correct attributes
    for i in range(len(users)):
        assert users[i].username == test_users[i].username
        assert users[i].user_type == test_users[i].user_type
        assert users[i].available_credit == test_users[i].available_credit

def test_write(setup_data):
    file_manager, test_users, test_file = setup_data

    # Write test users to the file
    file_manager.write(test_file, test_users)

    # Read the file and check that it has the correct number of lines
    with open(test_file, 'r') as file:
        lines = file.readlines()
        assert len(lines) == len(test_users) + 1  # +1 for the 'END' line

    # Check that the 'END' line is correct
    assert lines[-1].strip() == 'END_________________________'


# Create a test method that tests a failure to read from a file
def test_read_failure(setup_data):
    file_manager, test_users, test_file = setup_data

    # Attempt to read from a non-existent file
    with pytest.raises(FileNotFoundError):
        file_manager.read('non_existent_file.txt')

# Create a test method that tests a failure to write to a file
def test_write_failure(setup_data):
    file_manager, test_users, test_file = setup_data

    # Attempt to write to a read-only file
    with pytest.raises(PermissionError):
        file_manager.write('/etc/passwd', test_users)