"""
Test custom django management commands
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

# define the command to patch (using the path with . notation)
@patch('core.management.commands.wait_for_db.Command.check')
class Command(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if db ready"""
        patched_check.return_value = True

        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])

    # def test_wait_for_db_delay(self, patched_check):
    #     """Test waiting for database when getting OperationalError"""
    #     # raise some exceptions if db not ready
    #     # first 2 times raise psycopg2 error, next 3 times raise
    #     # operational error, 6th time return true
    #     # this will mimic the db not being ready for 5 seconds
    #     patched_check.side_effect = [Psycopg2Error] * 2 + \
    #         [OperationalError] * 3 + [True]
        
    #     call_command('wait_for_db')

    #     self.assertEqual(patched_check.call_count, 6)
    #     patched_check.assert_called_with(databases=['default'])



