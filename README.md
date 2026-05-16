# jntu-eduassist-platform
Multilingual AI-powered academic platform for JNTU students with results integration, AI assistance, practice questions, and community features.
# JNTU EduAssist Platform

Multilingual AI-powered academic platform for JNTU students with AI assistance, results integration, practice tools, and community features.

---

## Overview

JNTU EduAssist Platform is a student-focused educational platform designed to simplify academic workflows for JNTU students using modern AI systems and integrated academic services.

The platform combines:

- AI-powered academic assistance
- Direct JNTU results lookup
- Practice question generation
- Academic resources access
- Student discussion forum
- Multilingual learning support

into one centralized platform.

---

# Features

## AI Academic Assistant

Students can ask academic questions and receive instant answers using multiple AI models.

### Supported Models
- Qwen
- DeepSeek
- Groq Llama
- Groq Mixtral
- KAT-Coder

The platform allows students to choose different AI models depending on their learning or coding needs.

---

## JNTU Results Integration

The platform can fetch academic results directly from JNTU servers using APIs for faster and easier access.

### Features
- Quick results lookup
- Simplified access workflow
- Integrated directly into the platform

---

## Practice Questions

Students can generate practice questions for different subjects to prepare for examinations and improve understanding.

### Includes
- Subject-wise practice
- Revision assistance
- Self-assessment support

---

## Student Discussion Forum

A built-in student community platform where users can interact and collaborate academically.

### Forum Features
- User accounts and authentication
- Create posts
- Comment on discussions
- Like and share posts
- Follow and unfollow users
- Community interaction and collaboration

The forum is designed as a student-focused academic social platform.

---

## Academic Calendar Access

Students can access official academic calendars directly through the platform.

---

## Syllabus and Question Papers

The platform provides access to:
- Syllabus resources
- Previous year question papers
- Official JNTU PDF links

---

## Multilingual Support

Students can interact with the platform in multiple languages for a more accessible learning experience.

---

# Tech Stack

## Frontend
- HTML
- CSS
- JavaScript

## Backend
- Python
- Flask

## AI & Retrieval
- OpenRouter APIs
- Multiple LLM integrations
- Embedding-based retrieval
- ChromaDB

## Deployment
- Railway
- Render

---

# Project Structure

```txt
jntu-eduassist-platform/
├── .streamlit/
├── assets/
├── backend/
├── static/
├── templates/
├── app.py
├── main.py
├── embedding_service.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

# Screenshots

## Home Page
_Add homepage screenshot here_

## AI Assistant
_Add AI assistant screenshot here_

## Practice Questions
_Add practice questions screenshot here_

## Discussion Forum
_Add discussion forum screenshot here_

---

# Getting Started

## Clone the Repository

```bash
git clone https://github.com/your-username/jntu-eduassist-platform.git
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

# Environment Variables

Create a `.env` file and add your API keys.

Example:

```env
OPENROUTER_API_KEY=
GROQ_API_KEY=
SECRET_KEY=
```

---

# Future Improvements

- OCR-based handwritten answer evaluation
- Voice input support
- Personalized dashboards
- Better multilingual support
- Notifications and reminders
- AI-generated study plans
- Improved syllabus integration
- Mobile responsiveness improvements

---

# Vision

The goal of this project is to create a centralized AI-powered academic ecosystem for JNTU students where they can:

- access academic resources
- ask questions instantly
- prepare for exams
- connect with peers
- simplify academic workflows

through a single platform.

---

# Status

This project is actively under development.

---

# License

MIT License
