from django.urls import path
from . import views

urlpatterns = [
    path('chatbot_response', views.chatbot_response, name='chatbot_response'),
    path('history', views.get_chat_history, name='get_chat_history'),
    path('make_appointment', views.make_appointment,
         name='make_appointment'),
    path('get_all_appointments', views.get_all_appointments,
         name='get_all_appointments'),
    path('delete_all_appointments', views.delete_all_appointments,
         name='delete_all_appointments'),
    path('delete_appointment/<str:appointment_id>',
         views.delete_appointment, name='delete_appointment'),
    path('make_query', views.make_query, name='make_query'),
    path('get_all_queries', views.get_all_queries, name='get_all_queries'),
    path('delete_query/<str:query_id>',
         views.delete_query, name='delete_query'),
    path('delete_all_queries', views.delete_all_queries,
         name='delete_all_queries'),
    path('get_unresolved_queries', views.get_unresolved_queries,
         name='get_unresolved_queries'),
    path('update_query/<str:query_id>', views.update_query, name='update_query'),
    path('send_email_response', views.send_email_response,
         name='send_email_response'),


]
