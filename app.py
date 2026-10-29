"""
BlogSphere — Premium Editorial Publication & Dynamic CMS Platform
Engineered to replicate the modern editorial web design in Streamlit with zero visual compromises.
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
    initial_sidebar_state="collapsed"
)

# Custom High-End Editorial CSS
EDITORIAL_HEAD_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

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
    padding-top: 1rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    max-width: 1400px !important;
    margin: 0 auto !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent; height: 0.5rem;}
section[data-testid="stSidebar"] {display: none;}

/* Headings */
h1, h2, h3, h4 {
    font-family: var(--font-serif) !important;
    font-weight: 700 !important;
    letter-spacing: -0.025em !important;
    color: #0f172a !important;
}

/* Links */
a {
    transition: all 0.15s ease;
}
a:hover {
    opacity: 0.85;
}

/* Primary Button Styling */
div.stButton > button {
    border-radius: 0.65rem !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.45rem 1.15rem !important;
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

/* Drop Cap */
.drop-cap::first-letter {
    font-family: var(--font-serif);
    float: left;
    font-size: 4rem;
    line-height: 0.85;
    padding-top: 4px;
    padding-right: 12px;
    font-weight: 700;
    color: #d97706;
}
</style>
"""
st.markdown(EDITORIAL_HEAD_CSS, unsafe_allow_html=True)

# Read URL Query Parameters for Instant Navigation
query_slug = st.query_params.get("read")
query_view = st.query_params.get("view", "home")
query_cat = st.query_params.get("cat", "All")

# Session State for Admin
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "admin_email" not in st.session_state:
    st.session_state.admin_email = ""
if "edit_post_id" not in st.session_state:
    st.session_state.edit_post_id = None

# ==========================================================
# 1. PIXEL-PERFECT TOP NAVIGATION BAR (HTML Matching Tab 4)
# ==========================================================
nav_active_home = "border-bottom: 2px solid #d97706; color: #0f172a; font-weight: 600;" if query_view == "home" and not query_slug else "color: #64748b; font-weight: 500;"
nav_active_exp = "border-bottom: 2px solid #d97706; color: #0f172a; font-weight: 600;" if query_view == "explore" else "color: #64748b; font-weight: 500;"
nav_active_adm = "border-bottom: 2px solid #d97706; color: #d97706; font-weight: 600;" if query_view == "admin" else "color: #d97706; font-weight: 600;"

st.markdown(f"""
<div style="display: flex; align-items: center; justify-content: space-between; padding: 0.75rem 0 1.25rem 0; border-bottom: 1px solid rgba(226, 232, 240, 0.9); margin-bottom: 2.25rem;">
    <!-- Brand -->
    <a href="?view=home" target="_self" style="display: flex; align-items: center; gap: 0.75rem; text-decoration: none;">
        <div style="width: 38px; height: 38px; background: #0f172a; color: white; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.25rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            B
        </div>
        <div>
            <div style="font-family: 'Fraunces', serif; font-size: 1.45rem; font-weight: 800; line-height: 1; color: #0f172a; letter-spacing: -0.03em;">
                {PROJECT_NAME}
            </div>
            <div style="font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.14em; color: #b45309; margin-top: 2px;">
                Editorial & CMS
            </div>
        </div>
    </a>

    <!-- Center Navigation Links -->
    <div style="display: flex; align-items: center; gap: 2rem;">
        <a href="?view=home" target="_self" style="text-decoration: none; font-size: 0.925rem; padding-bottom: 4px; {nav_active_home}">
            Publications
        </a>
        <a href="?view=explore" target="_self" style="text-decoration: none; font-size: 0.925rem; padding-bottom: 4px; {nav_active_exp}">
            Explore & Archive
        </a>
        <a href="?view=admin" target="_self" style="text-decoration: none; font-size: 0.925rem; padding-bottom: 4px; display: inline-flex; align-items: center; gap: 0.35rem; {nav_active_adm}">
            <span>🛡️</span> <span>Admin Studio</span>
        </a>
    </div>

    <!-- Right Controls -->
    <div style="display: flex; align-items: center; gap: 0.85rem;">
        <a href="?view=deploy" target="_self" style="border: 1px solid #cbd5e1; padding: 0.45rem 0.9rem; border-radius: 8px; color: #334155; font-size: 0.8rem; font-weight: 600; text-decoration: none; background: #ffffff;">
            GitHub / Deploy
        </a>
        <a href="?view=admin" target="_self" style="background: #0f172a; color: #ffffff; padding: 0.45rem 1rem; border-radius: 8px; font-size: 0.8rem; font-weight: 600; text-decoration: none;">
            {'Admin Active ✓' if st.session_state.is_admin else 'Sign In'}
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# 2. ROUTE: ARTICLE DETAIL READER
# ==========================================================
if query_slug:
    post = db.get_post_by_slug(query_slug)
    if not post:
        st.error("Article not found.")
        st.markdown("<a href='?view=home' target='_self' style='text-decoration:none;'>← Back to publications</a>", unsafe_allow_html=True)
    else:
        db.increment_views(post["id"])

        # Back & Like Bar
        b_col, l_col = st.columns([5, 1.5])
        with b_col:
            st.markdown(f"<a href='?view=home' target='_self' style='color:#64748b; font-size:0.875rem; font-weight:600; text-decoration:none;'>← All Publications</a>", unsafe_allow_html=True)
        with l_col:
            if st.button(f"❤️ {post['likes']} Likes", key=f"like_{post['id']}", use_container_width=True):
                db.like_post(post["id"])
                st.toast("Thank you for your appreciation!")
                st.rerun()

        # Header
        st.markdown(f"""
        <div style="text-align: center; max-width: 820px; margin: 2rem auto;">
            <div style="font-size: 0.85rem; color: #64748b; margin-bottom: 0.75rem; font-weight: 500;">
                <span style="color: #b45309; font-weight: 700; text-transform: uppercase;">{post['category']}</span>
                <span>·</span>
                <span>{post['read_time']} min read</span>
                <span>·</span>
                <span>Published {str(post['published_at'])[:10]}</span>
            </div>
            <h1 style="font-family: 'Fraunces', serif; font-size: 3.5rem; line-height: 1.1; margin-bottom: 1rem; color: #0f172a;">
                {post['title']}
            </h1>
            <p style="font-family: 'Fraunces', serif; font-style: italic; font-size: 1.4rem; color: #475569; margin-bottom: 1.5rem;">
                {post['subtitle'] or ''}
            </p>
            <div style="display: inline-flex; align-items: center; gap: 0.75rem; background: rgba(241, 245, 249, 0.9); padding: 0.45rem 1.25rem; border-radius: 9999px;">
                <span style="font-weight: 600; font-size: 0.875rem;">By {post['author_name']}</span>
                <span style="color: #94a3b8;">·</span>
                <span style="font-size: 0.825rem; color: #64748b;">{post['views']} reads</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if post["featured_image"]:
            st.image(post["featured_image"], use_container_width=True)

        st.markdown("<hr style='border: none; border-top: 1px solid rgba(226, 232, 240, 0.9); margin: 2.5rem 0;' />", unsafe_allow_html=True)

        # Article Content
        st.markdown(f"<div style='font-size: 1.18rem; line-height: 1.85; color: #334155; max-width: 820px; margin: 0 auto;' class='drop-cap'>", unsafe_allow_html=True)
        st.markdown(post["content"], unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr style='border: none; border-top: 1px solid rgba(226, 232, 240, 0.9); margin: 2.5rem 0;' />", unsafe_allow_html=True)

        # Comments Section
        st.markdown("<div style='max-width: 820px; margin: 0 auto;'>", unsafe_allow_html=True)
        st.markdown("### 💬 Reader Responses & Discussion")
        comments = db.get_comments(post["id"])
        if comments:
            for c in comments:
                with st.chat_message("user"):
                    st.markdown(f"**{c['author_name']}** · *{str(c['created_at'])[:16]}*")
                    st.write(c["content"])
        else:
            st.info("No responses yet. Be the first to share your perspective below.")

        with st.form(key=f"art_comm_{post['id']}", clear_on_submit=True):
            st.markdown("#### Leave a response")
            c_name = st.text_input("Your Name", placeholder="e.g. Alex Morgan")
            c_email = st.text_input("Your Email (optional)", placeholder="alex@domain.com")
            c_body = st.text_area("Your thoughts", placeholder="Write your constructive response...")
            if st.form_submit_button("Post Response", use_container_width=True, type="primary"):
                if c_name.strip() and c_body.strip():
                    db.add_comment(post["id"], c_name.strip(), c_email.strip(), c_body.strip())
                    st.success("Your response has been published!")
                    st.rerun()
                else:
                    st.error("Please provide both your name and comment.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# 3. ROUTE: HOMEPAGE (Matching Tab 4 with Unified Hero Card)
# ==========================================================
elif query_view == "home":
    # Centered Masthead
    st.markdown(f"""
    <div style="text-align: center; max-width: 780px; margin: 0.5rem auto 2.5rem auto;">
        <div style="font-size: 0.725rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.18em; color: #b45309; margin-bottom: 0.5rem;">
            INDEPENDENT EDITORIAL & SYSTEMS PUBLISHING
        </div>
        <div style="font-family: 'Fraunces', serif; font-size: 3.85rem; font-weight: 800; line-height: 1.05; letter-spacing: -0.035em; color: #0f172a; margin-bottom: 0.75rem;">
            {PROJECT_NAME}
        </div>
        <div style="font-family: 'Fraunces', serif; font-style: italic; font-size: 1.35rem; color: #475569; line-height: 1.5;">
            {PROJECT_TAGLINE}
        </div>
    </div>
    """, unsafe_allow_html=True)

    all_published = db.get_posts(status="published")

    if all_published:
        flagship = next((p for p in all_published if p.get("is_featured") == 1), all_published[0])
        remaining = [p for p in all_published if p["id"] != flagship["id"]]

        hero_img = flagship.get("featured_image") or "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80"
        flagship_slug = flagship["slug"]

        # UNIFIED 2-COLUMN HERO CARD (ONE SINGLE CONTINUOUS CARD!)
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1.2fr 1fr; background: #0f172a; border-radius: 1.25rem; overflow: hidden; box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.25); border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 2.75rem;">
            <!-- Left Text Column -->
            <div style="padding: 3rem; display: flex; flex-direction: column; justify-content: space-between; color: #ffffff;">
                <div>
                    <div style="font-size: 0.725rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.14em; color: #fbbf24; margin-bottom: 1rem;">
                        ★ FEATURED DISPATCH · {flagship['category']} · {flagship['read_time']} MIN READ
                    </div>
                    <div style="font-family: 'Fraunces', serif; font-size: 2.5rem; font-weight: 700; line-height: 1.15; color: #ffffff; margin-bottom: 1rem;">
                        {flagship['title']}
                    </div>
                    <p style="font-size: 1.1rem; line-height: 1.6; color: #cbd5e1; margin-bottom: 1.75rem;">
                        {flagship['subtitle'] or flagship['excerpt']}
                    </p>
                </div>

                <div style="display: flex; align-items: center; justify-content: space-between; padding-top: 1.5rem; border-top: 1px solid rgba(255, 255, 255, 0.12);">
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <div style="width: 36px; height: 36px; border-radius: 50%; background: #d97706; color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem;">
                            {flagship['author_name'][0]}
                        </div>
                        <div>
                            <div style="font-weight: 600; font-size: 0.9rem; color: #ffffff;">{flagship['author_name']}</div>
                            <div style="font-size: 0.75rem; color: #94a3b8;">{str(flagship['published_at'])[:10]} · {flagship['views']} reads</div>
                        </div>
                    </div>

                    <a href="?read={flagship_slug}" target="_self" style="background: #f59e0b; color: #0f172a; font-weight: 700; font-size: 0.85rem; padding: 0.65rem 1.35rem; border-radius: 0.65rem; text-decoration: none; display: inline-flex; align-items: center; gap: 0.4rem; box-shadow: 0 4px 6px rgba(0,0,0,0.15);">
                        <span>Read Full Story</span> <span>→</span>
                    </a>
                </div>
            </div>

            <!-- Right Image Column -->
            <div style="position: relative; min-height: 100%;">
                <img src="{hero_img}" style="width: 100%; height: 100%; object-fit: cover; display: block;" />
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Trending Stories 4-Column Strip
        trending = sorted(all_published, key=lambda x: x.get("views", 0), reverse=True)[:4]
        if trending:
            st.markdown("""
            <div style="font-size: 0.775rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.14em; color: #b45309; margin-bottom: 1rem;">
                🔥 TRENDING DISPATCHES THIS WEEK
            </div>
            """, unsafe_allow_html=True)

            trend_cols = st.columns(len(trending))
            for idx, tp in enumerate(trending):
                with trend_cols[idx]:
                    st.markdown(f"""
                    <a href="?read={tp['slug']}" target="_self" style="text-decoration: none; display: block; background: #ffffff; border: 1px solid rgba(226, 232, 240, 0.9); border-radius: 0.875rem; padding: 1.15rem; transition: transform 0.2s ease;">
                        <div style="font-family: 'Fraunces', serif; font-size: 1.75rem; font-weight: 800; color: #cbd5e1; line-height: 1; margin-bottom: 0.35rem;">
                            0{idx+1}
                        </div>
                        <div style="font-size: 0.725rem; color: #b45309; font-weight: 700; text-transform: uppercase; margin-bottom: 0.35rem;">
                            {tp['category']} · {tp['read_time']}m
                        </div>
                        <div style="font-family: 'Fraunces', serif; font-size: 1rem; font-weight: 700; color: #0f172a; line-height: 1.3; margin-bottom: 0.5rem; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">
                            {tp['title']}
                        </div>
                        <div style="font-size: 0.75rem; color: #64748b;">
                            By {tp['author_name']}
                        </div>
                    </a>
                    """, unsafe_allow_html=True)

        st.markdown("<hr style='border: none; border-top: 1px solid rgba(226, 232, 240, 0.9); margin: 2.75rem 0 1.5rem 0;' />", unsafe_allow_html=True)

        # Horizontal Category Pills
        cat_items = ["All"] + DEFAULT_CATEGORIES
        pills_html = '<div style="display: flex; gap: 0.5rem; overflow-x: auto; padding-bottom: 0.5rem; margin-bottom: 1.5rem;">'
        for cat in cat_items:
            is_active = (query_cat == cat)
            active_bg = "background: #0f172a; color: #ffffff; font-weight: 700;" if is_active else "background: #ffffff; color: #475569; font-weight: 500; border: 1px solid rgba(226, 232, 240, 0.9);"
            pills_html += f'<a href="?view=home&cat={cat}" target="_self" style="padding: 0.45rem 1rem; border-radius: 9999px; font-size: 0.8rem; text-decoration: none; white-space: nowrap; {active_bg}">{cat}</a>'
        pills_html += '</div>'
        st.markdown(pills_html, unsafe_allow_html=True)

        # Filter remaining
        filtered_posts = remaining if query_cat == "All" else [p for p in remaining if p["category"] == query_cat]

        # 3-Column Latest Publications Grid
        st.markdown(f"### 📰 Latest Publications ({len(filtered_posts)})")
        grid_cols = st.columns(3)
        for i, p in enumerate(filtered_posts):
            with grid_cols[i % 3]:
                p_img = p.get("featured_image") or "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=800&q=80"
                summary = p["excerpt"][:110] + "..." if p["excerpt"] else p["content"][:110] + "..."
                st.markdown(f"""
                <div style="background: #ffffff; border: 1px solid rgba(226, 232, 240, 0.9); border-radius: 1rem; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.02); margin-bottom: 1.5rem;">
                    <img src="{p_img}" style="width: 100%; aspect-ratio: 16/10; object-fit: cover; display: block;" />
                    <div style="padding: 1.25rem;">
                        <div style="font-size: 0.75rem; color: #64748b; margin-bottom: 0.5rem;">
                            <span style="color: #b45309; font-weight: 700;">{p['category']}</span> · {p['read_time']} min read · {str(p['published_at'])[:10]}
                        </div>
                        <h4 style="font-family: 'Fraunces', serif; font-size: 1.2rem; font-weight: 700; color: #0f172a; line-height: 1.3; margin-bottom: 0.5rem;">
                            {p['title']}
                        </h4>
                        <p style="font-size: 0.875rem; color: #475569; line-height: 1.5; margin-bottom: 1.25rem;">
                            {summary}
                        </p>
                        <div style="display: flex; align-items: center; justify-content: space-between; padding-top: 0.75rem; border-top: 1px solid #f1f5f9; font-size: 0.8rem;">
                            <span style="font-weight: 600; color: #334155;">By {p['author_name']}</span>
                            <a href="?read={p['slug']}" target="_self" style="color: #d97706; font-weight: 700; text-decoration: none;">Read Story →</a>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Footer
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(226, 232, 240, 0.9); margin: 3rem 0 2rem 0;' />", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="padding: 1.5rem 0; text-align: center; color: #64748b; font-size: 0.825rem;">
        <div>© {datetime.datetime.now().year} <strong>{PROJECT_NAME}</strong> · Where engineering, design architecture, and strategic depth converge.</div>
        <div style="margin-top: 0.5rem; display: flex; gap: 1.5rem; justify-content: center;">
            <a href="?view=home" target="_self" style="color: #64748b; text-decoration: none;">Publications</a>
            <a href="?view=explore" target="_self" style="color: #64748b; text-decoration: none;">Archive</a>
            <a href="?view=admin" target="_self" style="color: #64748b; text-decoration: none;">Admin Studio</a>
            <a href="?view=deploy" target="_self" style="color: #64748b; text-decoration: none;">GitHub Deployment</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================================
# 4. ROUTE: EXPLORE ARCHIVE VIEW
# ==========================================================
elif query_view == "explore":
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
                <div style="font-size: 0.775rem; color: #64748b; margin-bottom: 0.35rem;">
                    <span style="color: #b45309; font-weight: 700;">{ap['category']}</span> · {ap['read_time']} min read · By {ap['author_name']}
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"### {ap['title']}")
                st.write(ap['excerpt'] or ap['content'][:160] + "...")
                if ap['tags']:
                    st.caption(f"Tags: {ap['tags']}")
            with c_btn:
                if ap.get("featured_image"):
                    st.image(ap["featured_image"], width=130)
                st.markdown(f"<a href='?read={ap['slug']}' target='_self' style='background:#d97706; color:white; padding:0.45rem 1rem; border-radius:8px; text-decoration:none; font-size:0.85rem; font-weight:600; display:inline-block; margin-top:0.5rem;'>Read Article</a>", unsafe_allow_html=True)

# ==========================================================
# 5. ROUTE: ADMIN STUDIO & CMS VIEW
# ==========================================================
elif query_view == "admin":
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

# ==========================================================
# 6. ROUTE: GITHUB & STREAMLIT DEPLOY GUIDE
# ==========================================================
elif query_view == "deploy":
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
