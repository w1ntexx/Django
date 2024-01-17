from django.urls import path, register_converter
from . import views
from . import convertor

register_converter(convertor.FourDigitYearConverter, "year4")

urlpatterns = [
    path("", views.index, name='home'),
    path("about/", views.about, name='about'),
    path('addpage/', views.add_page, name='add_page'),
    path('contact', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path("post/<slug:post_slug>/", views.show_post, name='post'),
    path("species/<slug:spec_slug>/", views.show_species, name='species'),
]
