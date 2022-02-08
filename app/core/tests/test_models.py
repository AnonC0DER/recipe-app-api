from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
##############################################


def sample_user(email='test@gmail.com', password='testpass'):
    '''Create a sample user'''
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    # Create user with email
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@gmail.com'
        password = 'testPass123'
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        # making sure the email address in user equals to email address passed in
        # assertEqual -> check that is user.email equals to email we passed in
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    
    # Email normalized (make the email address lower case)
    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@GMAIL.COM'
        user = get_user_model().objects.create_user(
            email,
            'testPass123'
        )

        self.assertEqual(user.email, email.lower())

    # Invalid email address
    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')
    
    # Create superuser
    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'testPass123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    # Tag string representation
    def test_tag_str(self):
        '''Test the tag string representation'''
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan',
        )

        self.assertEqual(str(tag), tag.name)

    # Ingredient string representation
    def test_ingredient_str(self):
        '''Test the ingredient string representation'''
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    # Create a recipe obj and retrieve it as str
    def test_recipe_str(self):
        '''Test the recipe string representation'''
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom suace',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)
    
    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        '''Test image is saved in the correct location'''
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'    

        self.assertEqual(file_path, exp_path)