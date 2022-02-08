'''
Sometimes when we want to use postgresql, an exception
happends. This because of postgresql prepration.
Before postgresql accept connection it must compelete some prepration,
and Django connect to database before the database is ready.
So that exception happend.
This why we use this helper function that wait for postgresql db.
It's called mocking.
'''
from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase
##################################


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        '''
        Test waiting for db when db is available.
        What happends when we call our command 
        and the database is already available.
        '''
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)
    

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        '''Test waiting for db'''
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
        