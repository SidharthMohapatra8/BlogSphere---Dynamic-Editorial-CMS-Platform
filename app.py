"""
BlogSphere — Modern Editorial Publication & Dynamic CMS Platform
Engineered for Python & Streamlit Community Cloud
"""
import streamlit as st
import datetime
import base64
import os
from config import (
    PROJECT_NAME, PROJECT_TAGLINE, PROJECT_DESCRIPTION,
    DEFAULT_CATEGORIES, ADMIN_EMAIL_DEFAULT, ADMIN_PASSWORD_DEFAULT
)
import database as db
from auth import verify_password, hash_password

st.set_page_config(
    page_title=f"{PROJECT_NAME} — Editorial & CMS",
    page_icon="✒️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Injected Styles (Clean and verified to never trigger code-block indentation)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
--font-serif: 'Fraunces', Georgia, serif;
--font-sans: 'Inter', -apple-system, sans-serif;
--font-mono: 'JetBrains Mono', monospace;
--bg-cream: #faf9f5;
--text-slate: #0f172a;
--accent-amber: #d97706;
}

html, body, [data-testid="stAppViewContainer"] {
font-family: var(--font-sans);
background-color: var(--bg-cream) !important;
color: var(--text-slate) !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent;}

h1, h2, h3, h4 {
font-family: var(--font-serif) !important;
font-weight: 700 !important;
letter-spacing: -0.025em !important;
color: #0f172a !important;
}

/* Card Styling */
div[data-testid="stVerticalBlockBorderWrapper"] {
background: #ffffff !important;
border: 1px solid rgba(226, 232, 240, 0.9) !important;
border-radius: 1rem !important;
padding: 1.25rem !important;
box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03) !important;
}

div.stButton > button[kind="primary"] {
background-color: #d97706 !important;
border-color: #d97706 !important;
color: #ffffff !important;
border-radius: 0.65rem !important;
font-weight: 600 !important;
}

div.stButton > button[kind="primary"]:hover {
background-color: #b45309 !important;
border-color: #b45309 !important;
}

div.stButton > button:not([kind="primary"]) {
border-radius: 0.65rem !important;
font-weight: 500 !important;
border: 1px solid #e2e8f0 !important;
background: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# Session state
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "admin_email" not in st.session_state:
    st.session_state.admin_email = ""
if "current_page" not in st.session_state:
    st.session_state.current_page = "Publications"
if "selected_slug" not in st.session_state:
    st.session_state.selected_slug = None
if "selected_cat" not in st.session_state:
    st.session_state.selected_cat = "All"
if "edit_post_id" not in st.session_state:
    st.session_state.edit_post_id = None

# TOP NAVIGATION BAR (Using clean Streamlit columns to guarantee zero HTML leakage)
nav1, nav2, nav3, nav4, nav5 = st.columns([3.5, 1.5, 1.5, 1.5, 1.5])
with nav1:
    st.markdown(f"### ✒️ **{PROJECT_NAME}**")
with nav2:
    if st.button("📰 Publications", use_container_width=True, type="primary" if st.session_state.current_page == "Publications" and not st.session_state.selected_slug else "secondary"):
        st.session_state.current_page = "Publications"
        st.session_state.selected_slug = None
        st.rerun()
with nav3:
    if st.button("🔍 Explore Archive", use_container_width=True, type="primary" if st.session_state.current_page == "Explore Archive" else "secondary"):
        st.session_state.current_page = "Explore Archive"
        st.session_state.selected_slug = None
        st.rerun()
with nav4:
    admin_btn_title = "🛡️ Admin Studio" if not st.session_state.is_admin else "🛡️ Studio (Logged In)"
    if st.button(admin_btn_title, use_container_width=True, type="primary" if st.session_state.current_page == "Admin Studio" else "secondary"):
        st.session_state.current_page = "Admin Studio"
        st.session_state.selected_slug = None
        st.rerun()
with nav5:
    if st.session_state.is_admin:
        if st.button("Sign Out", use_container_width=True):
            st.session_state.is_admin = False
            st.session_state.admin_email = ""
            st.rerun()
    else:
        if st.button("Sign In", use_container_width=True):
            st.session_state.current_page = "Admin Studio"
            st.session_state.selected_slug = None
            st.rerun()

st.divider()

# ==========================================================
# ROUTING
# ==========================================================

# 1. READ ARTICLE VIEW
if st.session_state.selected_slug:
    post = db.get_post_by_slug(st.session_state.selected_slug)
    if not post:
        st.error("Article not found.")
        if st.button("← Back to Publications"):
            st.session_state.selected_slug = None
            st.rerun()
    else:
        db.increment_views(post["id"])

        c_back, c_like, c_share = st.columns([6, 1.5, 1.5])
        with c_back:
            if st.button("← Back to Publications"):
                st.session_state.selected_slug = None
                st.rerun()
        with c_like:
            if st.button(f"❤️ {post['likes']} Likes", use_container_width=True):
                db.like_post(post["id"])
                st.toast("Thank you for your appreciation!")
                st.rerun()
        with c_share:
            if st.button("🔗 Copy Link", use_container_width=True):
                st.toast("Link copied!")

        st.caption(f"{post['category']} · {post['read_time']} min read · Published {str(post['published_at'])[:10]}")
        st.markdown(f"# {post['title']}")
        if post["subtitle"]:
            st.markdown(f"*{post['subtitle']}*")
        st.caption(f"Written by **{post['author_name']}** · {post['views']} reads")

        if post["featured_image"]:
            st.image(post["featured_image"], use_container_width=True)

        st.divider()
        st.markdown(post["content"])
        st.divider()

        # Comments
        st.markdown("### 💬 Reader Responses")
        comments = db.get_comments(post["id"])
        if comments:
            for c in comments:
                with st.chat_message("user"):
                    st.markdown(f"**{c['author_name']}** · *{str(c['created_at'])[:16]}*")
                    st.write(c["content"])
        else:
            st.info("No responses yet. Share your thoughts below.")

        with st.form(key=f"comm_{post['id']}", clear_on_submit=True):
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
                    st.error("Please provide both name and comment.")

# 2. PUBLICATIONS VIEW (Homepage)
elif st.session_state.current_page == "Publications":
    # Masthead
    st.markdown("<p style='text-align:center; font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.18em; color:#b45309; margin-bottom:0;'>INDEPENDENT EDITORIAL & SYSTEMS PUBLISHING</p>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align:center; font-size:3.5rem; margin-top:0.25rem; margin-bottom:0.5rem;'>{PROJECT_NAME}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-style:italic; font-size:1.25rem; color:#475569; margin-bottom:2rem;'>{PROJECT_TAGLINE}</p>", unsafe_allow_html=True)

    all_published = db.get_posts(status="published")

    if all_published:
        flagship = next((p for p in all_published if p.get("is_featured") == 1), all_published[0])
        remaining = [p for p in all_published if p["id"] != flagship["id"]]

        # Hero Banner
        with st.container(border=True):
            h_text, h_img = st.columns([1.2, 1], gap="medium")
            with h_text:
                st.caption(f"★ FEATURED DISPATCH · {flagship['category']} · {flagship['read_time']} MIN READ")
                st.markdown(f"## {flagship['title']}")
                st.write(flagship["subtitle"] or flagship["excerpt"])
                st.caption(f"By {flagship['author_name']} · {str(flagship['published_at'])[:10]} · {flagship['views']} reads")
                if st.button("Read Full Story →", key="flagship_btn", type="primary"):
                    st.session_state.selected_slug = flagship["slug"]
                    st.rerun()
            with h_img:
                h_pic = flagship.get("featured_image") or "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80"
                st.image(h_pic, use_container_width=True)

        st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

        # Category Filter Bar
        st.markdown("#### **Filter by Topic**")
        cat_options = ["All"] + DEFAULT_CATEGORIES
        cat_cols = st.columns(len(cat_options))
        for idx, cat in enumerate(cat_options):
            with cat_cols[idx]:
                is_active = (st.session_state.selected_cat == cat)
                if st.button(cat, key=f"cat_btn_{cat}", use_container_width=True, type="primary" if is_active else "secondary"):
                    st.session_state.selected_cat = cat
                    st.rerun()

        # Filtered posts
        filtered_posts = remaining if st.session_state.selected_cat == "All" else [p for p in remaining if p["category"] == st.session_state.selected_cat]

        st.markdown(f"### 📰 Latest Publications ({len(filtered_posts)})")
        if not filtered_posts:
            st.info("No articles found in this category.")
        else:
            cols = st.columns(3)
            for i, p in enumerate(filtered_posts):
                with cols[i % 3]:
                    with st.container(border=True):
                        if p.get("featured_image"):
                            st.image(p["featured_image"], use_container_width=True)
                        st.caption(f"{p['category']} · {p['read_time']} min read · {str(p['published_at'])[:10]}")
                        st.markdown(f"#### {p['title']}")
                        st.caption(p["excerpt"][:110] + "..." if p["excerpt"] else p["content"][:110] + "...")
                        st.caption(f"By {p['author_name']} · {p['likes']} likes · {p['views']} views")
                        if st.button("Read Story", key=f"p_btn_{p['id']}", use_container_width=True):
                            st.session_state.selected_slug = p["slug"]
                            st.rerun()

    # Newsletter
    st.divider()
    st.markdown("### 📬 The Sunday Dispatch Newsletter")
    st.write("Curated technical deep-dives and engineering perspectives delivered to your inbox.")
    nl1, nl2 = st.columns([3, 1])
    with nl1:
        s_mail = st.text_input("Newsletter Email", placeholder="reader@domain.com", label_visibility="collapsed")
    with nl2:
        if st.button("Subscribe", key="sub_btn", use_container_width=True, type="primary"):
            if s_mail and "@" in s_mail:
                if db.add_subscriber(s_mail):
                    st.success("Subscribed successfully! Welcome.")
                else:
                    st.info("You are already subscribed. Thank you!")
            else:
                st.error("Please enter a valid email address.")

# 3. EXPLORE ARCHIVE VIEW
elif st.session_state.current_page == "Explore Archive":
    st.markdown("# 🔍 Explore All Publications")
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
                st.caption(f"{ap['category']} · {ap['read_time']} min read · By {ap['author_name']}")
                st.markdown(f"### {ap['title']}")
                st.write(ap['excerpt'] or ap['content'][:160] + "...")
                if ap['tags']:
                    st.caption(f"Tags: {ap['tags']}")
            with c_btn:
                if ap.get("featured_image"):
                    st.image(ap["featured_image"], width=130)
                if st.button("Read Article", key=f"e_btn_{ap['id']}", use_container_width=True, type="primary"):
                    st.session_state.selected_slug = ap["slug"]
                    st.rerun()

# 4. ADMIN STUDIO & CMS VIEW
elif st.session_state.current_page == "Admin Studio":
    st.markdown("# 🛡️ Admin Studio & Content Management")

    if not st.session_state.is_admin:
        st.warning("Please sign in to access post creation, drafts, publishing, and settings.")
        l1, l2 = st.columns([1, 1])
        with l1:
            with st.form("admin_login"):
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
        with l2:
            st.info(f"""
            **Default Administrator Credentials:**
            - **Email**: `{ADMIN_EMAIL_DEFAULT}`
            - **Password**: `{ADMIN_PASSWORD_DEFAULT}`

            You can change your password in `config.py` or through the settings tab.
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

        with admin_tabs[2]:
            st.markdown("### Platform Branding")
            st.write(f"Current Publication Name: **{PROJECT_NAME}**")
            st.info("To rebrand permanently, update `PROJECT_NAME` in `config.py` or set the `BLOG_PROJECT_NAME` environment variable.")

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

# Footer
st.divider()
st.markdown(f"<p style='text-align:center; color:#64748b; font-size:0.85rem;'>© {datetime.datetime.now().year} <strong>{PROJECT_NAME}</strong> · Built with Python & Streamlit</p>", unsafe_allow_html=True)
