# 💳 Digital Wallet Backend System

A backend-only digital wallet system inspired by fintech applications like FamPay.  
Built with FastAPI and SQLAlchemy, focusing on secure authentication and transaction integrity.

---

## 🚀 Features

- User Registration & Login
- JWT-based Authentication
- Wallet Creation per User
- Credit (Add Money) & Debit (Pay Money)
- Transaction Ledger for Auditability
- Balance Safety (Prevents Overspending)
- Modular Backend Architecture

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Framework:** FastAPI  
- **Database:** SQLite  
- **ORM:** SQLAlchemy  
- **Authentication:** JWT (JSON Web Tokens)  

---

## 📂 Project Structure

wallet-backend/
│
├── app/
│ ├── main.py # App entry point
│ ├── database.py # DB configuration
│ ├── models.py # Database models
│ ├── schemas.py # Request/Response schemas
│ ├── auth.py # JWT & password hashing
│ └── wallet.py # Wallet & transaction APIs
│
├── wallet.db
└── README.md
