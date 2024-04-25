import calendar
from datetime import date

from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from .models import Expense
from .forms import ExpenseForm
from django.core.paginator import Paginator
import pdfkit



def index(request):
    current_month = date.today().month
    return render(request, 'expenses/index.html', {'month': current_month})


def contact(request):
    return render(request, 'expenses/contact.html', {})


@login_required
def add_expense(request):
    form = ExpenseForm(request.POST or None, user=request.user)

    if form.is_valid():
        form.save()
        current_month = date.today().month
        return redirect('/expenses/' + str(current_month))

    return render(request, 'expenses/expense-form.html', {'form': form})


@login_required
def month_view(request, month_id):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category_filter', '')
    sort_option = request.GET.get('sort_option', '')

    current_date = date.today()
    year = current_date.year
    current_month = date.today().month
    if month_id == 0:
        expenses = Expense.objects.filter(date__year=year, user=request.user)
        expenses_page = Expense.objects.filter(date__year=year, user=request.user)

    else:
        expenses = Expense.objects.filter(date__year=year, date__month=month_id, user=request.user)
        expenses_page = Expense.objects.filter(date__year=year, date__month=month_id, user=request.user)

    for code, name in Expense.CATEGORIES:
        if name == category_filter:
            category_filter = code

    if search_query != '':
        expenses_page = expenses_page.filter(
            Q(date__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(amount__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    if category_filter:
        expenses_page = expenses_page.filter(
            category__icontains=category_filter,
        )

    expenses_page = expenses_page.order_by(sort_option if sort_option else 'date')

    paginator = Paginator(expenses_page, 10)
    page = request.GET.get('page')
    expenses_page = paginator.get_page(page)

    total_gross_income = sum(expense.amount for expense in expenses if expense.category in ['gross_income'])
    total_net_income = sum(expense.amount for expense in expenses if expense.category in ['net_income'])
    total_expenses = sum(
        expense.amount for expense in expenses if expense.category not in ['gross_income', 'net_income'])

    balance = total_net_income - total_expenses

    category_totals = {}
    for code, name in Expense.CATEGORIES:
        if code in ['gross_income', 'net_income']:
            continue
        total_amount = sum(expense.amount for expense in expenses if expense.category == code)
        category_totals[name] = total_amount

    months = [calendar.month_name[i] for i in range(1, 13)]
    month_name = calendar.month_name[month_id]

    context = {
        'year': year,
        'month': month_name,
        'current_month': current_month,
        'expenses': expenses,
        'expenses_page': expenses_page,
        'paginator': paginator,
        'months': months,
        'total_gross_income': total_gross_income,
        'total_net_income': total_net_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'category_totals': category_totals,
        'month_id': month_id,
        'category_filter': category_filter,
        'sort_option': sort_option,
    }

    return render(request, 'expenses/monthView.html', context)


def pdf(request, month_id):
    current_date = date.today()
    year = current_date.year
    current_month = date.today().month

    if month_id == 0:
        expenses = Expense.objects.filter(date__year=year, user=request.user)

    else:
        expenses = Expense.objects.filter(date__year=year, date__month=month_id, user=request.user)

    total_gross_income = sum(expense.amount for expense in expenses if expense.category in ['gross_income'])
    total_net_income = sum(expense.amount for expense in expenses if expense.category in ['net_income'])
    total_expenses = sum(
        expense.amount for expense in expenses if expense.category not in ['gross_income', 'net_income'])

    balance = total_net_income - total_expenses

    category_totals = {}
    for code, name in Expense.CATEGORIES:
        if code in ['gross_income', 'net_income']:
            continue
        total_amount = sum(expense.amount for expense in expenses if expense.category == code)
        category_totals[name] = total_amount

    months = [calendar.month_name[i] for i in range(1, 13)]
    month_name = calendar.month_name[month_id]
    context = {
        'year': year,
        'month': month_name,
        'current_month': current_month,
        'expenses': expenses,
        'months': months,
        'total_gross_income': total_gross_income,
        'total_net_income': total_net_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'category_totals': category_totals,
        'month_id': month_id,
    }

    template = loader.get_template('expenses/expenses_page.html')
    html = template.render(context)
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
    }
    pdfs = pdfkit.from_string(html, False, options)
    response = HttpResponse(pdfs, content_type='application/pdf')
    filename = f"{month_name}{year}_expenses.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response


