from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    # setUp() function run before every test we run, sometimes there are set up tasks that need to be done before every test
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'admin@gmail.com',
            password = 'TestPass123'
        )
        # force_login() is a helper function from Client(), we use it instead of login() function when we use test and user must be logged  in
        # https://docs.djangoproject.com/en/4.0/topics/testing/tools/#django.test.Client.force_login
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = 'test@gmail.com',
            password = 'TestPass123',
            name = 'Test user'
        )
        
    
    def test_users_listed(self):
        '''Test users are listed on user page'''
        # the reason we use this helper function is if we wanna change the url in future we don't have to go through and change it
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        
        # check our res, check that http response is 200
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    
    def test_user_change_page(self):
        '''Test the user edit page works'''
        # this variable generates a url like this : /admin/core/user/{self.user.id}
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    
    def test_create_user_page(self):
        '''Test the create user page works'''
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
    
    