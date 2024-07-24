import pytest
from file_manager import GameCollectionFileManager
from collection import Collection

# Define a fixture for the file manager and test collections
@pytest.fixture
def setup_data():
    file_manager = GameCollectionFileManager()
    test_collections = [Collection('game1', 'owner1'), Collection('game2', 'owner2')]
    test_file = 'test_game_collection.txt'
    return file_manager, test_collections, test_file

# def test_read(setup_data):
#     file_manager, test_collections, test_file = setup_data

#     # Write test collections to the file
#     file_manager.write(test_file, test_collections)

#     # Read collections from the file
#     collections = file_manager.read(test_file)

#     # Check that the correct number of collections were read
#     assert len(collections) == len(test_collections)

#     # Check that the collections have the correct attributes
#     for i in range(len(collections)):
#         assert collections[i].game_name == test_collections[i].game_name
#         assert collections[i].owner == test_collections[i].owner

# def test_write(setup_data):
#     file_manager, test_collections, test_file = setup_data

#     # Write test collections to the file
#     file_manager.write(test_file, test_collections)

#     # Read the file and check that it has the correct number of lines
#     with open(test_file, 'r') as file:
#         lines = file.readlines()
#         assert len(lines) == len(test_collections) + 1  # +1 for the 'END' line

#     # Check that the 'END' line is correct
#     assert lines[-1].strip() == 'END__________________________________________'

# Create a test method that tests a failure to read from a file
def test_read_failure(setup_data):
    file_manager, test_collections, test_file = setup_data

    # Attempt to read from a non-existent file
    with pytest.raises(FileNotFoundError):
        file_manager.read('non_existent_file.txt')

# Create a test method that tests a failure to write to a file
def test_write_failure(setup_data):
    file_manager, test_collections, test_file = setup_data

    # Attempt to write to a read-only file
    with pytest.raises(PermissionError):
        file_manager.write('/etc/passwd', test_collections)