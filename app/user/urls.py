from django.urls import path
from .views import CreateTokenView, CreateUserView, ManageUserView
#################################


# identify which app we're creating url on (use it in our tests)
app_name = 'user'
urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('me/', ManageUserView.as_view(), name='me'),
    
]