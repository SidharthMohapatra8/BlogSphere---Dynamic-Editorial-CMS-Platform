# BlogSphere — 100% Pure Python Editorial & CMS Platform

> A premier publication and dynamic content management platform written in **100% pure Python** for seamless deployment to Streamlit Community Cloud and local environments. Zero JavaScript, zero CSS, zero HTML overhead.

## 🐍 100% Pure Python Stack

This application is built exclusively using Python and native Streamlit widgets:
- **Core App**: `app.py` (Pure Python Streamlit)
- **Database**: `database.py` (SQLite persistent storage with auto-seeding)
- **Security & Auth**: `auth.py` (PBKDF2-HMAC-SHA256 password hashing)
- **Configuration**: `config.py` (Single-point branding and customization)
- **Dependencies**: `requirements.txt`
- **Streamlit Theme**: `.streamlit/config.toml`

---

## 🚀 Running Locally

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/blogsphere.git
cd blogsphere

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch Streamlit
streamlit run app.py
```

---

## ☁️ Streamlit Community Cloud Deployment

1. On GitHub, make sure your repository has:
   - `app.py`
   - `config.py`
   - `database.py`
   - `auth.py`
   - `requirements.txt`
   - `.streamlit/config.toml`
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Connect your GitHub repository.
4. Set Main file path: `app.py`.
5. Click **Deploy**!

---

## 🛡️ Default Administrator Credentials
- **Email**: `admin@blogsphere.dev`
- **Password**: `admin123`
*(Can be changed in `config.py` or updated in the Admin Studio).*
