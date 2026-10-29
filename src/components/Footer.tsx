import React, { useState } from 'react';
import { Github, Send, Heart, BookOpen, ShieldCheck } from 'lucide-react';
import { SiteSettings } from '../types.ts';
import { storageService } from '../services/storage.ts';

interface FooterProps {
  settings: SiteSettings;
  onNavigateCategory: (cat: string) => void;
  onOpenStaticPage: (page: 'about' | 'privacy' | 'terms' | 'contact') => void;
  onOpenDeployModal: () => void;
  onShowToast: (msg: string) => void;
}

export const Footer: React.FC<FooterProps> = ({
  settings,
  onNavigateCategory,
  onOpenStaticPage,
  onOpenDeployModal,
  onShowToast
}) => {
  const [email, setEmail] = useState('');
  const [subscribed, setSubscribed] = useState(false);

  const handleSubscribe = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !email.includes('@')) {
      onShowToast("Please enter a valid email address.");
      return;
    }
    const success = storageService.addSubscriber(email);
    if (success) {
      setSubscribed(true);
      setEmail('');
      onShowToast("Subscribed to BlogSphere Editorial briefings!");
    } else {
      onShowToast("You are already subscribed. Thank you for your support!");
    }
  };

  return (
    <footer className="bg-stone-100 dark:bg-stone-950 border-t border-stone-200 dark:border-stone-800 transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-12 mb-12">
          
          {/* Brand & Mission */}
          <div className="md:col-span-5 space-y-4">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-stone-900 dark:bg-amber-500 text-white dark:text-stone-950 flex items-center justify-center font-bold text-base">
                B
              </div>
              <span className="font-editorial text-2xl font-bold tracking-tight text-stone-900 dark:text-stone-100">
                {settings.projectName}
              </span>
            </div>
            <p className="text-sm text-stone-600 dark:text-stone-400 leading-relaxed max-w-sm">
              {settings.description}
            </p>
            <div className="flex items-center gap-3 pt-2">
              <button
                onClick={onOpenDeployModal}
                className="inline-flex items-center gap-2 px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-white dark:bg-stone-900 border border-stone-300 dark:border-stone-700 text-stone-700 dark:text-stone-200 hover:border-amber-500 transition-colors shadow-xs"
              >
                <Github className="w-3.5 h-3.5" />
                <span>Streamlit Cloud & GitHub Ready</span>
              </button>
            </div>
          </div>

          {/* Editorial Categories */}
          <div className="md:col-span-3 space-y-3">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-stone-400 dark:text-stone-500">
              Editorial Categories
            </h4>
            <ul className="space-y-2 text-sm">
              {settings.categories.slice(0, 6).map(c => (
                <li key={c}>
                  <button
                    onClick={() => onNavigateCategory(c)}
                    className="text-stone-600 dark:text-stone-400 hover:text-amber-600 dark:hover:text-amber-400 transition-colors"
                  >
                    {c}
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {/* Newsletter Box */}
          <div className="md:col-span-4 space-y-3">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-stone-400 dark:text-stone-500">
              The Sunday Dispatch
            </h4>
            <p className="text-xs text-stone-600 dark:text-stone-400 leading-relaxed">
              Curated architectural deep-dives, systems insights, and interface design essays. No noise.
            </p>

            {subscribed ? (
              <div className="p-3 rounded-xl bg-amber-50 dark:bg-amber-950/40 text-amber-800 dark:text-amber-200 text-xs font-medium border border-amber-200 dark:border-amber-800">
                ✓ You are subscribed to future publications.
              </div>
            ) : (
              <form onSubmit={handleSubscribe} className="flex gap-2">
                <input
                  type="email"
                  required
                  placeholder="name@domain.com"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  className="flex-1 text-xs px-3.5 py-2.5 rounded-xl bg-white dark:bg-stone-900 border border-stone-300 dark:border-stone-700 text-stone-900 dark:text-white placeholder-stone-400 focus:outline-none focus:ring-2 focus:ring-amber-500"
                />
                <button
                  type="submit"
                  className="px-4 py-2.5 text-xs font-semibold text-white bg-amber-600 hover:bg-amber-700 rounded-xl transition-colors shadow-xs"
                >
                  Join
                </button>
              </form>
            )}
          </div>

        </div>

        {/* Bottom Bar with Links & Legal */}
        <div className="pt-8 border-t border-stone-200 dark:border-stone-800 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-stone-500 dark:text-stone-400">
          <div>
            © {new Date().getFullYear()} {settings.projectName}. Crafted with Python, Streamlit & TypeScript.
          </div>

          <div className="flex items-center gap-5">
            <button
              onClick={() => onOpenStaticPage('about')}
              className="hover:text-stone-900 dark:hover:text-stone-200 transition-colors"
            >
              About the Platform
            </button>
            <button
              onClick={() => onOpenStaticPage('contact')}
              className="hover:text-stone-900 dark:hover:text-stone-200 transition-colors"
            >
              Contact
            </button>
            <button
              onClick={() => onOpenStaticPage('privacy')}
              className="hover:text-stone-900 dark:hover:text-stone-200 transition-colors"
            >
              Privacy Policy
            </button>
            <button
              onClick={() => onOpenStaticPage('terms')}
              className="hover:text-stone-900 dark:hover:text-stone-200 transition-colors"
            >
              Terms of Service
            </button>
          </div>
        </div>

      </div>
    </footer>
  );
};
