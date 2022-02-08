import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
############################


class Command(BaseCommand):
    '''
    Django command to pause exection until database is available
    
    The handle() method takes one or more poll_ids and sets poll.opened to False for each one. 
    If the user referenced any nonexistent polls, a CommandError is raised. 
    The poll.opened attribute does not exist in the tutorial and was 
    added to polls.models.Question for this example.

    REF : https://docs.djangoproject.com/en/4.0/howto/custom-management-commands/
    
    These two *args, **options are allow us to passing in custom arguments
    and options to our management commands.
    
    We can print things out to the terminal using :
    self.stdout.write()

    We can use styles, too.
    self.stdout.write(self.style.SUCCESS('Database is ready !'))
    '''
    
    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = None
        # while db_conn is a false value
        while not db_conn:
            try:
                # try and set db.conn to the database connection
                db_conn = connections['default']
            # if it tried and the database was unavailable, then this message will print out to the terminal
            except OperationalError:
                self.stdout.write('Database unavailable, waiting one second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database is ready !'))