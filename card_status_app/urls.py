from django.urls import path
from .views import get_card_status, load_card_data

urlpatterns = [
    path('get_card_status/', get_card_status, name='get_card_status'), # get the card status by either passing the card_id or mb number or both
    path('load_card_data/', load_card_data, name='load_card_data'), # first run this, bcz it will load the data into the database.
]