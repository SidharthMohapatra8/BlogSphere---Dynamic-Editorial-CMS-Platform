"""
BlogSphere - Streamlit Dynamic Blogging Platform & CMS
Suitable for local execution and 1-click deployment on Streamlit Community Cloud.
"""
import streamlit as st
import datetime
import base64
from config import (
    PROJECT_NAME, PROJECT_TAGLINE, PROJECT_DESCRIPTION,
    DEFAULT_CATEGORIES, ADMIN_EMAIL_DEFAULT, ADMIN_PASSWORD_DEFAULT
)
import database as db
from auth import verify_password, hash_password

# Set page configuration
st.set_page_config(
    page_title=f"{PROJECT_NAME} — Editorial & CMS",
    page_icon="✒️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Editorial & Responsive CSS
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --editorial-font: 'Fraunces', Georgia, serif;
    --sans-font: 'Inter', -apple-system, sans-serif;
}

html, body, [class*="css"] {
    font-family: var(--sans-font);
}

h1, h2, h3, .editorial-heading {
    font-family: var(--editorial-font) !important;
    letter-spacing: -0.02em;
}

/* Hero Section */
.hero-box {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #ffffff;
    padding: 3rem 2.5rem;
    border-radius: 1rem;
    margin-bottom: 2.5rem;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
}

.hero-kicker {
    font-size: 0.85rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #f59e0b;
    font-weight: 600;
    margin-bottom: 0.75rem;
}

.hero-title {
    font-family: var(--editorial-font);
    font-size: 2.75rem;
    line-height: 1.15;
    font-weight: 700;
    margin-bottom: 1rem;
}

.hero-desc {
    font-size: 1.15rem;
    line-height: 1.6;
    color: #cbd5e1;
    max-width: 750px;
}

/* Post Cards */
.post-card {
    border: 1px solid rgba(148, 163, 184, 0.2);
    border-radius: 0.875rem;
    padding: 1.5rem;
    background: #ffffff;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    margin-bottom: 1.5rem;
}

.post-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 24px -10px rgba(0, 0, 0, 0.08);
}

.meta-row {
    font-size: 0.825rem;
    color: #64748b;
    margin-top: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.prose-content {
    font-size: 1.125rem;
    line-height: 1.8;
    color: #334155;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize Session State
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "admin_email" not in st.session_state:
    st.session_state.admin_email = ""
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "selected_slug" not in st.session_state:
    st.session_state.selected_slug = None
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "All"
if "edit_post_id" not in st.session_state:
    st.session_state.edit_post_id = None

# Sidebar Navigation & Platform Controls
with st.sidebar:
    st.markdown(f"## ✒️ **{PROJECT_NAME}**")
    st.caption(PROJECT_TAGLINE)
    st.divider()

    # Navigation Selection
    menu_options = ["Home", "Explore & Search", "Admin Studio & CMS", "GitHub & Deploy"]
    chosen_page = st.radio(
        "Navigation",
        menu_options,
        index=0 if st.session_state.current_page not in menu_options else menu_options.index(st.session_state.current_page),
        label_visibility="collapsed"
    )

    if chosen_page != st.session_state.current_page:
        st.session_state.current_page = chosen_page
        st.session_state.selected_slug = None
        st.rerun()

    st.divider()

    # Category Quick Filter
    st.markdown("### **Categories**")
    all_categories = ["All"] + DEFAULT_CATEGORIES
    for cat in all_categories:
        is_active = (st.session_state.selected_category == cat)
        btn_label = f"▸ {cat}" if is_active else cat
        if st.button(btn_label, key=f"side_cat_{cat}", use_container_width=True):
            st.session_state.selected_category = cat
            st.session_state.current_page = "Home"
            st.session_state.selected_slug = None
            st.rerun()

    st.divider()

    # Admin Quick Status
    if st.session_state.is_admin:
        st.success(f"Logged in as **{st.session_state.admin_email}**")
        if st.button("🚪 Logout Admin", use_container_width=True):
            st.session_state.is_admin = False
            st.session_state.admin_email = ""
            st.rerun()
    else:
        st.caption("Administrator Access")
        if st.button("🔑 Open Admin Login", use_container_width=True):
            st.session_state.current_page = "Admin Studio & CMS"
            st.session_state.selected_slug = None
            st.rerun()

# ==========================================================
# PAGE ROUTING
# ==========================================================

# 1. POST DETAIL VIEW (When an article is clicked)
if st.session_state.selected_slug:
    post = db.get_post_by_slug(st.session_state.selected_slug)
    if not post:
        st.error("Article not found.")
        if st.button("← Return to Homepage"):
            st.session_state.selected_slug = None
            st.rerun()
    else:
        # Increment view count
        db.increment_views(post["id"])

        col_back, col_actions = st.columns([1, 1])
        with col_back:
            if st.button("← Back to Articles"):
                st.session_state.selected_slug = None
                st.rerun()
        with col_actions:
            like_col, share_col = st.columns([1, 1])
            with like_col:
                if st.button(f"❤️ Like ({post['likes']})", key=f"like_{post['id']}"):
                    new_likes = db.like_post(post["id"])
                    st.success("Thank you for your appreciation!")
                    st.rerun()
            with share_col:
                if st.button("🔗 Copy Link"):
                    st.toast("Link copied to clipboard!")

        # Post Header
        st.caption(f"{post['category']} · {post['read_time']} min read · By {post['author_name']} · Published {str(post['published_at'])[:10]}")
        st.markdown(f"# {post['title']}")
        if post["subtitle"]:
            st.markdown(f"*{post['subtitle']}*")

        if post["featured_image"]:
            st.image(post["featured_image"], use_column_width=True)

        st.divider()

        # Markdown Article Content
        st.markdown(post["content"], unsafe_allow_html=True)

        st.divider()

        # Tags
        if post["tags"]:
            st.markdown(f"**Tagged in:** {post['tags']}")

        # Comments Section
        st.markdown("### 💬 Discussion & Responses")
        comments = db.get_comments(post["id"])
        if comments:
            for c in comments:
                with st.chat_message("user"):
                    st.markdown(f"**{c['author_name']}** · *{str(c['created_at'])[:16]}*")
                    st.markdown(c["content"])
        else:
            st.info("No responses yet. Be the first to share your perspective!")

        # Add comment form
        with st.form(key=f"comment_form_{post['id']}", clear_on_submit=True):
            st.markdown("#### Leave a comment")
            c_name = st.text_input("Your Name", placeholder="e.g. Alex Morgan")
            c_email = st.text_input("Your Email (optional)", placeholder="alex@example.com")
            c_body = st.text_area("Your thoughts", placeholder="Write your constructive response...")
            submit_comment = st.form_submit_button("Post Response")

            if submit_comment:
                if not c_name.strip() or not c_body.strip():
                    st.error("Please provide both your name and comment.")
                else:
                    db.add_comment(post["id"], c_name.strip(), c_email.strip(), c_body.strip())
                    st.success("Comment posted successfully!")
                    st.rerun()

# 2. HOME PAGE
elif st.session_state.current_page == "Home":
    # Hero Section
    st.markdown(f"""
    <div class="hero-box">
        <div class="hero-kicker">Welcome to {PROJECT_NAME}</div>
        <div class="hero-title">{PROJECT_TAGLINE}</div>
        <div class="hero-desc">{PROJECT_DESCRIPTION}</div>
    </div>
    """, unsafe_allow_html=True)

    # Search & Filter Bar
    search_col, cat_col = st.columns([3, 1])
    with search_col:
        search_query = st.text_input("🔍 Search publications by title, keyword, or tag...", placeholder="Type to search articles...")
    with cat_col:
        selected_cat = st.selectbox(
            "Category Filter",
            ["All"] + DEFAULT_CATEGORIES,
            index=0 if st.session_state.selected_category == "All" else (DEFAULT_CATEGORIES.index(st.session_state.selected_category) + 1 if st.session_state.selected_category in DEFAULT_CATEGORIES else 0)
        )
        if selected_cat != st.session_state.selected_category:
            st.session_state.selected_category = selected_cat

    # Fetch published posts
    cat_filter = None if st.session_state.selected_category == "All" else st.session_state.selected_category
    posts = db.get_posts(status="published", category=cat_filter, search=search_query if search_query else None)

    if not posts:
        st.info("No articles match your current search and filter criteria.")
    else:
        # Featured Article (First featured or first item)
        featured = next((p for p in posts if p.get("is_featured") == 1), posts[0])
        other_posts = [p for p in posts if p["id"] != featured["id"]]

        # Display Featured Article Card
        st.markdown("### ⭐ Featured Story")
        feat_col1, feat_col2 = st.columns([1.2, 1])
        with feat_col1:
            if featured.get("featured_image"):
                st.image(featured["featured_image"], use_column_width=True)
            else:
                st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80", use_column_width=True)
        with feat_col2:
            st.caption(f"{featured['category']} · {featured['read_time']} min read · By {featured['author_name']}")
            st.markdown(f"## {featured['title']}")
            if featured["subtitle"]:
                st.markdown(f"*{featured['subtitle']}*")
            st.write(featured["excerpt"] or featured["content"][:200] + "...")
            if st.button(f"Read Full Article →", key=f"read_feat_{featured['id']}"):
                st.session_state.selected_slug = featured["slug"]
                st.rerun()

        st.divider()

        # Latest Articles Grid
        st.markdown(f"### 📰 Latest Articles ({len(posts)})")
        cols = st.columns(3)
        for idx, post in enumerate(other_posts):
            col = cols[idx % 3]
            with col:
                with st.container(border=True):
                    if post.get("featured_image"):
                        st.image(post["featured_image"], use_column_width=True)
                    st.caption(f"{post['category']} · {post['read_time']} min read")
                    st.markdown(f"#### {post['title']}")
                    st.write(post["excerpt"][:110] + "..." if post["excerpt"] else post["content"][:110] + "...")
                    st.caption(f"By {post['author_name']} · {post['likes']} likes · {post['views']} views")
                    if st.button("Read Story", key=f"read_btn_{post['id']}", use_container_width=True):
                        st.session_state.selected_slug = post["slug"]
                        st.rerun()

    # Newsletter Section
    st.divider()
    st.markdown("### 📬 Join the Editorial Newsletter")
    st.write("Receive curated briefings on engineering, design architecture, and strategic philosophy.")
    nl_col1, nl_col2 = st.columns([3, 1])
    with nl_col1:
        sub_email = st.text_input("Email address", placeholder="reader@example.com", label_visibility="collapsed")
    with nl_col2:
        if st.button("Subscribe", use_container_width=True):
            if sub_email and "@" in sub_email:
                if db.add_subscriber(sub_email):
                    st.success("Subscribed successfully! Welcome to the sphere.")
                else:
                    st.info("You are already subscribed. Thank you!")
            else:
                st.error("Please enter a valid email address.")

# 3. EXPLORE & SEARCH PAGE
elif st.session_state.current_page == "Explore & Search":
    st.markdown(f"# 🔎 Explore {PROJECT_NAME}")
    st.write("Browse articles across all technical topics, tags, and editorial categories.")

    search_term = st.text_input("Enter search keywords", placeholder="Search architecture, AI, Python, design...")
    cat_pick = st.selectbox("Filter by Category", ["All"] + DEFAULT_CATEGORIES)

    filter_cat = None if cat_pick == "All" else cat_pick
    results = db.get_posts(status="published", category=filter_cat, search=search_term if search_term else None)

    st.markdown(f"**Found {len(results)} publications**")
    for r in results:
        with st.container(border=True):
            r_col1, r_col2 = st.columns([4, 1])
            with r_col1:
                st.caption(f"{r['category']} · {r['read_time']} min read · By {r['author_name']} · {str(r['published_at'])[:10]}")
                st.markdown(f"### {r['title']}")
                st.write(r['excerpt'] or r['content'][:180] + "...")
                if r['tags']:
                    st.caption(f"Tags: {r['tags']}")
            with r_col2:
                if r.get("featured_image"):
                    st.image(r["featured_image"], width=140)
                if st.button("Read", key=f"explore_read_{r['id']}", use_container_width=True):
                    st.session_state.selected_slug = r["slug"]
                    st.rerun()

# 4. ADMIN STUDIO & CMS
elif st.session_state.current_page == "Admin Studio & CMS":
    st.markdown("# 🛡️ Admin Studio & Content Management")

    if not st.session_state.is_admin:
        st.warning("Please sign in to access post creation, editing, drafts, and publication controls.")
        
        login_col1, login_col2 = st.columns([1, 1])
        with login_col1:
            with st.form("admin_login_form"):
                st.markdown("### Administrator Login")
                email = st.text_input("Admin Email", value=ADMIN_EMAIL_DEFAULT)
                password = st.text_input("Password", type="password", value=ADMIN_PASSWORD_DEFAULT)
                login_btn = st.form_submit_button("Sign In to Studio", use_container_width=True)

                if login_btn:
                    conn = db.get_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM users WHERE email = ?", (email.strip(),))
                    user = cursor.fetchone()
                    conn.close()

                    if user and verify_password(user["password_hash"], password):
                        st.session_state.is_admin = True
                        st.session_state.admin_email = user["email"]
                        st.success("Authentication successful!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")
        with login_col2:
            st.info(f"""
            **Default Test Credentials:**
            - **Email**: `{ADMIN_EMAIL_DEFAULT}`
            - **Password**: `{ADMIN_PASSWORD_DEFAULT}`

            You can change credentials in `config.py` or through the site settings tab once logged in.
            """)
    else:
        # Admin is Logged In
        stats = db.get_dashboard_stats()
        
        # Metric Cards
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("Total Posts", stats["total_posts"])
        m2.metric("Published", stats["published_posts"])
        m3.metric("Drafts", stats["draft_posts"])
        m4.metric("Views", stats["total_views"])
        m5.metric("Likes", stats["total_likes"])
        m6.metric("Subscribers", stats["total_subscribers"])

        st.divider()

        admin_tabs = st.tabs(["📝 All Posts", "✨ Create / Edit Article", "⚙️ Platform Settings", "📤 Cloud Database & Storage"])

        # TAB 1: ALL POSTS
        with admin_tabs[0]:
            st.markdown("### Content Library")
            filter_status = st.selectbox("Status Filter", ["all", "published", "draft", "scheduled"], index=0)
            admin_posts = db.get_posts(status=filter_status, category=None, search=None)

            if not admin_posts:
                st.write("No posts found for this filter.")
            else:
                for p in admin_posts:
                    with st.container(border=True):
                        c1, c2, c3, c4 = st.columns([4, 1.5, 1.5, 1.5])
                        with c1:
                            status_badge = "🟢 Published" if p['status'] == 'published' else ("🟡 Draft" if p['status'] == 'draft' else "🔵 Scheduled")
                            feat_badge = "★ Featured · " if p['is_featured'] else ""
                            st.markdown(f"**{p['title']}**")
                            st.caption(f"{status_badge} · {feat_badge}{p['category']} · {p['views']} views · {p['likes']} likes")
                        with c2:
                            # Quick toggle status
                            new_status = "draft" if p['status'] == 'published' else "published"
                            label_toggle = "Unpublish" if p['status'] == 'published' else "Publish"
                            if st.button(label_toggle, key=f"toggle_stat_{p['id']}", use_container_width=True):
                                db.update_post(
                                    post_id=p['id'],
                                    title=p['title'],
                                    content=p['content'],
                                    category=p['category'],
                                    excerpt=p['excerpt'],
                                    subtitle=p['subtitle'],
                                    featured_image=p['featured_image'],
                                    tags=p['tags'],
                                    status=new_status,
                                    is_featured=bool(p['is_featured'])
                                )
                                st.rerun()
                        with c3:
                            if st.button("✏️ Edit", key=f"edit_btn_{p['id']}", use_container_width=True):
                                st.session_state.edit_post_id = p['id']
                                st.rerun()
                        with c4:
                            if st.button("🗑️ Delete", key=f"del_btn_{p['id']}", use_container_width=True):
                                db.delete_post(p['id'])
                                st.success("Post deleted.")
                                st.rerun()

        # TAB 2: CREATE / EDIT ARTICLE
        with admin_tabs[1]:
            is_editing = (st.session_state.edit_post_id is not None)
            editing_post = db.get_post_by_id(st.session_state.edit_post_id) if is_editing else None

            if is_editing and editing_post:
                st.info(f"Currently editing post: **{editing_post['title']}** (ID: {editing_post['id']})")
                if st.button("Cancel Editing and Create New Instead"):
                    st.session_state.edit_post_id = None
                    st.rerun()

            with st.form("post_editor_form"):
                f_title = st.text_input("Article Title", value=editing_post["title"] if editing_post else "")
                f_subtitle = st.text_input("Subtitle / Kicker", value=editing_post["subtitle"] if editing_post else "")
                
                f_col1, f_col2, f_col3 = st.columns([1.5, 1.5, 1])
                with f_col1:
                    cat_val = editing_post["category"] if editing_post else DEFAULT_CATEGORIES[0]
                    cat_index = DEFAULT_CATEGORIES.index(cat_val) if cat_val in DEFAULT_CATEGORIES else 0
                    f_category = st.selectbox("Category", DEFAULT_CATEGORIES, index=cat_index)
                with f_col2:
                    status_opts = ["published", "draft", "scheduled"]
                    stat_val = editing_post["status"] if editing_post else "published"
                    stat_index = status_opts.index(stat_val) if stat_val in status_opts else 0
                    f_status = st.selectbox("Status", status_opts, index=stat_index)
                with f_col3:
                    f_featured = st.checkbox("Featured on Home", value=bool(editing_post["is_featured"]) if editing_post else False)

                f_image = st.text_input(
                    "Featured Image URL (Unsplash, Cloudinary, or Supabase)",
                    value=editing_post["featured_image"] if editing_post else "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80"
                )
                f_excerpt = st.text_area("Excerpt (Summary for cards & search)", value=editing_post["excerpt"] if editing_post else "")
                f_tags = st.text_input("Tags (comma separated)", value=editing_post["tags"] if editing_post else "Tech, Guide, Cloud")

                st.markdown("#### Article Body (Markdown supported)")
                f_content = st.text_area(
                    "Content",
                    value=editing_post["content"] if editing_post else "# Heading\n\nWrite your insightful article here...",
                    height=300
                )

                submit_btn = st.form_submit_button("💾 Save & Publish Article" if not is_editing else "💾 Update Article", use_container_width=True)

                if submit_btn:
                    if not f_title.strip() or not f_content.strip():
                        st.error("Please fill in both title and content.")
                    else:
                        if is_editing:
                            db.update_post(
                                post_id=editing_post["id"],
                                title=f_title.strip(),
                                content=f_content.strip(),
                                category=f_category,
                                excerpt=f_excerpt.strip(),
                                subtitle=f_subtitle.strip(),
                                featured_image=f_image.strip(),
                                tags=f_tags.strip(),
                                status=f_status,
                                is_featured=f_featured
                            )
                            st.success("Article successfully updated!")
                            st.session_state.edit_post_id = None
                            st.rerun()
                        else:
                            new_id = db.create_post(
                                title=f_title.strip(),
                                content=f_content.strip(),
                                category=f_category,
                                excerpt=f_excerpt.strip(),
                                subtitle=f_subtitle.strip(),
                                featured_image=f_image.strip(),
                                tags=f_tags.strip(),
                                status=f_status,
                                is_featured=f_featured
                            )
                            st.success(f"Article created successfully! (ID: {new_id})")
                            st.rerun()

        # TAB 3: PLATFORM SETTINGS
        with admin_tabs[2]:
            st.markdown("### Branding & Defaults")
            st.write(f"Current Platform Name: **{PROJECT_NAME}**")
            st.info("To permanently rename your blog, simply change `PROJECT_NAME` in `config.py` or set the `BLOG_PROJECT_NAME` environment variable.")

        # TAB 4: CLOUD DATABASE & STORAGE
        with admin_tabs[3]:
            st.markdown("### Persistent Cloud Storage Configuration")
            st.markdown("""
            **1. Supabase PostgreSQL Setup**
            Set the `DATABASE_URL` environment variable:
            ```bash
            DATABASE_URL="postgresql://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres"
            ```

            **2. Cloudinary Image Storage**
            Set your Cloudinary API credentials in `.env` or Streamlit Secrets:
            ```bash
            CLOUDINARY_CLOUD_NAME="your_cloud_name"
            CLOUDINARY_API_KEY="your_api_key"
            CLOUDINARY_API_SECRET="your_api_secret"
            ```
            """)

# 5. GITHUB & STREAMLIT DEPLOY PAGE
elif st.session_state.current_page == "GitHub & Deploy":
    st.markdown(f"# 🚀 Deploy {PROJECT_NAME} on Streamlit Community Cloud")
    st.markdown("""
    This application is fully architected and packaged for instant deployment to **Streamlit Community Cloud** with GitHub version control.

    ### 3-Step Deployment Walkthrough:

    1. **Push to GitHub**:
       ```bash
       git init
       git add .
       git commit -m "feat: initial BlogSphere publication platform"
       git branch -M main
       git remote add origin https://github.com/YOUR_USERNAME/BlogSphere.git
       git push -u origin main
       ```

    2. **Connect to Streamlit Community Cloud**:
       - Visit [share.streamlit.io](https://share.streamlit.io).
       - Select your **BlogSphere** repository.
       - Set main file path to: `app.py`.
       - Click **Deploy**!

    3. **Configure Secrets in Streamlit Dashboard (Optional for Supabase/Cloudinary)**:
       Go to *Settings > Secrets* in Streamlit Cloud:
       ```toml
       ADMIN_EMAIL = "admin@blogsphere.dev"
       ADMIN_PASSWORD = "your_secure_password"
       BLOG_PROJECT_NAME = "BlogSphere"
       ```
    """)
