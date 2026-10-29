import React from 'react';
import { Heart, Eye, ArrowUpRight } from 'lucide-react';
import { Post } from '../types.ts';

interface PostCardProps {
  post: Post;
  onReadPost: (slug: string) => void;
  variant?: 'standard' | 'compact' | 'featured-sub';
}

export const PostCard: React.FC<PostCardProps> = ({ post, onReadPost, variant = 'standard' }) => {
  const formattedDate = new Date(post.publishedAt || post.createdAt).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });

  if (variant === 'compact') {
    return (
      <article 
        onClick={() => onReadPost(post.slug)}
        className="group py-4 border-b border-stone-200 dark:border-stone-800 last:border-0 cursor-pointer flex items-baseline justify-between gap-4 transition-colors hover:bg-stone-50/50 dark:hover:bg-stone-900/40 px-2 rounded-lg"
      >
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 text-xs text-stone-500 dark:text-stone-400 mb-1">
            <span className="text-amber-700 dark:text-amber-400 font-medium">{post.category}</span>
            <span aria-hidden="true">·</span>
            <span>{post.readTime} min read</span>
          </div>
          <h4 className="font-editorial text-base font-semibold text-stone-900 dark:text-stone-100 group-hover:text-amber-600 dark:group-hover:text-amber-400 transition-colors line-clamp-1">
            {post.title}
          </h4>
        </div>
        <ArrowUpRight className="w-4 h-4 text-stone-400 opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0" />
      </article>
    );
  }

  return (
    <article 
      onClick={() => onReadPost(post.slug)}
      className="group flex flex-col justify-between rounded-xl bg-white dark:bg-stone-900/70 border border-stone-200/90 dark:border-stone-800/80 overflow-hidden shadow-xs hover:shadow-md hover:border-stone-300 dark:hover:border-stone-700 transition-all duration-200 cursor-pointer"
    >
      <div>
        {/* Card Thumbnail */}
        <div className="relative aspect-[16/10] overflow-hidden bg-stone-100 dark:bg-stone-800">
          <img
            src={post.featuredImage || 'https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=800&q=80'}
            alt={post.title}
            loading="lazy"
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 ease-out"
          />
          {post.status !== 'published' && (
            <span className="absolute top-3 left-3 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider bg-amber-500 text-stone-950 rounded">
              {post.status}
            </span>
          )}
        </div>

        {/* Card Body */}
        <div className="p-5 sm:p-6">
          {/* Unboxed Metadata Line (Zero-Pill Rule) */}
          <div className="flex items-center gap-2 text-xs text-stone-500 dark:text-stone-400 mb-2.5">
            <span className="font-medium text-amber-700 dark:text-amber-400">{post.category}</span>
            <span aria-hidden="true">·</span>
            <span>{post.readTime} min read</span>
            <span aria-hidden="true">·</span>
            <span>{formattedDate}</span>
          </div>

          {/* Heading */}
          <h3 className="font-editorial text-xl font-bold tracking-tight text-stone-900 dark:text-stone-100 group-hover:text-amber-600 dark:group-hover:text-amber-400 transition-colors line-clamp-2 leading-snug mb-2.5">
            {post.title}
          </h3>

          {/* Excerpt */}
          <p className="text-sm text-stone-600 dark:text-stone-300 line-clamp-2 leading-relaxed font-normal">
            {post.excerpt || post.content.replace(/#|\*|`|\[|\]/g, '').slice(0, 140) + '...'}
          </p>
        </div>
      </div>

      {/* Footer Byline */}
      <div className="px-5 sm:px-6 pb-5 pt-3 border-t border-stone-100 dark:border-stone-800/80 flex items-center justify-between text-xs text-stone-500 dark:text-stone-400">
        <div className="flex items-center gap-2">
          {post.authorAvatar ? (
            <img src={post.authorAvatar} alt={post.authorName} className="w-5 h-5 rounded-full object-cover" />
          ) : (
            <div className="w-5 h-5 rounded-full bg-amber-600 text-white flex items-center justify-center text-[10px] font-bold">
              {post.authorName.charAt(0)}
            </div>
          )}
          <span className="font-medium text-stone-700 dark:text-stone-300">{post.authorName}</span>
        </div>

        <div className="flex items-center gap-3">
          <span className="flex items-center gap-1 hover:text-rose-600">
            <Heart className="w-3.5 h-3.5" />
            <span>{post.likes}</span>
          </span>
          <span className="flex items-center gap-1">
            <Eye className="w-3.5 h-3.5" />
            <span>{post.views}</span>
          </span>
        </div>
      </div>
    </article>
  );
};
