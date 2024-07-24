import pytest
import os
import tempfile
from util import file_utils

class TestFileUtils:
    @pytest.fixture
    def setup(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.test_file = tempfile.mkstemp(dir=self.test_dir)[1]
        yield
        os.remove(self.test_file)
        os.rmdir(self.test_dir)

    def test_change_to_file_dir_existing(self, setup):
        # Test changing to an existing directory
        file_utils.change_to_file_dir(self.test_file)
        assert os.getcwd() == self.test_dir

    def test_change_to_file_dir_non_existing(self, setup):
        # Test changing to a non-existing directory
        non_existing_file = os.path.join(self.test_dir, "non_existing/file.txt")
        with pytest.raises(FileNotFoundError):
            file_utils.change_to_file_dir(non_existing_file)
