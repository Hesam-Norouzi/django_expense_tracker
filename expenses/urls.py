from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_expense, name='add_expense'),
    path('', views.expense_list, name='expense_list'),
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('report/', views.expense_report, name='expense_report'),
    path('edit/<int:expense_id>/', views.edit_expense, name='edit_expense'),


]