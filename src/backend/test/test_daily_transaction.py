import pytest
from unittest.mock import patch, mock_open
from datetime import datetime, timedelta
from file_manager import DailyTransactionFileManager

# @patch('glob.glob')
# def test_read(mock_glob):
#     # Arrange
#     dtfm = DailyTransactionFileManager()
#     mock_glob.return_value = ['file1.txt', 'file2.txt']

#     # Act
#     files = dtfm.read()

#     # Assert
#     assert len(files) == 2
#     assert files[0] == 'file1.txt'
#     assert files[1] == 'file2.txt'

# @patch('builtins.open', new_callable=mock_open)
# @patch('glob.glob')
# def test_write(mock_glob, mock_file):
#     # Arrange
#     dtfm = DailyTransactionFileManager()
#     mock_glob.return_value = ['file1.txt', 'file2.txt']
#     mock_file().read.side_effect = ['content1', 'content2']

#     # Act
#     dtfm.write()

#     # Assert
#     mock_file.assert_called_with('merged.txt', 'w')
#     mock_file().write.assert_any_call('content1')
#     mock_file().write.assert_any_call('content2')