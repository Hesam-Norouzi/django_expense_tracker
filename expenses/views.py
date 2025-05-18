from django.shortcuts import render, redirect
from .forms import ExpenseFrom
from django.contrib.auth.decorators import login_required
from .models import Expense

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseFrom(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseFrom()
    return render(request, 'expenses/add_expense.html', {'form': form})


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})