# 💰 Personal Expense Tracker – Pro Version

A **Python-based Personal Expense Tracker** designed to help users record, analyse, and manage their daily expenses.

The project provides expense management, CSV-based data storage, budget management, spending insights, expense reports, and visual spending charts through a simple command-line interface.

---

## 📌 Project Overview

Managing personal expenses manually can make it difficult to understand where money is being spent.

The **Personal Expense Tracker – Pro Version** provides a simple solution for recording expenses and analysing spending patterns.

The application allows users to:

* Add and store expenses
* View recorded expenses
* Delete expenses
* Generate expense reports
* Visualise spending through charts
* Create monthly budgets
* Create category-wise budgets
* Monitor budget utilisation
* Receive spending warnings
* Analyse monthly spending
* Compare current and previous month spending
* Generate smart spending insights
* Store data permanently using CSV files

---

## ✨ Features

### 🧾 Expense Management

Users can easily manage their expenses through the application.

* Add an expense
* Enter amount
* Select expense category
* Enter date
* Add an optional note
* View all recorded expenses
* Delete unwanted expenses

### 📊 Expense Reports

The application generates a detailed expense report containing:

* Total number of transactions
* Total amount spent
* Average expense
* Highest expense
* Category-wise spending
* Percentage contribution of each category
* Monthly spending breakdown

### 💰 Budget Management

The Pro Version includes a dedicated budget management system.

Users can create:

* Overall monthly budgets
* Category-wise monthly budgets

The application also provides:

* Budget amount
* Amount spent
* Remaining budget
* Budget utilisation percentage
* Visual progress bar
* Budget status

Example statuses:

```text
WITHIN BUDGET
MODERATE
WARNING - NEAR LIMIT
OVER BUDGET
```

### ⚠️ Spending Warnings

The tracker automatically checks category budgets after adding an expense.

If spending reaches:

* **80% or more** → Budget Alert
* **100% or more** → Budget Exceeded Warning

### 🧠 Smart Spending Insights

The application analyses recorded data and provides useful insights such as:

* Current month's total spending
* Average daily spending
* Highest spending category
* Largest transaction
* Monthly spending comparison
* Significant category changes
* Large transaction detection
* Overall budget utilisation

### 📈 Spending Charts

The project uses **Matplotlib** to visualise spending data.

Currently available visualisations include:

* Spending by category — Pie Chart
* Spending by month — Bar Chart

These charts make spending patterns easier to understand.

### 💾 CSV Data Storage

The application stores information locally using CSV files.

#### Expense Data

```text
expenses.csv
```

#### Budget Data

```text
budgets.csv
```

This means the project does not require a database server.

---

## 🗂️ Expense Categories

The application currently supports:

```text
Food
Transport
Entertainment
Shopping
Bills
Health
Education
Other
```

---

## 🛠️ Technologies Used

| Technology         | Purpose                         |
| ------------------ | ------------------------------- |
| Python             | Main programming language       |
| CSV                | Expense and budget data storage |
| Matplotlib         | Data visualisation              |
| OS Module          | File handling                   |
| Datetime           | Date and monthly calculations   |
| Exception Handling | Error management                |
| Lists              | Data management                 |
| Dictionaries       | Structured data                 |
| Functions          | Modular programming             |
| Loops & Conditions | Program logic                   |

---

## 📋 Main Menu

When the program starts, the following menu is displayed:

```text
========================================================
              PERSONAL EXPENSE TRACKER
========================================================
1.  Add an Expense
2.  View All Expenses
3.  Generate Expense Report
4.  Visualise Expenses
5.  Delete an Expense
6.  Budget Management
7.  Smart Spending Insights
8.  Save and Exit
========================================================
```

---

## ⚙️ Requirements

Before running the project, make sure you have:

* Python 3.x
* Matplotlib

Check your Python installation:

```bash
python --version
```

Install Matplotlib:

```bash
pip install matplotlib
```

If your system uses `python3`:

```bash
pip3 install matplotlib
```

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/personal-expense-tracker.git
```

### 2. Open the Project Folder

```bash
cd personal-expense-tracker
```

### 3. Install Dependencies

```bash
pip install matplotlib
```

### 4. Run the Application

```bash
python expense_tracker.py
```

---

## 📁 Project Structure

```text
personal-expense-tracker/
│
├── expense_tracker.py
├── expenses.csv
├── budgets.csv
├── README.md
└── .gitignore
```

> `expenses.csv` and `budgets.csv` are automatically created when data is saved if they do not already exist.

---

## 🧪 Example Usage

### Adding an Expense

```text
================ ADD EXPENSE ================

Amount        : 250

Categories:
  1. Food
  2. Transport
  3. Entertainment
  4. Shopping
  5. Bills
  6. Health
  7. Education
  8. Other

Category (number or name): 1

Date (YYYY-MM-DD, blank = today):

Note (optional): Lunch
```

The expense is then stored in `expenses.csv`.

---

## 💵 Example Budget

A user can create an overall monthly budget:

```text
================ SET BUDGET ================

1. Overall Monthly Budget
2. Category Monthly Budget

Choose budget type: 1

Month (YYYY-MM, blank = current): 2026-09

Budget for Overall - 2026-09

Amount        : 15000
```

The application then tracks spending against the configured budget.

---

## 📊 Example Budget Status

```text
================ BUDGET STATUS ================

Current month: 2026-09

------------- OVERALL BUDGET -------------

Overall

Budget     : Rs.15,000.00
Spent      : Rs.10,500.00
Remaining  : Rs.4,500.00
Used       : 70.0%
Progress   : [##############------]
STATUS     : MODERATE
```

---

## 🧠 Example Smart Insight

```text
================ SMART SPENDING INSIGHTS ================

--------------- CURRENT MONTH ---------------

Month: 2026-09
Total spending: Rs.10,500.00
Average daily spending: Rs.656.25

INSIGHT 1 - TOP CATEGORY

Food is your largest spending category.
You spent Rs.4,000.00 (38.1% of this month's spending).

INSIGHT 2 - LARGEST TRANSACTION

Largest expense: Rs.2,500.00
Category: Shopping
Date: 2026-09-10
```

---

## 🔄 How the Application Works

```text
                ┌─────────────────────┐
                │     Start Program   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Load CSV Data       │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    Main Menu        │
                └──────────┬──────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
        Add Expense   Reports/Charts   Budgets
             │             │             │
             └─────────────┼─────────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Analyse Spending    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Save Data to CSV    │
                └─────────────────────┘
```

---

## 🔐 Data Storage

The application uses two CSV files.

### `expenses.csv`

```text
date,category,amount,note
2026-09-16,Food,250.0,Lunch
2026-09-15,Transport,100.0,Metro
```

### `budgets.csv`

```text
type,category,month,amount
overall,Overall,2026-09,15000
category,Food,2026-09,5000
```

---

## 🎯 Project Objectives

The main objectives of this project are:

1. To develop a simple personal expense management system.
2. To provide an organised way to record financial transactions.
3. To analyse spending habits using Python.
4. To implement monthly and category-based budgeting.
5. To provide visual representations of spending data.
6. To demonstrate practical Python programming concepts.
7. To implement persistent data storage using CSV files.
8. To generate automated spending insights and warnings.

---

## 📚 Python Concepts Demonstrated

This project demonstrates several important Python concepts:

* Variables
* Data types
* Lists
* Dictionaries
* Functions
* Function parameters
* Return values
* Loops
* Conditional statements
* List comprehensions
* Lambda functions
* File handling
* CSV processing
* Exception handling
* Modules
* Date and time operations
* Data aggregation
* Basic data visualisation

---

## 🔮 Future Improvements

Possible future versions could include:

* SQLite/MySQL database integration
* User login and authentication
* Password protection
* GUI using Tkinter or PyQt
* Web version using Flask/Django
* Export reports to PDF
* Excel export
* Recurring expenses
* Income tracking
* Savings goals
* Expense search and filtering
* Custom user categories
* Dashboard with more interactive charts
* Email notifications for budget warnings
* Cloud data synchronisation
* Mobile application

---

## ⚠️ Disclaimer

This application is intended for **personal expense tracking and educational purposes**.

The spending insights generated by the application are based only on the data entered by the user and should not be considered professional financial advice.

---

## 👨‍💻 Author

**Vedant Sharma**

🎓 BCA – 2nd Year
🏫 SGTBIMIT
💻 Python / Software Development Student

### Personal Expense Tracker – Pro Version

Developed as a Python-based project to demonstrate practical programming concepts including:

* Python
* CSV file handling
* Data analysis
* Budget management
* Matplotlib visualisation
* Exception handling
* Functions, lists, and dictionaries

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

## 📄 License

This project can be used for **educational and personal purposes**.

You may modify and improve the project according to your requirements.
