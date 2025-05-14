# Software Development Project II

A Python-based desktop application built as part of a university project. It allows students to view, upload, and rate academic suggestions (PDFs), with authentication and profile features. Built with a modern GUI using `CustomTkinter`, and powered by a secure Node.js + MySQL backend.

---

## 🚀 Features

- 🔐 **User Authentication** – Secure login & registration using JWT.
- 📚 **Suggestion Feed** – View all uploaded suggestions without logging in.
- 📤 **Upload Suggestions** – Authenticated users can upload PDFs with metadata.
- ⭐ **Rating System** – Vote (star rating) on suggestions, restricted to your department.
- 👤 **Profile Section** – Displays uploaded suggestions and personal info.
- 💾 **Persistent Sessions** – Stay logged in even after closing the app.
- 📁 **Modular File Structure** – Clean separation of logic, state, and GUI.

---

## 🛠️ Tech Stack

### 🖥 Frontend
- **Python**
- **CustomTkinter** – Modern Tkinter-based GUI library
- **Pillow** – Image handling
- **requests**, `json`, `os` – API communication & session management

### 🧠 Backend
- **Node.js (Express.js)** – API server
- **MySQL** – Relational database for storing user data, suggestions, votes
- **Cloudinary** – File storage for images and PDFs
- **JWT** – Authentication & session management

---

## 🗂️ Project Structure

```
Softwere-Developement-Project-II/
├── .vscode/
├── app_state.py          # Manages global session state
├── auth_window.py        # Login/Registration UI
├── book.ico              # App icon
├── card.py               # Suggestion card UI
├── main.py               # Launches the app
├── profile_card.py       # User's uploaded suggestion display
├── upload.py             # Upload UI & logic
├── requirements.txt      # Python dependencies
├── README.md
```

---

## 📦 Getting Started

### ✅ Prerequisites

- Python 3.10+
- pip
- Node.js + npm (for backend setup)
- MySQL Server
- Cloudinary Account (for PDF/image storage)

### 🧰 Frontend Setup

```bash
git clone https://github.com/anas20023/Softwere-Developement-Project-II.git
cd Softwere-Developement-Project-II
pip install -r requirements.txt
python main.py
```

### ⚙️ Backend Setup (Node.js + MySQL)

> ⚠️ Backend is hosted separately. Make sure your `.env` contains:

```env
CLOUDINARY_CLOUD_NAME   =      "your's"
CLOUDINARY_API_KEY      =      "your's"
CLOUDINARY_API_SECRET   =      "your's"
```

Run the backend:

```bash
Please Contact with us For Backend Repo.....
```

---

## 📸 Screenshots

### 🔐 Login & Registration

![Login](https://i.postimg.cc/7PmnrhGK/Screenshot-2025-05-14-130543.png)

![Registration](https://i.postimg.cc/W4LMwJC1/Screenshot-2025-05-14-130557.png)

### 🏠 Suggestion Dashboard
![Dashboard](https://i.postimg.cc/gJMXQwSR/Screenshot-2025-05-14-130632.png)

![Dashboard](https://i.postimg.cc/cCgHzF8y/Screenshot-2025-05-14-130532.png)

### 📤 Upload Suggestion
![Upload](https://i.postimg.cc/Kcw4ThdZ/Screenshot-2025-05-14-130659.png)

### 👤 Profile View
![Profile](https://i.postimg.cc/4xTd8bfq/Screenshot-2025-05-14-130646.png)

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📜 License

This project is licensed under the **MIT License**.

---

## ✍️ Author

Developed by [Anas Ibn Belal](https://github.com/anas20023) and team for **Software Development Project II**.


## Team Members

- [Miel Mahmud Sifat](https://www.github.com/octokatherine)
- [Easin Arafat](https://www.github.com/octokatherine)
- [Kaniz Fatema Sadia](https://www.github.com/octokatherine)
- [Abdullah Al Masum Badhon](https://www.github.com/octokatherine)

