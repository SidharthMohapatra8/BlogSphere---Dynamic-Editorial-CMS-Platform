"""
BlogSphere - Central Configuration
Easily customize the project name, branding, and defaults in one place.
"""
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ==========================================
# BRANDING & PLATFORM CONFIGURATION
# (Change PROJECT_NAME here to rebrand anywhere)
# ==========================================
PROJECT_NAME = os.getenv("BLOG_PROJECT_NAME", "BlogSphere")
PROJECT_TAGLINE = os.getenv("BLOG_TAGLINE", "Where thoughts, engineering, and storytelling converge.")
PROJECT_DESCRIPTION = (
    "A premier publication and content management platform engineered "
    "for curious minds, thoughtful writers, and technical storytellers."
)
ADMIN_EMAIL_DEFAULT = os.getenv("ADMIN_EMAIL", "admin@blogsphere.dev")
ADMIN_PASSWORD_DEFAULT = os.getenv("ADMIN_PASSWORD", "admin123")

# Storage options: 'local' (SQLite + Base64/files), 'supabase' (Postgres + Supabase Storage), 'cloudinary'
STORAGE_PROVIDER = os.getenv("STORAGE_PROVIDER", "local")

# Database URL for Supabase PostgreSQL (leave empty for local SQLite)
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Cloudinary configuration (optional)
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "")

# Default editorial categories
DEFAULT_CATEGORIES = [
    "Technology",
    "Design & UI",
    "Engineering",
    "Artificial Intelligence",
    "Architecture",
    "Culture & Work"
]
