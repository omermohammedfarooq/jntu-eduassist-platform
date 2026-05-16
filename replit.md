# JNTU EduAssist AI

## Overview

JNTU EduAssist AI is a multilingual educational assistant platform designed for JNTU-H (Jawaharlal Nehru Technological University Hyderabad) university students. The application provides an AI-powered Q&A system, academic results lookup, practice question generation, and a community forum for student collaboration. The platform supports multiple Indian languages including Telugu, Hindi, Urdu, Tamil, and others to make education accessible to diverse student populations.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Framework**: Streamlit-based single-page application with a tabbed interface

The application uses Streamlit as the primary web framework, implementing a clean, minimal design system with a modern UI theme. The architecture follows a component-based approach:

- **Page Structure**: Main entry point (`main.py`) orchestrates the application flow with multiple tabs for different features (Assistant, Results, Practice, Forum, Profile)
- **Component System**: Reusable UI components in `eduassist/ui/components.py` handle navigation bars, language selectors, course selectors, and auth buttons
- **Theme System**: Custom CSS-based theme (`eduassist/config/theme.py`) implements a minimal, elegant design with Inter font family and consistent color variables
- **Session Management**: Streamlit session state manages user authentication, selected courses, conversation history, and UI state

**Design Rationale**: Streamlit was chosen for rapid development and built-in session management. The component-based approach allows for maintainable UI code with consistent styling across the application.

### Backend Architecture

**Pattern**: Service-oriented architecture with repository pattern for data access

The backend is organized into distinct service layers:

- **Services Layer** (`eduassist/services/`):
  - `knowledge_service.py`: Handles Q&A matching using keyword-based search in the knowledge base
  - `jntuh_client.py`: External API client for fetching JNTUH academic results
  - `translation_service.py`: Multilingual support using deep-translator and Google Translate
  - `auth_service.py`: User authentication with bcrypt password hashing
  - `forum_service.py`: Community forum post and comment management

- **Data Layer** (`eduassist/data/`):
  - `repositories.py`: Data access functions for courses and knowledge base JSON files
  - `database.py`: PostgreSQL database connection management using psycopg2 with context managers

**Design Rationale**: The service layer abstracts business logic from UI components, making the code testable and maintainable. The repository pattern separates data access concerns from business logic.

### Database Design

**Primary Database**: PostgreSQL with psycopg2 driver

**Schema Design**:
- **users table**: Stores user accounts with authentication credentials, profile information (branch, role), and password reset tokens
- **forum_posts table**: Stores community forum posts with user references, categories, and soft delete flags
- **post_reactions table**: Tracks likes/dislikes on forum posts
- **post_comments table**: Stores threaded comments on forum posts with soft delete support

**Connection Management**: Uses context managers (`get_db()`) for automatic transaction handling and connection cleanup. The `RealDictCursor` returns query results as dictionaries for easier data manipulation.

**Design Rationale**: PostgreSQL was chosen for its reliability and ACID compliance. The soft delete pattern (is_deleted flags) preserves data integrity while allowing content moderation. Foreign key constraints ensure referential integrity between users and their content.

### Authentication System

**Password Security**: bcrypt-based password hashing with salt generation

**Features**:
- User registration with username, email, password, full name, and branch selection
- Login with username or email
- Password reset with time-limited tokens (stored in users table)
- Role-based access control (student, teacher, admin)

**Session Management**: User data stored in Streamlit session state after successful authentication

**Design Rationale**: bcrypt provides robust password hashing with automatic salt generation. Token-based password reset is stored directly in the database for simplicity, avoiding the need for separate token storage.

### Knowledge Base System

**Storage**: JSON-based knowledge base (`knowledge_base.json`) with subject-topic hierarchy

**Structure**:
- Subject → Topic → {keywords, answer}
- Keywords array enables simple fuzzy matching
- Supports general knowledge base for cross-subject queries

**Search Algorithm**: Keyword-based matching with frequency scoring to find best topic match

**Alternative Considered**: ChromaDB with vector embeddings (`embedding_service.py` exists but appears unused in main flow)

**Design Rationale**: JSON-based storage provides simplicity and easy content management. Keyword matching is sufficient for educational Q&A where exact terminology is common. Vector search infrastructure exists for future enhancement.

### Translation System

**Service**: Google Translate API via deep-translator library

**Supported Languages**: 10 Indian languages including Telugu, Hindi, Urdu, Tamil, Kannada, Marathi, Bengali, Gujarati, Malayalam, plus English

**Caching**: Streamlit's `@st.cache_data` with 1-hour TTL reduces API calls for repeated translations

**Design Rationale**: Google Translate provides reliable translation quality for Indian languages. Caching balances API costs with user experience. The decorator-based caching is simple and effective.

### Course Management

**Data Structure**: Hierarchical JSON structure (courses.json):
- Degrees (B.Tech, etc.)
  - Branches (CSE, ECE, etc.)
    - Years (1-4)
      - Semesters (1-2)
        - Subjects (with names, topics, links)

**Access Pattern**: Cascading selectors allow users to drill down through degree → branch → year → semester → subject

**Design Rationale**: JSON structure mirrors the actual JNTU academic structure, making it intuitive for content management. File-based storage simplifies deployment without database dependencies for static content.

## External Dependencies

### Third-Party APIs

**JNTUH Results API** (`https://jntuhresults.dhethi.com/api/getAcademicResult`):
- Purpose: Fetch official academic results by hall ticket number
- Response handling: Manages queued requests, success states, and error conditions
- Timeout: 30 seconds configured
- Alternative: Official JNTUH portal links provided as fallback

**Google Translate API** (via deep-translator):
- Purpose: Real-time translation for multilingual support
- Languages: 10+ Indian languages
- Rate limiting: Managed through caching

### Database

**PostgreSQL**:
- Connection: Via `DATABASE_URL` environment variable
- Driver: psycopg2 with RealDictCursor for dictionary-based results
- Connection pooling: Context manager pattern for automatic cleanup

### Python Libraries

**Core Dependencies**:
- `streamlit`: Web application framework
- `psycopg2`: PostgreSQL database adapter
- `bcrypt`: Password hashing
- `deep-translator`: Translation service wrapper
- `requests`: HTTP client for JNTUH API
- `pandas`: Data formatting for results display

**Optional/Development**:
- `chromadb`: Vector database for semantic search (infrastructure present but not actively used)
- `pyngrok`: Colab deployment tunneling

### External Services Integration

**Google Colab Deployment**:
- `colab_runner.py` provides deployment script
- Uses pyngrok for public URL tunneling
- Automated dependency installation

**Design Rationale**: Colab support enables zero-infrastructure deployment for demonstrations and testing. The runner script abstracts the complexity of port forwarding and dependency management.

### File-Based Data Storage

**JSON Files**:
- `courses.json`: Course structure and subject catalog
- `knowledge_base.json`: Q&A content organized by subject and topic

**Design Rationale**: File-based storage for relatively static content (courses, Q&A) separates concerns from dynamic user data in PostgreSQL. This simplifies content updates and version control.