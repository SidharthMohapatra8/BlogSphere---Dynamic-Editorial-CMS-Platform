# BlogSphere — Modern Dynamic Editorial & CMS Platform

> A premium, dynamic blogging platform and content management system engineered for publishing on GitHub and deploying on Streamlit Community Cloud.

![BlogSphere Banner](https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1400&q=80)

## Features

- **Editorial-Grade Design**: Clean typography (Fraunces & Inter), zero visual clutter, unboxed quiet metadata, reading time estimation, and drop caps.
- **Dynamic Content Management (CMS)**:
  - Create, edit, and delete articles dynamically without code changes.
  - Save drafts, schedule posts, or publish immediately.
  - URL slug generation, tag indexing, category classification, and featured article pinned state.
  - Markdown editor with live preview and code syntax formatting.
- **Interactive Reader Experience**:
  - Live search across titles, content, and tags.
  - Interactive category filtering.
  - Real reader comments with persistence.
  - Like button counters and view tracking.
  - Newsletter subscription management.
- **Secure Administrator Studio**:
  - Password hashing with PBKDF2-HMAC-SHA256 and salt.
  - Protected CMS routes and metrics (Total Posts, Views, Likes, Subscribers).
  - Default credentials: `admin@blogsphere.dev` / `admin123`.
- **Hybrid Database & Cloud Storage**:
  - **Local**: Zero-configuration SQLite (`blogsphere.db`).
  - **Production**: 1-click connect to Supabase PostgreSQL via `DATABASE_URL`.
  - **Media**: Native image URL support + Cloudinary and Supabase Storage support.

---

## 🚀 Quickstart (Streamlit Community Cloud or Local)

### 1. Local Run with Python
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/blogsphere.git
cd blogsphere

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch BlogSphere
streamlit run app.py
```

### 2. Deploy to Streamlit Community Cloud in 60 Seconds
1. Push this repository to GitHub:
   ```bash
   git add .
   git commit -m "feat: initial BlogSphere platform"
   git push origin main
   ```
2. Navigate to [share.streamlit.io](https://share.streamlit.io).
3. Connect your GitHub account and select your **BlogSphere** repository.
4. Set Main file path to: `app.py`.
5. *(Optional)* Add secrets under **App Settings > Secrets**:
   ```toml
   ADMIN_EMAIL = "admin@blogsphere.dev"
   ADMIN_PASSWORD = "your_secure_password"
   BLOG_PROJECT_NAME = "BlogSphere"
   DATABASE_URL = "postgresql://postgres:password@db.ref.supabase.co:5432/postgres"
   ```
6. Click **Deploy**!

---

## 🎨 Changing the Platform Name
To rebrand the platform, change `PROJECT_NAME` in `config.py` or provide the `BLOG_PROJECT_NAME` environment variable. All page titles, footers, and headers update automatically.

---

## 🛡️ Default Administrator Credentials
- **Email**: `admin@blogsphere.dev`
- **Password**: `admin123`
*(Can be changed in `config.py` or updated in the Admin Studio).*

---

## 📄 License
MIT License. Built with passion for writers and engineers.
