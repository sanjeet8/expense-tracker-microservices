from django.urls import path
from .views import ExpenseListCreateView, ExpenseDetailView, ExpenseSummaryView, CategoryExpenseSummaryView


urlpatterns = [
    path('expenses/', ExpenseListCreateView.as_view(), name='expense-list-create'),
    path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
    path('expenses/summary/', ExpenseSummaryView.as_view(), name='expense-summary'),
    path('expenses/summary/category/', CategoryExpenseSummaryView.as_view(), name='category-expense-summary'),
]
