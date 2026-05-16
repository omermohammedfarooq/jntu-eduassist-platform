# 🎓 JNTU EduAssist Platform

A student-focused academic platform built for JNTU students that combines AI assistance, academic services, discussion forums, practice systems, and multilingual learning tools into one centralized system.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black)
![OpenRouter](https://img.shields.io/badge/OpenRouter-LLM%20APIs-purple)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Database-success)
![Status](https://img.shields.io/badge/Status-Active%20Development-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

# 📖 Overview

JNTU EduAssist was built to simplify common academic tasks for students by integrating AI tools, academic resources, and student collaboration features into a single platform.

The platform combines:
- AI-based academic assistance
- JNTU results integration
- Practice question generation
- Student discussion forums
- Academic calendar access
- Syllabus and resource downloads
- Multilingual interaction support

into one unified academic platform.

---

# 🚀 Live Demo

🌐 Website:  
https://jntu-eduassist-production.up.railway.app/

---

# ✨ Features

## 🤖 AI Academic Assistant

Students can ask academic questions and receive responses using multiple AI models integrated through APIs.

### Supported Models
- Qwen
- DeepSeek
- Groq Llama
- Groq Mixtral
- KAT-Coder

The assistant supports:
- Academic queries
- Coding help
- Explanations and summaries
- Multilingual interaction

---

## 📊 JNTU Results Integration

The platform can fetch academic results directly from JNTU servers using integrated APIs.

### Includes
- Quick result lookup
- Simplified access workflow
- Integrated results viewing

---

## 📝 Practice Question Generator

Generate practice questions for different subjects to support revision and exam preparation.

### Features
- Subject-wise question generation
- Self-assessment support
- Practice-based learning workflows

---

## 💬 Student Discussion Forum

A built-in student community system where users can interact and collaborate academically.

### Forum Features
- User authentication
- Create and share posts
- Comment on discussions
- Like posts
- Follow and unfollow users
- Student collaboration and interaction

The forum works as a student-focused academic social platform.

---

## 📚 Academic Resources

Students can access:
- Academic calendars
- Syllabus downloads
- Previous year question papers
- Official JNTU PDF resources

directly through the platform.

---

## 🌍 Multilingual Support

The platform supports multilingual interaction to make academic assistance more accessible for students from different language backgrounds.

---

# 📸 Screenshots

## 🏠 Home Dashboard (Light Mode)

![Home Dashboard](assets/Screenshots/Home_1_Lightmode.png)

---

## 🌙 Home Dashboard (Dark Mode)

![Home Dashboard Dark](assets/Screenshots/Home_1_Darkmode.png)

---

## 🤖 AI Assistant

![AI Assistant](assets/Screenshots/AI_chat.png)

---

## 📝 Practice Questions

![Practice Questions](assets/Screenshots/Practice_questions.png)

---

## 💬 Discussion Forum

![Discussion Forum](assets/Screenshots/Forum_Home.png)

---

## 📊 Results Integration

![Results](assets/Screenshots/Results_1.png)

---

## 📅 Academic Calendars

![Academic Calendars](assets/Screenshots/Academic_Calandars.png)

---

## 📥 Syllabus Downloads

![Syllabus Downloads](assets/Screenshots/Syllabus_Download.png)

---

# 🛠️ Tech Stack

## Frontend
- HTML
- CSS
- JavaScript

## Backend
- Python
- Flask

## AI & APIs
- OpenRouter APIs
- Multiple LLM integrations
- ChromaDB
- Embedding-based retrieval

## Deployment
- Railway
- Render

---

# 📂 Project Structure

```txt
jntu-eduassist-platform/
│
├── assets/
│   └── Screenshots/
│
├── eduassist/
├── static/
├── templates/
│
├── app.py
├── main.py
├── embedding_service.py
├── requirements.txt
├── pyproject.toml
├── render.yaml
└── README.md
```

---

# ⚙️ Getting Started

## Clone Repository

```bash
git clone https://github.com/omermohammedfarooq/jntu-eduassist-platform.git
cd jntu-eduassist-platform
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
python app.py
```

---

# 🔑 Environment Variables

Create a `.env` file and add your API keys.

Example:

```env
OPENROUTER_API_KEY=
GROQ_API_KEY=
SECRET_KEY=
```

---

# 🚧 Future Improvements

- OCR-based handwritten answer evaluation
- Voice input support
- Personalized student dashboards
- Improved multilingual support
- Mobile responsiveness improvements
- Expanded syllabus integration
- Better retrieval workflows

---

# 📌 Status

🚧 Currently under active development.

---

# 📄 License

MIT License
