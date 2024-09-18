from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('contact/', views.contact, name='contact'),
    path('checkout/', views.checkout, name='checkout'),
    path('details/<int:id>', views.details, name='details'),
    path('shop/', views.shop, name='shop'),
    path('members/', views.members, name='members'),
    path('register/', views.register, name='register'),
    path('password/', views.password, name='password'),
    path('home/<int:id>', views.homepage, name='home'),
    # category
    path('category/<str:category>',views.categoryPage),
    path('search/<str:category>', views.search),
    # cart
    path('add_to_cart/<int:id>',views.addToCart),
    path('remove/<int:id>', views.remove_from_cart),
    # path('add_product/',views.Add_New_Product),
]