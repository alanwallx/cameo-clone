from django.urls import path


from . import views

urlpatterns = [
    path("", views.stars, name="index"),
    path("stars", views.stars, name="stars"),
    path("star/<str:username>", views.star, name="star"),
    path("order", views.order, name="order"),
    path("order/<int:order_id>", views.specific_order, name="specific_order"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup, name="signup"),
    path("stars/upload/<int:order_id>", views.upload, name="upload"),
    path("orders", views.orders, name="orders"),
    path("stardashboard", views.stardashboard, name="stardashboard"),
    path("starcreate", views.starcreate, name="starcreate"),
    path("staredit/<int:pk>", views.staredit, name="staredit"),
    path("staradmin/<int:pk>", views.staradmin, name="staradmin"),
    path("profile/<int:pk>", views.profile, name="profile"),
    path("admindashboard", views.admindashboard, name="admindashboard"),
]
