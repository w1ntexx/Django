from django.urls import path, register_converter
from . import views
from . import convertor

register_converter(convertor.FourDigitYearConverter, "year4")

urlpatterns = [
    path("", views.CatHome.as_view(), name='home'),
    path("about/", views.about, name='about'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact', views.contact, name='contact'),
    path("post/<slug:post_slug>/", views.ShowPost.as_view(), name='post'),
    path("species/<slug:spec_slug>/", views.CatSpecies.as_view(), name='species'),
    path("tag/<slug:tag_slug>/", views.TagPostList.as_view(), name='tag'),
    path("edit/<slug:slug>/", views.UpdatePage.as_view(), name='edit_page') 
]


