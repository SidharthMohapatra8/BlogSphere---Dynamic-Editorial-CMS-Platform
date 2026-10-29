"""
BlogSphere — Modern Editorial Publication & Dynamic CMS Platform
100% Pure Python & Streamlit Native Architecture
"""
import streamlit as st
import datetime
import os
import re
from config import (
    PROJECT_NAME, PROJECT_TAGLINE, PROJECT_DESCRIPTION,
    DEFAULT_CATEGORIES, ADMIN_EMAIL_DEFAULT, ADMIN_PASSWORD_DEFAULT
)
import database as db
from auth import verify_password, hash_password

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================
st.set_page_config(
    page_title=f"{PROJECT_NAME} — Editorial & CMS",
    page_icon="✒️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session State
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "admin_email" not in st.session_state:
    st.session_state.admin_email = ""
if "current_view" not in st.session_state:
    st.session_state.current_view = "publications"
if "selected_slug" not in st.session_state:
    st.session_state.selected_slug = None
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "All"
if "editing_post_id" not in st.session_state:
    st.session_state.editing_post_id = None
if "viewed_posts" not in st.session_state:
    st.session_state.viewed_posts = set()

# Check URL Query Parameters for Direct Article Links
query_params = st.query_params
if "post" in query_params:
    st.session_state.selected_slug = query_params["post"]
    st.session_state.current_view = "publications"

# ==========================================================
# TOP NAVIGATION HEADER (100% PURE PYTHON & STREAMLIT)
# ==========================================================
nav_col_logo, nav_col_menu, nav_col_auth = st.columns([2, 4, 2])

with nav_col_logo:
    st.subheader(f"✒️ {PROJECT_NAME}")
    st.caption(f"_{PROJECT_TAGLINE}_")

with nav_col_menu:
    nav_options = ["📰 Publications", "🔍 Explore & Archive", "🛡️ Admin Studio"]
    view_map = {
        "📰 Publications": "publications",
        "🔍 Explore & Archive": "explore",
        "🛡️ Admin Studio": "admin"
    }
    
    # Calculate current selected index
    current_idx = 0
    if st.session_state.current_view == "explore":
        current_idx = 1
    elif st.session_state.current_view == "admin":
        current_idx = 2

    chosen_nav = st.radio(
        label="Main Navigation",
        options=nav_options,
        index=current_idx,
        horizontal=True,
        label_visibility="collapsed"
    )

    selected_view = view_map[chosen_nav]
    if selected_view != st.session_state.current_view:
        st.session_state.current_view = selected_view
        st.session_state.selected_slug = None
        st.rerun()

with nav_col_auth:
    if st.session_state.is_admin:
        st.write(f"👤 **{st.session_state.admin_email}**")
        if st.button("Sign Out", key="top_sign_out_btn"):
            st.session_state.is_admin = False
            st.session_state.admin_email = ""
            st.session_state.current_view = "publications"
            st.rerun()
    else:
        if st.session_state.current_view != "admin":
            if st.button("Admin Sign In", key="top_sign_in_btn"):
                st.session_state.current_view = "admin"
                st.session_state.selected_slug = None
                st.rerun()

st.divider()

# ==========================================================
# VIEW 1: ARTICLE READER (When a post is selected)
# ==========================================================
if st.session_state.selected_slug:
    post = db.get_post_by_slug(st.session_state.selected_slug)
    
    if not post:
        st.error("The requested article could not be found or has been moved.")
        if st.button("← Return to Publications"):
            st.session_state.selected_slug = None
            st.query_params.clear()
            st.rerun()
    else:
        # Increment view count once per user session
        if post["id"] not in st.session_state.viewed_posts:
            db.increment_views(post["id"])
            st.session_state.viewed_posts.add(post["id"])
            post = db.get_post_by_slug(st.session_state.selected_slug)

        # Back navigation button
        if st.button("← Back to All Publications", key="reader_back_btn"):
            st.session_state.selected_slug = None
            st.query_params.clear()
            st.rerun()

        # Article Header
        st.caption(f"CATEGORY: **{post['category'].upper()}** • {post.get('read_time', 5)} MIN READ")
        st.title(post["title"])
        
        if post.get("subtitle"):
            st.subheader(post["subtitle"])

        st.caption(f"Written by **{post.get('author_name', 'Editorial Desk')}** • Published on {str(post['created_at'])[:10]} • 👁️ {post.get('views', 0)} reads • ❤️ {post.get('likes', 0)} likes")
        
        st.divider()

        # Featured Image if available
        if post.get("featured_image"):
            st.image(post["featured_image"], use_container_width=True)

        # Article Body (Safe pure Markdown, no HTML)
        st.markdown(post["content"])

        st.divider()

        # Engagement Section (Like & Share)
        with st.container(border=True):
            col_like, col_share = st.columns([1, 3])
            with col_like:
                if st.button(f"❤️ Like Story ({post.get('likes', 0)})", key=f"like_btn_{post['id']}", type="primary"):
                    new_likes = db.like_post(post["id"])
                    st.toast(f"Thank you for liking this story! Total likes: {new_likes}")
                    st.rerun()
            with col_share:
                st.caption("Share this story with fellow engineers, designers, and thinkers.")

        # Comments Section
        st.subheader("💬 Reader Discussion")
        
        # New Comment Form
        with st.form(f"comment_form_{post['id']}", clear_on_submit=True):
            st.write("**Join the conversation**")
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                c_name = st.text_input("Your Name *", placeholder="e.g. Maya Chen")
            with col_c2:
                c_email = st.text_input("Your Email (optional)", placeholder="e.g. maya@example.com")
            
            c_text = st.text_area("Your Thoughts *", placeholder="Share your perspective or feedback...", height=100)
            submit_comment = st.form_submit_button("Post Comment", type="primary")

            if submit_comment:
                if c_name.strip() and c_text.strip():
                    db.add_comment(post["id"], c_name.strip(), c_email.strip(), c_text.strip())
                    st.success("Your comment has been published!")
                    st.rerun()
                else:
                    st.warning("Please provide both your name and comment.")

        # Existing Comments List
        comments = db.get_comments(post["id"])
        if comments:
            st.write(f"**{len(comments)} Thought{'s' if len(comments) != 1 else ''} Shared:**")
            for com in comments:
                with st.container(border=True):
                    st.write(f"**{com['author_name']}** • _{str(com['created_at'])[:16]}_")
                    st.write(com["content"])
        else:
            st.info("No comments yet. Be the first to share your perspective on this dispatch!")

        st.stop()

# ==========================================================
# VIEW 2: PUBLICATIONS (HOME)
# ==========================================================
elif st.session_state.current_view == "publications":
    posts = db.get_posts(status="published")
    
    # Hero / Featured Post
    featured_posts = [p for p in posts if p.get("is_featured") == 1]
    hero_post = featured_posts[0] if featured_posts else (posts[0] if posts else None)

    if hero_post:
        with st.container(border=True):
            hero_col1, hero_col2 = st.columns([1.3, 1])
            with hero_col1:
                st.caption(f"⭐ FEATURED DISPATCH • **{hero_post['category'].upper()}** • {hero_post.get('read_time', 5)} MIN READ")
                st.header(hero_post["title"])
                st.write(hero_post.get("excerpt", ""))
                st.caption(f"By **{hero_post.get('author_name', 'Editorial Desk')}** • {str(hero_post['created_at'])[:10]} • 👁️ {hero_post.get('views', 0)} reads")
                if st.button("Read Full Story →", key=f"hero_read_{hero_post['id']}", type="primary"):
                    st.session_state.selected_slug = hero_post["slug"]
                    st.query_params["post"] = hero_post["slug"]
                    st.rerun()
            with hero_col2:
                if hero_post.get("featured_image"):
                    st.image(hero_post["featured_image"], use_container_width=True)

    st.write("")
    
    # Category Filter Bar (Pure Python)
    st.subheader("Explore by Topic")
    all_categories = ["All"] + DEFAULT_CATEGORIES
    
    selected_cat = st.radio(
        label="Filter by Topic",
        options=all_categories,
        index=all_categories.index(st.session_state.selected_category) if st.session_state.selected_category in all_categories else 0,
        horizontal=True,
        label_visibility="collapsed"
    )
    if selected_cat != st.session_state.selected_category:
        st.session_state.selected_category = selected_cat
        st.rerun()

    # Filter posts based on category
    filtered_posts = posts
    if st.session_state.selected_category != "All":
        filtered_posts = [p for p in posts if p.get("category") == st.session_state.selected_category]

    st.write(f"Showing **{len(filtered_posts)}** publication{'s' if len(filtered_posts) != 1 else ''}")

    # Articles Grid (3 columns)
    if filtered_posts:
        cols = st.columns(3)
        for idx, post_item in enumerate(filtered_posts):
            with cols[idx % 3].container(border=True):
                if post_item.get("featured_image"):
                    st.image(post_item["featured_image"], use_container_width=True)
                
                st.caption(f"**{post_item['category']}** • {post_item.get('read_time', 5)} min read")
                st.markdown(f"### {post_item['title']}")
                
                excerpt_text = post_item.get("excerpt", "")
                if len(excerpt_text) > 130:
                    excerpt_text = excerpt_text[:130] + "..."
                st.write(excerpt_text)
                
                st.caption(f"By {post_item.get('author_name', 'Editorial Desk')} • ❤️ {post_item.get('likes', 0)} • 👁️ {post_item.get('views', 0)}")
                
                if st.button("Read Story", key=f"grid_post_{post_item['id']}", use_container_width=True):
                    st.session_state.selected_slug = post_item["slug"]
                    st.query_params["post"] = post_item["slug"]
                    st.rerun()
    else:
        st.info("No articles published in this category yet.")

    st.write("")
    st.divider()

    # Newsletter Box (Pure Python)
    with st.container(border=True):
        st.subheader("📬 Subscribe to The BlogSphere Dispatch")
        st.write("Receive curated essays, architectural post-mortems, and engineering insights directly in your inbox.")
        
        with st.form("home_newsletter_form", clear_on_submit=True):
            col_email, col_sub_btn = st.columns([3, 1])
            with col_email:
                sub_email = st.text_input("Email address", placeholder="your.name@company.com", label_visibility="collapsed")
            with col_sub_btn:
                sub_submitted = st.form_submit_button("Subscribe", type="primary", use_container_width=True)
            
            if sub_submitted:
                if sub_email and "@" in sub_email:
                    if db.add_subscriber(sub_email):
                        st.success("Welcome aboard! You have been subscribed to our weekly digest.")
                    else:
                        st.info("You are already subscribed with this email!")
                else:
                    st.warning("Please enter a valid email address.")

# ==========================================================
# VIEW 3: EXPLORE & ARCHIVE
# ==========================================================
elif st.session_state.current_view == "explore":
    st.header("🔍 Explore & Archive")
    st.caption("Search across our entire editorial catalog by title, theme, or author.")

    col_search, col_sort = st.columns([3, 1])
    with col_search:
        search_query = st.text_input("Search catalog", placeholder="Search articles, keywords, or topics...")
    with col_sort:
        sort_by = st.selectbox("Sort Order", ["Newest First", "Most Read", "Most Liked"])

    # Fetch matching posts
    matching_posts = db.get_posts(status="published", search=search_query.strip() if search_query else None)

    if sort_by == "Most Read":
        matching_posts.sort(key=lambda x: x.get("views", 0), reverse=True)
    elif sort_by == "Most Liked":
        matching_posts.sort(key=lambda x: x.get("likes", 0), reverse=True)
    else:
        matching_posts.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    st.write(f"Found **{len(matching_posts)}** result{'s' if len(matching_posts) != 1 else ''}")

    for post_item in matching_posts:
        with st.container(border=True):
            pcol1, pcol2 = st.columns([3, 1])
            with pcol1:
                st.caption(f"**{post_item['category']}** • {post_item.get('read_time', 5)} min read • {str(post_item['created_at'])[:10]}")
                st.subheader(post_item["title"])
                st.write(post_item.get("excerpt", ""))
                st.caption(f"Author: {post_item.get('author_name', 'Editorial Desk')} • 👁️ {post_item.get('views', 0)} views • ❤️ {post_item.get('likes', 0)} likes")
            with pcol2:
                if post_item.get("featured_image"):
                    st.image(post_item["featured_image"], use_container_width=True)
                if st.button("Read Story →", key=f"archive_read_{post_item['id']}", use_container_width=True):
                    st.session_state.selected_slug = post_item["slug"]
                    st.query_params["post"] = post_item["slug"]
                    st.rerun()

# ==========================================================
# VIEW 4: ADMIN STUDIO & CMS
# ==========================================================
elif st.session_state.current_view == "admin":
    # Authentication Check
    if not st.session_state.is_admin:
        st.header("🛡️ Editorial Studio Access")
        st.caption("Sign in to manage publications, draft stories, and review readership analytics.")

        with st.container(border=True):
            with st.form("admin_login_form"):
                login_email = st.text_input("Admin Email", value=ADMIN_EMAIL_DEFAULT)
                login_pass = st.text_input("Password", type="password", value=ADMIN_PASSWORD_DEFAULT)
                submit_login = st.form_submit_button("Sign In to Studio", type="primary", use_container_width=True)

                if submit_login:
                    # Verify credentials against SQLite users or defaults
                    conn = db.get_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT password_hash FROM users WHERE email = ?", (login_email.strip(),))
                    user_row = cursor.fetchone()
                    conn.close()

                    is_valid = False
                    if user_row and verify_password(login_pass, user_row[0]):
                        is_valid = True
                    elif login_email == ADMIN_EMAIL_DEFAULT and login_pass == ADMIN_PASSWORD_DEFAULT:
                        is_valid = True

                    if is_valid:
                        st.session_state.is_admin = True
                        st.session_state.admin_email = login_email.strip()
                        st.success("Authentication successful! Welcome to the Studio.")
                        st.rerun()
                    else:
                        st.error("Invalid email or password. Please verify your credentials.")
    else:
        # Logged-In Admin Studio
        admin_header_col1, admin_header_col2 = st.columns([3, 1])
        with admin_header_col1:
            st.header("🛡️ Editorial Studio & Content Management")
            st.caption(f"Authenticated as **{st.session_state.admin_email}**")
        with admin_header_col2:
            if st.button("🚪 Sign Out", key="admin_page_sign_out"):
                st.session_state.is_admin = False
                st.session_state.admin_email = ""
                st.session_state.current_view = "publications"
                st.rerun()

        # Analytics Metrics
        stats = db.get_dashboard_stats()
        mcol1, mcol2, mcol3, mcol4 = st.columns(4)
        mcol1.metric("Total Stories", stats["total_posts"])
        mcol2.metric("Published", stats["published_posts"])
        mcol3.metric("Total Views", stats["total_views"])
        mcol4.metric("Subscribers", stats["total_subscribers"])

        st.divider()

        # Admin Tabs
        tab_manage, tab_write, tab_subscribers = st.tabs([
            "📚 Manage Stories",
            "✍️ Write / Edit Story",
            "📬 Subscribers"
        ])

        # TAB 1: MANAGE STORIES
        with tab_manage:
            st.subheader("All Publications & Drafts")
            all_cms_posts = db.get_posts(status="all")
            
            if all_cms_posts:
                for cms_post in all_cms_posts:
                    with st.container(border=True):
                        c_info, c_actions = st.columns([3, 1.2])
                        with c_info:
                            status_badge = "🟢 PUBLISHED" if cms_post["status"] == "published" else "🟡 DRAFT"
                            featured_badge = "⭐ FEATURED" if cms_post.get("is_featured") == 1 else ""
                            st.write(f"**{cms_post['title']}**  `{status_badge}` {f'`{featured_badge}`' if featured_badge else ''}")
                            st.caption(f"Category: **{cms_post['category']}** • By {cms_post.get('author_name', 'Editorial Desk')} • 👁️ {cms_post.get('views', 0)} views • ❤️ {cms_post.get('likes', 0)} likes")
                        
                        with c_actions:
                            act_col1, act_col2 = st.columns(2)
                            with act_col1:
                                if st.button("✏️ Edit", key=f"edit_btn_{cms_post['id']}", use_container_width=True):
                                    st.session_state.editing_post_id = cms_post["id"]
                                    st.rerun()
                            with act_col2:
                                if st.button("🗑️ Delete", key=f"del_btn_{cms_post['id']}", use_container_width=True):
                                    db.delete_post(cms_post["id"])
                                    st.toast("Article deleted successfully.")
                                    st.rerun()

                            # Quick Toggle Status
                            new_status = "draft" if cms_post["status"] == "published" else "published"
                            toggle_label = "Unpublish to Draft" if cms_post["status"] == "published" else "Publish Live"
                            if st.button(toggle_label, key=f"toggle_btn_{cms_post['id']}", use_container_width=True):
                                db.update_post(
                                    post_id=cms_post["id"],
                                    title=cms_post["title"],
                                    content=cms_post["content"],
                                    category=cms_post["category"],
                                    excerpt=cms_post.get("excerpt", ""),
                                    subtitle=cms_post.get("subtitle", ""),
                                    featured_image=cms_post.get("featured_image", ""),
                                    tags=cms_post.get("tags", ""),
                                    status=new_status,
                                    is_featured=bool(cms_post.get("is_featured", 0))
                                )
                                st.rerun()
            else:
                st.info("No posts found in the database. Write your first story!")

        # TAB 2: WRITE / EDIT STORY
        with tab_write:
            editing_post = None
            if st.session_state.editing_post_id:
                editing_post = db.get_post_by_id(st.session_state.editing_post_id)
                st.subheader(f"Editing: {editing_post['title']}" if editing_post else "New Story")
                if st.button("← Cancel Editing & Create New Post"):
                    st.session_state.editing_post_id = None
                    st.rerun()
            else:
                st.subheader("Draft a New Story")

            with st.form("cms_story_form"):
                form_title = st.text_input(
                    "Article Title *",
                    value=editing_post["title"] if editing_post else ""
                )
                form_subtitle = st.text_input(
                    "Subtitle / Kicker",
                    value=editing_post.get("subtitle", "") if editing_post else ""
                )

                fcol1, fcol2, fcol3 = st.columns(3)
                with fcol1:
                    cat_index = 0
                    if editing_post and editing_post["category"] in DEFAULT_CATEGORIES:
                        cat_index = DEFAULT_CATEGORIES.index(editing_post["category"])
                    form_category = st.selectbox("Category", DEFAULT_CATEGORIES, index=cat_index)
                
                with fcol2:
                    status_index = 0
                    if editing_post and editing_post["status"] == "draft":
                        status_index = 1
                    form_status = st.selectbox("Status", ["published", "draft"], index=status_index)

                with fcol3:
                    form_featured = st.checkbox(
                        "Feature on Homepage",
                        value=bool(editing_post.get("is_featured", 0)) if editing_post else False
                    )

                form_image = st.text_input(
                    "Featured Image URL (Unsplash or direct image URL)",
                    value=editing_post.get("featured_image", "") if editing_post else "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&q=80"
                )

                form_excerpt = st.text_area(
                    "Short Excerpt",
                    value=editing_post.get("excerpt", "") if editing_post else "",
                    height=70,
                    placeholder="Brief 1-2 sentence overview for the cards..."
                )

                form_content = st.text_area(
                    "Article Body (Markdown format) *",
                    value=editing_post.get("content", "") if editing_post else "# Heading\n\nWrite your story here...",
                    height=350
                )

                form_tags = st.text_input(
                    "Tags (comma-separated)",
                    value=editing_post.get("tags", "") if editing_post else "Engineering, Architecture"
                )

                submit_story = st.form_submit_button(
                    "Update Publication" if editing_post else "Publish Story",
                    type="primary",
                    use_container_width=True
                )

                if submit_story:
                    if not form_title.strip() or not form_content.strip():
                        st.error("Title and Content are required fields.")
                    else:
                        if editing_post:
                            db.update_post(
                                post_id=editing_post["id"],
                                title=form_title.strip(),
                                content=form_content.strip(),
                                category=form_category,
                                excerpt=form_excerpt.strip(),
                                subtitle=form_subtitle.strip(),
                                featured_image=form_image.strip(),
                                tags=form_tags.strip(),
                                status=form_status,
                                is_featured=form_featured
                            )
                            st.session_state.editing_post_id = None
                            st.success("Publication updated successfully!")
                            st.rerun()
                        else:
                            new_id = db.create_post(
                                title=form_title.strip(),
                                content=form_content.strip(),
                                category=form_category,
                                excerpt=form_excerpt.strip(),
                                subtitle=form_subtitle.strip(),
                                featured_image=form_image.strip(),
                                tags=form_tags.strip(),
                                status=form_status,
                                is_featured=form_featured
                            )
                            st.success(f"New story published with ID #{new_id}!")
                            st.rerun()

        # TAB 3: SUBSCRIBERS
        with tab_subscribers:
            st.subheader("Newsletter Subscribers")
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, email, created_at FROM subscribers ORDER BY created_at DESC")
            subscribers = cursor.fetchall()
            conn.close()

            if subscribers:
                st.write(f"Total Registered Subscribers: **{len(subscribers)}**")
                for sub in subscribers:
                    with st.container(border=True):
                        st.write(f"✉️ **{sub['email']}**")
                        st.caption(f"Joined: {str(sub['created_at'])[:16]}")
            else:
                st.info("No subscribers registered yet.")
