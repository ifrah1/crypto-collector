from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('cryptos/', views.cryptos_index, name='index'),
    # path to see each crypto by it self
    path('cryptos/<int:crypto_id>/', views.cryptos_detail, name='detail'),
    # path to create a new crypto
    path('cryptos/create/', views.CryptoCreate.as_view(), name='cryptos_create'),
    # path to update crypto
    path('cryptos/<int:pk>/update/', views.CryptoUpdate.as_view(), name='cryptos_update'),
    # path to delete a crypto
    path('cryptos/<int:pk>/delete/', views.CryptoDelete.as_view(), name='cryptos_delete'),
    # path for adding the purchase 
    path('cryptos/<int:crypto_id>/add_purchase/', views.add_purchase, name='add_purchase'),

    # associate a feelings with a crypto (M:M)
    path('cryptos/<int:crypto_id>/assoc_feelings/<int:feeling_id>/', views.assoc_feeling, name='assoc_feeling'),

    # feelings urls
    path('feelings/', views.feelings_index, name='all_feelings'),
    path('feelings/<int:feeling_id>/', views.feeling_detail, name='feeling_detail'),
    path('feelings/create/', views.Create_feeling.as_view(), name='create_feeling'),
    path('feelings/<int:pk>/update/', views.Update_feeling.as_view(), name='update_feeling'),
    path('feelings/<int:pk>/delete/', views.Delete_feeling.as_view(), name='delete_feeling'),

]