# Python Finance System Backend

## Overview
This project is a Python-based finance tracking backend that allows users to manage their financial records (income and expenses).  
It supports role-based access (Admin, Analyst, Viewer), transaction CRUD operations, financial summaries, and recent activity tracking.  
Built using **FastAPI**, **SQLAlchemy**, and **SQLite** (or any preferred DB).

---

## Features

### Financial Records
- Create, Read, Update, Delete transactions
- Filter transactions by type, category, or date

### Summaries & Analytics
- Total income
- Total expenses
- Current balance
- Category-wise breakdown
- Monthly totals
- Recent activity

### Role-based Access
- **Admin**: Full access (CRUD + user management)
- **Analyst**: View & filter transactions, see detailed insights
- **Viewer**: View transactions and summaries only

### Validation & Error Handling
- Input validation using Pydantic
- Enums for transaction types and user roles
- Proper HTTP status codes (400, 404, 200)
- Meaningful error messages
## Tech Stack
- Python 3.11+
- FastAPI
- SQLAlchemy ORM
- SQLite (or PostgreSQL/MySQL if preferred)
- Uvicorn (ASGI server)
- Pydantic for input validation

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Vijaypro12/Finance-system
cd Finance-system
