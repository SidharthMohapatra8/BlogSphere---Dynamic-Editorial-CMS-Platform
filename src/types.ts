export type PostStatus = 'published' | 'draft' | 'scheduled';

export interface Comment {
  id: string;
  postId: string;
  authorName: string;
  authorEmail?: string;
  content: string;
  createdAt: string;
}

export interface Post {
  id: string;
  title: string;
  subtitle?: string;
  slug: string;
  content: string;
  excerpt: string;
  featuredImage: string;
  category: string;
  tags: string[];
  status: PostStatus;
  isFeatured: boolean;
  readTime: number; // minutes
  views: number;
  likes: number;
  publishedAt: string;
  scheduledAt?: string;
  createdAt: string;
  updatedAt: string;
  authorName: string;
  authorRole?: string;
  authorAvatar?: string;
}

export interface User {
  id: string;
  email: string;
  fullName: string;
  role: 'admin' | 'editor';
}

export interface SiteSettings {
  projectName: string;
  tagline: string;
  description: string;
  authorName: string;
  authorBio: string;
  authorAvatar: string;
  categories: string[];
}
