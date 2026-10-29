import React, { useState, useEffect } from 'react';
import { 
  ArrowLeft, 
  Heart, 
  Bookmark, 
  Share2, 
  Clock, 
  Calendar, 
  MessageSquare, 
  Send, 
  Check, 
  Eye,
  Type,
  List
} from 'lucide-react';
import { Post, Comment } from '../types.ts';
import { storageService } from '../services/storage.ts';

interface PostDetailProps {
  post: Post;
  onBack: () => void;
  onPostUpdated: (updatedPost: Post) => void;
  onReadPost: (slug: string) => void;
  allPosts: Post[];
  onShowToast: (msg: string) => void;
}

export const PostDetail: React.FC<PostDetailProps> = ({
  post,
  onBack,
  onPostUpdated,
  onReadPost,
  allPosts,
  onShowToast
}) => {
  const [likes, setLikes] = useState(post.likes);
  const [hasLiked, setHasLiked] = useState(false);
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [comments, setComments] = useState<Comment[]>([]);
  const [commentName, setCommentName] = useState('');
  const [commentEmail, setCommentEmail] = useState('');
  const [commentText, setCommentText] = useState('');
  const [fontSize, setFontSize] = useState<'normal' | 'large' | 'huge'>('normal');
  const [scrollProgress, setScrollProgress] = useState(0);

  // Load comments & bookmark status on mount
  useEffect(() => {
    // Record view
    storageService.incrementViews(post.id);
    setComments(storageService.getComments(post.id));
    const bookmarks = storageService.getBookmarks();
    setIsBookmarked(bookmarks.includes(post.id));

    // Scroll progress handler
    const handleScroll = () => {
      const totalScroll = document.documentElement.scrollTop;
      const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      if (windowHeight > 0) {
        setScrollProgress(Math.min(100, Math.max(0, (totalScroll / windowHeight) * 100)));
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, [post.id]);

  // Handle Like
  const handleLike = () => {
    if (hasLiked) return;
    const newCount = storageService.likePost(post.id);
    setLikes(newCount);
    setHasLiked(true);
    onPostUpdated({ ...post, likes: newCount });
    onShowToast("Thank you for supporting this story!");
  };

  // Handle Bookmark
  const handleBookmark = () => {
    const isNowBookmarked = storageService.toggleBookmark(post.id);
    setIsBookmarked(isNowBookmarked);
    onShowToast(isNowBookmarked ? "Article saved to bookmarks" : "Article removed from bookmarks");
  };

  // Handle Share
  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href);
    onShowToast("Story URL copied to clipboard!");
  };

  // Handle Add Comment
  const handleCommentSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!commentText.trim()) return;

    const newComment = storageService.addComment(
      post.id,
      commentName.trim() || 'Reader',
      commentText.trim(),
      commentEmail.trim()
    );

    setComments(prev => [newComment, ...prev]);
    setCommentText('');
    setCommentName('');
    setCommentEmail('');
    onShowToast("Your response has been published.");
  };

  // Extract headings for Table of Contents
  const headings = post.content
    .split('\n')
    .filter(line => line.startsWith('## ') || line.startsWith('### '))
    .map(line => {
      const level = line.startsWith('### ') ? 3 : 2;
      const text = line.replace(/^#{2,3}\s+/, '').trim();
      const id = text.toLowerCase().replace(/[^a-z0-9]+/g, '-');
      return { text, id, level };
    });

  const formattedDate = new Date(post.publishedAt || post.createdAt).toLocaleDateString('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric'
  });

  // Render markdown parser
  const renderMarkdown = (content: string) => {
    const paragraphs = content.split('\n\n');
    return paragraphs.map((block, idx) => {
      const trimmed = block.trim();
      if (!trimmed) return null;

      // H2
      if (trimmed.startsWith('## ')) {
        const text = trimmed.replace(/^##\s+/, '');
        const id = text.toLowerCase().replace(/[^a-z0-9]+/g, '-');
        return (
          <h2 key={idx} id={id} className="font-editorial text-2xl sm:text-3xl font-bold tracking-tight text-stone-900 dark:text-stone-100 mt-10 mb-4 pt-4 border-t border-stone-200/60 dark:border-stone-800/60">
            {text}
          </h2>
        );
      }

      // H3
      if (trimmed.startsWith('### ')) {
        const text = trimmed.replace(/^###\s+/, '');
        const id = text.toLowerCase().replace(/[^a-z0-9]+/g, '-');
        return (
          <h3 key={idx} id={id} className="font-editorial text-xl font-bold text-stone-800 dark:text-stone-200 mt-6 mb-3">
            {text}
          </h3>
        );
      }

      // Blockquote
      if (trimmed.startsWith('> ')) {
        const text = trimmed.replace(/^>\s+/, '');
        return (
          <blockquote key={idx} className="border-l-4 border-amber-500 pl-5 py-1.5 my-6 italic text-lg text-stone-700 dark:text-stone-300 bg-amber-50/40 dark:bg-amber-950/20 rounded-r-lg">
            {text}
          </blockquote>
        );
      }

      // Code Block
      if (trimmed.startsWith('```')) {
        const lines = trimmed.split('\n');
        const codeLines = lines.slice(1, -1).join('\n');
        return (
          <pre key={idx} className="font-mono bg-stone-900 text-stone-100 p-5 rounded-xl overflow-x-auto my-6 text-sm leading-relaxed border border-stone-800">
            <code>{codeLines}</code>
          </pre>
        );
      }

      // Ordered or Unordered Lists
      if (trimmed.match(/^(\d+\.|\-|\*)\s+/)) {
        const items = trimmed.split('\n').filter(Boolean);
        const isOrdered = /^\d+\./.test(items[0]);
        return isOrdered ? (
          <ol key={idx} className="list-decimal pl-6 my-4 space-y-2 text-stone-700 dark:text-stone-300">
            {items.map((it, i) => (
              <li key={i}>{it.replace(/^\d+\.\s+/, '')}</li>
            ))}
          </ol>
        ) : (
          <ul key={idx} className="list-disc pl-6 my-4 space-y-2 text-stone-700 dark:text-stone-300">
            {items.map((it, i) => (
              <li key={i}>{it.replace(/^[-*]\s+/, '')}</li>
            ))}
          </ul>
        );
      }

      // First paragraph has a drop cap for editorial flair
      const isFirstParagraph = idx === 0;

      return (
        <p 
          key={idx} 
          className={`leading-relaxed text-stone-700 dark:text-stone-300 my-5 font-normal ${
            isFirstParagraph ? 'drop-cap text-lg' : ''
          }`}
        >
          {trimmed}
        </p>
      );
    });
  };

  // Related posts
  const relatedPosts = allPosts
    .filter(p => p.id !== post.id && p.status === 'published' && p.category === post.category)
    .slice(0, 2);

  const fontSizeClass = {
    normal: 'text-base sm:text-lg',
    large: 'text-lg sm:text-xl',
    huge: 'text-xl sm:text-2xl'
  }[fontSize];

  return (
    <article className="min-h-screen pb-24">
      {/* Scroll Progress Bar */}
      <div 
        className="fixed top-0 left-0 h-1 bg-amber-500 z-50 transition-all duration-150"
        style={{ width: `${scrollProgress}%` }}
      />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pt-8">
        {/* Navigation Bar / Reading Controls */}
        <div className="flex items-center justify-between py-4 mb-8 border-b border-stone-200/80 dark:border-stone-800">
          <button
            onClick={onBack}
            className="inline-flex items-center gap-2 text-xs font-semibold text-stone-600 dark:text-stone-400 hover:text-stone-950 dark:hover:text-white transition-colors py-1.5 px-2.5 rounded-lg hover:bg-stone-100 dark:hover:bg-stone-800"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>All Articles</span>
          </button>

          {/* Reading Customization Controls */}
          <div className="flex items-center gap-2">
            {/* Font Size Adjuster */}
            <div className="flex items-center bg-stone-100 dark:bg-stone-800 p-0.5 rounded-lg text-xs">
              <button
                onClick={() => setFontSize('normal')}
                className={`px-2 py-1 rounded font-medium transition-colors ${fontSize === 'normal' ? 'bg-white dark:bg-stone-700 text-stone-900 dark:text-white shadow-xs' : 'text-stone-500'}`}
                title="Normal font size"
              >
                A
              </button>
              <button
                onClick={() => setFontSize('large')}
                className={`px-2 py-1 rounded font-medium transition-colors ${fontSize === 'large' ? 'bg-white dark:bg-stone-700 text-stone-900 dark:text-white shadow-xs' : 'text-stone-500'}`}
                title="Large font size"
              >
                A+
              </button>
            </div>

            {/* Bookmark button */}
            <button
              onClick={handleBookmark}
              className={`p-2 rounded-lg text-stone-600 dark:text-stone-300 hover:bg-stone-100 dark:hover:bg-stone-800 transition-colors ${isBookmarked ? 'text-amber-600 dark:text-amber-400' : ''}`}
              title={isBookmarked ? "Bookmarked" : "Bookmark article"}
            >
              <Bookmark className={`w-4 h-4 ${isBookmarked ? 'fill-current' : ''}`} />
            </button>

            {/* Share button */}
            <button
              onClick={handleShare}
              className="p-2 rounded-lg text-stone-600 dark:text-stone-300 hover:bg-stone-100 dark:hover:bg-stone-800 transition-colors"
              title="Copy link"
            >
              <Share2 className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Article Header */}
        <header className="mb-10 text-center max-w-3xl mx-auto">
          {/* Unboxed Metadata (Zero-Pill Rule) */}
          <div className="flex items-center justify-center gap-2 text-xs font-medium text-stone-500 dark:text-stone-400 mb-4 tracking-wide uppercase">
            <span className="text-amber-700 dark:text-amber-400">{post.category}</span>
            <span aria-hidden="true">·</span>
            <span>{post.readTime} min read</span>
            <span aria-hidden="true">·</span>
            <span>{formattedDate}</span>
          </div>

          <h1 className="font-editorial text-3xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-stone-900 dark:text-stone-50 mb-6 leading-[1.12]">
            {post.title}
          </h1>

          {post.subtitle && (
            <p className="font-editorial text-lg sm:text-2xl text-stone-600 dark:text-stone-300 italic mb-8 max-w-2xl mx-auto leading-relaxed">
              {post.subtitle}
            </p>
          )}

          {/* Author Byline */}
          <div className="inline-flex items-center gap-3 py-3 px-4 rounded-xl bg-stone-100/70 dark:bg-stone-900/60 border border-stone-200/60 dark:border-stone-800">
            {post.authorAvatar ? (
              <img src={post.authorAvatar} alt={post.authorName} className="w-10 h-10 rounded-full object-cover ring-2 ring-stone-200 dark:ring-stone-700" />
            ) : (
              <div className="w-10 h-10 rounded-full bg-amber-600 text-white flex items-center justify-center font-bold text-sm">
                {post.authorName.charAt(0)}
              </div>
            )}
            <div className="text-left">
              <div className="text-sm font-semibold text-stone-900 dark:text-stone-100">{post.authorName}</div>
              <div className="text-xs text-stone-500 dark:text-stone-400">{post.authorRole || 'Editorial Desk'}</div>
            </div>
          </div>
        </header>

        {/* Featured Banner Image */}
        {post.featuredImage && (
          <div className="mb-12 rounded-2xl overflow-hidden shadow-md border border-stone-200/70 dark:border-stone-800">
            <img
              src={post.featuredImage}
              alt={post.title}
              className="w-full h-auto max-h-[550px] object-cover"
            />
          </div>
        )}

        {/* Table of Contents (if multi-heading) */}
        {headings.length > 1 && (
          <nav className="mb-10 p-5 rounded-xl bg-amber-50/50 dark:bg-stone-900/50 border border-amber-200/50 dark:border-stone-800">
            <div className="flex items-center gap-2 text-xs font-semibold text-amber-900 dark:text-amber-400 uppercase tracking-wider mb-3">
              <List className="w-3.5 h-3.5" />
              <span>Table of Contents</span>
            </div>
            <ul className="space-y-1.5 text-sm">
              {headings.map((h, i) => (
                <li key={i} className={h.level === 3 ? 'pl-4' : ''}>
                  <a 
                    href={`#${h.id}`}
                    className="text-stone-600 dark:text-stone-300 hover:text-amber-600 dark:hover:text-amber-400 transition-colors"
                  >
                    {h.text}
                  </a>
                </li>
              ))}
            </ul>
          </nav>
        )}

        {/* Article Body Content */}
        <div className={`prose-editorial ${fontSizeClass}`}>
          {renderMarkdown(post.content)}
        </div>

        {/* Tags */}
        {post.tags && post.tags.length > 0 && (
          <div className="mt-12 pt-6 border-t border-stone-200 dark:border-stone-800 flex flex-wrap items-center gap-2">
            <span className="text-xs text-stone-500 font-medium">Topics:</span>
            {post.tags.map((tag, i) => (
              <span key={i} className="text-xs text-stone-600 dark:text-stone-400 bg-stone-100 dark:bg-stone-800 px-2.5 py-1 rounded-md">
                #{tag.trim()}
              </span>
            ))}
          </div>
        )}

        {/* Appreciation & Action Bar */}
        <div className="my-10 p-6 rounded-2xl bg-stone-100/80 dark:bg-stone-900/60 border border-stone-200/80 dark:border-stone-800 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <button
              onClick={handleLike}
              disabled={hasLiked}
              className={`inline-flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold transition-all shadow-xs ${
                hasLiked 
                  ? 'bg-rose-100 text-rose-700 dark:bg-rose-950/40 dark:text-rose-400' 
                  : 'bg-white dark:bg-stone-800 text-stone-800 dark:text-stone-200 hover:bg-rose-50 dark:hover:bg-rose-950/30 hover:text-rose-600'
              }`}
            >
              <Heart className={`w-4 h-4 ${hasLiked ? 'fill-current text-rose-600' : ''}`} />
              <span>{likes} {likes === 1 ? 'Appreciation' : 'Appreciations'}</span>
            </button>

            <span className="text-xs text-stone-500 flex items-center gap-1.5">
              <Eye className="w-3.5 h-3.5" />
              <span>{post.views} reads</span>
            </span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleShare}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-medium text-stone-700 dark:text-stone-200 bg-white dark:bg-stone-800 rounded-xl hover:bg-stone-200/60 dark:hover:bg-stone-700 transition-colors shadow-xs"
            >
              <Share2 className="w-3.5 h-3.5" />
              <span>Share Publication</span>
            </button>
          </div>
        </div>

        {/* Author Bio Box */}
        <div className="my-12 p-6 rounded-2xl bg-white dark:bg-stone-900/80 border border-stone-200 dark:border-stone-800 flex flex-col sm:flex-row items-center sm:items-start gap-5">
          {post.authorAvatar ? (
            <img src={post.authorAvatar} alt={post.authorName} className="w-16 h-16 rounded-full object-cover ring-4 ring-amber-500/20" />
          ) : (
            <div className="w-16 h-16 rounded-full bg-amber-600 text-white flex items-center justify-center font-bold text-xl">
              {post.authorName.charAt(0)}
            </div>
          )}
          <div className="text-center sm:text-left flex-1">
            <div className="text-xs uppercase tracking-wider font-semibold text-amber-700 dark:text-amber-400 mb-1">About the Author</div>
            <h4 className="font-editorial text-lg font-bold text-stone-900 dark:text-stone-100">{post.authorName}</h4>
            <p className="text-sm text-stone-600 dark:text-stone-300 mt-1 leading-relaxed">
              Writer and contributor at BlogSphere specializing in software architecture, resilient engineering, and editorial systems.
            </p>
          </div>
        </div>

        {/* Discussion & Responses Section */}
        <section className="mt-14 pt-10 border-t border-stone-200 dark:border-stone-800">
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center gap-2">
              <MessageSquare className="w-5 h-5 text-amber-600" />
              <h3 className="font-editorial text-2xl font-bold text-stone-900 dark:text-stone-100">
                Responses ({comments.length})
              </h3>
            </div>
          </div>

          {/* Add Comment Form */}
          <form onSubmit={handleCommentSubmit} className="mb-10 p-5 rounded-2xl bg-stone-100/70 dark:bg-stone-900/60 border border-stone-200/80 dark:border-stone-800">
            <h4 className="text-sm font-semibold text-stone-900 dark:text-stone-100 mb-3">Add your perspective</h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-3">
              <input
                type="text"
                placeholder="Your Name (e.g., Alex Reed)"
                value={commentName}
                onChange={e => setCommentName(e.target.value)}
                className="w-full text-sm px-3.5 py-2.5 rounded-xl bg-white dark:bg-stone-800 border border-stone-300 dark:border-stone-700 text-stone-900 dark:text-white placeholder-stone-400 focus:outline-none focus:ring-2 focus:ring-amber-500"
              />
              <input
                type="email"
                placeholder="Your Email (optional, not published)"
                value={commentEmail}
                onChange={e => setCommentEmail(e.target.value)}
                className="w-full text-sm px-3.5 py-2.5 rounded-xl bg-white dark:bg-stone-800 border border-stone-300 dark:border-stone-700 text-stone-900 dark:text-white placeholder-stone-400 focus:outline-none focus:ring-2 focus:ring-amber-500"
              />
            </div>
            <textarea
              required
              rows={3}
              placeholder="What are your thoughts on this story? Polite and constructive discourse is welcome."
              value={commentText}
              onChange={e => setCommentText(e.target.value)}
              className="w-full text-sm p-3.5 rounded-xl bg-white dark:bg-stone-800 border border-stone-300 dark:border-stone-700 text-stone-900 dark:text-white placeholder-stone-400 focus:outline-none focus:ring-2 focus:ring-amber-500 mb-3 resize-y"
            />
            <div className="flex justify-end">
              <button
                type="submit"
                className="inline-flex items-center gap-2 px-5 py-2 text-xs font-semibold text-white bg-amber-600 hover:bg-amber-700 rounded-xl transition-colors shadow-sm"
              >
                <Send className="w-3.5 h-3.5" />
                <span>Submit Response</span>
              </button>
            </div>
          </form>

          {/* Comment List */}
          <div className="space-y-4">
            {comments.length === 0 ? (
              <p className="text-sm text-stone-500 italic py-4">No comments yet. Be the first to start the conversation.</p>
            ) : (
              comments.map(c => (
                <div key={c.id} className="p-4 rounded-xl bg-white dark:bg-stone-900 border border-stone-200/70 dark:border-stone-800">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-semibold text-stone-900 dark:text-stone-100">{c.authorName}</span>
                    <span className="text-[11px] text-stone-400">
                      {new Date(c.createdAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                    </span>
                  </div>
                  <p className="text-sm text-stone-700 dark:text-stone-300 leading-relaxed">{c.content}</p>
                </div>
              ))
            )}
          </div>
        </section>

        {/* Related Articles */}
        {relatedPosts.length > 0 && (
          <section className="mt-16 pt-10 border-t border-stone-200 dark:border-stone-800">
            <h3 className="font-editorial text-xl font-bold text-stone-900 dark:text-stone-100 mb-6">
              More from {post.category}
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {relatedPosts.map(rp => (
                <div
                  key={rp.id}
                  onClick={() => onReadPost(rp.slug)}
                  className="p-5 rounded-xl bg-white dark:bg-stone-900/60 border border-stone-200 dark:border-stone-800 hover:border-amber-500/50 cursor-pointer transition-all group"
                >
                  <span className="text-[11px] text-amber-700 dark:text-amber-400 uppercase font-semibold">
                    {rp.readTime} min read
                  </span>
                  <h4 className="font-editorial text-base font-bold text-stone-900 dark:text-stone-100 group-hover:text-amber-600 dark:group-hover:text-amber-400 transition-colors mt-1 mb-2 line-clamp-2">
                    {rp.title}
                  </h4>
                  <p className="text-xs text-stone-500 line-clamp-2">{rp.excerpt}</p>
                </div>
              ))}
            </div>
          </section>
        )}
      </div>
    </article>
  );
};
