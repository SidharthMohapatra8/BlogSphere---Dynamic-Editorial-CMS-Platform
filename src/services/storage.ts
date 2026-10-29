import { Post, SiteSettings, Comment, User } from '../types.ts';
import { INITIAL_POSTS, DEFAULT_SETTINGS, INITIAL_COMMENTS } from '../data/initialData.ts';

const STORAGE_KEYS = {
  POSTS: 'blogsphere_posts_v1',
  SETTINGS: 'blogsphere_settings_v1',
  COMMENTS: 'blogsphere_comments_v1',
  SUBSCRIBERS: 'blogsphere_subscribers_v1',
  ADMIN_SESSION: 'blogsphere_admin_session_v1',
  BOOKMARKS: 'blogsphere_bookmarks_v1',
  THEME: 'blogsphere_theme_v1'
};

export const storageService = {
  // POSTS
  getPosts(): Post[] {
    try {
      const data = localStorage.getItem(STORAGE_KEYS.POSTS);
      if (!data) {
        localStorage.setItem(STORAGE_KEYS.POSTS, JSON.stringify(INITIAL_POSTS));
        return INITIAL_POSTS;
      }
      return JSON.parse(data);
    } catch {
      return INITIAL_POSTS;
    }
  },

  savePosts(posts: Post[]) {
    localStorage.setItem(STORAGE_KEYS.POSTS, JSON.stringify(posts));
  },

  getPostBySlug(slug: string): Post | undefined {
    const posts = this.getPosts();
    return posts.find(p => p.slug === slug);
  },

  getPostById(id: string): Post | undefined {
    const posts = this.getPosts();
    return posts.find(p => p.id === id);
  },

  createPost(newPostData: Omit<Post, 'id' | 'createdAt' | 'updatedAt' | 'views' | 'likes'>): Post {
    const posts = this.getPosts();
    const now = new Date().toISOString();
    const id = `post-${Date.now()}`;
    
    // Auto-generate unique slug if duplicate
    let slug = newPostData.slug || newPostData.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
    if (posts.some(p => p.slug === slug)) {
      slug = `${slug}-${Date.now().toString().slice(-4)}`;
    }

    const newPost: Post = {
      ...newPostData,
      id,
      slug,
      views: 0,
      likes: 0,
      createdAt: now,
      updatedAt: now,
      publishedAt: newPostData.publishedAt || now
    };

    posts.unshift(newPost);
    this.savePosts(posts);
    return newPost;
  },

  updatePost(id: string, updates: Partial<Post>): Post | null {
    const posts = this.getPosts();
    const index = posts.findIndex(p => p.id === id);
    if (index === -1) return null;

    posts[index] = {
      ...posts[index],
      ...updates,
      updatedAt: new Date().toISOString()
    };

    this.savePosts(posts);
    return posts[index];
  },

  deletePost(id: string): boolean {
    const posts = this.getPosts();
    const filtered = posts.filter(p => p.id !== id);
    if (filtered.length !== posts.length) {
      this.savePosts(filtered);
      return true;
    }
    return false;
  },

  likePost(id: string): number {
    const posts = this.getPosts();
    const post = posts.find(p => p.id === id);
    if (!post) return 0;
    post.likes = (post.likes || 0) + 1;
    this.savePosts(posts);
    return post.likes;
  },

  incrementViews(id: string) {
    const posts = this.getPosts();
    const post = posts.find(p => p.id === id);
    if (!post) return;
    post.views = (post.views || 0) + 1;
    this.savePosts(posts);
  },

  // COMMENTS
  getComments(postId: string): Comment[] {
    try {
      const data = localStorage.getItem(STORAGE_KEYS.COMMENTS);
      let commentsMap: Record<string, Comment[]> = {};
      if (data) {
        commentsMap = JSON.parse(data);
      } else {
        // Hydrate initial comments
        commentsMap = Object.entries(INITIAL_COMMENTS).reduce((acc, [pid, list]) => {
          acc[pid] = list.map(c => ({
            id: c.id,
            postId: pid,
            authorName: c.authorName,
            content: c.content,
            createdAt: c.createdAt
          }));
          return acc;
        }, {} as Record<string, Comment[]>);
        localStorage.setItem(STORAGE_KEYS.COMMENTS, JSON.stringify(commentsMap));
      }
      return commentsMap[postId] || [];
    } catch {
      return [];
    }
  },

  addComment(postId: string, authorName: string, content: string, authorEmail?: string): Comment {
    const comments = this.getComments(postId);
    const newComment: Comment = {
      id: `comment-${Date.now()}`,
      postId,
      authorName: authorName.trim() || 'Anonymous Reader',
      authorEmail: authorEmail?.trim(),
      content: content.trim(),
      createdAt: new Date().toISOString()
    };
    const updated = [newComment, ...comments];

    try {
      const data = localStorage.getItem(STORAGE_KEYS.COMMENTS);
      const commentsMap = data ? JSON.parse(data) : {};
      commentsMap[postId] = updated;
      localStorage.setItem(STORAGE_KEYS.COMMENTS, JSON.stringify(commentsMap));
    } catch {
      // ignore
    }

    return newComment;
  },

  // SUBSCRIBERS
  getSubscribers(): string[] {
    try {
      const data = localStorage.getItem(STORAGE_KEYS.SUBSCRIBERS);
      return data ? JSON.parse(data) : ['reader@blogsphere.dev'];
    } catch {
      return [];
    }
  },

  addSubscriber(email: string): boolean {
    const subs = this.getSubscribers();
    const clean = email.trim().toLowerCase();
    if (subs.includes(clean)) return false;
    subs.push(clean);
    localStorage.setItem(STORAGE_KEYS.SUBSCRIBERS, JSON.stringify(subs));
    return true;
  },

  // BOOKMARKS
  getBookmarks(): string[] {
    try {
      const data = localStorage.getItem(STORAGE_KEYS.BOOKMARKS);
      return data ? JSON.parse(data) : [];
    } catch {
      return [];
    }
  },

  toggleBookmark(postId: string): boolean {
    const bookmarks = this.getBookmarks();
    const exists = bookmarks.includes(postId);
    const updated = exists ? bookmarks.filter(id => id !== postId) : [...bookmarks, postId];
    localStorage.setItem(STORAGE_KEYS.BOOKMARKS, JSON.stringify(updated));
    return !exists;
  },

  // SETTINGS
  getSettings(): SiteSettings {
    try {
      const data = localStorage.getItem(STORAGE_KEYS.SETTINGS);
      return data ? JSON.parse(data) : DEFAULT_SETTINGS;
    } catch {
      return DEFAULT_SETTINGS;
    }
  },

  saveSettings(settings: SiteSettings) {
    localStorage.setItem(STORAGE_KEYS.SETTINGS, JSON.stringify(settings));
  },

  // ADMIN AUTH
  getAdminSession(): User | null {
    try {
      const data = localStorage.getItem(STORAGE_KEYS.ADMIN_SESSION);
      return data ? JSON.parse(data) : null;
    } catch {
      return null;
    }
  },

  login(email: string, pass: string): User | null {
    // Default credentials matching python config
    if (email.trim().toLowerCase() === 'admin@blogsphere.dev' && pass === 'admin123') {
      const user: User = {
        id: 'usr-admin-1',
        email: 'admin@blogsphere.dev',
        fullName: 'Elena Vance (Admin)',
        role: 'admin'
      };
      localStorage.setItem(STORAGE_KEYS.ADMIN_SESSION, JSON.stringify(user));
      return user;
    }
    return null;
  },

  logout() {
    localStorage.removeItem(STORAGE_KEYS.ADMIN_SESSION);
  },

  // RESET
  resetDefaults() {
    localStorage.setItem(STORAGE_KEYS.POSTS, JSON.stringify(INITIAL_POSTS));
    localStorage.setItem(STORAGE_KEYS.SETTINGS, JSON.stringify(DEFAULT_SETTINGS));
  }
};
