"""
BlogSphere — Premium Editorial Publication & Dynamic CMS Platform
Engineered to replicate the modern editorial web design in Streamlit.
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

# Page configuration - start with collapsed sidebar so it looks like a clean website!
st.set_page_config(
    page_title=f"{PROJECT_NAME} — Editorial & CMS Platform",
    page_icon="✒️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom High-End Editorial CSS to transform Streamlit into a modern publication
FULL_EDITORIAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* Typography & Base Root */
:root {
    --font-serif: 'Fraunces', Georgia, serif;
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
    --color-bg: #faf9f5;
    --color-text-main: #0f172a;
    --color-accent: #d97706;
}

html, body, [data-testid="stAppViewContainer"] {
    font-family: var(--font-sans);
    background-color: var(--color-bg) !important;
    color: var(--color-text-main) !important;
}

/* Remove default Streamlit top padding and watermarks */
.main > div {
    padding-top: 1.5rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 1350px !important;
    margin: 0 auto !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent; height: 1rem;}

/* Headings */
h1, h2, h3, h4 {
    font-family: var(--font-serif) !important;
    font-weight: 700 !important;
    letter-spacing: -0.025em !important;
    color: #0f172a !important;
}

/* Top Navbar Container */
.top-navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 0 1.25rem 0;
    margin-bottom: 2rem;
    border-bottom: 1px solid rgba(226, 232, 240, 0.9);
}

.brand-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 2.25rem;
    height: 2.25rem;
    background: #0f172a;
    color: #ffffff;
    border-radius: 0.5rem;
    font-weight: 700;
    font-size: 1.15rem;
    margin-right: 0.75rem;
}

.brand-name {
    font-family: var(--font-serif);
    font-size: 1.5rem;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.03em;
    line-height: 1;
}

.brand-sub {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 700;
    color: #b45309;
    margin-top: 0.15rem;
}

/* Masthead Header */
.masthead-section {
    text-align: center;
    max-width: 780px;
    margin: 1rem auto 3rem auto;
}

.masthead-kicker {
    font-size: 0.725rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    color: #b45309;
    margin-bottom: 0.65rem;
}

.masthead-title {
    font-family: var(--font-serif);
    font-size: 4rem;
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.035em;
    color: #0f172a;
    margin-bottom: 0.85rem;
}

.masthead-tagline {
    font-family: var(--font-serif);
    font-style: italic;
    font-size: 1.35rem;
    color: #475569;
    line-height: 1.5;
}

/* Dark Hero Feature Card */
.dark-hero-card {
    background: #0f172a;
    border-radius: 1.25rem;
    color: #ffffff;
    padding: 3rem;
    margin-bottom: 2.5rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.15);
}

.hero-kicker-tag {
    font-size: 0.725rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #fbbf24;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.hero-main-title {
    font-family: var(--font-serif);
    font-size: 2.75rem;
    font-weight: 700;
    line-height: 1.15;
    color: #ffffff;
    margin-bottom: 1.25rem;
}

.hero-lead-text {
    font-size: 1.15rem;
    line-height: 1.65;
    color: #cbd5e1;
    margin-bottom: 1.75rem;
}

.hero-author-strip {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 0.875rem;
    color: #94a3b8;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255, 255, 255, 0.12);
}

/* Card Styling for 3-Column Grid */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff !important;
    border: 1px solid rgba(226, 232, 240, 0.9) !important;
    border-radius: 1rem !important;
    padding: 1.25rem !important;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 24px -10px rgba(0, 0, 0, 0.1) !important;
}

/* Button Customization */
div.stButton > button {
    border-radius: 0.65rem !important;
    font-weight: 600 !important;
    font-size: 0.825rem !important;
    padding: 0.45rem 1rem !important;
    transition: all 0.15s ease !important;
}

div.stButton > button[kind="primary"] {
    background-color: #d97706 !important;
    border-color: #d97706 !important;
    color: #ffffff !important;
}

div.stButton > button[kind="primary"]:hover {
    background-color: #b45309 !important;
    border-color: #b45309 !important;
    transform: scale(1.02);
}

/* Unboxed Clean Metadata Line */
.unboxed-meta {
    font-size: 0.775rem;
    color: #64748b;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    margin-bottom: 0.5rem;
}

.unboxed-meta .cat-label {
    color: #b45309;
    font-weight: 600;
}

/* Trending Block */
.trending-num {
    font-family: var(--font-serif);
    font-size: 1.75rem;
    font-weight: 800;
    color: #cbd5e1;
    line-height: 1;
    margin-bottom: 0.25rem;
}
</style>
"""
st.markdown(FULL_EDITORIAL_CSS, unsafe_allow_html=True)

# Initialize Session State
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "admin_email" not in st.session_state:
    st.session_state.admin_email = ""
if "nav_page" not in st.session_state:
    st.session_state.nav_page = "home"
if "selected_slug" not in st.session_state:
    st.session_state.selected_slug = None
if "selected_cat" not in st.session_state:
    st.session_state.selected_cat = "All"
if "edit_post_id" not in st.session_state:
    st.session_state.edit_post_id = None

# ==========================================================
# TOP EDITORIAL NAVBAR (Just like the custom website!)
# ==========================================================
nav_col_brand, nav_col_links, nav_col_cta = st.columns([3.5, 5, 2.5])

with nav_col_brand:
    st.markdown(f"""
    <div style="display: flex; align-items: center; cursor: pointer;">
        <div class="brand-badge">B</div>
        <div>
            <div class="brand-name">{PROJECT_NAME}</div>
            <div class="brand-sub">Editorial & CMS</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with nav_col_links:
    btn_home, btn_explore, btn_admin, btn_deploy = st.columns(4)
    with btn_home:
        if st.button("Publications", key="nav_home", use_container_width=True):
            st.session_state.nav_page = "home"
            st.session_state.selected_slug = None
            st.rerun()
    with btn_explore:
        if st.button("Archive & Search", key="nav_exp", use_container_width=True):
            st.session_state.nav_page = "explore"
            st.session_state.selected_slug = None
            st.rerun()
    with btn_admin:
        admin_label = "🛡️ Admin Studio" if not st.session_state.is_admin else "🛡️ Studio (Active)"
        if st.button(admin_label, key="nav_adm", use_container_width=True):
            st.session_state.nav_page = "admin"
            st.session_state.selected_slug = None
            st.rerun()
    with btn_deploy:
        if st.button("🚀 GitHub / Deploy", key="nav_dep", use_container_width=True):
            st.session_state.nav_page = "deploy"
            st.session_state.selected_slug = None
            st.rerun()

with nav_col_cta:
    if st.session_state.is_admin:
        col_new, col_logout = st.columns([1.5, 1])
        with col_new:
            if st.button("+ Write Story", key="top_write", type="primary", use_container_width=True):
                st.session_state.nav_page = "admin"
                st.session_state.edit_post_id = None
                st.rerun()
        with col_logout:
            if st.button("Logout", key="top_logout", use_container_width=True):
                st.session_state.is_admin = False
                st.session_state.admin_email = ""
                st.rerun()
    else:
        if st.button("Admin Sign In", key="top_login", use_container_width=True):
            st.session_state.nav_page = "admin"
            st.session_state.selected_slug = None
            st.rerun()

st.markdown("<hr style='border: none; border-top: 1px solid rgba(226, 232, 240, 0.9); margin: 0.5rem 0 2rem 0;' />", unsafe_allow_html=True)

# ==========================================================
# PAGE ROUTING
# ==========================================================

# 1. READ ARTICLE VIEW
if st.session_state.selected_slug:
    article = db.get_post_by_slug(st.session_state.selected_slug)
    if not article:
        st.error("Article not found.")
        if st.button("← Return to Publications"):
            st.session_state.selected_slug = None
            st.rerun()
    else:
        db.increment_views(article["id"])

        # Breadcrumb & Actions
        b_col, a_col1, a_col2 = st.columns([6, 1.5, 1.5])
        with b_col:
            if st.button("← All Publications", key="art_back"):
                st.session_state.selected_slug = None
                st.rerun()
        with a_col1:
            if st.button(f"❤️ {article['likes']} Appreciations", key=f"like_{article['id']}", use_container_width=True):
                db.like_post(article["id"])
                st.toast("Thank you for your appreciation!")
                st.rerun()
        with a_col2:
            if st.button("🔗 Copy Link", key="art_copy", use_container_width=True):
                st.toast("Story URL copied to clipboard!")

        # Article Header
        st.markdown(f"""
        <div style="text-align: center; max-width: 850px; margin: 2rem auto;">
            <div class="unboxed-meta" style="justify-content: center; font-size: 0.85rem;">
                <span class="cat-label">{article['category']}</span>
                <span>·</span>
                <span>{article['read_time']} min read</span>
                <span>·</span>
                <span>Published {str(article['published_at'])[:10]}</span>
            </div>
            <h1 style="font-family: Fraunces, serif; font-size: 3.5rem; line-height: 1.1; margin-bottom: 1rem;">
                {article['title']}
            </h1>
            <p style="font-family: Fraunces, serif; font-style: italic; font-size: 1.4rem; color: #475569; margin-bottom: 1.5rem;">
                {article['subtitle'] or ''}
            </p>
            <div style="display: inline-flex; align-items: center; gap: 0.75rem; background: rgba(241, 245, 249, 0.8); padding: 0.5rem 1.25rem; border-radius: 9999px;">
                <span style="font-weight: 600; font-size: 0.9rem;">By {article['author_name']}</span>
                <span style="color: #94a3b8;">·</span>
                <span style="font-size: 0.825rem; color: #64748b;">{article['views']} reads</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if article["featured_image"]:
            st.image(article["featured_image"], use_container_width=True)

        st.markdown("<hr style='border: none; border-top: 1px solid rgba(226, 232, 240, 0.9); margin: 2.5rem 0;' />", unsafe_allow_html=True)

        # Article Body
        st.markdown(f"<div style='font-size: 1.2rem; line-height: 1.85; color: #334155; max-width: 850px; margin: 0 auto;'>", unsafe_allow_html=True)
        st.markdown(article["content"], unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr style='border: none; border-top: 1px solid rgba(226, 232, 240, 0.9); margin: 2.5rem 0;' />", unsafe_allow_html=True)

        # Comments Section
        st.markdown("<div style='max-width: 850px; margin: 0 auto;'>", unsafe_allow_html=True)
        st.markdown("### 💬 Reader Responses & Discussion")
        comments = db.get_comments(article["id"])
        if comments:
            for c in comments:
                with st.chat_message("user"):
                    st.markdown(f"**{c['author_name']}** · *{str(c['created_at'])[:16]}*")
                    st.write(c["content"])
        else:
            st.info("No responses yet. Be the first to share your perspective below.")

        with st.form(key=f"art_comm_{article['id']}", clear_on_submit=True):
            st.markdown("#### Leave a response")
            c_name = st.text_input("Your Name", placeholder="e.g. Alex Morgan")
            c_email = st.text_input("Your Email (optional)", placeholder="alex@domain.com")
            c_body = st.text_area("Your thoughts", placeholder="Write your constructive response...")
            if st.form_submit_button("Post Response", use_container_width=True, type="primary"):
                if c_name.strip() and c_body.strip():
                    db.add_comment(article["id"], c_name.strip(), c_email.strip(), c_body.strip())
                    st.success("Your response has been published!")
                    st.rerun()
                else:
                    st.error("Please provide both your name and comment.")
        st.markdown("</div>", unsafe_allow_html=True)

# 2. HOMEPAGE VIEW (Full Website Layout)
elif st.session_state.nav_page == "home":
    # Big Centered Masthead
    st.markdown(f"""
    <div class="masthead-section">
        <div class="masthead-kicker">INDEPENDENT EDITORIAL & SYSTEMS PUBLISHING</div>
        <div class="masthead-title">{PROJECT_NAME}</div>
        <div class="masthead-tagline">{PROJECT_TAGLINE}</div>
    </div>
    """, unsafe_allow_html=True)

    # Fetch all published posts
    all_published = db.get_posts(status="published")

    if not all_published:
        st.info("No publications currently online.")
    else:
        # Flagship Featured Hero Story
        flagship = next((p for p in all_published if p.get("is_featured") == 1), all_published[0])
        remaining = [p for p in all_published if p["id"] != flagship["id"]]

        # Display Hero Card with Dark Split Background (matching React website!)
        hero_col_text, hero_col_img = st.columns([1.15, 1])
        with hero_col_text:
            st.markdown(f"""
            <div style="background: #0f172a; padding: 2.75rem; border-radius: 1.25rem 0 0 1.25rem; color: #ffffff; height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div class="hero-kicker-tag">
                        <span>★ FEATURED DISPATCH</span>
                        <span>·</span>
                        <span>{flagship['category']}</span>
                        <span>·</span>
                        <span>{flagship['read_time']} MIN READ</span>
                    </div>
                    <div style="font-family: Fraunces, serif; font-size: 2.35rem; font-weight: 700; line-height: 1.15; margin-bottom: 1rem; color: #ffffff;">
                        {flagship['title']}
                    </div>
                    <p style="font-size: 1.05rem; line-height: 1.6; color: #cbd5e1; margin-bottom: 1.5rem;">
                        {flagship['subtitle'] or flagship['excerpt']}
                    </p>
                </div>
                <div class="hero-author-strip">
                    <span style="font-weight: 600; color: #ffffff;">By {flagship['author_name']}</span>
                    <span>·</span>
                    <span>{str(flagship['published_at'])[:10]}</span>
                    <span>·</span>
                    <span>{flagship['views']} reads</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Read Full Story →", key=f"hero_read_{flagship['id']}", type="primary", use_container_width=True):
                st.session_state.selected_slug = flagship["slug"]
                st.rerun()

        with hero_col_img:
            hero_img = flagship.get("featured_image") or "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80"
            st.image(hero_img, use_container_width=True)

        st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)

        # Trending Stories Horizontal Strip
        trending = sorted(all_published, key=lambda x: x.get("views", 0), reverse=True)[:4]
        if trending:
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.775rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; color: #b45309; margin-bottom: 1rem;">
                <span>🔥 TRENDING DISPATCHES THIS WEEK</span>
            </div>
            """, unsafe_allow_html=True)
            
            trend_cols = st.columns(len(trending))
            for idx, tp in enumerate(trending):
                with trend_cols[idx]:
                    with st.container(border=True):
                        st.markdown(f"<div class='trending-num'>0{idx+1}</div>", unsafe_allow_html=True)
                        st.markdown(f"""
                        <div class="unboxed-meta">
                            <span class="cat-label">{tp['category']}</span>
                            <span>·</span>
                            <span>{tp['read_time']}m</span>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f"<h5 style='font-family: Fraunces, serif; font-size: 1rem; line-height: 1.25; margin-bottom: 0.5rem;'>{tp['title']}</h5>", unsafe_allow_html=True)
                        if st.button("Read", key=f"trend_btn_{tp['id']}", use_container_width=True):
                            st.session_state.selected_slug = tp["slug"]
                            st.rerun()

        st.markdown("<hr style='border: none; border-top: 1px solid rgba(226, 232, 240, 0.9); margin: 2.5rem 0 1.5rem 0;' />", unsafe_allow_html=True)

        # Horizontal Category Filter Buttons (Exactly like the React website!)
        st.markdown("#### **Filter by Discipline**")
        cat_filter_list = ["All"] + DEFAULT_CATEGORIES
        cat_columns = st.columns(len(cat_filter_list))
        for idx, cat_item in enumerate(cat_filter_list):
            with cat_columns[idx]:
                is_active = (st.session_state.selected_cat == cat_item)
                btn_type = "primary" if is_active else "secondary"
                if st.button(cat_item, key=f"cat_top_{cat_item}", type=btn_type, use_container_width=True):
                    st.session_state.selected_cat = cat_item
                    st.rerun()

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        # Filter remaining posts
        if st.session_state.selected_cat != "All":
            filtered_posts = [p for p in remaining if p["category"] == st.session_state.selected_cat]
        else:
            filtered_posts = remaining

        # 3-Column Latest Publications Grid
        st.markdown(f"### 📰 Latest Publications ({len(filtered_posts)})")
        
        if not filtered_posts:
            st.info("No other articles found in this category.")
        else:
            grid_cols = st.columns(3)
            for i, p in enumerate(filtered_posts):
                col = grid_cols[i % 3]
                with col:
                    with st.container(border=True):
                        if p.get("featured_image"):
                            st.image(p["featured_image"], use_container_width=True)
                        st.markdown(f"""
                        <div class="unboxed-meta" style="margin-top: 0.5rem;">
                            <span class="cat-label">{p['category']}</span>
                            <span>·</span>
                            <span>{p['read_time']} min read</span>
                            <span>·</span>
                            <span>{str(p['published_at'])[:10]}</span>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f"<h4 style='font-family: Fraunces, serif; font-size: 1.25rem; line-height: 1.25; margin-bottom: 0.4rem;'>{p['title']}</h4>", unsafe_allow_html=True)
                        st.caption(p["excerpt"][:110] + "..." if p["excerpt"] else p["content"][:110] + "...")
                        st.caption(f"By {p['author_name']} · {p['likes']} likes · {p['views']} views")
                        if st.button("Read Full Story", key=f"grid_read_{p['id']}", use_container_width=True):
                            st.session_state.selected_slug = p["slug"]
                            st.rerun()

    # The Sunday Dispatch Newsletter Footer Section
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(226, 232, 240, 0.9); margin: 3rem 0 2rem 0;' />", unsafe_allow_html=True)
    st.markdown("### 📬 The Sunday Dispatch Newsletter")
    st.write("Curated technical deep-dives, systems insights, and interface design essays. No noise.")
    nl_c1, nl_c2 = st.columns([3, 1])
    with nl_c1:
        sub_mail = st.text_input("Your email", placeholder="reader@domain.com", label_visibility="collapsed")
    with nl_c2:
        if st.button("Subscribe", key="home_sub", type="primary", use_container_width=True):
            if sub_mail and "@" in sub_mail:
                if db.add_subscriber(sub_mail):
                    st.success("Subscribed successfully! Welcome to the sphere.")
                else:
                    st.info("You are already subscribed. Thank you!")
            else:
                st.error("Please provide a valid email.")

# 3. EXPLORE ARCHIVE VIEW
elif st.session_state.nav_page == "explore":
    st.markdown(f"# 🔍 Explore All Publications")
    st.write("Browse and filter the complete archive of articles across categories and tags.")

    e_search = st.text_input("Search keywords", placeholder="Type keywords like Python, Architecture, Design, AI...")
    e_cat = st.selectbox("Filter Category", ["All"] + DEFAULT_CATEGORIES)

    filter_cat = None if e_cat == "All" else e_cat
    arch_posts = db.get_posts(status="published", category=filter_cat, search=e_search if e_search else None)

    st.markdown(f"**Found {len(arch_posts)} publications**")
    for ap in arch_posts:
        with st.container(border=True):
            c_info, c_btn = st.columns([4.5, 1.2])
            with c_info:
                st.markdown(f"""
                <div class="unboxed-meta">
                    <span class="cat-label">{ap['category']}</span>
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
            with c_btn:
                if ap.get("featured_image"):
                    st.image(ap["featured_image"], width=130)
                if st.button("Read", key=f"e_read_{ap['id']}", use_container_width=True):
                    st.session_state.selected_slug = ap["slug"]
                    st.rerun()

# 4. ADMIN STUDIO & CMS VIEW
elif st.session_state.nav_page == "admin":
    st.markdown("# 🛡️ Admin Studio & Content Management")

    if not st.session_state.is_admin:
        st.warning("Please sign in to access post creation, drafts, publishing, and settings.")
        l_c1, l_c2 = st.columns([1, 1])
        with l_c1:
            with st.form("admin_sign_in"):
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
        with l_c2:
            st.info(f"""
            **Default Administrator Credentials:**
            - **Email**: `{ADMIN_EMAIL_DEFAULT}`
            - **Password**: `{ADMIN_PASSWORD_DEFAULT}`

            You can change your password in `config.py` or via the platform settings tab.
            """)
    else:
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
elif st.session_state.nav_page == "deploy":
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
