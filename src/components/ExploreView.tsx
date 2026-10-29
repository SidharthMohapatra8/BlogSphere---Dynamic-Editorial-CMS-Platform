import React, { useState } from 'react';
import { Search, Filter, SlidersHorizontal, ArrowUpDown } from 'lucide-react';
import { Post, SiteSettings } from '../types.ts';
import { PostCard } from './PostCard.tsx';

interface ExploreViewProps {
  posts: Post[];
  settings: SiteSettings;
  onReadPost: (slug: string) => void;
  selectedCategory: string;
  onSelectCategory: (cat: string) => void;
}

export const ExploreView: React.FC<ExploreViewProps> = ({
  posts,
  settings,
  onReadPost,
  selectedCategory,
  onSelectCategory
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState<'latest' | 'popular' | 'likes'>('latest');
  const [readTimeFilter, setReadTimeFilter] = useState<'all' | 'short' | 'medium' | 'long'>('all');
  const [visibleCount, setVisibleCount] = useState(6);

  // Filter only published
  const published = posts.filter(p => p.status === 'published');

  // Apply filters
  const filtered = published.filter(p => {
    const matchesCat = selectedCategory === 'All' || p.category === selectedCategory;
    const matchesSearch = !searchQuery.trim() || 
      p.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.excerpt.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.tags.some(t => t.toLowerCase().includes(searchQuery.toLowerCase()));

    let matchesTime = true;
    if (readTimeFilter === 'short') matchesTime = p.readTime <= 4;
    else if (readTimeFilter === 'medium') matchesTime = p.readTime >= 5 && p.readTime <= 8;
    else if (readTimeFilter === 'long') matchesTime = p.readTime > 8;

    return matchesCat && matchesSearch && matchesTime;
  });

  // Sort
  const sorted = [...filtered].sort((a, b) => {
    if (sortBy === 'popular') return (b.views || 0) - (a.views || 0);
    if (sortBy === 'likes') return (b.likes || 0) - (a.likes || 0);
    return new Date(b.publishedAt || b.createdAt).getTime() - new Date(a.publishedAt || a.createdAt).getTime();
  });

  const displayList = sorted.slice(0, visibleCount);
  const hasMore = sorted.length > visibleCount;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      {/* Page Header */}
      <div className="max-w-3xl mb-10">
        <span className="text-xs font-semibold uppercase tracking-wider text-amber-700 dark:text-amber-400 block mb-2">
          The Archive & Dispatch
        </span>
        <h1 className="font-editorial text-4xl sm:text-5xl font-bold tracking-tight text-stone-900 dark:text-stone-100 mb-3">
          Explore all Publications
        </h1>
        <p className="text-stone-600 dark:text-stone-300 text-base leading-relaxed">
          Deep dives, technical commentary, and foundational essays organized by discipline and craft.
        </p>
      </div>

      {/* Control Strip */}
      <div className="space-y-4 mb-10 p-5 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200/80 dark:border-stone-800 shadow-xs">
        {/* Search Input & Sort Selector */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="relative w-full sm:flex-1">
            <Search className="w-4 h-4 text-stone-400 absolute left-3.5 top-3" />
            <input
              type="text"
              placeholder="Search across all publications..."
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              className="w-full text-xs pl-10 pr-4 py-2.5 rounded-xl bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 text-stone-900 dark:text-white placeholder-stone-400 focus:outline-none focus:ring-2 focus:ring-amber-500"
            />
          </div>

          <div className="flex items-center gap-2 w-full sm:w-auto justify-end">
            <div className="flex items-center gap-1.5 text-xs text-stone-500">
              <ArrowUpDown className="w-3.5 h-3.5" />
              <span>Sort:</span>
            </div>
            <select
              value={sortBy}
              onChange={e => setSortBy(e.target.value as any)}
              className="text-xs px-3 py-2 rounded-xl bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 text-stone-800 dark:text-stone-200 focus:outline-none focus:ring-2 focus:ring-amber-500"
            >
              <option value="latest">Newest First</option>
              <option value="popular">Most Read</option>
              <option value="likes">Most Appreciated</option>
            </select>
          </div>
        </div>

        {/* Category Tabs (Interactive buttons) */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 pt-1 scrollbar-none">
          {['All', ...settings.categories].map(cat => {
            const active = selectedCategory === cat;
            return (
              <button
                key={cat}
                onClick={() => onSelectCategory(cat)}
                className={`text-xs font-medium px-3.5 py-1.5 rounded-lg whitespace-nowrap transition-colors ${
                  active
                    ? 'bg-stone-900 text-white dark:bg-amber-500 dark:text-stone-950 font-semibold shadow-xs'
                    : 'bg-stone-100 dark:bg-stone-800 text-stone-600 dark:text-stone-300 hover:bg-stone-200 dark:hover:bg-stone-700'
                }`}
              >
                {cat}
              </button>
            );
          })}
        </div>

        {/* Read Time Filter */}
        <div className="flex items-center gap-2 pt-2 border-t border-stone-100 dark:border-stone-800 text-xs text-stone-500">
          <span>Read length:</span>
          {(['all', 'short', 'medium', 'long'] as const).map(f => (
            <button
              key={f}
              onClick={() => setReadTimeFilter(f)}
              className={`px-2 py-0.5 rounded capitalize ${
                readTimeFilter === f
                  ? 'text-amber-700 dark:text-amber-400 font-semibold underline'
                  : 'text-stone-500 hover:text-stone-800 dark:hover:text-stone-200'
              }`}
            >
              {f === 'all' ? 'Any' : f === 'short' ? '< 5m' : f === 'medium' ? '5-8m' : '8m+'}
            </button>
          ))}
        </div>
      </div>

      {/* Grid of Results */}
      {sorted.length === 0 ? (
        <div className="p-16 text-center rounded-2xl bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800">
          <p className="font-editorial text-lg text-stone-700 dark:text-stone-300 mb-2">No matching publications</p>
          <p className="text-xs text-stone-500 mb-4">Try adjusting your search terms or selecting a different category.</p>
          <button
            onClick={() => {
              setSearchQuery('');
              onSelectCategory('All');
              setReadTimeFilter('all');
            }}
            className="px-4 py-2 text-xs font-semibold rounded-lg bg-amber-600 text-white"
          >
            Clear Filters
          </button>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8 mb-12">
            {displayList.map(post => (
              <PostCard
                key={post.id}
                post={post}
                onReadPost={onReadPost}
              />
            ))}
          </div>

          {/* Load More Button */}
          {hasMore && (
            <div className="text-center pt-4">
              <button
                onClick={() => setVisibleCount(prev => prev + 6)}
                className="px-6 py-2.5 text-xs font-semibold rounded-xl bg-white dark:bg-stone-800 border border-stone-300 dark:border-stone-700 text-stone-800 dark:text-stone-200 hover:bg-stone-100 dark:hover:bg-stone-700 transition-colors shadow-xs"
              >
                Load More Publications ({sorted.length - visibleCount} remaining)
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};
