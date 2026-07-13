from django.urls import path
from .views import (
    ProductListView,
    AddToCartView,
    CartListView,
    DeleteFromCartView,
    UpdateCartQuantityView,
    get_profile,
    update_profile,
)
from .views import (
    RegisterView,
    LoginView
)
from .views import get_reviews
from .views import create_order, save_order

urlpatterns = [
    path('products/<str:category>/', ProductListView.as_view()),
    path('cart/', CartListView.as_view()),
    path('cart/add/', AddToCartView.as_view()),
    path('cart/delete/<int:pk>/', DeleteFromCartView.as_view()),
    path('cart/update/<int:pk>/', UpdateCartQuantityView.as_view()),
      path(
        'register/',
        RegisterView.as_view()
    ),
     path(
        'login/',
        LoginView.as_view()
    ),
    path("profile/", get_profile),
    path("profile/update/", update_profile),
    path(
    "reviews/",
    get_reviews
),
    path(
    "create-order/",
    create_order
),
    path(
        "save-order/",
        save_order
    ),
   
]

git config --global user.name "aajin2837-source"
git config --global user.email "aajin2837@gamil.com"