from .forms import ExpenseForm, CategoryForm
from .models import Expense, Category
from datetime import date, timedelta
import calendar
from django.utils import timezone
from django.utils.timezone import now
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Sum, Avg, Max, Count
from django.db.models.functions import TruncMonth
from django.views.decorators.http import require_GET


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST or None, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(user=request.user)
    return render(request, 'expenses/add_expense.html', {
    'form': form,
    'view_title': 'Add New Expense',
    'button_text': 'Save'
})



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
        expenses = expenses.filter(category__id=category_query)
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

    category_summary = this_month_expenses.values('category__name').annotate(
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
        form = ExpenseForm(request.POST or None, instance=expense, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(user=request.user, instance=expense)
    return render(request, 'expenses/edit_expense.html', {
    'form': form,
    'view_title': 'Edit Expense',
    'button_text': 'Save'
})



@login_required
def manage_categories(request):
    if request.method == 'POST':
        if 'add_category' in request.POST:
            name = request.POST.get('name', '').strip()
            if name:
                Category.objects.create(user=request.user, name=name)
                messages.success(request, "Category added successfully.")
            else:
                messages.error(request, "Category name cannot be empty.")

        elif 'edit_category' in request.POST:
            category_id = request.POST.get('category_id')
            new_name = request.POST.get('new_name', '').strip()
            try:
                category = Category.objects.get(id=category_id, user=request.user)
                if new_name:
                    category.name = new_name
                    category.save()
                    messages.success(request, "Category updated successfully.")
                else:
                    messages.error(request, "New category name cannot be empty.")
            except Category.DoesNotExist:
                messages.error(request, "Category not found.")

        elif 'delete_category' in request.POST:
            category_id = request.POST.get('category_id')
            try:
                category = Category.objects.get(id=category_id, user=request.user)
                category.delete()
                messages.success(request, "Category deleted successfully.")
            except Category.DoesNotExist:
                messages.error(request, "Category not found.")

    categories = Category.objects.filter(user=request.user)
    return render(request, 'expenses/manage_categories.html', {'categories': categories})


def add_category_ajax(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if not name:
            return JsonResponse({'status': 'error', 'message': 'Category name required'})

        try:
            category, created = Category.objects.get_or_create(user=request.user, name=name)
            if not created:
                return JsonResponse({'status': 'error', 'message': 'This category already exists'})
            return JsonResponse({'status': 'success', 'id': category.id, 'name': category.name})
        except IntegrityError:
            return JsonResponse({'status': 'error', 'message': 'Category already exists'})



@login_required
def edit_category_ajax(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == 'POST':
        new_name = request.POST.get('name', '').strip()
        if new_name:
            category.name = new_name
            category.save()
            return JsonResponse({'status': 'success', 'id': category.id, 'name': category.name})
        return JsonResponse({'status': 'error', 'message': 'New name cannot be empty.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@login_required
def delete_category_ajax(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == 'POST':
        category.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@login_required
def dashboard(request):
    return render(request, 'expenses/dashboard.html')

@login_required
@require_GET
def dashboard_data(request):
    user = request.user
    today = now()
    current_month = today.month
    current_year = today.year

    # All expenses for this user
    expenses = Expense.objects.filter(user=user)

    # --- Monthly Stats ---
    monthly_expenses = expenses.filter(date__year=current_year, date__month=current_month)

    total_spent = monthly_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    count_expenses = monthly_expenses.count()
    avg_expense = monthly_expenses.aggregate(Avg('amount'))['amount__avg'] or 0
    max_expense = monthly_expenses.aggregate(Max('amount'))['amount__max'] or 0
    last_expense = monthly_expenses.order_by('-date').first()
    last_date = last_expense.date.strftime("%Y-%m-%d") if last_expense else "N/A"

    # --- Growth compared to previous month ---
    previous_month = current_month - 1 or 12
    previous_year = current_year if current_month > 1 else current_year - 1

    prev_total = expenses.filter(date__year=previous_year, date__month=previous_month)\
                         .aggregate(Sum('amount'))['amount__sum'] or 0
    growth = ((total_spent - prev_total) / prev_total) * 100 if prev_total > 0 else None

    # --- Pie Chart: category distribution for current month ---
    category_data_qs = monthly_expenses.values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')

    category_labels = [item['category__name'] or 'Uncategorized' for item in category_data_qs]
    category_data = [float(item['total']) for item in category_data_qs]

    top_category = category_data_qs[0]['category__name'] if category_data_qs else "N/A"

    # --- Bar Chart: total per month for this year ---
    month_labels = []
    monthly_totals = []

    for i in range(1, 13):
        label = calendar.month_abbr[i]
        month_labels.append(label)
        total = expenses.filter(date__year=current_year, date__month=i)\
                        .aggregate(Sum('amount'))['amount__sum'] or 0
        monthly_totals.append(float(total))

    # --- Last 6 months (optional: use if needed for line/bar chart) ---
    last_6_months_qs = expenses.filter(
        date__gte=today.replace(day=1) - timedelta(days=180)
    ).annotate(month=TruncMonth('date')).values('month').annotate(
        total=Sum('amount')
    ).order_by('month')

    last_6_months = [item['month'].strftime('%b %Y') for item in last_6_months_qs]
    last_6_totals = [float(item['total']) for item in last_6_months_qs]

    return JsonResponse({
        # Pie chart
        'category_labels': category_labels,
        'category_data': category_data,

        # Bar chart (12 months)
        'months': month_labels,
        'month_totals': monthly_totals,

        # Optional last 6 months
        'last_6_months': last_6_months,
        'last_6_totals': last_6_totals,

        # Stats
        'total_spent': round(total_spent, 2),
        'count_expenses': count_expenses,
        'avg_expense': round(avg_expense, 2),
        'max_expense': round(max_expense, 2),
        'last_date': last_date,
        'growth_percent': round(growth, 2) if growth is not None else None,
        'top_category': top_category,
    })