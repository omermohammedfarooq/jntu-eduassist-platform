"""Authentication pages with clean UI."""

import streamlit as st
from eduassist.services.auth_service import (
    create_user, authenticate_user, 
    generate_reset_token, reset_password_with_token,
    get_user_by_email, BRANCHES, ROLES
)
from eduassist.services.translation_service import translate_text


def render_auth_page():
    """Render the authentication page."""
    lang = st.session_state.get('selected_language', 'english')
    
    # Back button
    if st.button("← " + translate_text("Back to Home", lang)):
        st.session_state.current_page = 'home'
        st.rerun()
    
    st.divider()
    
    if st.session_state.get('user'):
        render_profile(lang)
    else:
        st.title(translate_text("Account", lang))
        
        tab1, tab2, tab3 = st.tabs([
            translate_text("Login", lang),
            translate_text("Sign Up", lang),
            translate_text("Forgot Password", lang)
        ])
        
        with tab1:
            render_login_form(lang)
        
        with tab2:
            render_signup_form(lang)
        
        with tab3:
            render_forgot_password_form(lang)


def render_login_form(lang):
    """Render login form."""
    st.subheader(translate_text("Login to Your Account", lang))
    
    with st.form("login_form"):
        username_or_email = st.text_input(
            translate_text("Username or Email", lang),
            placeholder=translate_text("Enter your username or email", lang)
        )
        password = st.text_input(
            translate_text("Password", lang),
            type="password",
            placeholder=translate_text("Enter your password", lang)
        )
        
        submitted = st.form_submit_button(translate_text("Login", lang), use_container_width=True)
        
        if submitted:
            if not username_or_email or not password:
                st.error(translate_text("Please fill in all fields", lang))
            else:
                user, error = authenticate_user(username_or_email, password)
                if user:
                    st.session_state.user = user
                    st.session_state.current_page = 'home'
                    st.success(f"{translate_text('Welcome back', lang)}, {user['full_name']}!")
                    st.rerun()
                else:
                    st.error(translate_text(error or "Login failed", lang))


def render_signup_form(lang):
    """Render signup form."""
    st.subheader(translate_text("Create a New Account", lang))
    
    with st.form("signup_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input(
                translate_text("Username", lang) + " *",
                placeholder=translate_text("Choose a username", lang)
            )
            email = st.text_input(
                translate_text("Email", lang) + " *",
                placeholder="your@email.com"
            )
            password = st.text_input(
                translate_text("Password", lang) + " *",
                type="password",
                placeholder=translate_text("Min 6 characters", lang)
            )
        
        with col2:
            full_name = st.text_input(
                translate_text("Full Name", lang) + " *",
                placeholder=translate_text("Your full name", lang)
            )
            branch = st.selectbox(
                translate_text("Branch / Department", lang) + " *",
                options=BRANCHES,
                index=0
            )
            confirm_password = st.text_input(
                translate_text("Confirm Password", lang) + " *",
                type="password",
                placeholder=translate_text("Repeat password", lang)
            )
        
        role = st.selectbox(
            translate_text("I am a...", lang),
            options=["student", "teacher"],
            format_func=lambda x: translate_text(x.title(), lang)
        )
        
        submitted = st.form_submit_button(translate_text("Sign Up", lang), use_container_width=True)
        
        if submitted:
            if not all([username, email, password, full_name, branch, confirm_password]):
                st.error(translate_text("Please fill in all required fields", lang))
            elif password != confirm_password:
                st.error(translate_text("Passwords do not match", lang))
            elif len(password) < 6:
                st.error(translate_text("Password must be at least 6 characters", lang))
            elif "@" not in email:
                st.error(translate_text("Please enter a valid email address", lang))
            else:
                user, error = create_user(username, email, password, full_name, branch, role)
                if user:
                    st.session_state.user = user
                    st.session_state.current_page = 'home'
                    st.success(translate_text("Account created successfully!", lang))
                    st.rerun()
                else:
                    st.error(translate_text(error or "Registration failed", lang))


def render_forgot_password_form(lang):
    """Render forgot password form."""
    st.subheader(translate_text("Reset Your Password", lang))
    
    if st.session_state.get('reset_token_sent'):
        st.info(translate_text("A reset token has been generated. In a real app, this would be sent via email.", lang))
        
        with st.form("reset_password_form"):
            token = st.text_input(
                translate_text("Reset Token", lang),
                placeholder=translate_text("Paste your reset token", lang)
            )
            new_password = st.text_input(
                translate_text("New Password", lang),
                type="password",
                placeholder=translate_text("Min 6 characters", lang)
            )
            confirm_password = st.text_input(
                translate_text("Confirm New Password", lang),
                type="password",
                placeholder=translate_text("Repeat new password", lang)
            )
            
            submitted = st.form_submit_button(translate_text("Reset Password", lang), use_container_width=True)
            
            if submitted:
                if not all([token, new_password, confirm_password]):
                    st.error(translate_text("Please fill in all fields", lang))
                elif new_password != confirm_password:
                    st.error(translate_text("Passwords do not match", lang))
                elif len(new_password) < 6:
                    st.error(translate_text("Password must be at least 6 characters", lang))
                else:
                    success, message = reset_password_with_token(token, new_password)
                    if success:
                        st.success(translate_text(message, lang))
                        st.session_state.reset_token_sent = False
                        st.rerun()
                    else:
                        st.error(translate_text(message, lang))
        
        if st.button(translate_text("Request New Token", lang)):
            st.session_state.reset_token_sent = False
            st.rerun()
    else:
        with st.form("forgot_password_form"):
            email = st.text_input(
                translate_text("Email Address", lang),
                placeholder=translate_text("Enter your email address", lang)
            )
            
            submitted = st.form_submit_button(translate_text("Send Reset Token", lang), use_container_width=True)
            
            if submitted:
                if not email:
                    st.error(translate_text("Please enter your email", lang))
                else:
                    user = get_user_by_email(email)
                    if user:
                        token = generate_reset_token(email)
                        if token:
                            st.session_state.reset_token = token
                            st.session_state.reset_token_sent = True
                            st.info(f"{translate_text('Reset token (for demo)', lang)}: {token}")
                            st.rerun()
                    else:
                        st.error(translate_text("No account found with this email", lang))


def render_profile(lang):
    """Render user profile page."""
    user = st.session_state.user
    
    st.title(f"👤 {translate_text('Welcome', lang)}, {user['full_name']}!")
    st.write(f"@{user['username']} · {user['email']}")
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.caption(translate_text("Branch", lang))
            st.write(f"**{user.get('branch', 'N/A')}**")
    
    with col2:
        with st.container(border=True):
            st.caption(translate_text("Role", lang))
            st.write(f"**{translate_text(user['role'].title(), lang)}**")
    
    with col3:
        with st.container(border=True):
            st.caption(translate_text("Status", lang))
            st.write("**✅ " + translate_text("Active", lang) + "**")
    
    st.divider()
    
    col_back, col_logout = st.columns(2)
    with col_back:
        if st.button("← " + translate_text("Back to Home", lang), use_container_width=True):
            st.session_state.current_page = 'home'
            st.rerun()
    with col_logout:
        if st.button(translate_text("Logout", lang), use_container_width=True, type="primary"):
            st.session_state.user = None
            st.success(translate_text("Logged out successfully!", lang))
            st.rerun()
