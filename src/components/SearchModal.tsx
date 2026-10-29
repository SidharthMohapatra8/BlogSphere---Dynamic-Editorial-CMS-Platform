import React, { useState, useEffect } from 'react';
import { Search, X, ArrowRight, BookOpen } from 'lucide-react';
import { Post } from '../types.ts';

interface SearchModalProps {
  isOpen: boolean;
  onClose: () => void;
  posts: Post[];
  onSelectPost: (slug: string) => void;
}

export const SearchModal: React.FC<SearchModalProps> = ({
  isOpen,
  onClose,
  posts,
  onSelectPost
}) => {
  const [query, setQuery] = useState('');

  // Handle Escape key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        onClose();
      }
    };
    if (isOpen) {
      window.addEventListener('keydown', handleKeyDown);
    }
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const results = query.trim()
    ? posts.filter(p => {
        const q = query.toLowerCase();
        return (
          p.title.toLowerCase().includes(q) ||
          p.category.toLowerCase().includes(q) ||
          p.excerpt.toLowerCase().includes(q) ||
          p.tags.some(t => t.toLowerCase().includes(q))
        );
      })
    : posts.slice(0, 4);

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 p-4 bg-stone-950/60 backdrop-blur-xs">
      <div className="w-full max-w-2xl rounded-2xl bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        
        {/* Search Input Bar */}
        <div className="flex items-center px-4 py-3.5 border-b border-stone-200 dark:border-stone-800">
          <Search className="w-5 h-5 text-amber-600 mr-3 flex-shrink-0" />
          <input
            autoFocus
            type="text"
            placeholder="Search stories by topic, keyword, or tag..."
            value={query}
            onChange={e => setQuery(e.target.value)}
            className="w-full text-base bg-transparent text-stone-900 dark:text-stone-100 placeholder-stone-400 focus:outline-none"
          />
          {query && (
            <button
              onClick={() => setQuery('')}
              className="p-1 text-stone-400 hover:text-stone-600 dark:hover:text-stone-200 mr-1"
            >
              <X className="w-4 h-4" />
            </button>
          )}
          <kbd className="text-[10px] bg-stone-100 dark:bg-stone-800 text-stone-500 px-2 py-1 rounded border border-stone-200 dark:border-stone-700 font-mono">
            ESC
          </kbd>
        </div>

        {/* Results List */}
        <div className="max-h-96 overflow-y-auto p-2 divide-y divide-stone-100 dark:divide-stone-800/60">
          <div className="px-3 py-1.5 text-[11px] font-semibold uppercase tracking-wider text-stone-400">
            {query.trim() ? `Search Results (${results.length})` : 'Recommended Stories'}
          </div>

          {results.length === 0 ? (
            <div className="p-8 text-center text-sm text-stone-400">
              No matching publications found for "{query}".
            </div>
          ) : (
            results.map(post => (
              <div
                key={post.id}
                onClick={() => {
                  onSelectPost(post.slug);
                  onClose();
                }}
                className="p-3.5 rounded-xl hover:bg-stone-100 dark:hover:bg-stone-800/70 cursor-pointer transition-colors group flex items-start justify-between gap-4"
              >
                <div>
                  <div className="flex items-center gap-2 text-[11px] text-amber-700 dark:text-amber-400 font-medium mb-1">
                    <span>{post.category}</span>
                    <span aria-hidden="true">·</span>
                    <span className="text-stone-400">{post.readTime} min read</span>
                  </div>
                  <h4 className="font-editorial text-base font-bold text-stone-900 dark:text-stone-100 group-hover:text-amber-600 dark:group-hover:text-amber-400 transition-colors">
                    {post.title}
                  </h4>
                  <p className="text-xs text-stone-500 dark:text-stone-400 line-clamp-1 mt-0.5">
                    {post.excerpt}
                  </p>
                </div>
                <ArrowRight className="w-4 h-4 text-stone-400 group-hover:text-amber-500 group-hover:translate-x-1 transition-all flex-shrink-0 mt-2" />
              </div>
            ))
          )}
        </div>

      </div>
    </div>
  );
};
