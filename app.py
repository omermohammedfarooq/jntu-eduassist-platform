"""
CLONE OF : JNTU EduAssist AI - Flask Application
Main application file with routes and configuration
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_session import Session
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import services
from eduassist.services.auth_service import (
    authenticate_user, create_user, generate_reset_token, 
    reset_password_with_token, get_user_by_email
)
from eduassist.services.forum_service import (
    create_post, get_posts, toggle_reaction, add_comment,
    delete_post, delete_comment, get_total_posts
)
from eduassist.services.translation_service import translate_text, LANGUAGE_NAMES
from eduassist.services.jntuh_client import JNTUHClient
from eduassist.services.ai_service import initialize_ai_service, get_ai_service
from eduassist.data.database import init_database
from eduassist.data.repositories import load_courses, load_knowledge_base

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
Session(app)

# Configure Flask-Mail for password reset emails
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

# Initialize email service
from eduassist.services.email_service import init_mail
init_mail(app)

# Initialize database
init_database()

# Load data
courses = load_courses()
knowledge_base = load_knowledge_base()

# Initialize AI Services (OpenRouter - December 2025)
openrouter_key = os.getenv('OPENROUTER_API_KEY')

if openrouter_key:
    initialize_ai_service(openrouter_key)
    print("[OK] AI Services initialized with OpenRouter")
    
    # Show which models are available
    ai_service = get_ai_service()
    if ai_service:
        available = ai_service.get_available_models()
        print(f"[INFO] Available models: {', '.join([m['name'] for m in available])}")
else:
    print("[WARNING] No OpenRouter API key found in environment variables")


# ============================================================================
# CONTEXT PROCESSOR - Inject variables into all templates
# ============================================================================

@app.context_processor
def inject_language():
    """Inject current language into all templates."""
    lang = session.get('language', 'english')
    return dict(current_lang=lang)


# ============================================================================
# TEMPLATE FILTERS
# ============================================================================

@app.template_filter('format_display_name')
def format_display_name(full_name):
    """
    Format a full name for display in the navigation bar.
    Returns first name + last initial (e.g., "Mohammad O.")
    If name is already short (<=15 chars), return as is.
    """
    if not full_name:
        return "User"
    
    # If name is already short, just return it
    if len(full_name) <= 15:
        return full_name
    
    # Split the name into parts
    parts = full_name.strip().split()
    
    if len(parts) == 1:
        # Only one name, truncate if too long
        return parts[0][:15]
    elif len(parts) == 2:
        # First + Last: show "First L."
        return f"{parts[0]} {parts[1][0]}."
    else:
        # Multiple names: show "First L."
        return f"{parts[0]} {parts[-1][0]}."


@app.template_filter('translate')
def translate_filter(text):
    """
    Translate text to the user's selected language.
    Uses pre-translated dictionary for instant translations.
    Usage in templates: {{ "Hello World"|translate }}
    """
    if not text:
        return text
    
    lang = session.get('language', 'english')
    
    # If English, return original text immediately
    if lang == 'english' or lang == 'en':
        return text
    
    try:
        from eduassist.services.ui_translations import get_translation
        result = get_translation(str(text), lang)
        # Debug: print if translation was found
        if result != text:
            print(f"[Translate] '{text[:30]}...' -> '{result[:30]}...' ({lang})")
        return result
    except Exception as e:
        print(f"[Translation Filter Error] {e}")
        return text


# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def home():
    """Home page with dashboard."""
    user = session.get('user')
    lang = session.get('language', 'english')
    return render_template('home.html', user=user, lang=lang, courses=courses)


@app.before_request
def set_language_from_request():
    """Set language from URL parameter or session."""
    # Check URL parameter first
    lang_param = request.args.get('lang')
    if lang_param:
        session['language'] = lang_param
        session.modified = True
    
    # Ensure language is set (default to english)
    if 'language' not in session:
        session['language'] = 'english'
        session.modified = True


@app.route('/set-language', methods=['POST'])
def set_language():
    """Set user's language preference."""
    lang = request.form.get('language', 'english')
    session['language'] = lang
    session.modified = True
    print(f"[Language] Changed to: {lang}")
    
    # Get clean URL without any existing lang parameter
    referrer = request.referrer or url_for('home')
    
    # Remove existing lang parameter if present
    import re
    # Remove ?lang=xxx or &lang=xxx
    clean_url = re.sub(r'[?&]lang=[^&]*', '', referrer)
    # Fix URL if it now ends with ? or has ?& or &&
    clean_url = re.sub(r'\?$', '', clean_url)
    clean_url = re.sub(r'\?&', '?', clean_url)
    clean_url = re.sub(r'&&', '&', clean_url)
    
    # Add new lang parameter
    if '?' in clean_url:
        redirect_url = f"{clean_url}&lang={lang}"
    else:
        redirect_url = f"{clean_url}?lang={lang}"
    
    return redirect(redirect_url)


@app.route('/toggle-theme', methods=['POST'])
def toggle_theme():
    """Toggle dark/light theme."""
    # Theme is handled client-side with localStorage
    return jsonify({'status': 'ok'})


# ============================================================================
# AUTH ROUTES
# ============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page."""
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email')
        password = request.form.get('password')
        
        user, error = authenticate_user(username_or_email, password)
        if user:
            session['user'] = user
            session.permanent = True
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash(error or 'Login failed', 'error')
    
    return render_template('auth.html', mode='login')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page."""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        branch = request.form.get('branch')
        role = request.form.get('role', 'student')
        
        # Validation
        if not all([username, email, password, full_name, branch]):
            flash('Please fill in all required fields', 'error')
        elif password != confirm_password:
            flash('Passwords do not match', 'error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
        else:
            user, error = create_user(username, email, password, full_name, branch, role)
            if user:
                session['user'] = user
                session.permanent = True
                flash('Account created successfully!', 'success')
                return redirect(url_for('home'))
            else:
                flash(error or 'Registration failed', 'error')
    
    return render_template('auth.html', mode='signup')


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password page."""
    if request.method == 'POST':
        email = request.form.get('email')
        
        # Check if user exists
        user = get_user_by_email(email)
        if not user:
            # We show the same message whether user exists or not for security
            flash('If an account exists with this email, you will receive a password reset link.', 'info')
            return redirect(url_for('login'))
        
        # Generate reset token
        token = generate_reset_token(email)
        
        if token:
            # Send email
            from eduassist.services.email_service import send_password_reset_email
            base_url = request.url_root.rstrip('/')
            success, message = send_password_reset_email(email, token, base_url)
            
            if success:
                flash('Password reset link sent to your email. Please check your inbox (and spam folder).', 'success')
            else:
                flash(f'Error sending email: {message}', 'error')
        else:
            flash('Error generating reset token. Please try again.', 'error')
            
        return redirect(url_for('login'))
        
    return render_template('forgot_password.html')


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password page."""
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
        else:
            success, message = reset_password_with_token(token, password)
            if success:
                flash('Your password has been reset successfully. Please login with your new password.', 'success')
                return redirect(url_for('login'))
            else:
                flash(message, 'error')
                
    return render_template('reset_password.html', token=token)


@app.route('/logout')
def logout():
    """Logout user."""
    session.pop('user', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('home'))


# ============================================================================
# FEATURE ROUTES
# ============================================================================

@app.route('/ask')
def ask():
    """Q&A page."""
    user = session.get('user')
    lang = session.get('language', 'english')
    return render_template('ask.html', user=user, lang=lang, courses=courses)


@app.route('/results')
def results():
    """Results lookup page."""
    user = session.get('user')
    lang = session.get('language', 'english')
    return render_template('results.html', user=user, lang=lang)


@app.route('/fetch-results', methods=['POST'])
def fetch_results():
    """Fetch JNTUH results."""
    hall_ticket = request.form.get('hall_ticket', '').strip().upper()
    
    if not hall_ticket:
        return jsonify({'error': 'Please enter a hall ticket number'})
    
    client = JNTUHClient()
    results = client.fetch_results(hall_ticket)
    return jsonify(results)


@app.route('/practice')
def practice():
    """Practice questions page."""
    user = session.get('user')
    lang = session.get('language', 'english')
    return render_template('practice.html', user=user, lang=lang, courses=courses)


@app.route('/forum')
def forum():
    """Discussion forum page with search and sorting."""
    user = session.get('user')
    
    if not user:
        flash('Please login to access the forum', 'error')
        return redirect(url_for('login'))
    
    lang = session.get('language', 'english')
    
    # Get query parameters
    search_query = request.args.get('q', '')
    sort_by = request.args.get('sort', 'date')
    category = request.args.get('category', 'All')
    page = request.args.get('page', 1, type=int)
    
    # Import enhanced forum functions
    from eduassist.services.forum_service_enhanced import search_posts, get_posts_sorted, search_users
    from eduassist.services.forum_service import CATEGORIES
    
    # Get posts based on search or sorting
    if search_query:
        posts = search_posts(search_query, sort_by, page)
        users = search_users(search_query)
    else:
        posts = get_posts_sorted(sort_by, category, page)
        users = []
    
    total_posts = get_total_posts(category if category != 'All' else None)
    
    return render_template('forum.html', 
                          user=user, 
                          lang=lang, 
                          posts=posts,
                          users=users,
                          total_posts=total_posts,
                          search_query=search_query,
                          sort_by=sort_by,
                          current_category=category,
                          categories=CATEGORIES,
                          page=page)



@app.route('/forum/create-post', methods=['POST'])
def create_forum_post():
    """Create a new forum post with optional image."""
    user = session.get('user')
    
    if not user:
        return jsonify({'error': 'Please login'}), 401
    
    title = request.form.get('title')
    content = request.form.get('content')
    category = request.form.get('category', 'general')
    
    if not title or not content:
        return jsonify({'error': 'Title and content required'}), 400
    
    # Handle image upload
    image_url = None
    if 'image' in request.files:
        image = request.files['image']
        if image and image.filename:
            # Validate file type
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
            filename = image.filename.lower()
            if '.' in filename and filename.rsplit('.', 1)[1] in allowed_extensions:
                # Generate unique filename
                import uuid
                ext = filename.rsplit('.', 1)[1]
                unique_filename = f"{uuid.uuid4().hex}.{ext}"
                
                # Ensure upload directory exists
                upload_dir = os.path.join(app.static_folder, 'uploads', 'forum')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Save the file
                filepath = os.path.join(upload_dir, unique_filename)
                image.save(filepath)
                
                # Store relative URL for database
                image_url = f"/static/uploads/forum/{unique_filename}"
            else:
                return jsonify({'error': 'Invalid image format. Allowed: PNG, JPG, JPEG, GIF, WEBP'}), 400
    
    post = create_post(user['id'], title, content, category, image_url)
    return jsonify({'success': True, 'post': post})


@app.route('/calendars')
def calendars():
    """Academic calendars page."""
    user = session.get('user')
    lang = session.get('language', 'english')
    return render_template('calendars.html', user=user, lang=lang)


@app.route('/syllabus')
def syllabus():
    """Syllabus download page."""
    user = session.get('user')
    lang = session.get('language', 'english')
    return render_template('syllabus.html', user=user, lang=lang)


@app.route('/api/get-branches', methods=['POST'])
def get_branches():
    """Get available branches for a given degree, regulation, and year."""
    from eduassist.services.syllabus_scraper import JNTUHSyllabusClient
    
    degree = request.form.get('degree')
    regulation = request.form.get('regulation')
    year = request.form.get('year')
    
    if not degree or not regulation or not year:
        return jsonify({'error': 'Degree, regulation, and year are required'}), 400
    
    client = JNTUHSyllabusClient()
    result = client.get_branches(degree, regulation, year)
    
    return jsonify(result)


@app.route('/api/get-syllabus-pdf', methods=['POST'])
def get_syllabus_pdf():
    """Get direct PDF URL for a specific syllabus."""
    from eduassist.services.syllabus_scraper import JNTUHSyllabusClient
    
    degree = request.form.get('degree')
    regulation = request.form.get('regulation')
    year = request.form.get('year')
    branch = request.form.get('branch')
    
    if not all([degree, regulation, year, branch]):
        return jsonify({'error': 'All fields are required'}), 400
    
    client = JNTUHSyllabusClient()
    result = client.get_syllabus_pdf(degree, regulation, year, branch)
    
    return jsonify(result)


# ============================================================================
# ENHANCED FORUM ROUTES
# ============================================================================

from eduassist.services.forum_service_enhanced import (
    search_posts, get_posts_sorted, follow_user, unfollow_user, is_following,
    get_followers, get_following, toggle_comment_reaction, get_comments_with_reactions,
    get_user_profile, get_user_posts, get_user_comments, get_user_liked_posts,
    update_user_bio, promote_to_admin, demote_from_admin, get_all_admins
)
from eduassist.services.forum_service import get_post_by_id, CATEGORIES


@app.route('/forum/post/<int:post_id>')
def view_post(post_id):
    """View individual post with comments."""
    user = session.get('user')
    
    if not user:
        flash('Please login to view posts', 'error')
        return redirect(url_for('login'))
    
    post = get_post_by_id(post_id)
    if not post:
        flash('Post not found', 'error')
        return redirect(url_for('forum'))
    
    comments = get_comments_with_reactions(post_id, user['id'])
    is_author_followed = is_following(user['id'], post['user_id']) if user['id'] != post['user_id'] else None
    
    return render_template('post_detail.html', 
                          user=user, 
                          post=post, 
                          comments=comments,
                          is_author_followed=is_author_followed,
                          categories=CATEGORIES)


@app.route('/profile/<username>')
def view_profile(username):
    """View user profile."""
    user = session.get('user')
    
    if not user:
        flash('Please login to view profiles', 'error')
        return redirect(url_for('login'))
    
    from eduassist.services.auth_service import get_user_by_username
    
    profile_user = get_user_by_username(username)
    if not profile_user:
        flash('User not found', 'error')
        return redirect(url_for('forum'))
    
    profile = get_user_profile(profile_user['id'])
    user_posts = get_user_posts(profile_user['id'])
    user_comments = get_user_comments(profile_user['id'])
    liked_posts = get_user_liked_posts(profile_user['id'])
    
    is_own_profile = user['id'] == profile_user['id']
    is_followed = is_following(user['id'], profile_user['id']) if not is_own_profile else None
    
    # Get followers and following lists for own profile
    followers_list = get_followers(profile_user['id']) if is_own_profile else []
    following_list = get_following(profile_user['id']) if is_own_profile else []
    
    return render_template('profile.html',
                          user=user,
                          profile=profile,
                          user_posts=user_posts,
                          user_comments=user_comments,
                          liked_posts=liked_posts,
                          is_own_profile=is_own_profile,
                          is_followed=is_followed,
                          followers_list=followers_list,
                          following_list=following_list)


@app.route('/profile')
def my_profile():
    """View own profile."""
    user = session.get('user')
    
    if not user:
        flash('Please login to view your profile', 'error')
        return redirect(url_for('login'))
    
    return redirect(url_for('view_profile', username=user['username']))


@app.route('/api/follow/<int:user_id>', methods=['POST'])
def api_follow_user(user_id):
    """Follow a user."""
    user = session.get('user')
    
    if not user:
        return jsonify({'error': 'Please login'}), 401
    
    success, message = follow_user(user['id'], user_id)
    return jsonify({'success': success, 'message': message})


@app.route('/api/unfollow/<int:user_id>', methods=['POST'])
def api_unfollow_user(user_id):
    """Unfollow a user."""
    user = session.get('user')
    
    if not user:
        return jsonify({'error': 'Please login'}), 401
    
    success, message = unfollow_user(user['id'], user_id)
    return jsonify({'success': success, 'message': message})


@app.route('/api/remove-follower/<int:user_id>', methods=['POST'])
def api_remove_follower(user_id):
    """Remove a follower (kick someone who follows you)."""
    user = session.get('user')
    
    if not user:
        return jsonify({'error': 'Please login'}), 401
    
    # To remove a follower, we unfollow them from the OTHER direction
    # i.e., we make THEM unfollow US
    success, message = unfollow_user(user_id, user['id'])  # follower unfollows current user
    return jsonify({'success': success, 'message': message})


@app.route('/api/unlike-post/<int:post_id>', methods=['POST'])
def api_unlike_post(post_id):
    """Unlike a post (remove like reaction)."""
    user = session.get('user')
    
    if not user:
        return jsonify({'error': 'Please login'}), 401
    
    # Toggle removes if already exists
    toggle_reaction(post_id, user['id'], 'like')
    return jsonify({'success': True})

@app.route('/api/comment/<int:comment_id>/react', methods=['POST'])
def react_to_comment(comment_id):
    """React to a comment (like/unlike)."""
    user = session.get('user')
    
    if not user:
        return jsonify({'error': 'Please login'}), 401
    
    reaction_type = request.form.get('reaction', 'like')
    toggle_comment_reaction(comment_id, user['id'], reaction_type)
    
    return jsonify({'success': True})


@app.route('/api/post/<int:post_id>/react', methods=['POST'])
def react_to_post(post_id):
    """React to a post (like/dislike)."""
    user = session.get('user')
    
    if not user:
        return jsonify({'error': 'Please login'}), 401
    
    reaction_type = request.form.get('reaction', 'like')
    toggle_reaction(post_id, user['id'], reaction_type)
    
    return jsonify({'success': True})


@app.route('/api/post/<int:post_id>/comment', methods=['POST'])
def add_post_comment(post_id):
    """Add a comment to a post."""
    user = session.get('user')
    
    if not user:
        return jsonify({'error': 'Please login'}), 401
    
    content = request.form.get('content')
    if not content:
        return jsonify({'error': 'Comment cannot be empty'}), 400
    
    comment = add_comment(post_id, user['id'], content)
    return jsonify({'success': True, 'comment': comment})


@app.route('/api/profile/bio', methods=['POST'])
def update_bio():
    """Update user bio."""
    user = session.get('user')
    
    if not user:
        return jsonify({'error': 'Please login'}), 401
    
    bio = request.form.get('bio', '')
    update_user_bio(user['id'], bio)
    
    return jsonify({'success': True})


@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard for user management."""
    user = session.get('user')
    
    if not user:
        flash('Please login', 'error')
        return redirect(url_for('login'))
    
    if user.get('role') != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('forum'))
    
    admins = get_all_admins()
    
    return render_template('admin_dashboard.html', user=user, admins=admins)


@app.route('/api/admin/promote', methods=['POST'])
def api_promote_admin():
    """Promote user to admin."""
    user = session.get('user')
    
    if not user or user.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    email = request.form.get('email')
    if not email:
        return jsonify({'error': 'Email required'}), 400
    
    success, message = promote_to_admin(user['id'], email)
    return jsonify({'success': success, 'message': message})


@app.route('/api/admin/demote', methods=['POST'])
def api_demote_admin():
    """Demote admin to student."""
    user = session.get('user')
    
    if not user or user.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    email = request.form.get('email')
    if not email:
        return jsonify({'error': 'Email required'}), 400
    
    success, message = demote_from_admin(user['id'], email)
    return jsonify({'success': success, 'message': message})


@app.route('/api/post/<int:post_id>/delete', methods=['POST'])
def api_delete_post(post_id):
    """Delete a post."""
    user = session.get('user')
    
    if not user:
        return jsonify({'error': 'Please login'}), 401
    
    success, message = delete_post(post_id, user['id'])
    return jsonify({'success': success, 'message': message})


@app.route('/api/comment/<int:comment_id>/delete', methods=['POST'])
def api_delete_comment(comment_id):
    """Delete a comment."""
    user = session.get('user')
    
    if not user:
        return jsonify({'error': 'Please login'}), 401
    
    success, message = delete_comment(comment_id, user['id'])
    return jsonify({'success': success, 'message': message})


# ============================================================================
# AI CHAT ROUTES
# ============================================================================

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Send message to AI and get response."""
    user_message = request.json.get('message', '').strip()
    selected_model = request.json.get('model', 'llama-3.3')
    language = request.json.get('language', 'english')
    conversation_id = request.json.get('conversation_id', None)
    
    if not user_message:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    ai_service = get_ai_service()
    if not ai_service:
        return jsonify({'error': 'AI service not available. Please check configuration.'}), 503
    
    try:
        # Get AI response
        result = ai_service.send_message(user_message, selected_model, language)
        
        if result['success']:
            # Save to database if user is logged in
            user = session.get('user')
            if user and conversation_id:
                # Save user message
                add_message(conversation_id, 'user', user_message)
                # Save AI response
                add_message(conversation_id, 'assistant', result['response'])
            
            return jsonify({
                'success': True,
                'response': result['response'],
                'model': result['model'],
                'language': language
            })
        else:
            return jsonify({'error': result.get('error', 'Unknown error')}), 500
    except Exception as e:
        return jsonify({'error': f'AI error: {str(e)}'}), 500


@app.route('/api/chat/clear', methods=['POST'])
def api_clear_chat():
    """Clear chat history."""
    selected_model = request.json.get('model', None)
    
    ai_service = get_ai_service()
    if ai_service:
        ai_service.clear_history(selected_model)
        return jsonify({'success': True, 'message': 'Chat history cleared'})
    return jsonify({'error': 'AI service not available'}), 503


@app.route('/api/chat/models', methods=['GET'])
def api_get_models():
    """Get list of available AI models."""
    ai_service = get_ai_service()
    if ai_service:
        models = ai_service.get_available_models()
        return jsonify({'success': True, 'models': models})
    return jsonify({'error': 'AI service not available'}), 503


# ============================================================================
# CHAT CONVERSATION MANAGEMENT ROUTES
# ============================================================================

from eduassist.services.chat_service import (
    create_conversation, get_user_conversations, get_conversation,
    add_message, delete_conversation, generate_title_from_message,
    update_conversation_title
)

@app.route('/api/chat/conversations', methods=['GET'])
def api_get_conversations():
    """Get all conversations for the logged-in user."""
    user = session.get('user')
    if not user:
        return jsonify({'error': 'Not logged in'}), 401
    
    conversations = get_user_conversations(user['id'])
    return jsonify({'success': True, 'conversations': conversations})


@app.route('/api/chat/conversation/<int:conversation_id>', methods=['GET'])
def api_get_conversation(conversation_id):
    """Get a specific conversation with all messages."""
    user = session.get('user')
    if not user:
        return jsonify({'error': 'Not logged in'}), 401
    
    conversation = get_conversation(conversation_id, user['id'])
    if not conversation:
        return jsonify({'error': 'Conversation not found'}), 404
    
    return jsonify({'success': True, 'conversation': conversation})


@app.route('/api/chat/conversation', methods=['POST'])
def api_create_conversation():
    """Create a new conversation."""
    user = session.get('user')
    if not user:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    title = data.get('title', 'New Chat')
    model = data.get('model', 'llama-3.3')
    language = data.get('language', 'english')
    
    conversation_id = create_conversation(user['id'], title, model, language)
    return jsonify({'success': True, 'conversation_id': conversation_id})


@app.route('/api/chat/conversation/<int:conversation_id>', methods=['DELETE'])
def api_delete_conversation(conversation_id):
    """Delete a conversation."""
    user = session.get('user')
    if not user:
        return jsonify({'error': 'Not logged in'}), 401
    
    success = delete_conversation(conversation_id, user['id'])
    if success:
        return jsonify({'success': True})
    return jsonify({'error': 'Failed to delete conversation'}), 400


@app.route('/api/chat/conversation/<int:conversation_id>/title', methods=['PUT'])
def api_update_conversation_title(conversation_id):
    """Update conversation title."""
    user = session.get('user')
    if not user:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    title = data.get('title', '')
    
    if not title:
        return jsonify({'error': 'Title required'}), 400
    
    success = update_conversation_title(conversation_id, user['id'], title)
    if success:
        return jsonify({'success': True})
    return jsonify({'error': 'Failed to update title'}), 400


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    """404 error handler."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    """500 error handler."""
    return render_template('500.html'), 500


# ============================================================================
# RUN APP
# ============================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
