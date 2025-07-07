# 📦 Courier Management System API (Django REST Framework)

A scalable RESTful backend API for a Courier Management System with multiple roles and Stripe payment.

---
<!-- IoI47BGEXhXRlElQ -->

##  Tech Stack

- Python 3.10
- Django 4.2
- Django REST Framework
- JWT (SimpleJWT)
- Stripe Payment (Test Mode)
- Docker + Gunicorn

---

##  Features

-  Register/Login with JWT
-  Role-based permissions (Admin, User, Delivery Man)
-  Order management
-  Assign delivery man
-  Stripe payment integration
-  REST API versioning
-  Docker support

---

##  Test Credentials

| Role        | Email              | Password     |
|-------------|--------------------|--------------|
| Admin       | admin@mail.com     | admin123     |
| DeliveryMan | delivery@mail.com  | delivery123  |
| User        | user@mail.com      | user123      |

---

##  Setup Instructions (Local)

```bash
git clone <this-repo>
cd courier-management
cp .env.example .env
docker-compose up --build
