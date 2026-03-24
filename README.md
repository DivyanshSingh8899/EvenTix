 📌 Event Registration & Ticket Booking System

A web-based Event Registration & Ticket Booking System that allows users to browse events, register, and book tickets online. The system also provides an admin dashboard to manage events and view bookings.

---

# 🌐 Live Website

You can access the live website here:

👉 Website Link:[EvenTix](https://eventix-v1.vercel.app/)


---

# 📖 Project Overview

This project is designed to simplify the process of **event registration and ticket booking**. Users can view available events, register, and book tickets seamlessly through an interactive web interface.

The system also includes an **admin panel** where administrators can create, update, and manage events as well as track all bookings.

---

# ✨ Features

### 👤 User Features

* User Registration and Login
* Browse Available Events
* View Event Details
* Book Tickets Online
* Receive Booking Confirmation
* QR Code Ticket Generation
* View Booking History

### 🛠 Admin Features

* Admin Login Dashboard
* Create, Update, and Delete Events
* Manage Ticket Availability
* View Registered Participants
* Download Booking Records

---

# 🧰 Technologies Used

### Frontend

* HTML
* CSS
* JavaScript
* Bootstrap

### Backend

* Flask

### Database

* SQLite

### Development Environment

* Visual Studio Code

---

# 🗂 Project Structure

```
event-booking-system
│
├── static
│   ├── css
│   └── js
│
├── templates
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── events.html
│   ├── event_detail.html
│   ├── booking.html
│   └── admin_dashboard.html
│
├── app.py
├── database.db
└── requirements.txt
```

---

# ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```
git clone https://github.com/yourusername/event-booking-system.git
```

### 2️⃣ Navigate to Project Folder

```
cd event-booking-system
```

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```
python app.py
```

### 5️⃣ Open in Browser

```
http://127.0.0.1:5000
```

---

# 📊 Database Schema

### Users Table

| Field    | Description        |
| -------- | ------------------ |
| id       | User ID            |
| name     | User Name          |
| email    | Email Address      |
| password | Encrypted Password |

### Events Table

| Field    | Description    |
| -------- | -------------- |
| id       | Event ID       |
| title    | Event Name     |
| date     | Event Date     |
| location | Event Location |
| price    | Ticket Price   |

### Bookings Table

| Field    | Description       |
| -------- | ----------------- |
| id       | Booking ID        |
| user_id  | User Reference    |
| event_id | Event Reference   |
| tickets  | Number of Tickets |

---

Example:

* Home Page
* Event Listing Page
* Booking Page
* Admin Dashboard

---

# 🚀 Future Improvements

* Online Payment Integration
* Email Ticket Confirmation
* QR Code Ticket Verification
* Mobile Responsive Improvements
* Event Recommendation System


# 👨‍💻 Author
Divyansh Singh
