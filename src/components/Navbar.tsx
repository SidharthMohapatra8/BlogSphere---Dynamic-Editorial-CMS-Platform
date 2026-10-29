import React, { useState } from 'react';
import { 
  Search, 
  Moon, 
  Sun, 
  ShieldCheck, 
  BookOpen, 
  Compass, 
  Github, 
  Menu, 
  X,
  LogOut,
  PenSquare
} from 'lucide-react';
import { SiteSettings, User } from '../types.ts';

interface NavbarProps {
  settings: SiteSettings;
  currentView: string;
  onNavigate: (view: string, slug?: string) => void;
  isDark: boolean;
  onToggleTheme: () => void;
  currentUser: User | null;
  onLogout: () => void;
  onOpenSearch: () => void;
  onOpenDeployModal: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  settings,
  currentView,
  onNavigate,
  isDark,
  onToggleTheme,
  currentUser,
  onLogout,
  onOpenSearch,
  onOpenDeployModal
}) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-40 w-full backdrop-blur-md bg-[#faf9f5]/90 dark:bg-[#111215]/90 border-b border-stone-200/80 dark:border-stone-800 transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-18 flex items-center justify-between">
        {/* Brand / Masthead */}
        <div className="flex items-center gap-8">
          <button 
            onClick={() => onNavigate('home')}
            className="flex items-center gap-2.5 text-left group focus:outline-none"
          >
            <div className="w-9 h-9 rounded-lg bg-stone-900 dark:bg-amber-500 text-white dark:text-stone-950 flex items-center justify-center font-bold text-lg shadow-sm transition-transform group-hover:scale-105">
              <span>B</span>
            </div>
            <div>
              <span className="font-editorial text-2xl font-bold tracking-tight text-stone-900 dark:text-stone-100 block leading-tight">
                {settings.projectName}
              </span>
              <span className="text-[10px] tracking-widest uppercase font-semibold text-amber-700 dark:text-amber-400 block -mt-0.5">
                Editorial & CMS
              </span>
            </div>
          </button>

          {/* Desktop Navigation Links */}
          <nav className="hidden md:flex items-center gap-6 text-sm font-medium">
            <button
              onClick={() => onNavigate('home')}
              className={`transition-colors hover:text-stone-900 dark:hover:text-stone-100 ${
                currentView === 'home' 
                  ? 'text-stone-950 dark:text-white font-semibold underline underline-offset-8 decoration-amber-500 decoration-2' 
                  : 'text-stone-600 dark:text-stone-400'
              }`}
            >
              Publications
            </button>
            <button
              onClick={() => onNavigate('explore')}
              className={`transition-colors hover:text-stone-900 dark:hover:text-stone-100 ${
                currentView === 'explore' 
                  ? 'text-stone-950 dark:text-white font-semibold underline underline-offset-8 decoration-amber-500 decoration-2' 
                  : 'text-stone-600 dark:text-stone-400'
              }`}
            >
              Explore & Archive
            </button>
            <button
              onClick={() => onNavigate('admin')}
              className={`flex items-center gap-1.5 transition-colors hover:text-stone-900 dark:hover:text-stone-100 ${
                currentView === 'admin' 
                  ? 'text-amber-600 dark:text-amber-400 font-semibold' 
                  : 'text-stone-600 dark:text-stone-400'
              }`}
            >
              <ShieldCheck className="w-4 h-4 text-amber-600 dark:text-amber-400" />
              <span>Admin Studio</span>
            </button>
          </nav>
        </div>

        {/* Right Action Cluster */}
        <div className="flex items-center gap-2 sm:gap-3">
          {/* Quick Search Button */}
          <button
            onClick={onOpenSearch}
            className="flex items-center gap-2 px-3 py-1.5 text-xs text-stone-500 dark:text-stone-400 bg-stone-200/60 dark:bg-stone-800/80 rounded-lg hover:bg-stone-200 dark:hover:bg-stone-700 transition-colors focus:outline-none"
            title="Search articles (Ctrl+K)"
          >
            <Search className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Search</span>
            <kbd className="hidden sm:inline px-1.5 py-0.5 text-[10px] bg-stone-100 dark:bg-stone-900 rounded border border-stone-300 dark:border-stone-700 font-mono">⌘K</kbd>
          </button>


          {/* New Article Shortcut (if admin) */}
          {currentUser && (
            <button
              onClick={() => onNavigate('new-post')}
              className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-white bg-amber-600 hover:bg-amber-700 rounded-lg shadow-sm transition-colors"
            >
              <PenSquare className="w-3.5 h-3.5" />
              <span>Write Story</span>
            </button>
          )}

          {/* Theme Switcher */}
          <button
            onClick={onToggleTheme}
            aria-label="Toggle theme"
            className="p-2 text-stone-600 dark:text-stone-300 hover:text-stone-900 dark:hover:text-white rounded-lg hover:bg-stone-100 dark:hover:bg-stone-800 transition-colors focus:outline-none"
          >
            {isDark ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4" />}
          </button>

          {/* Admin Avatar or Login */}
          {currentUser ? (
            <div className="hidden sm:flex items-center gap-2 pl-2 border-l border-stone-200 dark:border-stone-800">
              <span className="text-xs font-medium text-stone-700 dark:text-stone-300 hidden xl:inline">
                {currentUser.fullName}
              </span>
              <button
                onClick={onLogout}
                title="Log out of Admin Studio"
                className="p-1.5 text-stone-500 hover:text-rose-600 rounded-md hover:bg-rose-50 dark:hover:bg-rose-950/40 transition-colors"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <button
              onClick={() => onNavigate('admin')}
              className="hidden sm:inline-flex items-center text-xs font-semibold px-3 py-1.5 text-stone-700 dark:text-stone-200 hover:bg-stone-200/50 dark:hover:bg-stone-800 rounded-lg transition-colors"
            >
              Sign In
            </button>
          )}

          {/* Mobile Menu Toggle */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 text-stone-600 dark:text-stone-300 hover:bg-stone-100 dark:hover:bg-stone-800 rounded-lg"
            aria-label="Open navigation menu"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden px-4 pt-2 pb-4 bg-[#faf9f5] dark:bg-[#111215] border-b border-stone-200 dark:border-stone-800 space-y-2">
          <button
            onClick={() => { onNavigate('home'); setMobileMenuOpen(false); }}
            className="block w-full text-left py-2 px-3 text-sm font-medium text-stone-800 dark:text-stone-200 rounded-md hover:bg-stone-100 dark:hover:bg-stone-800"
          >
            Publications
          </button>
          <button
            onClick={() => { onNavigate('explore'); setMobileMenuOpen(false); }}
            className="block w-full text-left py-2 px-3 text-sm font-medium text-stone-800 dark:text-stone-200 rounded-md hover:bg-stone-100 dark:hover:bg-stone-800"
          >
            Explore & Archive
          </button>
          <button
            onClick={() => { onNavigate('admin'); setMobileMenuOpen(false); }}
            className="block w-full text-left py-2 px-3 text-sm font-medium text-amber-600 dark:text-amber-400 rounded-md hover:bg-amber-50 dark:hover:bg-amber-950/30"
          >
            Admin Studio & CMS
          </button>

          {currentUser && (
            <button
              onClick={() => { onNavigate('new-post'); setMobileMenuOpen(false); }}
              className="block w-full text-left py-2 px-3 text-sm font-medium text-white bg-amber-600 rounded-md"
            >
              Write New Story
            </button>
          )}
        </div>
      )}
    </header>
  );
};
