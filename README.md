# 📘 CampusManager: Student Management System 

CampusManager is a desktop application built using Python's Tkinter library to streamline the management of student records. It features a secure login system, MySQL database integration, and a complete CRUD interface.

---

## 🚀 Features

- **User Authentication:** Secure login screen for authorized access.
- **Database Connectivity:** Connects to a MySQL server for persistent storage.
- **CRUD Operations:**
  - Add Student: Enter student ID, name, mobile, email, address, gender, and DOB.
  - Search Student: Filter by ID, name, mobile, email, or address.
  - Update Student: Select and update existing records using a pre-filled form.
  - Delete Student: Remove selected records.
- **Data Display:** Sortable Treeview table for student records.
- **Data Export:** Export all student records to a CSV file.
- **Dynamic UI:** Real-time clock and animated CampusManager title slider.
- **Error Handling:** User-friendly messages for validation and DB errors.

---

## 🛠 Technologies Used 

- **Python 3.x**
- **Tkinter** – GUI Framework
- **Pillow (PIL)** – For image rendering (backgrounds, icons)
- **ttkthemes** – Custom styling for Tkinter
- **pymysql** – Python to MySQL database connector
- **csv** – For exporting records to `.csv` format

---

## ⚙️ Setup and Installation

### ✅ Prerequisites

- Python 3.x installed
- MySQL Server running
- Required Python packages:

```bash
pip install Pillow pymysql ttkthemes
