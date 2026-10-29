import { Post, SiteSettings } from '../types.ts';

export const DEFAULT_SETTINGS: SiteSettings = {
  projectName: "BlogSphere",
  tagline: "Where engineering, design architecture, and strategic depth converge.",
  description: "A modern, high-craft publication engineered for developers, architects, and thoughtful creators. Publish dynamically with Python, Streamlit, and GitHub readiness.",
  authorName: "Elena Vance",
  authorBio: "Principal systems architect and editorial writer exploring the intersection of distributed computing, interface craft, and calm software.",
  authorAvatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80",
  categories: [
    "Technology",
    "Design & UI",
    "Engineering",
    "Artificial Intelligence",
    "Architecture",
    "Culture & Work"
  ]
};

export const INITIAL_POSTS: Post[] = [
  {
    id: "post-1",
    title: "The Architecture of Calm Software: Building for the Next Decade",
    subtitle: "Why velocity without reflection produces compounding technical debt, and how intentional craftsmanship wins.",
    slug: "the-architecture-of-calm-software",
    excerpt: "Why velocity without reflection produces compounding technical debt, and how intentional craftsmanship builds systems that endure for decades.",
    category: "Engineering",
    tags: ["Architecture", "Systems", "Philosophy"],
    status: "published",
    isFeatured: true,
    readTime: 6,
    views: 1420,
    likes: 89,
    publishedAt: "2026-10-24T09:00:00Z",
    createdAt: "2026-10-24T09:00:00Z",
    updatedAt: "2026-10-24T09:00:00Z",
    authorName: "Elena Vance",
    authorRole: "Principal Systems Architect",
    authorAvatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80",
    featuredImage: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1400&q=80",
    content: `In an industry perpetually infatuated with breakneck iteration and frantic release cadences, a subtle renaissance is taking shape: the philosophy of **Calm Software**.

Calm software does not shout. It does not bombard its practitioners with noisy telemetry or arbitrary notifications. It is predictable, robust, and mathematically sound.

## The True Cost of Ambient Complexity

When engineering teams prioritize speed of keystroke over depth of design, every saved hour at inception incurs tenfold repayment during incident triage. The remedy is not stagnation—it is discipline:

1. **State Isolation**: Decouple transient interaction states from durable domain truth.
2. **Defensive Boundaries**: Validate at the perimeter; trust within the core.
3. **Ergonomic Simplicity**: Choose boring technology when the problem space itself is novel.

> "Simplicity is prerequisite for reliability." — Edsger W. Dijkstra

## Designing for Longevity

As systems age, their survivability depends entirely on their conceptual clarity. When you craft a service today, imagine another engineer inspecting it on a cold Tuesday five years from now. Give them reason to admire your restraint.

### Practical Tenets for Engineers
- **Strict Data Contracts**: Treat your database schema as a binding civic constitution.
- **Fail Deterministically**: Silent failures cause catastrophic data drift. Crash early with clean error context.
- **Audit Trails**: Real-world operations require clear, tamper-evident histories.

When you refuse the seduction of frantic complexity, you build software that users quietly love.`
  },
  {
    id: "post-2",
    title: "Designing Modern Editorial Systems with Streamlit & Python",
    subtitle: "Merging Python's computational supremacy with rapid interactive web applications for publishing.",
    slug: "designing-modern-editorial-systems-with-streamlit-python",
    excerpt: "How to bridge backend computational power with responsive editorial presentation using Python and modern web tooling.",
    category: "Technology",
    tags: ["Python", "Streamlit", "WebDev"],
    status: "published",
    isFeatured: true,
    readTime: 4,
    views: 980,
    likes: 64,
    publishedAt: "2026-10-26T14:30:00Z",
    createdAt: "2026-10-26T14:30:00Z",
    updatedAt: "2026-10-26T14:30:00Z",
    authorName: "Marcus Reynolds",
    authorRole: "Full-Stack Python Engineer",
    authorAvatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80",
    featuredImage: "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=1400&q=80",
    content: `For years, building an expressive editorial portal required juggling multiple disparate frameworks: a Python data pipeline on one side and an orchestration of microservices on the other.

With **Streamlit Community Cloud** and modern component architectures, the gap between backend computational depth and elegant human-centered UI has virtually vanished.

## Key Architectural Pillars

- **Single Source of Truth**: Leverage SQLite for zero-configuration local runs and seamless cutover to PostgreSQL in production.
- **Dynamic Content Ingestion**: Markdown editors paired with instant visual diffing allow authors to compose without context-switching.
- **Deterministic Deployment**: A standard \`requirements.txt\` file and repository sync mean code to production in sixty seconds.

\`\`\`python
# Minimalist database connection pattern
import sqlite3

def get_db():
    conn = sqlite3.connect('blogsphere.db')
    conn.row_factory = sqlite3.Row
    return conn
\`\`\`

## Streamlit Cloud Deployment Simplicity

By deploying to Streamlit Community Cloud:
1. Push your Git commits to GitHub.
2. Select your repository in Streamlit Cloud.
3. Streamlit automatically boots up the app container, executes requirements, and serves your responsive blog worldwide.

The outcome is an ultra-fast turnaround time from idea to published live platform.`
  },
  {
    id: "post-3",
    title: "Typographic Hierarchy in Contemporary Editorial Design",
    subtitle: "How proportion, leading, and contrast establish reading rhythm and digital prestige.",
    slug: "typographic-hierarchy-in-contemporary-editorial-design",
    excerpt: "Exploring proportion, leading, and visual contrast to create compelling, reader-first publication interfaces.",
    category: "Design & UI",
    tags: ["Typography", "UI/UX", "Editorial"],
    status: "published",
    isFeatured: false,
    readTime: 5,
    views: 750,
    likes: 42,
    publishedAt: "2026-10-27T11:15:00Z",
    createdAt: "2026-10-27T11:15:00Z",
    updatedAt: "2026-10-27T11:15:00Z",
    authorName: "Claire Moreau",
    authorRole: "Editorial Design Lead",
    authorAvatar: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=400&q=80",
    featuredImage: "https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=1400&q=80",
    content: `Typography is not merely the clothing of words; it is the physical architecture of thought on a screen.

When a reader lands on an article, their subconscious evaluates hierarchy before comprehension begins. Are the margins breathing? Does the headline command attention without screaming? Does the drop cap establish an inviting point of entry?

## The Vertical Rhythm Formula

To achieve serene reading rhythm, typography must adhere to consistent proportional scaling:
- **Display Heading**: 40px–56px with tight letter-spacing (\`-0.025em\`)
- **Body Text**: 17px–19px with generous line-height (\`1.7–1.8\`)
- **Metadata**: 13px muted, devoid of heavy pill borders to maintain editorial purity.

Notice how classical print newspapers never contained capsule-shaped plastic stickers next to author bylines. They relied on typographic punctuation: quiet mid-dots, em-dashes, and proportional weights.

### Anti-Slop Discipline
Avoid neon pill badges on your blog cards. Let the headline lead. Let the photograph anchor. The words will do the rest.`
  },
  {
    id: "post-4",
    title: "Autonomous Agents and the Evolution of Knowledge Synthesis",
    subtitle: "Moving beyond chat interfaces into proactive research compilation and continuous indexing.",
    slug: "autonomous-agents-and-the-evolution-of-knowledge-synthesis",
    excerpt: "How background intelligent synthesis workflows are reshaping how research and technical publications are curated.",
    category: "Artificial Intelligence",
    tags: ["AI", "Research", "Agents"],
    status: "published",
    isFeatured: false,
    readTime: 7,
    views: 1120,
    likes: 78,
    publishedAt: "2026-10-28T08:00:00Z",
    createdAt: "2026-10-28T08:00:00Z",
    updatedAt: "2026-10-28T08:00:00Z",
    authorName: "Elena Vance",
    authorRole: "Principal Systems Architect",
    authorAvatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80",
    featuredImage: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1400&q=80",
    content: `The first generation of conversational AI trained users to treat neural networks like query engines. You ask a question; you parse an answer.

The paradigm shifting now is **Autonomous Knowledge Synthesis**: background agents that monitor information streams, analyze conflicting hypotheses, and construct comprehensive briefing memos asynchronously.

\`\`\`
Incoming Telemetry -> Semantic Parser -> Synthesis Graph -> Editorial Publication
\`\`\`

## The Human in the Synthesis Loop

Rather than replacing editorial insight, autonomous agents amplify domain experts. The editor becomes a curator of synthesis, refining nuances and ensuring that empathy and original perspective remain paramount.`
  },
  {
    id: "post-5",
    title: "Building Resilient Offline-First Data Pipelines",
    subtitle: "Strategies for local-first synchronization and conflict-free replicated data types.",
    slug: "building-resilient-offline-first-data-pipelines",
    excerpt: "How to craft applications that guarantee uncompromised performance regardless of network stability.",
    category: "Architecture",
    tags: ["CRDT", "LocalFirst", "Databases"],
    status: "draft",
    isFeatured: false,
    readTime: 8,
    views: 0,
    likes: 0,
    publishedAt: "2026-10-29T10:00:00Z",
    createdAt: "2026-10-29T10:00:00Z",
    updatedAt: "2026-10-29T10:00:00Z",
    authorName: "Marcus Reynolds",
    authorRole: "Full-Stack Python Engineer",
    authorAvatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80",
    featuredImage: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1400&q=80",
    content: `Draft in progress. Examining SQLite as an edge storage buffer with background sync to PostgreSQL.`
  }
];

export const INITIAL_COMMENTS: Record<string, Array<{ id: string; authorName: string; createdAt: string; content: string }>> = {
  "post-1": [
    {
      id: "c-1",
      authorName: "Sarah Lin",
      createdAt: "2026-10-25T11:20:00Z",
      content: "This perspective on Calm Software resonates deeply. We spent the last quarter removing unnecessary alerting micro-tools and our incident recovery time actually improved."
    },
    {
      id: "c-2",
      authorName: "David K.",
      createdAt: "2026-10-26T16:45:00Z",
      content: "The quote by Dijkstra is timeless. Simplicity requires so much more courage than adding another dependency."
    }
  ],
  "post-2": [
    {
      id: "c-3",
      authorName: "Julian Vance",
      createdAt: "2026-10-27T10:15:00Z",
      content: "Deploying Python apps directly via Streamlit Cloud has transformed how quickly our research group ships technical briefings."
    }
  ]
};
