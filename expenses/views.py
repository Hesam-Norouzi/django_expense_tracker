from django.shortcuts import render, redirect, get_object_or_404
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

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    expense.delete()
    return redirect('expense_list')