/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import { 
  ArrowRight, 
  TrendingUp, 
  Sparkles, 
  BookOpen, 
  Filter, 
  Search, 
  CheckCircle2,
  ChevronRight,
  Flame
} from 'lucide-react';
import { Post, SiteSettings, User } from './types.ts';
import { storageService } from './services/storage.ts';
import { Navbar } from './components/Navbar.tsx';
import { Footer } from './components/Footer.tsx';
import { HeroSection } from './components/HeroSection.tsx';
import { PostCard } from './components/PostCard.tsx';
import { PostDetail } from './components/PostDetail.tsx';
import { AdminDashboard } from './components/AdminDashboard.tsx';
import { PostEditor } from './components/PostEditor.tsx';
import { ExploreView } from './components/ExploreView.tsx';
import { SearchModal } from './components/SearchModal.tsx';
import { DeployModal } from './components/DeployModal.tsx';
import { StaticPageModal } from './components/StaticPageModal.tsx';
import { Toast } from './components/Toast.tsx';

export default function App() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [settings, setSettings] = useState<SiteSettings>(storageService.getSettings());
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [currentView, setCurrentView] = useState<'home' | 'explore' | 'post-detail' | 'admin' | 'new-post' | 'edit-post'>('home');
  const [activeSlug, setActiveSlug] = useState<string | null>(null);
  const [editingPost, setEditingPost] = useState<Post | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  
  // Modals & UI States
  const [isDark, setIsDark] = useState<boolean>(() => {
    return localStorage.getItem('blogsphere_theme') === 'dark' ||
      window.matchMedia('(prefers-color-scheme: dark)').matches;
  });
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [isDeployModalOpen, setIsDeployModalOpen] = useState(false);
  const [staticPage, setStaticPage] = useState<'about' | 'privacy' | 'terms' | 'contact' | null>(null);
  const [toastMessage, setToastMessage] = useState<string | null>(null);
  const [homePageCount, setHomePageCount] = useState(6);

  // Initialize data on mount
  useEffect(() => {
    const loadedPosts = storageService.getPosts();
    setPosts(loadedPosts);
    const session = storageService.getAdminSession();
    setCurrentUser(session);
  }, []);

  // Theme synchronization
  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('blogsphere_theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('blogsphere_theme', 'light');
    }
  }, [isDark]);

  // Synchronize document title with settings.projectName
  useEffect(() => {
    document.title = `${settings.projectName} — Editorial & CMS Platform`;
  }, [settings.projectName]);

  // Global Keyboard listener (Cmd+K for search)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsSearchOpen(prev => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const showToast = (msg: string) => {
    setToastMessage(msg);
  };

  const handleNavigate = (view: string, slug?: string) => {
    if (view === 'post-detail' && slug) {
      setActiveSlug(slug);
      setCurrentView('post-detail');
    } else if (view === 'new-post') {
      if (!currentUser) {
        showToast("Please sign in as admin first.");
        setCurrentView('admin');
      } else {
        setEditingPost(null);
        setCurrentView('new-post');
      }
    } else {
      setCurrentView(view as any);
      setActiveSlug(null);
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleReadPost = (slug: string) => {
    setActiveSlug(slug);
    setCurrentView('post-detail');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleLogin = (email: string, pass: string): boolean => {
    const user = storageService.login(email, pass);
    if (user) {
      setCurrentUser(user);
      return true;
    }
    return false;
  };

  const handleLogout = () => {
    storageService.logout();
    setCurrentUser(null);
    showToast("Signed out of Administrator Studio.");
    if (currentView === 'new-post' || currentView === 'edit-post') {
      setCurrentView('home');
    }
  };

  const handleSavePost = (
    postData: Omit<Post, 'id' | 'createdAt' | 'updatedAt' | 'views' | 'likes'>,
    existingId?: string
  ) => {
    if (existingId) {
      const updated = storageService.updatePost(existingId, postData);
      if (updated) {
        setPosts(storageService.getPosts());
        showToast("Publication updated successfully!");
        handleReadPost(updated.slug);
      }
    } else {
      const created = storageService.createPost(postData);
      setPosts(storageService.getPosts());
      showToast("New article created and published dynamically!");
      handleReadPost(created.slug);
    }
  };

  const handleDeletePost = (id: string) => {
    storageService.deletePost(id);
    setPosts(storageService.getPosts());
    showToast("Publication permanently deleted.");
    if (currentView === 'post-detail') {
      setCurrentView('home');
    }
  };

  const handleToggleStatus = (id: string) => {
    const post = posts.find(p => p.id === id);
    if (!post) return;
    const nextStatus = post.status === 'published' ? 'draft' : 'published';
    storageService.updatePost(id, { status: nextStatus });
    setPosts(storageService.getPosts());
    showToast(`Story marked as ${nextStatus}`);
  };

  const handleUpdateSettings = (newSettings: SiteSettings) => {
    storageService.saveSettings(newSettings);
    setSettings(newSettings);
  };

  const handleResetData = () => {
    storageService.resetDefaults();
    setPosts(storageService.getPosts());
    setSettings(storageService.getSettings());
    showToast("Sample editorial stories restored.");
  };

  // Active post for detail view
  const activePost = activeSlug ? posts.find(p => p.slug === activeSlug) : null;

  // Filter published posts for home view
  const publishedPosts = posts.filter(p => p.status === 'published');
  const featuredPost = publishedPosts.find(p => p.isFeatured) || publishedPosts[0];
  const remainingPublished = publishedPosts.filter(p => p.id !== featuredPost?.id);

  const homeFilteredPosts = selectedCategory === 'All'
    ? remainingPublished
    : remainingPublished.filter(p => p.category === selectedCategory);

  const trendingPosts = [...publishedPosts].sort((a, b) => (b.views || 0) - (a.views || 0)).slice(0, 4);

  return (
    <div className="min-h-screen flex flex-col bg-[#faf9f5] dark:bg-[#111215] text-stone-800 dark:text-stone-100 font-sans transition-colors duration-200">
      {/* Toast Notifier */}
      <Toast message={toastMessage} onClose={() => setToastMessage(null)} />

      {/* Global Navigation Bar */}
      <Navbar
        settings={settings}
        currentView={currentView}
        onNavigate={handleNavigate}
        isDark={isDark}
        onToggleTheme={() => setIsDark(!isDark)}
        currentUser={currentUser}
        onLogout={handleLogout}
        onOpenSearch={() => setIsSearchOpen(true)}
        onOpenDeployModal={() => setIsDeployModalOpen(true)}
      />

      {/* Main Content Area */}
      <main className="flex-1">
        {/* VIEW 1: POST DETAIL VIEW */}
        {currentView === 'post-detail' && activePost && (
          <PostDetail
            post={activePost}
            allPosts={posts}
            onBack={() => handleNavigate('home')}
            onPostUpdated={(updated) => {
              setPosts(storageService.getPosts());
            }}
            onReadPost={handleReadPost}
            onShowToast={showToast}
          />
        )}

        {/* VIEW 2: EXPLORE ARCHIVE VIEW */}
        {currentView === 'explore' && (
          <ExploreView
            posts={posts}
            settings={settings}
            onReadPost={handleReadPost}
            selectedCategory={selectedCategory}
            onSelectCategory={setSelectedCategory}
          />
        )}

        {/* VIEW 3: ADMIN STUDIO & CMS */}
        {currentView === 'admin' && (
          <AdminDashboard
            posts={posts}
            settings={settings}
            currentUser={currentUser}
            onLogin={handleLogin}
            onLogout={handleLogout}
            onNewPost={() => handleNavigate('new-post')}
            onEditPost={(post) => {
              setEditingPost(post);
              setCurrentView('edit-post');
            }}
            onDeletePost={handleDeletePost}
            onToggleStatus={handleToggleStatus}
            onUpdateSettings={handleUpdateSettings}
            onResetData={handleResetData}
            onOpenDeployModal={() => setIsDeployModalOpen(true)}
            onShowToast={showToast}
          />
        )}

        {/* VIEW 4: CREATE / EDIT STORY EDITOR */}
        {(currentView === 'new-post' || currentView === 'edit-post') && (
          <PostEditor
            initialPost={currentView === 'edit-post' ? editingPost : null}
            settings={settings}
            onSave={handleSavePost}
            onCancel={() => handleNavigate(currentUser ? 'admin' : 'home')}
            onShowToast={showToast}
          />
        )}

        {/* VIEW 5: HOMEPAGE */}
        {currentView === 'home' && (
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
            
            {/* Masthead Banner */}
            <div className="text-center max-w-3xl mx-auto mb-12 sm:mb-16">
              <span className="text-[11px] font-bold uppercase tracking-widest text-amber-700 dark:text-amber-400 mb-2 block">
                Independent Editorial & Systems Publishing
              </span>
              <h1 className="font-editorial text-4xl sm:text-6xl font-bold tracking-tight text-stone-900 dark:text-stone-100 mb-4 leading-[1.08]">
                {settings.projectName}
              </h1>
              <p className="font-editorial text-lg sm:text-xl text-stone-600 dark:text-stone-300 italic max-w-xl mx-auto leading-relaxed">
                {settings.tagline}
              </p>
            </div>

            {/* Flagship Hero Article */}
            {featuredPost && (
              <HeroSection post={featuredPost} onReadPost={handleReadPost} />
            )}

            {/* Trending & Editorial Curations Strip */}
            {trendingPosts.length > 0 && (
              <section className="mb-14 p-6 sm:p-8 rounded-2xl bg-white dark:bg-stone-900/60 border border-stone-200/80 dark:border-stone-800 shadow-xs">
                <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-amber-700 dark:text-amber-400 mb-4">
                  <Flame className="w-4 h-4 text-amber-500" />
                  <span>Trending Dispatches This Week</span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                  {trendingPosts.map((tp, idx) => (
                    <div
                      key={tp.id}
                      onClick={() => handleReadPost(tp.slug)}
                      className="group cursor-pointer flex flex-col justify-between"
                    >
                      <div>
                        <span className="text-2xl font-bold font-editorial text-stone-300 dark:text-stone-700 block mb-1">
                          0{idx + 1}
                        </span>
                        <div className="flex items-center gap-2 text-[11px] text-stone-400 mb-1">
                          <span className="font-medium text-amber-700 dark:text-amber-400">{tp.category}</span>
                          <span>·</span>
                          <span>{tp.readTime}m</span>
                        </div>
                        <h4 className="font-editorial text-sm sm:text-base font-bold text-stone-900 dark:text-stone-100 group-hover:text-amber-600 dark:group-hover:text-amber-400 transition-colors line-clamp-2">
                          {tp.title}
                        </h4>
                      </div>
                      <span className="text-[11px] text-stone-400 mt-2 block">By {tp.authorName}</span>
                    </div>
                  ))}
                </div>
              </section>
            )}

            {/* Interactive Category Filter Segmented Buttons */}
            <div className="mb-10 flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-stone-200 dark:border-stone-800">
              <div className="flex items-center gap-2 overflow-x-auto py-1 scrollbar-none">
                {['All', ...settings.categories].map(cat => {
                  const isActive = selectedCategory === cat;
                  return (
                    <button
                      key={cat}
                      onClick={() => setSelectedCategory(cat)}
                      className={`text-xs font-medium px-4 py-2 rounded-xl transition-all whitespace-nowrap ${
                        isActive
                          ? 'bg-stone-900 text-white dark:bg-amber-500 dark:text-stone-950 font-semibold shadow-xs'
                          : 'bg-white dark:bg-stone-800 text-stone-600 dark:text-stone-300 hover:bg-stone-100 dark:hover:bg-stone-700 border border-stone-200/80 dark:border-stone-700'
                      }`}
                    >
                      {cat}
                    </button>
                  );
                })}
              </div>

              <div className="flex items-center gap-2 text-xs text-stone-500">
                <span>Showing {homeFilteredPosts.length} publications</span>
              </div>
            </div>

            {/* Latest Publications Grid */}
            <section className="mb-16">
              <div className="flex items-center justify-between mb-8">
                <div>
                  <h2 className="font-editorial text-2xl sm:text-3xl font-bold tracking-tight text-stone-900 dark:text-stone-100">
                    Latest Publications
                  </h2>
                  <p className="text-xs text-stone-500 mt-0.5">
                    Fresh perspectives on software architecture, design systems, and thoughtful engineering.
                  </p>
                </div>

                <button
                  onClick={() => handleNavigate('explore')}
                  className="inline-flex items-center gap-1 text-xs font-semibold text-amber-700 dark:text-amber-400 hover:underline"
                >
                  <span>View Archive</span>
                  <ChevronRight className="w-3.5 h-3.5" />
                </button>
              </div>

              {homeFilteredPosts.length === 0 ? (
                <div className="p-12 text-center rounded-2xl bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800">
                  <p className="text-stone-500 text-sm">No stories in this category yet.</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
                  {homeFilteredPosts.slice(0, homePageCount).map(post => (
                    <PostCard
                      key={post.id}
                      post={post}
                      onReadPost={handleReadPost}
                    />
                  ))}
                </div>
              )}

              {/* Load More Option */}
              {homeFilteredPosts.length > homePageCount && (
                <div className="text-center mt-12">
                  <button
                    onClick={() => setHomePageCount(prev => prev + 6)}
                    className="px-6 py-2.5 text-xs font-semibold rounded-xl bg-white dark:bg-stone-800 border border-stone-300 dark:border-stone-700 text-stone-800 dark:text-stone-200 hover:bg-stone-100 dark:hover:bg-stone-700 transition-colors shadow-xs"
                  >
                    Load More Articles ({homeFilteredPosts.length - homePageCount} remaining)
                  </button>
                </div>
              )}
            </section>

            {/* Deploy Helper Banner */}
            <section className="p-8 sm:p-10 rounded-2xl bg-gradient-to-br from-amber-500/10 via-amber-600/5 to-transparent border border-amber-500/30 flex flex-col md:flex-row items-center justify-between gap-6">
              <div>
                <span className="text-xs uppercase font-bold text-amber-700 dark:text-amber-400 tracking-wider block mb-1">
                  Ready for GitHub & Streamlit Community Cloud
                </span>
                <h3 className="font-editorial text-2xl font-bold text-stone-900 dark:text-stone-100 mb-2">
                  Deploy this exact blog platform in 60 seconds
                </h3>
                <p className="text-sm text-stone-600 dark:text-stone-300 max-w-xl leading-relaxed">
                  The complete Python backend, SQLite database schema, Streamlit UI, and requirements.txt are pre-packaged in the repository root.
                </p>
              </div>

              <button
                onClick={() => setIsDeployModalOpen(true)}
                className="px-6 py-3 rounded-xl bg-stone-900 text-white dark:bg-amber-500 dark:text-stone-950 font-semibold text-xs shadow-md hover:scale-105 transition-transform flex-shrink-0"
              >
                Inspect Deployment Files & Guide →
              </button>
            </section>

          </div>
        )}
      </main>

      {/* Global Footer */}
      <Footer
        settings={settings}
        onNavigateCategory={(cat) => {
          setSelectedCategory(cat);
          handleNavigate('home');
        }}
        onOpenStaticPage={(page) => setStaticPage(page)}
        onOpenDeployModal={() => setIsDeployModalOpen(true)}
        onShowToast={showToast}
      />

      {/* Modals */}
      <SearchModal
        isOpen={isSearchOpen}
        onClose={() => setIsSearchOpen(false)}
        posts={publishedPosts}
        onSelectPost={handleReadPost}
      />

      <DeployModal
        isOpen={isDeployModalOpen}
        onClose={() => setIsDeployModalOpen(false)}
        onShowToast={showToast}
      />

      <StaticPageModal
        page={staticPage}
        onClose={() => setStaticPage(null)}
        settings={settings}
      />
    </div>
  );
}
