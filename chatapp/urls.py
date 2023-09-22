from django.urls import path
from chatapp import views

urlpatterns = [
    path('api/register/', views.RegisterView.as_view()),
    path('api/login/', views.LoginView.as_view()),
    path('api/logout/', views.LogoutView.as_view(), name='logout'),
    path('api/online-users/', views.OnlineUsersView.as_view()),
    path('api/chat/start/', views.StartChatView.as_view()),
    path('api/chat/suggested-friends/<int:user_id>/', views.suggested_friends,name = "suggrested-friends"),
]
