import React, { useState } from 'react';
import { 
  Plus, 
  FileEdit, 
  Trash2, 
  Eye, 
  Heart, 
  Search, 
  CheckCircle, 
  Clock, 
  Layers, 
  Users, 
  Settings as SettingsIcon, 
  Database, 
  AlertTriangle,
  ExternalLink,
  ShieldAlert,
  ArrowRight
} from 'lucide-react';
import { Post, SiteSettings, User } from '../types.ts';

interface AdminDashboardProps {
  posts: Post[];
  settings: SiteSettings;
  currentUser: User | null;
  onLogin: (email: string, pass: string) => boolean;
  onLogout: () => void;
  onNewPost: () => void;
  onEditPost: (post: Post) => void;
  onDeletePost: (id: string) => void;
  onToggleStatus: (id: string) => void;
  onUpdateSettings: (newSettings: SiteSettings) => void;
  onResetData: () => void;
  onOpenDeployModal: () => void;
  onShowToast: (msg: string) => void;
}

export const AdminDashboard: React.FC<AdminDashboardProps> = ({
  posts,
  settings,
  currentUser,
  onLogin,
  onLogout,
  onNewPost,
  onEditPost,
  onDeletePost,
  onToggleStatus,
  onUpdateSettings,
  onResetData,
  onOpenDeployModal,
  onShowToast
}) => {
  // Login form state
  const [loginEmail, setLoginEmail] = useState('admin@blogsphere.dev');
  const [loginPass, setLoginPass] = useState('admin123');
  const [loginError, setLoginError] = useState('');

  // Dashboard filtering
  const [activeTab, setActiveTab] = useState<'posts' | 'settings' | 'cloud'>('posts');
  const [statusFilter, setStatusFilter] = useState<'all' | 'published' | 'draft' | 'scheduled'>('all');
  const [searchTerm, setSearchTerm] = useState('');

  // Delete modal state
  const [deletingPost, setDeletingPost] = useState<Post | null>(null);

  // Settings form state
  const [projectName, setProjectName] = useState(settings.projectName);
  const [tagline, setTagline] = useState(settings.tagline);
  const [description, setDescription] = useState(settings.description);
  const [authorName, setAuthorName] = useState(settings.authorName);
  const [authorBio, setAuthorBio] = useState(settings.authorBio);
  const [authorAvatar, setAuthorAvatar] = useState(settings.authorAvatar);

  // Handle Login
  const handleLoginSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoginError('');
    const success = onLogin(loginEmail, loginPass);
    if (!success) {
      setLoginError('Invalid credentials. Check email or password.');
    } else {
      onShowToast("Welcome back to BlogSphere Admin Studio.");
    }
  };

  // Metrics
  const totalPosts = posts.length;
  const publishedPosts = posts.filter(p => p.status === 'published').length;
  const draftPosts = posts.filter(p => p.status === 'draft').length;
  const totalViews = posts.reduce((acc, p) => acc + (p.views || 0), 0);
  const totalLikes = posts.reduce((acc, p) => acc + (p.likes || 0), 0);

  // Filtered posts
  const filteredPosts = posts.filter(p => {
    const matchesStatus = statusFilter === 'all' || p.status === statusFilter;
    const matchesSearch = !searchTerm || 
      p.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.tags.some(t => t.toLowerCase().includes(searchTerm.toLowerCase()));
    return matchesStatus && matchesSearch;
  });

  // Handle Save Settings
  const handleSaveSettings = (e: React.FormEvent) => {
    e.preventDefault();
    onUpdateSettings({
      ...settings,
      projectName: projectName.trim(),
      tagline: tagline.trim(),
      description: description.trim(),
      authorName: authorName.trim(),
      authorBio: authorBio.trim(),
      authorAvatar: authorAvatar.trim()
    });
    onShowToast("Platform branding and settings updated!");
  };

  // IF NOT LOGGED IN -> RENDER AUTH SCREEN
  if (!currentUser) {
    return (
      <div className="max-w-md mx-auto px-4 py-16">
        <div className="p-8 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200/90 dark:border-stone-800 shadow-lg text-center">
          <div className="w-12 h-12 rounded-xl bg-amber-500/10 text-amber-600 flex items-center justify-center mx-auto mb-4">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <h2 className="font-editorial text-2xl font-bold text-stone-900 dark:text-stone-100 mb-1">
            Admin Studio Access
          </h2>
          <p className="text-xs text-stone-500 mb-6">
            Sign in to manage publications, drafts, authors, and platform deployment settings.
          </p>

          {loginError && (
            <div className="p-3 mb-4 rounded-xl bg-rose-50 dark:bg-rose-950/40 text-rose-700 dark:text-rose-300 text-xs text-left">
              {loginError}
            </div>
          )}

          <form onSubmit={handleLoginSubmit} className="space-y-4 text-left">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-stone-500 mb-1">
                Admin Email
              </label>
              <input
                type="email"
                required
                value={loginEmail}
                onChange={e => setLoginEmail(e.target.value)}
                className="w-full text-xs px-3.5 py-2.5 rounded-xl bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 text-stone-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-amber-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-stone-500 mb-1">
                Password
              </label>
              <input
                type="password"
                required
                value={loginPass}
                onChange={e => setLoginPass(e.target.value)}
                className="w-full text-xs px-3.5 py-2.5 rounded-xl bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 text-stone-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-amber-500"
              />
            </div>

            <button
              type="submit"
              className="w-full py-2.5 text-xs font-semibold text-white bg-amber-600 hover:bg-amber-700 rounded-xl transition-colors shadow-sm"
            >
              Sign In to Studio
            </button>
          </form>

          {/* Quick Demo Fill Helper */}
          <div className="mt-6 pt-5 border-t border-stone-100 dark:border-stone-800 text-left">
            <span className="text-[11px] font-semibold text-stone-500 block mb-1.5 uppercase tracking-wider">
              Default Credentials:
            </span>
            <div className="text-xs bg-stone-50 dark:bg-stone-800/80 p-2.5 rounded-lg border border-stone-200 dark:border-stone-700 text-stone-600 dark:text-stone-300 font-mono space-y-1">
              <div>Email: admin@blogsphere.dev</div>
              <div>Password: admin123</div>
            </div>
            <button
              type="button"
              onClick={() => {
                setLoginEmail('admin@blogsphere.dev');
                setLoginPass('admin123');
              }}
              className="mt-2 text-xs text-amber-600 dark:text-amber-400 font-medium hover:underline"
            >
              Autofill Demo Credentials
            </button>
          </div>
        </div>
      </div>
    );
  }

  // LOGGED IN ADMIN DASHBOARD
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Top Banner */}
      <div className="flex flex-wrap items-center justify-between gap-4 mb-8 pb-4 border-b border-stone-200/80 dark:border-stone-800">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-amber-700 dark:text-amber-400 uppercase tracking-wider mb-1">
            <span>Admin Studio</span>
            <span aria-hidden="true">·</span>
            <span>{currentUser.fullName}</span>
          </div>
          <h1 className="font-editorial text-3xl font-bold text-stone-900 dark:text-stone-100">
            Content Management System
          </h1>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={onNewPost}
            className="inline-flex items-center gap-2 px-4 py-2 text-xs font-semibold text-white bg-amber-600 hover:bg-amber-700 rounded-xl shadow-sm transition-colors"
          >
            <Plus className="w-4 h-4" />
            <span>Write New Story</span>
          </button>

          <button
            onClick={onLogout}
            className="px-3 py-2 text-xs font-medium text-stone-600 dark:text-stone-400 hover:bg-stone-100 dark:hover:bg-stone-800 rounded-xl transition-colors"
          >
            Sign Out
          </button>
        </div>
      </div>

      {/* KPI Metrics */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4 mb-8">
        <div className="p-5 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200/80 dark:border-stone-800 shadow-xs">
          <div className="text-xs text-stone-500 uppercase font-medium mb-1">Total Stories</div>
          <div className="text-2xl font-bold font-editorial text-stone-900 dark:text-stone-100">{totalPosts}</div>
        </div>
        <div className="p-5 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200/80 dark:border-stone-800 shadow-xs">
          <div className="text-xs text-stone-500 uppercase font-medium mb-1">Published</div>
          <div className="text-2xl font-bold font-editorial text-emerald-600 dark:text-emerald-400">{publishedPosts}</div>
        </div>
        <div className="p-5 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200/80 dark:border-stone-800 shadow-xs">
          <div className="text-xs text-stone-500 uppercase font-medium mb-1">Drafts</div>
          <div className="text-2xl font-bold font-editorial text-amber-600 dark:text-amber-400">{draftPosts}</div>
        </div>
        <div className="p-5 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200/80 dark:border-stone-800 shadow-xs">
          <div className="text-xs text-stone-500 uppercase font-medium mb-1">Total Reads</div>
          <div className="text-2xl font-bold font-editorial text-stone-900 dark:text-stone-100">{totalViews.toLocaleString()}</div>
        </div>
        <div className="p-5 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200/80 dark:border-stone-800 shadow-xs">
          <div className="text-xs text-stone-500 uppercase font-medium mb-1">Total Likes</div>
          <div className="text-2xl font-bold font-editorial text-rose-600 dark:text-rose-400">{totalLikes.toLocaleString()}</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 mb-6 border-b border-stone-200 dark:border-stone-800">
        <button
          onClick={() => setActiveTab('posts')}
          className={`pb-3 px-2 text-sm font-semibold transition-colors border-b-2 -mb-[2px] ${
            activeTab === 'posts'
              ? 'border-amber-600 text-stone-900 dark:text-stone-100'
              : 'border-transparent text-stone-500 hover:text-stone-800 dark:hover:text-stone-200'
          }`}
        >
          Publications & Drafts ({posts.length})
        </button>
        <button
          onClick={() => setActiveTab('settings')}
          className={`pb-3 px-2 text-sm font-semibold transition-colors border-b-2 -mb-[2px] ${
            activeTab === 'settings'
              ? 'border-amber-600 text-stone-900 dark:text-stone-100'
              : 'border-transparent text-stone-500 hover:text-stone-800 dark:hover:text-stone-200'
          }`}
        >
          Platform Branding
        </button>
        <button
          onClick={() => setActiveTab('cloud')}
          className={`pb-3 px-2 text-sm font-semibold transition-colors border-b-2 -mb-[2px] ${
            activeTab === 'cloud'
              ? 'border-amber-600 text-stone-900 dark:text-stone-100'
              : 'border-transparent text-stone-500 hover:text-stone-800 dark:hover:text-stone-200'
          }`}
        >
          Cloud Database & Storage (Supabase / Cloudinary)
        </button>
      </div>

      {/* TAB 1: POSTS TABLE */}
      {activeTab === 'posts' && (
        <div className="space-y-4">
          {/* Filter Bar */}
          <div className="flex flex-wrap items-center justify-between gap-3 p-4 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200/80 dark:border-stone-800">
            {/* Search */}
            <div className="relative flex-1 min-w-[240px]">
              <Search className="w-4 h-4 text-stone-400 absolute left-3 top-3" />
              <input
                type="text"
                placeholder="Search publications by title, category, or tag..."
                value={searchTerm}
                onChange={e => setSearchTerm(e.target.value)}
                className="w-full text-xs pl-9 pr-4 py-2.5 rounded-xl bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 text-stone-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-amber-500"
              />
            </div>

            {/* Status Segmented Control */}
            <div className="flex items-center bg-stone-100 dark:bg-stone-800 p-1 rounded-xl text-xs font-medium">
              {(['all', 'published', 'draft', 'scheduled'] as const).map(s => (
                <button
                  key={s}
                  onClick={() => setStatusFilter(s)}
                  className={`px-3 py-1.5 rounded-lg capitalize transition-colors ${
                    statusFilter === s
                      ? 'bg-white dark:bg-stone-700 text-stone-900 dark:text-white shadow-xs font-semibold'
                      : 'text-stone-500 hover:text-stone-800'
                  }`}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>

          {/* Posts List */}
          {filteredPosts.length === 0 ? (
            <div className="p-12 text-center rounded-2xl bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800">
              <p className="text-stone-500 text-sm">No stories match your filter criteria.</p>
            </div>
          ) : (
            <div className="bg-white dark:bg-stone-900 rounded-2xl border border-stone-200/80 dark:border-stone-800 overflow-hidden shadow-xs divide-y divide-stone-100 dark:divide-stone-800">
              {filteredPosts.map(post => (
                <div key={post.id} className="p-4 sm:p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 hover:bg-stone-50/70 dark:hover:bg-stone-800/40 transition-colors">
                  <div className="flex items-center gap-4 min-w-0">
                    <img
                      src={post.featuredImage || 'https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=200&q=80'}
                      alt={post.title}
                      className="w-16 h-14 rounded-lg object-cover flex-shrink-0 bg-stone-100 dark:bg-stone-800"
                    />
                    <div className="min-w-0">
                      <div className="flex items-center gap-2 text-xs text-stone-500 dark:text-stone-400 mb-1">
                        <span className={`font-semibold uppercase text-[10px] ${
                          post.status === 'published' ? 'text-emerald-600' : 'text-amber-600'
                        }`}>
                          ● {post.status}
                        </span>
                        <span aria-hidden="true">·</span>
                        <span>{post.category}</span>
                        {post.isFeatured && (
                          <>
                            <span aria-hidden="true">·</span>
                            <span className="text-amber-600 font-medium">★ Featured</span>
                          </>
                        )}
                      </div>
                      <h3 className="font-editorial text-base font-bold text-stone-900 dark:text-stone-100 truncate">
                        {post.title}
                      </h3>
                      <div className="flex items-center gap-3 text-xs text-stone-400 mt-0.5">
                        <span>{post.views} reads</span>
                        <span>·</span>
                        <span>{post.likes} likes</span>
                        <span>·</span>
                        <span>{post.readTime} min read</span>
                      </div>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2 w-full sm:w-auto justify-end pt-2 sm:pt-0 border-t sm:border-0 border-stone-100 dark:border-stone-800">
                    <button
                      onClick={() => onToggleStatus(post.id)}
                      className="px-2.5 py-1.5 text-xs font-medium rounded-lg border border-stone-200 dark:border-stone-700 text-stone-600 dark:text-stone-300 hover:bg-stone-100 dark:hover:bg-stone-800 transition-colors"
                      title="Toggle between draft and published"
                    >
                      {post.status === 'published' ? 'Unpublish' : 'Publish'}
                    </button>
                    <button
                      onClick={() => onEditPost(post)}
                      className="p-1.5 rounded-lg text-stone-600 dark:text-stone-300 hover:bg-stone-100 dark:hover:bg-stone-800 transition-colors"
                      title="Edit article"
                    >
                      <FileEdit className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => setDeletingPost(post)}
                      className="p-1.5 rounded-lg text-stone-500 hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/40 transition-colors"
                      title="Delete article"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* TAB 2: PLATFORM BRANDING & SETTINGS */}
      {activeTab === 'settings' && (
        <div className="max-w-2xl bg-white dark:bg-stone-900 p-6 sm:p-8 rounded-2xl border border-stone-200/80 dark:border-stone-800 space-y-6">
          <div>
            <h2 className="font-editorial text-xl font-bold text-stone-900 dark:text-stone-100">
              Platform Configuration
            </h2>
            <p className="text-xs text-stone-500">
              Customize the publication name, masthead tagline, and author profile.
            </p>
          </div>

          <form onSubmit={handleSaveSettings} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-stone-500 mb-1">
                Project / Publication Name
              </label>
              <input
                type="text"
                required
                value={projectName}
                onChange={e => setProjectName(e.target.value)}
                className="w-full text-sm font-semibold px-3.5 py-2.5 rounded-xl bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 text-stone-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-amber-500"
              />
              <p className="text-[11px] text-stone-400 mt-1">Changes the masthead name across all pages and headers.</p>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-stone-500 mb-1">
                Masthead Tagline
              </label>
              <input
                type="text"
                value={tagline}
                onChange={e => setTagline(e.target.value)}
                className="w-full text-xs px-3.5 py-2.5 rounded-xl bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 text-stone-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-amber-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-stone-500 mb-1">
                Platform Description
              </label>
              <textarea
                rows={3}
                value={description}
                onChange={e => setDescription(e.target.value)}
                className="w-full text-xs p-3.5 rounded-xl bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 text-stone-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-amber-500"
              />
            </div>

            <div className="pt-2 border-t border-stone-100 dark:border-stone-800">
              <h3 className="text-xs font-semibold uppercase tracking-wider text-stone-500 mb-3">
                Default Author Profile
              </h3>
              <div className="space-y-3">
                <div>
                  <label className="block text-[11px] font-medium text-stone-600 dark:text-stone-400 mb-1">
                    Author Display Name
                  </label>
                  <input
                    type="text"
                    value={authorName}
                    onChange={e => setAuthorName(e.target.value)}
                    className="w-full text-xs px-3.5 py-2 rounded-xl bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 text-stone-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-amber-500"
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-medium text-stone-600 dark:text-stone-400 mb-1">
                    Author Bio
                  </label>
                  <textarea
                    rows={2}
                    value={authorBio}
                    onChange={e => setAuthorBio(e.target.value)}
                    className="w-full text-xs p-3 rounded-xl bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 text-stone-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-amber-500"
                  />
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between pt-4 border-t border-stone-100 dark:border-stone-800">
              <button
                type="button"
                onClick={onResetData}
                className="text-xs text-rose-600 hover:underline"
              >
                Reset to Sample Editorial Stories
              </button>

              <button
                type="submit"
                className="px-5 py-2 text-xs font-semibold text-white bg-amber-600 hover:bg-amber-700 rounded-xl shadow-xs transition-colors"
              >
                Save Configuration
              </button>
            </div>
          </form>
        </div>
      )}

      {/* TAB 3: CLOUD DATABASE & STORAGE */}
      {activeTab === 'cloud' && (
        <div className="max-w-3xl space-y-6">
          <div className="p-6 sm:p-8 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200/80 dark:border-stone-800">
            <div className="flex items-center gap-2 text-amber-700 dark:text-amber-400 mb-2">
              <Database className="w-5 h-5" />
              <h3 className="font-editorial text-lg font-bold">Supabase PostgreSQL Architecture</h3>
            </div>
            <p className="text-xs text-stone-600 dark:text-stone-300 leading-relaxed mb-4">
              BlogSphere operates with local SQLite out of the box. When deploying to Streamlit Community Cloud or any persistent hosting, you can connect directly to Supabase PostgreSQL without writing a single line of SQL.
            </p>
            <div className="bg-stone-950 text-stone-200 p-4 rounded-xl font-mono text-xs overflow-x-auto">
              DATABASE_URL="postgresql://postgres:[YOUR-PASSWORD]@db.[REF].supabase.co:5432/postgres"
            </div>
          </div>

          <div className="p-6 sm:p-8 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200/80 dark:border-stone-800">
            <h3 className="font-editorial text-lg font-bold text-stone-900 dark:text-stone-100 mb-2">
              Cloudinary Media Storage
            </h3>
            <p className="text-xs text-stone-600 dark:text-stone-300 leading-relaxed mb-4">
              For high-volume image hosting with automatic responsive resizing and WebP transformation, configure your Cloudinary credentials in `.env` or Streamlit Secrets:
            </p>
            <div className="bg-stone-950 text-stone-200 p-4 rounded-xl font-mono text-xs overflow-x-auto space-y-1">
              <div>CLOUDINARY_CLOUD_NAME="your_cloud_name"</div>
              <div>CLOUDINARY_API_KEY="your_api_key"</div>
              <div>CLOUDINARY_API_SECRET="your_api_secret"</div>
            </div>
          </div>
        </div>
      )}

      {/* DELETE CONFIRMATION MODAL */}
      {deletingPost && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-stone-950/60 backdrop-blur-xs">
          <div className="w-full max-w-md p-6 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 shadow-xl">
            <div className="w-10 h-10 rounded-xl bg-rose-100 text-rose-600 dark:bg-rose-950/50 flex items-center justify-center mb-4">
              <AlertTriangle className="w-5 h-5" />
            </div>
            <h3 className="font-editorial text-xl font-bold text-stone-900 dark:text-stone-100 mb-2">
              Delete Publication?
            </h3>
            <p className="text-xs text-stone-600 dark:text-stone-300 mb-6 leading-relaxed">
              Are you sure you want to permanently delete <strong className="text-stone-900 dark:text-white">"{deletingPost.title}"</strong>? This action removes the article and its associated comments.
            </p>
            <div className="flex items-center justify-end gap-3">
              <button
                type="button"
                onClick={() => setDeletingPost(null)}
                className="px-4 py-2 text-xs font-semibold text-stone-600 dark:text-stone-400 hover:bg-stone-100 dark:hover:bg-stone-800 rounded-xl transition-colors"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={() => {
                  onDeletePost(deletingPost.id);
                  setDeletingPost(null);
                }}
                className="px-4 py-2 text-xs font-semibold text-white bg-rose-600 hover:bg-rose-700 rounded-xl transition-colors"
              >
                Delete Permanently
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
