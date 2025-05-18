from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExpenseFrom
from django.contrib.auth.decorators import login_required
from .models import Expense
from django.db.models import Sum
from datetime import date

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

    title_query = request.GET.get('title')
    category_query = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if title_query:
        expenses = expenses.filter(title__icontains=title_query)
    if category_query:
        expenses = expenses.filter(category=category_query)
    if start_date and end_date:
        expenses = expenses.filter(date__range=[start_date, end_date])

    context = {
        'expenses': expenses,
        'title_query': title_query,
        'category_query': category_query,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'expenses/expense_list.html', context)


@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    expense.delete()
    return redirect('expense_list')

@login_required
def expense_report(request):
    today = date.today()
    this_month_expenses = Expense.objects.filter(
        user=request.user,
        date__month=today.month,
        date__year=today.year
    )

    total_amount = this_month_expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    category_summary = this_month_expenses.values('category').annotate(
        total=Sum('amount')
    ).order_by('-total')

    context = {
        'total_amount': total_amount,
        'category_summary': category_summary,
        'month': today.strftime('%B'),
        'year': today.year
    }
    return render(request, 'expenses/expense_report.html', context)


@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        form = ExpenseFrom(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseFrom(instance=expense)
    return render(request, 'expenses/edit_expense.html', {'form': form})
