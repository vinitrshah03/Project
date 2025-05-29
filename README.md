# 🛡️ Cybersecurity Intelligence Toolkit 🔍🌐  
A Flask-Powered Web App to Explore Threat Intelligence, Security Tools, and Personalized AI Recommendations

---

## 📖 Overview

SecureX is an integrated Flask-based web application that brings together real-world cybersecurity features, APIs, and tools. Designed for students, developers, and professionals, it allows you to explore cyber threats, analyze vulnerabilities, evaluate password complexity, and understand keylogging concepts — all in one place.

Built with modularity and personalization in mind, this project combines powerful external APIs, AI-driven suggestions, and a secure, extensible architecture.

---

## 🚀 Features at a Glance

- 🔎 **Shodan API Integration**  
  Search open devices, IPs, and exposed services directly from the app.

- 🌍 **Google Maps API Integration**  
  Visualize geographic data and map-based search results.

- 🔐 **Google OAuth Login**  
  Secure user authentication via Google accounts.

- 🧠 **Personalized Recommendations**  
  Smart suggestions based on recent user searches.

- 📋 **CVE & CPE Vulnerability Exploration**  
  Search software configurations (CPE) and known vulnerabilities (CVE).

- 🔐 **Password Strength Checker**  
  Instantly analyze and evaluate the complexity of user-defined passwords.

- 🎮 **Keylogger Simulation (Sandboxed & Educational)**  
  A non-malicious, offline keylogging demonstration to educate users about privacy risks.

- 📥 **Security Downloads**  
  Access downloadable files such as CVE lists, CPE lists, and common password databases.

---

## 🗂️ Project Structure

```bash
Project/
│
├── app.py                    # Main Flask application entry point
├── config.py                 # Configuration settings (API keys, constants, etc.)
├── recommender.py            # AI-based recommendation logic (under development)
├── requirements.txt          # List of dependencies
├── login_register.sql        # MySQL database schema for users
├── sample inputs.txt         # Sample inputs for testing
│
├── templates/                # HTML templates for UI
│   └── *.html
│
├── static/                   # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
│
├── downloads/                # Downloadable security files (CVE, CPE, password lists)
│
├── tests/                    # Testing framework
│   ├── HTML/                 # HTML file testing
│   ├── CSS/                  # CSS validation tests
│   ├── JS/                   # JavaScript behavior testing
│   └── Python/               # Unit tests for Python logic
````

---

## 🧪 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/vinitrshah03/Project.git
cd Project
```

---

### 2️⃣ Create and Activate Virtual Environment

#### PowerShell (Windows):

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### Bash (Linux/macOS):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3️⃣ Install Required Dependencies

```bash
pip install -r requirements.txt
```

> 💡 You can add additional libraries to `requirements.txt` if extending the project.

---

### 4️⃣ Run the Application Locally

```bash
python -m flask run
```

Open your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

### 5️⃣ Run All Tests

```bash
python -m unittest discover -s tests/Python -p "test_*.py"
```

> This command runs all unit tests in the Python module. Frontend tests may require manual or browser-based testing.

---

## ⚙️ Customization Guidelines

| 🛠️ What to Change        | 📍 File Location | 💡 Description                                        |
| ------------------------- | ---------------- | ----------------------------------------------------- |
| Add new HTML page         | `templates/`     | Create or duplicate existing `.html`                  |
| Add/modify routes         | `app.py`         | Define Flask routes here                              |
| Change API keys           | `config.py`      | Store Shodan/Google keys here                         |
| Update styling            | `static/css/`    | Modify or add CSS files                               |
| Modify JS behavior        | `static/js/`     | Add or adjust JavaScript                              |
| Update AI recommendations | `recommender.py` | Adjust how user search history influences suggestions |
| Add downloadable files    | `downloads/`     | Upload your own datasets                              |

---

## 🔐 Security Advice & Disclaimer

> ⚠️ **Disclaimer**
> This toolkit is for **educational and ethical use only**. Do **NOT** use any feature of this app to:
>
> * Target unauthorized systems
> * Conduct real-world reconnaissance
> * Violate API providers' terms of service

> ⚠️ **Security Tips**
>
> * Use `.env` or `config.py` to store sensitive keys — never hardcode.
> * Passwords in the database are **hashed**, but still avoid using real credentials.
> * Always test sandbox features like the keylogger in **safe environments**.

---

## 🙌 Contributing

Pull requests, feature ideas, and issue reports are welcome. This is a learning-focused open project, and your contributions are appreciated!

---

## 👤 About the Developer

**Vinit Shah (Me)**
GitHub: [@vinitrshah03](https://github.com/vinitrshah03)
