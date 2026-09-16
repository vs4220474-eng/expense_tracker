"""
=========================================================
        PERSONAL EXPENSE TRACKER - PRO VERSION

Features:
- Add expenses
- View expenses
- Delete expenses
- Expense reports
- Spending charts
- Budget management
- Category budgets
- Monthly budget
- Budget utilization
- Spending insights
- Monthly comparisons
- Spending warnings
- CSV data storage

Main concepts:
- Lists
- Dictionaries
- Functions
- Loops
- Conditions
- CSV file handling
- Exception handling
- Matplotlib
=========================================================
"""

import csv
import os
from datetime import datetime, timedelta

# ---------------------------------------------------------
# MATPLOTLIB
# ---------------------------------------------------------

try:
    import matplotlib.pyplot as plt
    CHARTS_AVAILABLE = True
except ImportError:
    CHARTS_AVAILABLE = False


# =========================================================
# CONFIGURATION
# =========================================================

DATA_FILE = "expenses.csv"
BUDGET_FILE = "budgets.csv"

FIELDNAMES = [
    "date",
    "category",
    "amount",
    "note"
]

BUDGET_FIELDNAMES = [
    "type",
    "category",
    "month",
    "amount"
]

CURRENCY = "Rs."

CATEGORIES = [
    "Food",
    "Transport",
    "Entertainment",
    "Shopping",
    "Bills",
    "Health",
    "Education",
    "Other"
]


# =========================================================
# UTILITY FUNCTIONS
# =========================================================

def clear_line():
    print("-" * 70)


def pause():
    input("\nPress Enter to continue...")


def current_month():
    return datetime.today().strftime("%Y-%m")


def format_money(amount):
    return f"{CURRENCY}{amount:,.2f}"


# =========================================================
# EXPENSE FILE HANDLING
# =========================================================

def load_expenses(filename=DATA_FILE):
    """Read expenses from CSV."""

    expenses = []

    if not os.path.exists(filename):
        return expenses

    try:
        with open(
            filename,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                try:
                    row["amount"] = float(row["amount"])
                except (ValueError, TypeError, KeyError):
                    continue

                row.setdefault("note", "")
                row.setdefault("category", "Other")
                row.setdefault("date", "")

                expenses.append(row)

    except OSError as error:
        print("Could not read expense file:", error)

    return expenses


def save_expenses(expenses, filename=DATA_FILE):
    """Save expenses to CSV."""

    try:
        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=FIELDNAMES
            )

            writer.writeheader()

            for expense in expenses:
                writer.writerow({
                    "date": expense["date"],
                    "category": expense["category"],
                    "amount": expense["amount"],
                    "note": expense.get("note", "")
                })

        return True

    except OSError as error:
        print("Could not save expense file:", error)
        return False


# =========================================================
# BUDGET FILE HANDLING
# =========================================================

def load_budgets(filename=BUDGET_FILE):
    """Load budgets from CSV."""

    budgets = []

    if not os.path.exists(filename):
        return budgets

    try:
        with open(
            filename,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                try:
                    row["amount"] = float(row["amount"])
                except (ValueError, TypeError, KeyError):
                    continue

                budgets.append(row)

    except OSError as error:
        print("Could not read budget file:", error)

    return budgets


def save_budgets(budgets, filename=BUDGET_FILE):
    """Save budgets to CSV."""

    try:
        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=BUDGET_FIELDNAMES
            )

            writer.writeheader()

            for budget in budgets:
                writer.writerow({
                    "type": budget["type"],
                    "category": budget["category"],
                    "month": budget["month"],
                    "amount": budget["amount"]
                })

        return True

    except OSError as error:
        print("Could not save budget file:", error)
        return False


# =========================================================
# INPUT VALIDATION
# =========================================================

def ask_amount():

    while True:

        text = input("Amount        : ").strip()

        try:
            amount = float(text)

        except ValueError:
            print("  -> Enter a valid number.")
            continue

        if amount <= 0:
            print("  -> Amount must be greater than 0.")
            continue

        return round(amount, 2)


def ask_date():

    while True:

        text = input(
            "Date (YYYY-MM-DD, blank = today): "
        ).strip()

        if text == "":
            return datetime.today().strftime("%Y-%m-%d")

        try:
            date_object = datetime.strptime(
                text,
                "%Y-%m-%d"
            )

        except ValueError:
            print(
                "  -> Wrong format. Example: 2026-09-16"
            )
            continue

        return date_object.strftime("%Y-%m-%d")


def ask_category():

    print("\nCategories:")

    for index, name in enumerate(
        CATEGORIES,
        start=1
    ):
        print(f"  {index}. {name}")

    while True:

        choice = input(
            "Category (number or name): "
        ).strip()

        if choice == "":
            print("  -> Category cannot be empty.")
            continue

        if choice.isdigit():

            number = int(choice)

            if 1 <= number <= len(CATEGORIES):
                return CATEGORIES[number - 1]

            print(
                f"  -> Choose 1-{len(CATEGORIES)}."
            )
            continue

        return choice.title()


def ask_month():

    while True:

        text = input(
            "Month (YYYY-MM, blank = current): "
        ).strip()

        if text == "":
            return current_month()

        try:
            datetime.strptime(
                text,
                "%Y-%m"
            )

            return text

        except ValueError:
            print(
                "  -> Invalid month. Example: 2026-09"
            )


# =========================================================
# EXPENSE OPERATIONS
# =========================================================

def add_expense(expenses):

    print("\n================ ADD EXPENSE ================")

    amount = ask_amount()
    category = ask_category()
    date = ask_date()

    note = input(
        "Note (optional): "
    ).strip()

    expense = {
        "date": date,
        "category": category,
        "amount": amount,
        "note": note
    }

    expenses.append(expense)

    save_expenses(expenses)

    print("\nExpense saved successfully.")
    print(
        f"{format_money(amount)} → {category}"
    )

    # Check budget immediately
    check_expense_budget(expenses, category, date)


def view_expenses(expenses):

    print("\n================ ALL EXPENSES ================")

    if not expenses:
        print("No expenses recorded yet.")
        return

    ordered = sorted(
        expenses,
        key=lambda item: item["date"],
        reverse=True
    )

    print(
        f"{'No.':<5}"
        f"{'Date':<13}"
        f"{'Category':<17}"
        f"{'Amount':>14}   "
        f"Note"
    )

    clear_line()

    for number, expense in enumerate(
        ordered,
        start=1
    ):

        amount_text = format_money(
            expense["amount"]
        )

        print(
            f"{number:<5}"
            f"{expense['date']:<13}"
            f"{expense['category']:<17}"
            f"{amount_text:>14}   "
            f"{expense.get('note', '')}"
        )

    clear_line()

    print(
        f"{'TOTAL':<35}"
        f"{format_money(total_spent(expenses)):>14}"
    )


def delete_expense(expenses):

    if not expenses:
        print("\nNothing to delete.")
        return

    view_expenses(expenses)

    choice = input(
        "\nNumber to delete (blank = cancel): "
    ).strip()

    if choice == "":
        return

    try:
        index = int(choice)

    except ValueError:
        print("  -> Enter a valid number.")
        return

    ordered = sorted(
        expenses,
        key=lambda item: item["date"],
        reverse=True
    )

    if not 1 <= index <= len(ordered):
        print("  -> Invalid expense number.")
        return

    removed = ordered[index - 1]

    expenses.remove(removed)

    save_expenses(expenses)

    print(
        f"\nDeleted {removed['category']} "
        f"expense of {format_money(removed['amount'])}."
    )


# =========================================================
# CALCULATIONS
# =========================================================

def total_spent(expenses):

    return sum(
        expense["amount"]
        for expense in expenses
    )


def spending_by_category(expenses):

    totals = {}

    for expense in expenses:

        category = expense["category"]

        totals[category] = (
            totals.get(category, 0)
            + expense["amount"]
        )

    return totals


def spending_by_month(expenses):

    totals = {}

    for expense in expenses:

        month = expense["date"][:7]

        totals[month] = (
            totals.get(month, 0)
            + expense["amount"]
        )

    return dict(sorted(totals.items()))


def highest_expense(expenses):

    if not expenses:
        return None

    return max(
        expenses,
        key=lambda item: item["amount"]
    )


def expenses_for_month(expenses, month):

    return [
        expense
        for expense in expenses
        if expense["date"].startswith(month)
    ]


def category_spending_for_month(
    expenses,
    category,
    month
):

    return sum(
        expense["amount"]
        for expense in expenses
        if (
            expense["category"] == category
            and expense["date"].startswith(month)
        )
    )


# =========================================================
# REPORT
# =========================================================

def generate_report(expenses):

    print("\n================ EXPENSE REPORT ================")

    if not expenses:
        print("No data available.")
        return

    total = total_spent(expenses)

    count = len(expenses)

    average = total / count

    print(f"Entries recorded : {count}")
    print(f"Total spent      : {format_money(total)}")
    print(f"Average expense  : {format_money(average)}")

    biggest = highest_expense(expenses)

    print(
        f"Highest expense  : "
        f"{format_money(biggest['amount'])} "
        f"on {biggest['category']} "
        f"({biggest['date']})"
    )

    print("\n--------------- CATEGORY BREAKDOWN ---------------")

    category_totals = spending_by_category(
        expenses
    )

    for category, amount in sorted(
        category_totals.items(),
        key=lambda pair: pair[1],
        reverse=True
    ):

        share = (
            amount / total * 100
            if total > 0
            else 0
        )

        bar = "#" * int(
            share / 4
        )

        print(
            f"{category:<18}"
            f"{format_money(amount):>14}"
            f"   {share:>5.1f}%  "
            f"{bar}"
        )

    print("\n--------------- MONTHLY BREAKDOWN ---------------")

    for month, amount in spending_by_month(
        expenses
    ).items():

        print(
            f"{month:<18}"
            f"{format_money(amount):>14}"
        )


# =========================================================
# BUDGET MANAGEMENT
# =========================================================

def set_budget(budgets):

    print("\n================ SET BUDGET ================")

    print("1. Overall Monthly Budget")
    print("2. Category Monthly Budget")

    choice = input(
        "\nChoose budget type: "
    ).strip()

    if choice == "1":

        budget_type = "overall"
        category = "Overall"

    elif choice == "2":

        budget_type = "category"
        category = ask_category()

    else:

        print("Invalid choice.")
        return

    month = ask_month()

    print(
        f"\nBudget for {category} - {month}"
    )

    amount = ask_amount()

    # Update existing budget
    updated = False

    for budget in budgets:

        if (
            budget["type"] == budget_type
            and budget["category"] == category
            and budget["month"] == month
        ):

            budget["amount"] = amount
            updated = True
            break

    # Create new budget
    if not updated:

        budgets.append({
            "type": budget_type,
            "category": category,
            "month": month,
            "amount": amount
        })

    save_budgets(budgets)

    if updated:
        print("\nBudget updated successfully.")
    else:
        print("\nBudget created successfully.")

    print(
        f"{category} budget: "
        f"{format_money(amount)}"
    )


def get_budget(
    budgets,
    budget_type,
    category,
    month
):

    for budget in budgets:

        if (
            budget["type"] == budget_type
            and budget["category"] == category
            and budget["month"] == month
        ):
            return budget["amount"]

    return None


def view_budgets(
    expenses,
    budgets
):

    print("\n================ BUDGET STATUS ================")

    month = current_month()

    print(f"Current month: {month}")

    overall_budget = get_budget(
        budgets,
        "overall",
        "Overall",
        month
    )

    month_expenses = expenses_for_month(
        expenses,
        month
    )

    total = total_spent(
        month_expenses
    )

    print("\n------------- OVERALL BUDGET -------------")

    if overall_budget is None:

        print("No overall monthly budget set.")

    else:

        show_budget_status(
            "Overall",
            overall_budget,
            total
        )

    print("\n------------- CATEGORY BUDGETS -------------")

    category_totals = spending_by_category(
        month_expenses
    )

    category_budget_found = False

    for category in CATEGORIES:

        budget_amount = get_budget(
            budgets,
            "category",
            category,
            month
        )

        if budget_amount is None:
            continue

        category_budget_found = True

        spent = category_totals.get(
            category,
            0
        )

        show_budget_status(
            category,
            budget_amount,
            spent
        )

    if not category_budget_found:

        print(
            "No category budgets configured."
        )


def show_budget_status(
    name,
    budget,
    spent
):

    remaining = budget - spent

    if budget > 0:

        percentage = (
            spent / budget
        ) * 100

    else:

        percentage = 0

    # Keep visual bar between 0 and 100
    visual_percentage = min(
        max(percentage, 0),
        100
    )

    filled = int(
        visual_percentage / 5
    )

    bar = (
        "#" * filled
        + "-" * (20 - filled)
    )

    print(f"\n{name}")

    print(
        f"Budget     : {format_money(budget)}"
    )

    print(
        f"Spent      : {format_money(spent)}"
    )

    print(
        f"Remaining  : {format_money(remaining)}"
    )

    print(
        f"Used       : {percentage:.1f}%"
    )

    print(
        f"Progress   : [{bar}]"
    )

    if percentage >= 100:

        print(
            "STATUS     : OVER BUDGET"
        )

    elif percentage >= 80:

        print(
            "STATUS     : WARNING - NEAR LIMIT"
        )

    elif percentage >= 50:

        print(
            "STATUS     : MODERATE"
        )

    else:

        print(
            "STATUS     : WITHIN BUDGET"
        )


def check_expense_budget(
    expenses,
    category,
    date
):

    month = date[:7]

    # Load current budgets
    budgets = load_budgets()

    budget = get_budget(
        budgets,
        "category",
        category,
        month
    )

    if budget is None:
        return

    spent = category_spending_for_month(
        expenses,
        category,
        month
    )

    percentage = (
        spent / budget
    ) * 100

    if percentage >= 100:

        print(
            "\nWARNING:"
        )

        print(
            f"You have exceeded your "
            f"{category} budget."
        )

        print(
            f"Spent: {format_money(spent)} / "
            f"{format_money(budget)}"
        )

    elif percentage >= 80:

        print(
            "\nBudget Alert:"
        )

        print(
            f"{category} budget is "
            f"{percentage:.1f}% used."
        )


def budget_management(
    expenses,
    budgets
):

    while True:

        print(
            "\n================ BUDGET MANAGEMENT ================"
        )

        print("1. Set / Update Budget")
        print("2. View Budget Status")
        print("3. Back to Main Menu")

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":

            set_budget(budgets)

        elif choice == "2":

            view_budgets(
                expenses,
                budgets
            )

            pause()

        elif choice == "3":

            break

        else:

            print(
                "Invalid choice."
            )


# =========================================================
# SPENDING INSIGHTS
# =========================================================

def generate_insights(
    expenses,
    budgets
):

    print("\n================ SMART SPENDING INSIGHTS ================")

    if not expenses:

        print(
            "\nNo expense data available."
        )

        print(
            "Add some expenses first."
        )

        return

    month = current_month()

    current_expenses = expenses_for_month(
        expenses,
        month
    )

    current_total = total_spent(
        current_expenses
    )

    # -----------------------------------------------------
    # BASIC SUMMARY
    # -----------------------------------------------------

    print("\n--------------- CURRENT MONTH ---------------")

    print(
        f"Month: {month}"
    )

    print(
        f"Total spending: "
        f"{format_money(current_total)}"
    )

    if current_expenses:

        average_daily = (
            current_total
            / datetime.today().day
        )

        print(
            f"Average daily spending: "
            f"{format_money(average_daily)}"
        )

    # -----------------------------------------------------
    # TOP CATEGORY
    # -----------------------------------------------------

    category_totals = spending_by_category(
        current_expenses
    )

    if category_totals:

        top_category = max(
            category_totals,
            key=category_totals.get
        )

        top_amount = category_totals[
            top_category
        ]

        share = (
            top_amount / current_total * 100
            if current_total > 0
            else 0
        )

        print(
            "\nINSIGHT 1 - TOP CATEGORY"
        )

        print(
            f"{top_category} is your largest "
            f"spending category."
        )

        print(
            f"You spent {format_money(top_amount)} "
            f"({share:.1f}% of this month's spending)."
        )

    # -----------------------------------------------------
    # LARGEST EXPENSE
    # -----------------------------------------------------

    largest = highest_expense(
        current_expenses
    )

    if largest:

        print(
            "\nINSIGHT 2 - LARGEST TRANSACTION"
        )

        print(
            f"Largest expense: "
            f"{format_money(largest['amount'])}"
        )

        print(
            f"Category: {largest['category']}"
        )

        print(
            f"Date: {largest['date']}"
        )

        if largest.get("note"):

            print(
                f"Note: {largest['note']}"
            )

    # -----------------------------------------------------
    # MONTHLY COMPARISON
    # -----------------------------------------------------

    today = datetime.today()

    first_day_current = today.replace(
        day=1
    )

    previous_month_date = (
        first_day_current
        - timedelta(days=1)
    )

    previous_month = (
        previous_month_date.strftime("%Y-%m")
    )

    previous_expenses = expenses_for_month(
        expenses,
        previous_month
    )

    previous_total = total_spent(
        previous_expenses
    )

    print(
        "\nINSIGHT 3 - MONTHLY COMPARISON"
    )

    if previous_total > 0:

        difference = (
            current_total
            - previous_total
        )

        percentage_change = (
            difference
            / previous_total
        ) * 100

        if difference > 0:

            print(
                f"Spending is {percentage_change:.1f}% "
                f"higher than {previous_month}."
            )

        elif difference < 0:

            print(
                f"Spending is {abs(percentage_change):.1f}% "
                f"lower than {previous_month}."
            )

        else:

            print(
                "Spending is unchanged compared "
                "with the previous month."
            )

        print(
            f"Previous month: "
            f"{format_money(previous_total)}"
        )

        print(
            f"Current month: "
            f"{format_money(current_total)}"
        )

    else:

        print(
            f"No spending data available "
            f"for {previous_month}."
        )

    # -----------------------------------------------------
    # CATEGORY INCREASE
    # -----------------------------------------------------

    if previous_expenses:

        previous_categories = spending_by_category(
            previous_expenses
        )

        print(
            "\nINSIGHT 4 - CATEGORY CHANGES"
        )

        changes_found = False

        for category in category_totals:

            current_amount = category_totals.get(
                category,
                0
            )

            previous_amount = previous_categories.get(
                category,
                0
            )

            if previous_amount > 0:

                change = (
                    (
                        current_amount
                        - previous_amount
                    )
                    / previous_amount
                ) * 100

                if abs(change) >= 20:

                    changes_found = True

                    if change > 0:

                        print(
                            f"{category}: "
                            f"+{change:.1f}%"
                        )

                    else:

                        print(
                            f"{category}: "
                            f"{change:.1f}%"
                        )

        if not changes_found:

            print(
                "No major category change detected."
            )

    # -----------------------------------------------------
    # LARGE EXPENSE DETECTION
    # -----------------------------------------------------

    print(
        "\nINSIGHT 5 - LARGE EXPENSE DETECTION"
    )

    if len(current_expenses) >= 3:

        average_expense = (
            current_total
            / len(current_expenses)
        )

        large_expenses = [
            expense
            for expense in current_expenses
            if expense["amount"]
            >= average_expense * 2
        ]

        if large_expenses:

            print(
                f"{len(large_expenses)} transaction(s) "
                f"are at least twice your average "
                f"transaction amount."
            )

            for expense in sorted(
                large_expenses,
                key=lambda x: x["amount"],
                reverse=True
            )[:5]:

                print(
                    f"- {expense['date']} | "
                    f"{expense['category']} | "
                    f"{format_money(expense['amount'])}"
                )

        else:

            print(
                "No unusually large transactions "
                "detected using the current rule."
            )

    else:

        print(
            "Not enough transactions to detect "
            "unusually large expenses."
        )

    # -----------------------------------------------------
    # BUDGET INSIGHTS
    # -----------------------------------------------------

    print(
        "\nINSIGHT 6 - BUDGET STATUS"
    )

    overall_budget = get_budget(
        budgets,
        "overall",
        "Overall",
        month
    )

    if overall_budget is not None:

        percentage = (
            current_total
            / overall_budget
        ) * 100

        remaining = (
            overall_budget
            - current_total
        )

        print(
            f"Overall budget usage: "
            f"{percentage:.1f}%"
        )

        if remaining >= 0:

            print(
                f"Remaining budget: "
                f"{format_money(remaining)}"
            )

        else:

            print(
                f"Budget exceeded by: "
                f"{format_money(abs(remaining))}"
            )

    else:

        print(
            "No overall monthly budget configured."
        )

    # -----------------------------------------------------
    # GENERAL SUMMARY
    # -----------------------------------------------------

    print(
        "\n--------------- SUMMARY ---------------"
    )

    print(
        f"Transactions this month: "
        f"{len(current_expenses)}"
    )

    print(
        f"Total this month: "
        f"{format_money(current_total)}"
    )

    if current_total > 0:

        print(
            "Your spending data has been "
            "successfully analysed."
        )

    print(
        "\nNote: Insights are calculated from "
        "your recorded data and are not financial advice."
    )


# =========================================================
# CHARTS
# =========================================================

def show_charts(expenses):

    try:
        import matplotlib.pyplot as plt

    except ImportError:

        print(
            "\nMatplotlib is not installed."
        )

        print(
            "Install it using:"
        )

        print(
            "pip install matplotlib"
        )

        pause()

        return

    print(
        "\n=================== SPENDING CHARTS ==================="
    )

    if not expenses:

        print(
            "\nNo data to plot yet."
        )

        pause()

        return

    category_totals = spending_by_category(
        expenses
    )

    month_totals = spending_by_month(
        expenses
    )

    total = total_spent(
        expenses
    )

    if not category_totals:

        print(
            "No valid chart data."
        )

        pause()

        return

    # =====================================================
    # CATEGORY PIE
    # =====================================================

    fig = plt.figure(
        figsize=(14, 7)
    )

    fig.suptitle(
        "PERSONAL EXPENSE TRACKER - SPENDING ANALYSIS",
        fontsize=18,
        fontweight="bold"
    )

    ax1 = fig.add_subplot(
        1,
        2,
        1
    )

    categories = list(
        category_totals.keys()
    )

    category_amounts = list(
        category_totals.values()
    )

    wedges, texts, autotexts = ax1.pie(
        category_amounts,
        labels=categories,
        autopct="%1.1f%%",
        startangle=90,
        counterclock=False
    )

    for autotext in autotexts:

        autotext.set_fontsize(10)
        autotext.set_fontweight("bold")

    ax1.set_title(
        f"Spending by Category\n"
        f"Total: {format_money(total)}",
        fontsize=13,
        fontweight="bold",
        pad=15
    )

    # =====================================================
    # MONTHLY BAR
    # =====================================================

    ax2 = fig.add_subplot(
        1,
        2,
        2
    )

    months = list(
        month_totals.keys()
    )

    month_amounts = list(
        month_totals.values()
    )

    bars = ax2.bar(
        months,
        month_amounts
    )

    ax2.set_title(
        "Spending by Month",
        fontsize=13,
        fontweight="bold",
        pad=15
    )

    ax2.set_xlabel(
        "Month"
    )

    ax2.set_ylabel(
        f"Amount ({CURRENCY})"
    )

    plt.setp(
        ax2.get_xticklabels(),
        rotation=45,
        ha="right"
    )

    for bar, amount in zip(
        bars,
        month_amounts
    ):

        ax2.text(
            bar.get_x()
            + bar.get_width() / 2,
            bar.get_height(),
            format_money(amount),
            ha="center",
            va="bottom",
            fontsize=9
        )

    plt.tight_layout(
        rect=[
            0,
            0,
            1,
            0.94
        ]
    )

    try:

        plt.show()

    except Exception as error:

        print(
            "\nUnable to display chart."
        )

        print(
            "Error:",
            error
        )

    plt.close(fig)


# =========================================================
# MAIN MENU
# =========================================================

def show_menu():

    print(
        "\n"
        "========================================================\n"
        "              PERSONAL EXPENSE TRACKER\n"
        "========================================================"
    )

    print(
        "1.  Add an Expense"
    )

    print(
        "2.  View All Expenses"
    )

    print(
        "3.  Generate Expense Report"
    )

    print(
        "4.  Visualise Expenses"
    )

    print(
        "5.  Delete an Expense"
    )

    print(
        "6.  Budget Management"
    )

    print(
        "7.  Smart Spending Insights"
    )

    print(
        "8.  Save and Exit"
    )

    print(
        "========================================================"
    )


# =========================================================
# MAIN PROGRAM
# =========================================================

def main():

    expenses = load_expenses()

    budgets = load_budgets()

    print(
        "\n========================================================"
    )

    print(
        "       PERSONAL EXPENSE TRACKER - STARTING"
    )

    print(
        "========================================================"
    )

    print(
        f"Loaded expenses : {len(expenses)}"
    )

    print(
        f"Loaded budgets  : {len(budgets)}"
    )

    print(
        f"Data file       : {DATA_FILE}"
    )

    print(
        f"Budget file     : {BUDGET_FILE}"
    )

    while True:

        show_menu()

        choice = input(
            "Enter your choice: "
        ).strip()

        # -------------------------------------------------
        # ADD EXPENSE
        # -------------------------------------------------

        if choice == "1":

            add_expense(
                expenses
            )

            pause()

        # -------------------------------------------------
        # VIEW EXPENSES
        # -------------------------------------------------

        elif choice == "2":

            view_expenses(
                expenses
            )

            pause()

        # -------------------------------------------------
        # REPORT
        # -------------------------------------------------

        elif choice == "3":

            generate_report(
                expenses
            )

            pause()

        # -------------------------------------------------
        # CHARTS
        # -------------------------------------------------

        elif choice == "4":

            show_charts(
                expenses
            )

        # -------------------------------------------------
        # DELETE
        # -------------------------------------------------

        elif choice == "5":

            delete_expense(
                expenses
            )

            pause()

        # -------------------------------------------------
        # BUDGET MANAGEMENT
        # -------------------------------------------------

        elif choice == "6":

            budget_management(
                expenses,
                budgets
            )

        # -------------------------------------------------
        # INSIGHTS
        # -------------------------------------------------

        elif choice == "7":

            generate_insights(
                expenses,
                budgets
            )

            pause()

        # -------------------------------------------------
        # EXIT
        # -------------------------------------------------

        elif choice == "8":

            save_expenses(
                expenses
            )

            save_budgets(
                budgets
            )

            print(
                "\nData saved successfully."
            )

            print(
                "Thank you for using Personal Expense Tracker."
            )

            break

        # -------------------------------------------------
        # INVALID
        # -------------------------------------------------

        else:

            print(
                "\n-> Invalid choice."
            )

            print(
                "Please select a number from 1 to 8."
            )


# =========================================================
# PROGRAM ENTRY POINT
# =========================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print(
            "\n\nProgram interrupted."
        )

        print(
            "Exiting safely."
        )