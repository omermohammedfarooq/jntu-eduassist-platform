import streamlit as st
from datetime import datetime
from eduassist.services.forum_service import (
    create_post, get_posts, get_post_by_id,
    toggle_reaction, get_user_reaction,
    add_comment, get_comments,
    delete_post, delete_comment,
    CATEGORIES, get_total_posts
)
from eduassist.services.translation_service import translate_text

def render_forum_page():
    lang = st.session_state.get('selected_language', 'english')
    
    st.markdown(f"""
        <p style="color: #a1a1aa; margin-bottom: 1.5rem;">
            {translate_text("Connect with fellow students and teachers to discuss academics, career, and campus life.", lang)}
        </p>
    """, unsafe_allow_html=True)
    
    user = st.session_state.get('user')
    
    if not user:
        st.warning(translate_text("Please login to participate in discussions. You can view posts without logging in.", lang))
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        translated_categories = [translate_text(cat, lang) for cat in CATEGORIES]
        all_text = translate_text("All", lang)
        selected_idx = st.selectbox(
            translate_text("Filter by Category", lang), 
            range(len(CATEGORIES) + 1),
            format_func=lambda i: all_text if i == 0 else translated_categories[i-1]
        )
        selected_category = "All" if selected_idx == 0 else CATEGORIES[selected_idx - 1]
    
    with col2:
        if user:
            if st.button(translate_text("Create New Post", lang), use_container_width=True):
                st.session_state.show_create_post = True
    
    with col3:
        if 'forum_page' not in st.session_state:
            st.session_state.forum_page = 1
    
    if st.session_state.get('show_create_post') and user:
        render_create_post_form(user, lang)
    
    if st.session_state.get('viewing_post_id'):
        render_post_detail(st.session_state.viewing_post_id, user, lang)
    else:
        render_posts_list(selected_category, user, lang)

def render_create_post_form(user, lang):
    st.markdown(f"### {translate_text('Create New Post', lang)}")
    
    with st.form("create_post_form"):
        title = st.text_input(translate_text("Title", lang) + "*")
        content = st.text_area(translate_text("Content", lang) + "*", height=150)
        category = st.selectbox(translate_text("Category", lang) + "*", CATEGORIES)
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button(translate_text("Post", lang), use_container_width=True)
        with col2:
            cancel = st.form_submit_button(translate_text("Cancel", lang), use_container_width=True)
        
        if submitted:
            if not title or not content:
                st.error(translate_text("Please fill in title and content", lang))
            else:
                post = create_post(user['id'], title, content, category)
                st.success(translate_text("Post created successfully!", lang))
                st.session_state.show_create_post = False
                st.rerun()
        
        if cancel:
            st.session_state.show_create_post = False
            st.rerun()

def render_posts_list(category, user, lang):
    posts = get_posts(page=st.session_state.forum_page, per_page=10, category=category)
    total = get_total_posts(category)
    
    if not posts:
        st.info(translate_text("No posts yet. Be the first to start a discussion!", lang))
        return
    
    for post in posts:
        render_post_card(post, user, lang)
    
    total_pages = (total + 9) // 10
    if total_pages > 1:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.write(f"{translate_text('Page', lang)} {st.session_state.forum_page} {translate_text('of', lang)} {total_pages}")
        with col1:
            if st.session_state.forum_page > 1:
                if st.button(translate_text("Previous", lang)):
                    st.session_state.forum_page -= 1
                    st.rerun()
        with col3:
            if st.session_state.forum_page < total_pages:
                if st.button(translate_text("Next", lang)):
                    st.session_state.forum_page += 1
                    st.rerun()

def render_post_card(post, user, lang):
    with st.container():
        st.markdown(f"""
        <div class="forum-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="category-tag">{translate_text(post['category'], lang)}</span>
                <span class="meta">{format_time(post['created_at'], lang)}</span>
            </div>
            <h4>{post['title']}</h4>
            <p style="color: #a1a1aa; line-height: 1.6;">{post['content'][:200]}{'...' if len(post['content']) > 200 else ''}</p>
            <div class="meta" style="margin-top: 0.75rem;">
                {translate_text("By", lang)}: {post['full_name'] or post['username']} ({translate_text(post['user_role'].title(), lang)})
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
        
        with col1:
            user_reaction = get_user_reaction(post['id'], user['id']) if user else None
            like_label = f"{'Liked' if user_reaction == 'like' else translate_text('Like', lang)} ({post['likes']})"
            if st.button(like_label, key=f"like_{post['id']}", disabled=not user):
                toggle_reaction(post['id'], user['id'], 'like')
                st.rerun()
        
        with col2:
            dislike_label = f"{'Disliked' if user_reaction == 'dislike' else translate_text('Dislike', lang)} ({post['dislikes']})"
            if st.button(dislike_label, key=f"dislike_{post['id']}", disabled=not user):
                toggle_reaction(post['id'], user['id'], 'dislike')
                st.rerun()
        
        with col3:
            if st.button(f"{translate_text('Comments', lang)} ({post['comment_count']})", key=f"comment_{post['id']}"):
                st.session_state.viewing_post_id = post['id']
                st.rerun()
        
        with col4:
            if st.button(translate_text("Share", lang), key=f"share_{post['id']}"):
                st.session_state[f"share_link_{post['id']}"] = True
        
        with col5:
            if user and (user['role'] == 'admin' or (user['id'] == post.get('user_id'))):
                if st.button(translate_text("Delete", lang), key=f"delete_{post['id']}"):
                    success, msg = delete_post(post['id'], user['id'])
                    if success:
                        st.success(translate_text(msg, lang))
                        st.rerun()
                    else:
                        st.error(translate_text(msg, lang))
        
        if st.session_state.get(f"share_link_{post['id']}"):
            st.info(f"{translate_text('Share this discussion', lang)}: Post #{post['id']} - {post['title']}")

def render_post_detail(post_id, user, lang):
    post = get_post_by_id(post_id)
    
    if not post:
        st.error(translate_text("Post not found", lang))
        st.session_state.viewing_post_id = None
        return
    
    if st.button(translate_text("Back to Forum", lang)):
        st.session_state.viewing_post_id = None
        st.rerun()
    
    st.markdown(f"""
    <div class="forum-card" style="padding: 2rem;">
        <span class="category-tag">{translate_text(post['category'], lang)}</span>
        <h2 style="margin: 1rem 0;">{post['title']}</h2>
        <p style="color: #f5f5f7; line-height: 1.8;">{post['content']}</p>
        <hr style="border-color: rgba(255,255,255,0.1); margin: 1.5rem 0;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="meta">{translate_text("Posted by", lang)}: {post['full_name'] or post['username']} ({translate_text(post['user_role'].title(), lang)})</span>
            <span class="meta">{format_time(post['created_at'], lang)}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"### {translate_text('Comments', lang)}")
    
    comments = get_comments(post_id)
    
    if user:
        with st.form(f"comment_form_{post_id}"):
            comment_content = st.text_area(translate_text("Add a comment", lang), height=100)
            if st.form_submit_button(translate_text("Post Comment", lang)):
                if comment_content:
                    add_comment(post_id, user['id'], comment_content)
                    st.success(translate_text("Comment added!", lang))
                    st.rerun()
                else:
                    st.error(translate_text("Please enter a comment", lang))
    
    if comments:
        for comment in comments:
            st.markdown(f"""
            <div style="border-left: 3px solid #6366f1; padding-left: 1rem; margin: 1rem 0; background: rgba(99, 102, 241, 0.05); padding: 1rem; border-radius: 0 8px 8px 0;">
                <strong style="color: #f5f5f7;">{comment['full_name'] or comment['username']}</strong> 
                <span style="color: #a1a1aa;">({translate_text(comment['user_role'].title(), lang)})</span>
                <span style="color: #71717a; font-size: 0.8em;"> - {format_time(comment['created_at'], lang)}</span>
                <p style="color: #a1a1aa; margin-top: 0.5rem;">{comment['content']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if user and user['role'] == 'admin':
                if st.button(translate_text("Delete Comment", lang), key=f"del_comment_{comment['id']}"):
                    success, msg = delete_comment(comment['id'], user['id'])
                    if success:
                        st.rerun()
    else:
        st.info(translate_text("No comments yet. Be the first to comment!", lang))

def format_time(dt, lang='english'):
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
    now = datetime.now()
    diff = now - dt.replace(tzinfo=None)
    
    if diff.days > 7:
        return dt.strftime("%b %d, %Y")
    elif diff.days > 0:
        days_text = translate_text("day" if diff.days == 1 else "days", lang)
        ago_text = translate_text("ago", lang)
        return f"{diff.days} {days_text} {ago_text}"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        hours_text = translate_text("hour" if hours == 1 else "hours", lang)
        ago_text = translate_text("ago", lang)
        return f"{hours} {hours_text} {ago_text}"
    elif diff.seconds > 60:
        mins = diff.seconds // 60
        mins_text = translate_text("minute" if mins == 1 else "minutes", lang)
        ago_text = translate_text("ago", lang)
        return f"{mins} {mins_text} {ago_text}"
    else:
        return translate_text("Just now", lang)
