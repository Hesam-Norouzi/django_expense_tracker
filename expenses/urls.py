from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_expense, name='add_expense'),
    path('', views.expense_list, name='expense_list'),
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('report/', views.expense_report, name='expense_report'),
    path('edit/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('categories/', views.manage_categories, name='manage_categories'),
    path('categories/add/', views.add_category_ajax, name='add_category_ajax'),
    path('categories/edit/<int:category_id>/', views.edit_category_ajax, name='edit_category_ajax'),
    path('categories/delete/<int:category_id>/', views.delete_category_ajax, name='delete_category_ajax'),


]