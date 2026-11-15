from django.urls import path
from . import views

# TODO 14: API URL patterns (include() adds the 'api/' prefix)
urlpatterns = [
    path('quote/', views.random_quote_api, name='random_quote_api'),
    path('quotes/', views.quotes_api, name='quotes_api'),
    path('quotes/<int:id>/', views.quote_detail_api, name='quote_detail_api'),
]
