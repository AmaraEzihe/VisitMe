from django.urls import path
from . import views
from django.shortcuts import render


urlpatterns = [
    path('', views.landing, name='landing'),
    path('checkin/', views.CheckIn, name='checkin'),
    path('checkindetails/<int:visit_id>/', views.CheckInDetails, name='checkindets'),
    path('visitorspass/<int:visitor_id>/', views.VisitorsPass, name='visitorspass'),
    path('pagenotfound/', views.PageNotFound, name='pagenotfound'),
    path("photo/<int:visitor_id>/", views.PhotoPage, name="photo_page"),
    path("visitorphoto/<int:visitor_id>/", views.Visitor_Photo, name="visitorphoto"),
    path("sendmail/<int:visitor_id>/", views.SendMail, name="sendmail"),
    path("checkout/", views.CheckOut, name="checkout"),
    path("checkoutdetails/<int:visitor_id>/", views.CheckOutDetails, name="checkoutdetails"),
]

