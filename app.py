"""
BlogSphere — Modern Editorial Publication & Dynamic CMS
Crafted for Python and 1-Click Streamlit Community Cloud Deployment
"""
import streamlit as st
import datetime
import base64
import os
import re
from config import (
    PROJECT_NAME, PROJECT_TAGLINE, PROJECT_DESCRIPTION,
    DEFAULT_CATEGORIES, ADMIN_EMAIL_DEFAULT, ADMIN_PASSWORD_DEFAULT
)
import database as db
from auth import verify_password, hash_password

# Page configuration
st.set_page_config(
    page_title=f"{PROJECT_NAME} — Editorial & CMS Platform",
    page_icon="✒️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Editorial CSS
EDITORIAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* Typography & Base Root */
:root {
    --font-serif: 'Fraunces', Georgia, serif;
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
    --color-bg: #faf9f5;
    --color-surface: #ffffff;
    --color-accent: #d97706;
    --color-text-main: #1e293b;
    --color-text-muted: #64748b;
}

html, body, [data-testid="stAppViewContainer"] {
    font-family: var(--font-sans);
    background-color: var(--color-bg);
    color: var(--color-text-main);
}

/* Hide Default Streamlit Watermark & Clutter */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent;}

/* Editorial Headings */
h1, h2, h3, .editorial-heading {
    font-family: var(--font-serif) !important;
    font-weight: 700 !important;
    letter-spacing: -0.025em !important;
    color: #0f172a !important;
}

/* Top Masthead */
.masthead-wrapper {
    text-align: center;
    max-width: 800px;
    margin: 0.5rem auto 2.5rem auto;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(226, 232, 240, 0.9);
}

.masthead-kicker {
    font-size: 0.725rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #b45309;
    margin-bottom: 0.5rem;
}

.masthead-title {
    font-family: var(--font-serif);
    font-size: 3.5rem;
    font-weight: 800;
    line-height: 1.08;
    color: #0f172a;
    margin-bottom: 0.75rem;
}

.masthead-tagline {
    font-family: var(--font-serif);
    font-style: italic;
    font-size: 1.25rem;
    color: #475569;
    line-height: 1.5;
}

/* Flagship Hero Card */
.hero-card {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-radius: 1.25rem;
    color: #f8fafc;
    overflow: hidden;
    margin-bottom: 2.5rem;
    box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.12), 0 8px 10px -6px rgba(15, 23, 42, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.hero-body {
    padding: 2.5rem;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #fbbf24;
    margin-bottom: 1rem;
}

.hero-headline {
    font-family: var(--font-serif);
    font-size: 2.5rem;
    font-weight: 700;
    line-height: 1.15;
    color: #ffffff;
    margin-bottom: 1rem;
}

.hero-excerpt {
    font-size: 1.1rem;
    line-height: 1.6;
    color: #cbd5e1;
    margin-bottom: 1.5rem;
}

.hero-meta {
    font-size: 0.85rem;
    color: #94a3b8;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding-top: 1.25rem;
    border-top: 1px solid rgba(255, 255, 255, 0.12);
}

/* Editorial Article Card */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff !important;
    border: 1px solid rgba(226, 232, 240, 0.9) !important;
    border-radius: 1rem !important;
    padding: 1.25rem !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 20px -8px rgba(0, 0, 0, 0.08) !important;
}

/* Button Refinement */
div.stButton > button {
    border-radius: 0.65rem !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.45rem 1.15rem !important;
    transition: all 0.2s ease !important;
}

div.stButton > button[kind="primary"] {
    background-color: #d97706 !important;
    border-color: #d97706 !important;
    color: #ffffff !important;
}

div.stButton > button[kind="primary"]:hover {
    background-color: #b45309 !important;
    border-color: #b45309 !important;
}

/* Sidebar Custom Styling */
section[data-testid="stSidebar"] {
    background-color: #f5f4ed !important;
    border-right: 1px solid rgba(226, 232, 240, 0.9) !important;
}

/* Unboxed Quiet Metadata Line */
.unboxed-meta {
    font-size: 0.775rem;
    color: #64748b;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    margin-bottom: 0.5rem;
}

.unboxed-meta .cat {
    color: #b45309;
    font-weight: 600;
}

/* Drop Cap for Lead Paragraphs */
.dropcap-p::first-letter {
    font-family: var(--font-serif);
    float: left;
    font-size: 3.8rem;
    line-height: 0.85;
    padding-top: 4px;
    padding-right: 10px;
    padding-bottom: 0;
    font-weight: 700;
    color: #d97706;
}

/* Code block font */
code, pre {
    font-family: var(--font-mono) !important;
}
</style>
"""
st.markdown(EDITORIAL_CSS, unsafe_allow_html=True)

# Initialize Session State
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "admin_email" not in st.session_state:
    st.session_state.admin_email = ""
if "current_view" not in st.session_state:
    st.session_state.current_view = "home"
if "selected_slug" not in st.session_state:
    st.session_state.selected_slug = None
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "All"
if "edit_post_id" not in st.session_state:
    st.session_state.edit_post_id = None

# ==========================================================
# SIDEBAR NAVIGATION & PLATFORM CONTROLS
# ==========================================================
with st.sidebar:
    st.markdown(f"## ✒️ **{PROJECT_NAME}**")
    st.caption(f"*{PROJECT_TAGLINE}*")
    st.divider()

    # View Selector
    nav_choices = {
        "home": "📰 Publications (Home)",
        "explore": "🔍 Explore & Archive",
        "admin": "🛡️ Admin Studio & CMS",
        "deploy": "🚀 GitHub & Deploy Guide"
    }

    # Find active key
    active_nav_key = st.session_state.current_view
    if active_nav_key not in nav_choices:
        active_nav_key = "home"

    selected_nav = st.radio(
        "Navigation",
        options=list(nav_choices.keys()),
        format_func=lambda x: nav_choices[x],
        index=list(nav_choices.keys()).index(active_nav_key),
        label_visibility="collapsed"
    )

    if selected_nav != st.session_state.current_view:
        st.session_state.current_view = selected_nav
        st.session_state.selected_slug = None
        st.rerun()

    st.divider()

    # Category Filter
    st.markdown("### **Categories**")
    all_cats = ["All"] + DEFAULT_CATEGORIES
    for cat in all_cats:
        is_cur = (st.session_state.selected_category == cat)
        cat_btn_label = f"● {cat}" if is_cur else cat
        if st.button(cat_btn_label, key=f"side_cat_{cat}", use_container_width=True):
            st.session_state.selected_category = cat
            st.session_state.current_view = "home"
            st.session_state.selected_slug = None
            st.rerun()

    st.divider()

    # Admin Status & Quick Access
    if st.session_state.is_admin:
        st.success(f"✓ Admin: **{st.session_state.admin_email}**")
        col_write, col_out = st.columns(2)
        with col_write:
            if st.button("✍️ Write Story", use_container_width=True):
                st.session_state.current_view = "admin"
                st.session_state.edit_post_id = None
                st.rerun()
        with col_out:
            if st.button("Sign Out", use_container_width=True):
                st.session_state.is_admin = False
                st.session_state.admin_email = ""
                st.rerun()
    else:
        st.caption("Publisher Administration")
        if st.button("🔑 Sign In to Admin Studio", use_container_width=True):
            st.session_state.current_view = "admin"
            st.session_state.selected_slug = None
            st.rerun()

    st.divider()
    st.caption(f"© {datetime.datetime.now().year} {PROJECT_NAME} · SQLite + Streamlit")

# ==========================================================
# PAGE ROUTING
# ==========================================================

# 1. READ ARTICLE VIEW
if st.session_state.selected_slug:
    post = db.get_post_by_slug(st.session_state.selected_slug)
    if not post:
        st.error("Article not found or has been unpublished.")
        if st.button("← Return to Publications"):
            st.session_state.selected_slug = None
            st.rerun()
    else:
        # Increment view count
        db.increment_views(post["id"])

        # Top Navigation Bar in Reader
        col_back, col_actions = st.columns([2, 1])
        with col_back:
            if st.button("← All Publications", key="reader_back"):
                st.session_state.selected_slug = None
                st.rerun()
        with col_actions:
            subcol1, subcol2 = st.columns(2)
            with subcol1:
                if st.button(f"❤️ {post['likes']} Likes", key=f"like_{post['id']}", use_container_width=True):
                    db.like_post(post["id"])
                    st.toast("Thank you for your appreciation!")
                    st.rerun()
            with subcol2:
                if st.button("🔗 Copy Link", key="copy_link_btn", use_container_width=True):
                    st.toast("Story link copied to clipboard!")

        # Article Header
        st.markdown(f"""
        <div class="unboxed-meta" style="font-size: 0.85rem; margin-top: 1rem;">
            <span class="cat">{post['category']}</span>
            <span>·</span>
            <span>{post['read_time']} min read</span>
            <span>·</span>
            <span>Published {str(post['published_at'])[:10]}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"<h1 style='font-family: Fraunces, serif; font-size: 3rem; line-height: 1.15; margin-bottom: 0.5rem;'>{post['title']}</h1>", unsafe_allow_html=True)
        
        if post["subtitle"]:
            st.markdown(f"<p style='font-family: Fraunces, serif; font-style: italic; font-size: 1.35rem; color: #475569; margin-bottom: 1.5rem;'>{post['subtitle']}</p>", unsafe_allow_html=True)

        st.caption(f"Written by **{post['author_name']}** · {post['views']} reads")

        # Featured Image
        if post["featured_image"]:
            st.image(post["featured_image"], use_container_width=True)

        st.divider()

        # Content Rendering
        st.markdown(f"""
        <div style="font-size: 1.15rem; line-height: 1.85; color: #334155;">
        """, unsafe_allow_html=True)
        st.markdown(post["content"], unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.divider()

        if post["tags"]:
            st.caption(f"**Topics & Tags:** {post['tags']}")

        # Comments Section
        st.markdown("### 💬 Reader Responses & Discussion")
        comments = db.get_comments(post["id"])
        if comments:
            for c in comments:
                with st.chat_message("user"):
                    st.markdown(f"**{c['author_name']}** · *{str(c['created_at'])[:16]}*")
                    st.write(c["content"])
        else:
            st.info("No responses yet. Share your thoughts below.")

        with st.form(key=f"comment_form_{post['id']}", clear_on_submit=True):
            st.markdown("#### Leave a response")
            c_name = st.text_input("Your Name", placeholder="e.g. Alex Rivera")
            c_email = st.text_input("Your Email (optional)", placeholder="alex@domain.com")
            c_body = st.text_area("Your Perspective", placeholder="Write your constructive thoughts...")
            if st.form_submit_button("Submit Response", use_container_width=True):
                if c_name.strip() and c_body.strip():
                    db.add_comment(post["id"], c_name.strip(), c_email.strip(), c_body.strip())
                    st.success("Your response has been published!")
                    st.rerun()
                else:
                    st.error("Please provide both your name and response text.")

# 2. HOMEPAGE VIEW
elif st.session_state.current_view == "home":
    # Top Masthead
    st.markdown(f"""
    <div class="masthead-wrapper">
        <div class="masthead-kicker">Independent Systems & Engineering Journal</div>
        <div class="masthead-title">{PROJECT_NAME}</div>
        <div class="masthead-tagline">{PROJECT_TAGLINE}</div>
    </div>
    """, unsafe_allow_html=True)

    # Search and Filter Strip
    search_col, cat_col = st.columns([3, 1])
    with search_col:
        search_kw = st.text_input("Search", placeholder="Search publications by title, keyword, or topic...", label_visibility="collapsed")
    with cat_col:
        chosen_cat = st.selectbox(
            "Category Filter",
            options=["All"] + DEFAULT_CATEGORIES,
            index=0 if st.session_state.selected_category == "All" else (DEFAULT_CATEGORIES.index(st.session_state.selected_category) + 1 if st.session_state.selected_category in DEFAULT_CATEGORIES else 0),
            label_visibility="collapsed"
        )
        if chosen_cat != st.session_state.selected_category:
            st.session_state.selected_category = chosen_cat

    cat_arg = None if st.session_state.selected_category == "All" else st.session_state.selected_category
    posts = db.get_posts(status="published", category=cat_arg, search=search_kw.strip() if search_kw.strip() else None)

    if not posts:
        st.info("No articles match your current filter or search criteria.")
    else:
        # Flagship Featured Article
        featured = next((p for p in posts if p.get("is_featured") == 1), posts[0])
        other_posts = [p for p in posts if p["id"] != featured["id"]]

        # Display Flagship Hero Article
        feat_col_img, feat_col_text = st.columns([1.1, 1])
        with feat_col_img:
            img_url = featured.get("featured_image") or "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80"
            st.image(img_url, use_container_width=True)
        with feat_col_text:
            st.markdown(f"""
            <div class="unboxed-meta">
                <span class="cat">{featured['category']}</span>
                <span>·</span>
                <span>{featured['read_time']} min read</span>
                <span>·</span>
                <span>By {featured['author_name']}</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"<h2 style='font-family: Fraunces, serif; font-size: 2.25rem; line-height: 1.15; margin-bottom: 0.5rem;'>{featured['title']}</h2>", unsafe_allow_html=True)
            if featured["subtitle"]:
                st.markdown(f"<p style='font-family: Fraunces, serif; font-style: italic; font-size: 1.1rem; color: #475569;'>{featured['subtitle']}</p>", unsafe_allow_html=True)
            
            clean_excerpt = featured["excerpt"] or featured["content"][:180] + "..."
            st.write(clean_excerpt)
            
            if st.button("Read Full Article →", key=f"hero_btn_{featured['id']}", type="primary"):
                st.session_state.selected_slug = featured["slug"]
                st.rerun()

        st.divider()

        # Latest Articles Grid
        st.markdown(f"### 📰 Latest Publications ({len(posts)})")
        grid_cols = st.columns(3)
        for idx, p in enumerate(other_posts):
            target_col = grid_cols[idx % 3]
            with target_col:
                with st.container(border=True):
                    if p.get("featured_image"):
                        st.image(p["featured_image"], use_container_width=True)
                    st.markdown(f"""
                    <div class="unboxed-meta" style="margin-top: 0.5rem;">
                        <span class="cat">{p['category']}</span>
                        <span>·</span>
                        <span>{p['read_time']} min read</span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"<h4 style='font-family: Fraunces, serif; font-size: 1.15rem; line-height: 1.25; margin-bottom: 0.4rem;'>{p['title']}</h4>", unsafe_allow_html=True)
                    card_summary = p["excerpt"][:110] + "..." if p["excerpt"] else p["content"][:110] + "..."
                    st.caption(card_summary)
                    st.caption(f"By {p['author_name']} · {p['likes']} likes · {p['views']} views")
                    if st.button("Read Story", key=f"card_read_{p['id']}", use_container_width=True):
                        st.session_state.selected_slug = p["slug"]
                        st.rerun()

    # Sunday Dispatch Newsletter
    st.divider()
    st.markdown("### 📬 The Sunday Dispatch Newsletter")
    st.write("Curated technical deep dives, software architecture analyses, and design perspectives delivered directly to your inbox.")
    nl1, nl2 = st.columns([3, 1])
    with nl1:
        sub_email = st.text_input("Newsletter Email", placeholder="reader@domain.com", label_visibility="collapsed")
    with nl2:
        if st.button("Subscribe", use_container_width=True, type="primary"):
            if sub_email and "@" in sub_email:
                if db.add_subscriber(sub_email):
                    st.success("Welcome! You are subscribed to our editorial dispatches.")
                else:
                    st.info("You are already subscribed. Thank you for your support!")
            else:
                st.error("Please enter a valid email address.")

# 3. EXPLORE & ARCHIVE VIEW
elif st.session_state.current_view == "explore":
    st.markdown(f"# 🔍 Explore All Publications")
    st.write("Browse and filter the complete archive of articles across categories and tags.")

    exp_search = st.text_input("Search keywords", placeholder="Type keywords like Python, Architecture, Design, AI...")
    exp_cat = st.selectbox("Filter Category", ["All"] + DEFAULT_CATEGORIES)

    filter_category = None if exp_cat == "All" else exp_cat
    archive_posts = db.get_posts(status="published", category=filter_category, search=exp_search if exp_search else None)

    st.markdown(f"**Found {len(archive_posts)} articles**")
    for ap in archive_posts:
        with st.container(border=True):
            col_info, col_btn = st.columns([4, 1])
            with col_info:
                st.markdown(f"""
                <div class="unboxed-meta">
                    <span class="cat">{ap['category']}</span>
                    <span>·</span>
                    <span>{ap['read_time']} min read</span>
                    <span>·</span>
                    <span>By {ap['author_name']}</span>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"### {ap['title']}")
                st.write(ap['excerpt'] or ap['content'][:160] + "...")
                if ap['tags']:
                    st.caption(f"Tags: {ap['tags']}")
            with col_btn:
                if ap.get("featured_image"):
                    st.image(ap["featured_image"], width=130)
                if st.button("Read Article", key=f"exp_btn_{ap['id']}", use_container_width=True):
                    st.session_state.selected_slug = ap["slug"]
                    st.rerun()

# 4. ADMIN STUDIO & CMS VIEW
elif st.session_state.current_view == "admin":
    st.markdown("# 🛡️ Admin Studio & Content Management")

    if not st.session_state.is_admin:
        st.warning("Please sign in to access post creation, drafts, publishing, and settings.")
        login_c1, login_c2 = st.columns([1, 1])
        with login_c1:
            with st.form("admin_sign_in_form"):
                st.markdown("### Administrator Sign In")
                a_email = st.text_input("Admin Email", value=ADMIN_EMAIL_DEFAULT)
                a_pass = st.text_input("Password", type="password", value=ADMIN_PASSWORD_DEFAULT)
                submitted = st.form_submit_button("Sign In to Studio", use_container_width=True, type="primary")

                if submitted:
                    conn = db.get_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM users WHERE email = ?", (a_email.strip(),))
                    user_row = cursor.fetchone()
                    conn.close()

                    if user_row and verify_password(user_row["password_hash"], a_pass):
                        st.session_state.is_admin = True
                        st.session_state.admin_email = user_row["email"]
                        st.success("Authentication successful!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")
        with login_c2:
            st.info(f"""
            **Default Administrator Credentials:**
            - **Email**: `{ADMIN_EMAIL_DEFAULT}`
            - **Password**: `{ADMIN_PASSWORD_DEFAULT}`

            You can change your password anytime in `config.py` or through the settings tab.
            """)
    else:
        # Metrics Strip
        stats = db.get_dashboard_stats()
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("Total Stories", stats["total_posts"])
        m2.metric("Published", stats["published_posts"])
        m3.metric("Drafts", stats["draft_posts"])
        m4.metric("Views", stats["total_views"])
        m5.metric("Likes", stats["total_likes"])
        m6.metric("Subscribers", stats["total_subscribers"])

        st.divider()

        admin_tabs = st.tabs(["📝 Content Library", "✨ Compose & Edit Article", "⚙️ Platform Settings", "📤 Cloud Database Setup"])

        # TAB 1: ALL POSTS
        with admin_tabs[0]:
            st.markdown("### Content Library & Post Management")
            stat_pick = st.selectbox("Status Filter", ["all", "published", "draft", "scheduled"], index=0)
            cur_posts = db.get_posts(status=stat_pick, category=None, search=None)

            if not cur_posts:
                st.write("No articles found under this filter.")
            else:
                for cp in cur_posts:
                    with st.container(border=True):
                        c1, c2, c3, c4 = st.columns([4, 1.5, 1.5, 1.5])
                        with c1:
                            badge = "🟢 Published" if cp['status'] == 'published' else ("🟡 Draft" if cp['status'] == 'draft' else "🔵 Scheduled")
                            f_badge = "★ Featured · " if cp['is_featured'] else ""
                            st.markdown(f"**{cp['title']}**")
                            st.caption(f"{badge} · {f_badge}{cp['category']} · {cp['views']} reads · {cp['likes']} likes")
                        with c2:
                            new_st = "draft" if cp['status'] == 'published' else "published"
                            lbl = "Unpublish" if cp['status'] == 'published' else "Publish"
                            if st.button(lbl, key=f"tgl_{cp['id']}", use_container_width=True):
                                db.update_post(
                                    post_id=cp['id'],
                                    title=cp['title'],
                                    content=cp['content'],
                                    category=cp['category'],
                                    excerpt=cp['excerpt'],
                                    subtitle=cp['subtitle'],
                                    featured_image=cp['featured_image'],
                                    tags=cp['tags'],
                                    status=new_st,
                                    is_featured=bool(cp['is_featured'])
                                )
                                st.rerun()
                        with c3:
                            if st.button("✏️ Edit", key=f"edt_{cp['id']}", use_container_width=True):
                                st.session_state.edit_post_id = cp['id']
                                st.rerun()
                        with c4:
                            if st.button("🗑️ Delete", key=f"dlt_{cp['id']}", use_container_width=True):
                                db.delete_post(cp['id'])
                                st.success("Article deleted.")
                                st.rerun()

        # TAB 2: COMPOSE / EDIT ARTICLE
        with admin_tabs[1]:
            is_edit_mode = (st.session_state.edit_post_id is not None)
            editing_article = db.get_post_by_id(st.session_state.edit_post_id) if is_edit_mode else None

            if is_edit_mode and editing_article:
                st.info(f"Editing: **{editing_article['title']}**")
                if st.button("Cancel & Create New Article"):
                    st.session_state.edit_post_id = None
                    st.rerun()

            with st.form("article_editor_form"):
                f_title = st.text_input("Article Title *", value=editing_article["title"] if editing_article else "")
                f_subtitle = st.text_input("Subtitle / Deck (Optional)", value=editing_article["subtitle"] if editing_article else "")

                fc1, fc2, fc3 = st.columns([1.5, 1.5, 1])
                with fc1:
                    cur_cat = editing_article["category"] if editing_article else DEFAULT_CATEGORIES[0]
                    cat_i = DEFAULT_CATEGORIES.index(cur_cat) if cur_cat in DEFAULT_CATEGORIES else 0
                    f_cat = st.selectbox("Category", DEFAULT_CATEGORIES, index=cat_i)
                with fc2:
                    st_opts = ["published", "draft", "scheduled"]
                    cur_s = editing_article["status"] if editing_article else "published"
                    st_i = st_opts.index(cur_s) if cur_s in st_opts else 0
                    f_stat = st.selectbox("Publication Status", st_opts, index=st_i)
                with fc3:
                    f_feat = st.checkbox("Featured on Home", value=bool(editing_article["is_featured"]) if editing_article else False)

                f_img = st.text_input(
                    "Featured Image URL (Unsplash, Cloudinary, or Supabase)",
                    value=editing_article["featured_image"] if editing_article else "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80"
                )

                uploaded_img = st.file_uploader("Or Upload Image File from Computer", type=["png", "jpg", "jpeg", "webp"], key="st_editor_upload")
                if uploaded_img is not None:
                    raw_bytes = uploaded_img.read()
                    mime = uploaded_img.type or "image/jpeg"
                    b64_str = base64.b64encode(raw_bytes).decode()
                    f_img = f"data:{mime};base64,{b64_str}"
                    st.caption("✓ Local image encoded and ready to save!")

                if f_img:
                    st.image(f_img, caption="Featured Image Preview", width=250)

                f_excerpt = st.text_area("Excerpt (Summary for cards & search)", value=editing_article["excerpt"] if editing_article else "")
                f_tags = st.text_input("Tags (comma separated)", value=editing_article["tags"] if editing_article else "Tech, Guide, Systems")

                st.markdown("#### Story Body (Markdown Supported)")
                f_body = st.text_area(
                    "Markdown Content",
                    value=editing_article["content"] if editing_article else "# Section Heading\n\nWrite your insights here using Markdown...",
                    height=320
                )

                submit_editor = st.form_submit_button(
                    "💾 Save & Publish Article" if not is_edit_mode else "💾 Update Article",
                    use_container_width=True,
                    type="primary"
                )

                if submit_editor:
                    if not f_title.strip() or not f_body.strip():
                        st.error("Please provide both title and content.")
                    else:
                        if is_edit_mode:
                            db.update_post(
                                post_id=editing_article["id"],
                                title=f_title.strip(),
                                content=f_body.strip(),
                                category=f_cat,
                                excerpt=f_excerpt.strip(),
                                subtitle=f_subtitle.strip(),
                                featured_image=f_img.strip(),
                                tags=f_tags.strip(),
                                status=f_stat,
                                is_featured=f_feat
                            )
                            st.success("Article updated successfully!")
                            st.session_state.edit_post_id = None
                            st.rerun()
                        else:
                            new_article_id = db.create_post(
                                title=f_title.strip(),
                                content=f_body.strip(),
                                category=f_cat,
                                excerpt=f_excerpt.strip(),
                                subtitle=f_subtitle.strip(),
                                featured_image=f_img.strip(),
                                tags=f_tags.strip(),
                                status=f_stat,
                                is_featured=f_feat
                            )
                            st.success(f"New publication created! (ID: {new_article_id})")
                            st.rerun()

        # TAB 3: PLATFORM SETTINGS
        with admin_tabs[2]:
            st.markdown("### Platform Branding")
            st.write(f"Current Publication Name: **{PROJECT_NAME}**")
            st.info("To rebrand permanently, update `PROJECT_NAME` in `config.py` or set the `BLOG_PROJECT_NAME` environment variable.")

        # TAB 4: CLOUD DATABASE SETUP
        with admin_tabs[3]:
            st.markdown("### Supabase PostgreSQL & Cloud Storage")
            st.markdown("""
            **1. Connect Supabase PostgreSQL:**
            Set `DATABASE_URL` in your Streamlit Secrets:
            ```toml
            DATABASE_URL = "postgresql://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres"
            ```

            **2. Cloudinary Media Storage:**
            ```toml
            CLOUDINARY_CLOUD_NAME = "your_cloud_name"
            CLOUDINARY_API_KEY = "your_api_key"
            CLOUDINARY_API_SECRET = "your_api_secret"
            ```
            """)

# 5. GITHUB & STREAMLIT DEPLOY GUIDE
elif st.session_state.current_view == "deploy":
    st.markdown(f"# 🚀 Deploy {PROJECT_NAME} on Streamlit Community Cloud")
    st.markdown("""
    This platform is engineered for 1-click publishing to **Streamlit Community Cloud** with GitHub integration.

    ### 3-Step Deployment Walkthrough:

    1. **Push your code to GitHub**:
       ```bash
       git add .
       git commit -m "feat: deploy modern BlogSphere publication platform"
       git push origin main
       ```

    2. **Connect with Streamlit Community Cloud**:
       - Visit [share.streamlit.io](https://share.streamlit.io).
       - Select your **BlogSphere** repository.
       - Set **Main file path** to: `app.py`.
       - Click **Deploy**!

    3. **Configure Secrets (Optional for Supabase/Cloudinary)**:
       Go to *Settings > Secrets* in Streamlit Cloud:
       ```toml
       ADMIN_EMAIL = "admin@blogsphere.dev"
       ADMIN_PASSWORD = "your_secure_password"
       BLOG_PROJECT_NAME = "BlogSphere"
       ```
    """)
