# Django Expense Tracker – Development Log

## Stage 1: Initial Project Setup
- Create the project using the command `django-admin startproject config`
- Create an application named `expense` using the command `python manage.py startapp expenses`
- Add the application to `INSTALLED_APPS` in `settings.py`
- Run `python manage.py migrate` to create the initial SQLite database

## Stage 2: Create Expense model

Created an Expense model in expenses/models.py with the following fields:

- title: short description of the expense.
- amount: decimal value of the expense.
- category: choice field for categorizing the expense.
- date: date of the expense.
- user: ForeignKey to the logged-in user (one-to-many).

Applied migrations:
```python
python manage.py makemigrations tasks
python manage.py migrate
```
This creates the necessary database table to store Expense records.

## Stage 3: Add Expense Form & Template

- Created a `templates/expenses/add_expense.html` file to render the form for adding expenses.
- Used Django’s `forms.ModelForm` to generate the form from the `Expense` model.
- Created a `base.html` layout file for consistent design across pages.
- The form is protected with CSRF token and rendered using `{{ form.as_p }}` for simplicity.

📌 URL `/add/` now allows authenticated users to add new expenses.


## Stage 4: Expense List and Delete Feature

- Implemented `expense_list` view to show all expenses of the logged-in user.
- Created `delete_expense` view to allow the user to delete their own expenses.
- Updated `urls.py` with:
  - `/` → expense list
  - `/delete/<id>/` → delete view
- Built `expense_list.html` to display expense table with delete buttons.
- Protected both views with `@login_required`.

## Stage 5: Filtering and Searching Expenses

- Updated `expense_list` view to support filtering by:
  - Title (icontains)
  - Category (exact match)
  - Date range (`start_date` and `end_date`)
- Added a form in `expense_list.html` to submit filters via GET method

This improves user experience by allowing quick searches and targeted views of expenses.

## Stage 6: Monthly Report

- Created `expense_report` view that shows:
  - Total expenses for the current month
  - Expenses grouped by category
- Added template `expense_report.html` for display
- Route: `/report/`

This gives users a quick overview of their spending habits for the current month.

## Stage 7: Edit Expense

- Created `edit_expense` view to allow users to update their own expenses.
- Added URL route: `edit/<int:expense_id>/`
- Created template: `edit_expense.html` with a pre-filled form for editing.
- Updated `expense_list.html` to include an "Edit" link per expense.

This stage completed full CRUD functionality for user expenses.
