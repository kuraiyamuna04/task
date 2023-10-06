from django.urls import path
from . import views

urlpatterns = [
    path("sign-up", views.SignUpView.as_view(), name="sign-up"),
    path("usersign-up", views.ProfileSignUpView.as_view(), name="sign-up"),
    path("login", views.LoginView.as_view(), name="login"),
    path("profile", views.ProfileView.as_view(), name="profile"),
    path("admin", views.AdminAccessView.as_view(), name="admin_login"),
    path("updateProfile/<str:pk>", views.UpdateProfileView.as_view(), name="admin_profile_update"),
    path("create-user", views.CreateView.as_view(), name="create-user"),
    path("create-userprofile", views.ManagerCreateProfileView.as_view(), name="create-userprofile"),
]
