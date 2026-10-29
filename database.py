"""
BlogSphere - Database Module
Supports SQLite for seamless local and Streamlit Community Cloud execution,
with ready-to-use pluggability for Supabase PostgreSQL via DATABASE_URL.
"""
import sqlite3
import os
import datetime
import re
from typing import List, Dict, Any, Optional
from config import DATABASE_URL, ADMIN_EMAIL_DEFAULT, ADMIN_PASSWORD_DEFAULT, DEFAULT_CATEGORIES
from auth import hash_password

DB_PATH = os.path.join(os.path.dirname(__file__), "blogsphere.db")

def get_connection():
    """Returns a database connection (SQLite by default)."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes schema and seeds default data."""
    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'admin',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Posts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        subtitle TEXT,
        slug TEXT UNIQUE NOT NULL,
        content TEXT NOT NULL,
        excerpt TEXT,
        featured_image TEXT,
        category TEXT NOT NULL,
        tags TEXT,
        status TEXT NOT NULL DEFAULT 'published', -- 'draft', 'published', 'scheduled'
        is_featured INTEGER NOT NULL DEFAULT 0,
        read_time INTEGER DEFAULT 5,
        views INTEGER DEFAULT 0,
        likes INTEGER DEFAULT 0,
        scheduled_at TIMESTAMP,
        published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        author_name TEXT DEFAULT 'Editorial Desk'
    );
    """)

    # Comments table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        author_name TEXT NOT NULL,
        author_email TEXT,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE
    );
    """)

    # Newsletter subscribers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscribers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Seed Admin User if none exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (ADMIN_EMAIL_DEFAULT,))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (email, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
            (ADMIN_EMAIL_DEFAULT, hash_password(ADMIN_PASSWORD_DEFAULT), "Elena Vance", "admin")
        )

    # Seed Sample Articles if table empty
    cursor.execute("SELECT COUNT(*) FROM posts")
    if cursor.fetchone()[0] == 0:
        seed_sample_articles(cursor)

    conn.commit()
    conn.close()

def generate_slug(title: str) -> str:
    """Generates a clean URL slug from title."""
    s = title.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s)
    return s.strip('-')

def calculate_read_time(content: str) -> int:
    """Estimates reading time in minutes based on 200 words per minute."""
    words = len(content.split())
    minutes = max(1, round(words / 200))
    return minutes

def seed_sample_articles(cursor):
    sample_posts = [
        (
            "The Architecture of Calm Software: Building for the Next Decade",
            "Why velocity without reflection produces technical debt, and how intentional craftsmanship wins.",
            "the-architecture-of-calm-software",
            """In an industry perpetually infatuated with breakneck iteration and frantic release cadences, a subtle renaissance is taking shape: the philosophy of **Calm Software**.

Calm software does not shout. It does not bombard its practitioners with noisy telemetry or arbitrary notifications. It is predictable, robust, and mathematically sound.

### The True Cost of Ambient Complexity
When engineering teams prioritize speed of keystroke over depth of design, every saved hour at inception incurs tenfold repayment during incident triage. The remedy is not stagnation—it is discipline:

1. **State Isolation**: Decouple transient interaction states from durable domain truth.
2. **Defensive Boundaries**: Validate at the perimeter; trust within the core.
3. **Ergonomic Simplicity**: Choose boring technology when the problem space itself is novel.

> "Simplicity is prerequisite for reliability." — Edsger W. Dijkstra

### Designing for Longevity
As systems age, their survivability depends entirely on their conceptual clarity. When you craft a service today, imagine another engineer inspecting it on a cold Tuesday five years from now. Give them reason to admire your restraint.
""",
            "Why velocity without reflection produces technical debt, and how intentional craftsmanship builds systems that endure for decades.",
            "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1400&q=80",
            "Engineering",
            "Architecture, Systems, Philosophy",
            "published",
            1,
            6,
            1420,
            89,
            "Elena Vance"
        ),
        (
            "Designing Modern Editorial Systems with Streamlit & Python",
            "Merging Python's data supremacy with rapid interactive web applications for publishing.",
            "designing-modern-editorial-systems-with-streamlit-python",
            """For years, building an expressive editorial portal required juggling multiple disparate frameworks: a Python data pipeline on one side and an orchestration of microservices on the other.

With **Streamlit Community Cloud** and modern component architectures, the gap between backend computational depth and elegant human-centered UI has virtually vanished.

### Key Architectural Pillars
- **Single Source of Truth**: Leverage SQLite for zero-configuration local runs and seamless cutover to PostgreSQL in production.
- **Dynamic Content Ingestion**: Markdown editors paired with instant visual diffing allow authors to compose without context-switching.
- **Deterministic Deployment**: A standard `requirements.txt` file and repository sync mean code to production in sixty seconds.

```python
# Minimalist database connection pattern
import sqlite3

def get_db():
    conn = sqlite3.connect('blogsphere.db')
    conn.row_factory = sqlite3.Row
    return conn
```

By decoupling content storage from presentation rendering, our publishing engine stays fast, lightweight, and completely auditable.
""",
            "How to bridge backend computational power with responsive editorial presentation using Python and modern web tooling.",
            "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=1400&q=80",
            "Technology",
            "Python, Streamlit, WebDev",
            "published",
            1,
            4,
            980,
            64,
            "Marcus Reynolds"
        ),
        (
            "Typographic Hierarchy in Contemporary Editorial Design",
            "How proportion, leading, and contrast establish reading rhythm and digital prestige.",
            "typographic-hierarchy-in-contemporary-editorial-design",
            """Typography is not merely the clothing of words; it is the physical architecture of thought on a screen.

When a reader lands on an article, their subconscious evaluates hierarchy before comprehension begins. Are the margins breathing? Does the headline command attention without screaming? Does the drop cap establish an inviting point of entry?

### The Vertical Rhythm Formula
To achieve serene reading rhythm, typography must adhere to consistent proportional scaling:
- **Display Heading**: 40px–56px with tight letter-spacing (`-0.025em`)
- **Body Text**: 17px–19px with generous line-height (`1.7–1.8`)
- **Metadata**: 13px muted, devoid of heavy pill borders to maintain editorial purity.

Notice how classical print newspapers never contained capsule-shaped plastic stickers next to author bylines. They relied on typographic punctuation: quiet mid-dots, em-dashes, and proportional weights.
""",
            "Exploring proportion, leading, and visual contrast to create compelling, reader-first publication interfaces.",
            "https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=1400&q=80",
            "Design & UI",
            "Typography, UI/UX, Editorial",
            "published",
            0,
            5,
            750,
            42,
            "Claire Moreau"
        ),
        (
            "Autonomous Agents and the Evolution of Knowledge Synthesis",
            "Moving beyond chat interfaces into proactive research compilation and continuous indexing.",
            "autonomous-agents-and-the-evolution-of-knowledge-synthesis",
            """The first generation of conversational AI trained users to treat neural networks like query engines. You ask a question; you parse an answer.

The paradigm shifting now is **Autonomous Knowledge Synthesis**: agents that monitor information streams, analyze conflicting hypotheses, and construct comprehensive briefing memos asynchronously.

```
Incoming Telemetry -> Semantic Parser -> Synthesis Graph -> Editorial Publication
```

### The Human in the Synthesis Loop
Rather than replacing editorial insight, autonomous agents amplify domain experts. The editor becomes a curator of synthesis, refining nuances and ensuring that empathy and original perspective remain paramount.
""",
            "How background intelligent synthesis workflows are reshaping how research and technical publications are curated.",
            "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1400&q=80",
            "Artificial Intelligence",
            "AI, Research, Agents",
            "published",
            0,
            7,
            1120,
            78,
            "Elena Vance"
        )
    ]

    for post in sample_posts:
        cursor.execute("""
        INSERT INTO posts (
            title, subtitle, slug, content, excerpt, featured_image,
            category, tags, status, is_featured, read_time, views, likes, author_name
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, post)

def get_posts(status: Optional[str] = 'published', category: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM posts WHERE 1=1"
    params = []

    if status and status != 'all':
        query += " AND status = ?"
        params.append(status)

    if category and category != 'All':
        query += " AND category = ?"
        params.append(category)

    if search:
        query += " AND (title LIKE ? OR content LIKE ? OR tags LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term])

    query += " ORDER BY is_featured DESC, created_at DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    posts = [dict(row) for row in rows]
    conn.close()
    return posts

def get_post_by_slug(slug: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE slug = ?", (slug,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_post_by_id(post_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def create_post(title: str, content: str, category: str, excerpt: str = "",
                subtitle: str = "", featured_image: str = "", tags: str = "",
                status: str = "published", is_featured: bool = False,
                scheduled_at: str = None, author_name: str = "Editorial Desk") -> int:
    conn = get_connection()
    cursor = conn.cursor()
    slug = generate_slug(title)
    
    # Ensure unique slug
    cursor.execute("SELECT id FROM posts WHERE slug = ?", (slug,))
    if cursor.fetchone():
        slug = f"{slug}-{int(datetime.datetime.now().timestamp())}"

    read_time = calculate_read_time(content)
    if not excerpt:
        clean_text = re.sub(r'#+\s+|\*+|_|`+', '', content)
        excerpt = clean_text[:160] + "..." if len(clean_text) > 160 else clean_text

    cursor.execute("""
    INSERT INTO posts (
        title, subtitle, slug, content, excerpt, featured_image,
        category, tags, status, is_featured, read_time, scheduled_at, author_name
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        title, subtitle, slug, content, excerpt, featured_image,
        category, tags, status, 1 if is_featured else 0, read_time, scheduled_at, author_name
    ))
    post_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return post_id

def update_post(post_id: int, title: str, content: str, category: str,
                excerpt: str = "", subtitle: str = "", featured_image: str = "",
                tags: str = "", status: str = "published", is_featured: bool = False,
                scheduled_at: str = None) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    read_time = calculate_read_time(content)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    UPDATE posts SET
        title = ?, subtitle = ?, content = ?, excerpt = ?,
        featured_image = ?, category = ?, tags = ?, status = ?,
        is_featured = ?, read_time = ?, scheduled_at = ?, updated_at = ?
    WHERE id = ?
    """, (
        title, subtitle, content, excerpt, featured_image,
        category, tags, status, 1 if is_featured else 0, read_time,
        scheduled_at, now, post_id
    ))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

def delete_post(post_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

def increment_views(post_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE posts SET views = views + 1 WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()

def like_post(post_id: int) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE posts SET likes = likes + 1 WHERE id = ?", (post_id,))
    conn.commit()
    cursor.execute("SELECT likes FROM posts WHERE id = ?", (post_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def add_comment(post_id: int, author_name: str, author_email: str, content: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO comments (post_id, author_name, author_email, content)
    VALUES (?, ?, ?, ?)
    """, (post_id, author_name, author_email, content))
    comment_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return comment_id

def get_comments(post_id: int) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM comments WHERE post_id = ? ORDER BY created_at DESC
    """, (post_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_subscriber(email: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO subscribers (email) VALUES (?)", (email.strip().lower(),))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def get_dashboard_stats() -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM posts")
    total_posts = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM posts WHERE status = 'published'")
    published_posts = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM posts WHERE status = 'draft'")
    draft_posts = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT category) FROM posts")
    total_categories = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(views), SUM(likes) FROM posts")
    stats = cursor.fetchone()
    total_views = stats[0] or 0
    total_likes = stats[1] or 0

    cursor.execute("SELECT COUNT(*) FROM subscribers")
    total_subscribers = cursor.fetchone()[0]

    conn.close()
    return {
        "total_posts": total_posts,
        "published_posts": published_posts,
        "draft_posts": draft_posts,
        "total_categories": total_categories,
        "total_views": total_views,
        "total_likes": total_likes,
        "total_subscribers": total_subscribers
    }

# Auto-initialize on import
init_db()
