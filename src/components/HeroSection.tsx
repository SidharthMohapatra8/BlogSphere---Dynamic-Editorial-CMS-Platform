import React from 'react';
import { ArrowRight, Sparkles, BookOpen } from 'lucide-react';
import { Post } from '../types.ts';

interface HeroSectionProps {
  post: Post;
  onReadPost: (slug: string) => void;
}

export const HeroSection: React.FC<HeroSectionProps> = ({ post, onReadPost }) => {
  const formattedDate = new Date(post.publishedAt || post.createdAt).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });

  return (
    <section className="mb-14 relative group">
      <div className="relative overflow-hidden rounded-2xl bg-stone-900 text-stone-100 border border-stone-800 shadow-xl transition-all duration-300">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-0 items-stretch">
          
          {/* Left Text / Editorial Content */}
          <div className="lg:col-span-7 p-8 sm:p-10 lg:p-14 flex flex-col justify-between z-10">
            <div>
              {/* Kicker & Meta */}
              <div className="flex items-center gap-2 text-xs font-medium text-amber-400 tracking-wider uppercase mb-4">
                <Sparkles className="w-3.5 h-3.5" />
                <span>Featured Dispatch</span>
                <span aria-hidden="true" className="text-stone-600">·</span>
                <span className="text-stone-300">{post.category}</span>
                <span aria-hidden="true" className="text-stone-600">·</span>
                <span className="text-stone-400">{post.readTime} min read</span>
              </div>

              {/* Title */}
              <h1 
                onClick={() => onReadPost(post.slug)}
                className="font-editorial text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight text-white mb-4 leading-[1.15] cursor-pointer hover:text-amber-200 transition-colors"
              >
                {post.title}
              </h1>

              {/* Subtitle / Excerpt */}
              <p className="text-base sm:text-lg text-stone-300 font-normal leading-relaxed mb-6 line-clamp-3">
                {post.subtitle || post.excerpt}
              </p>
            </div>

            {/* Author Byline & CTA */}
            <div className="pt-6 border-t border-stone-800/80 flex flex-wrap items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                {post.authorAvatar && (
                  <img
                    src={post.authorAvatar}
                    alt={post.authorName}
                    className="w-10 h-10 rounded-full object-cover ring-2 ring-amber-500/30"
                  />
                )}
                <div>
                  <div className="text-sm font-medium text-white">{post.authorName}</div>
                  <div className="text-xs text-stone-400 flex items-center gap-1.5">
                    <span>{formattedDate}</span>
                    <span aria-hidden="true">·</span>
                    <span>{post.views.toLocaleString()} views</span>
                  </div>
                </div>
              </div>

              <button
                onClick={() => onReadPost(post.slug)}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-stone-950 font-semibold text-sm transition-all hover:gap-3 shadow-md focus:outline-none"
              >
                <span>Read Full Story</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Right Image Container */}
          <div className="lg:col-span-5 relative min-h-[300px] lg:min-h-full overflow-hidden">
            <img
              src={post.featuredImage || 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80'}
              alt={post.title}
              className="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-700 ease-out"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-stone-950/80 via-transparent lg:bg-gradient-to-r lg:from-stone-900 lg:to-transparent" />
          </div>

        </div>
      </div>
    </section>
  );
};
