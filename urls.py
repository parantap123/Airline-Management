from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    url(r'^employee/$', views.detail, name='employee'),
    url(r'^customer/$', views.customer, name='customer'),
    url(r'^employee/employee_login/$', views.employee_login, name='employee_login'),
    url(r'^employee/employee_login/airplane_list/$', views.airplane_list, name='airplane_list'),
    url(r'^employee/employee_login/scheduled_traffic_list/$', views.scheduled_traffic_list, name='scheduled_traffic_list'),
    #url(r'^employee/employee_login/$', views.employee_login, name='employee_login'),
    url(r'^customer/customer_create/$', views.customer_create, name='customer_create'),
    url(r'^customer/customer_webpage/$', views.customer_signin, name='customer_webpage'),
    #url(r'^customer/customer_webpage/see_flights/(^?P<user_name>[w]+)/$', views.see_flights, name='see_flights'),
    path('customer/customer_webpage/<str:user_name>/see_flights', views.see_flights, name='see_flights'),
    path('customer/customer_webpage/<str:user_name>/see_flights/flight_list', views.flight_list, name='flight_list'),
    path('customer/customer_webpage/<str:user_name>/see_flights/flight_list/flight_book', views.flight_book, name='flight_book'),
    path('customer/customer_webpage/<str:user_name>/check_status/', views.customer_check_status, name='check_status'),
    path('customer/customer_webpage/<str:user_name>/update', views.update, name='update'),
    path('customer/customer_webpage/<str:user_name>/update/updating', views.updating, name='updating'),
    url(r'^customer/customer_webpage/logout/$', views.logout_view, name='logout_view'),
    path('customer/customer_webpage/<str:user_name>/', views.go_back, name='go_back'),
    path('customer/customer_webpage/<str:user_name>/check_status/', views.customer_check_status, name='check_status'),
    path('customer/customer_webpage/<str:user_name>/check_status/got_status/', views.customer_got_status, name='got_status'),
    path('customer/customer_webpage/<str:user_name>/web_checkin/', views.web_checkin, name='web_checkin'),
    path('customer/customer_webpage/<str:user_name>/web_checkin/boarding_pass', views.boarding_pass, name='boarding_pass'),
    #path('customer/customer_webpage/<str:user_name>/see_flights', views.see_flights, name='see_flights'),
]
# urlpatterns = [
#     path('', views.index, name='index'),
#     url(r'^employee/$', views.detail, name='employee'),
#     url(r'^customer/$', views.customer, name='customer'),
#     url(r'^employee/employee_login/$', views.employee_login, name='employee_login'),
#     url(r'^customer/customer_create/$', views.customer_create, name='customer_create'),
#     url(r'^customer/customer_webpage/$', views.customer_signin, name='customer_webpage'),
#     #url(r'^customer/customer_webpage/see_flights/(^?P<user_name>[w]+)/$', views.see_flights, name='see_flights'),
#     path('customer/customer_webpage/<str:user_name>/see_flights', views.see_flights, name='see_flights'),
#     path('customer/customer_webpage/<str:user_name>/see_flights/flight_list', views.flight_list, name='flight_list'),
#     path('customer/customer_webpage/<str:user_name>/check_status/', views.customer_check_status, name='check_status'),
#     path('customer/customer_webpage/<str:user_name>/check_status/got_status/', views.customer_got_status, name='got_status'),
# ]