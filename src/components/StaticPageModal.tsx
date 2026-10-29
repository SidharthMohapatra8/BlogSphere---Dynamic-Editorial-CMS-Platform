import React from 'react';
import { X, ShieldCheck, Mail, BookOpen } from 'lucide-react';
import { SiteSettings } from '../types.ts';

interface StaticPageModalProps {
  page: 'about' | 'privacy' | 'terms' | 'contact' | null;
  onClose: () => void;
  settings: SiteSettings;
}

export const StaticPageModal: React.FC<StaticPageModalProps> = ({ page, onClose, settings }) => {
  if (!page) return null;

  const contentMap = {
    about: {
      title: `About ${settings.projectName}`,
      subtitle: 'The philosophy and architecture of our editorial platform.',
      body: (
        <div className="space-y-4 text-sm leading-relaxed text-stone-700 dark:text-stone-300">
          <p>
            {settings.projectName} is a modern, dynamic publishing platform created to bridge high-craft writing with production-grade engineering principles.
          </p>
          <p>
            Rather than relying on closed-source monolithic CMS platforms, {settings.projectName} is engineered to be portable: run it locally with SQLite or scale it to millions of readers via Supabase PostgreSQL and Streamlit Community Cloud.
          </p>
          <h4 className="font-editorial text-base font-bold text-stone-900 dark:text-stone-100 pt-2">
            The Three Editorial Tenets
          </h4>
          <ul className="list-disc pl-5 space-y-1.5">
            <li><strong>Clarity Over Velocity</strong>: Thoughtful, technical writing that stands the test of time.</li>
            <li><strong>Zero Visual Clutter</strong>: Eliminating distracting candy badges and banners in favor of serene typography.</li>
            <li><strong>Total Author Sovereignty</strong>: Content stored in open Markdown formats with zero vendor lock-in.</li>
          </ul>
        </div>
      )
    },
    contact: {
      title: 'Editorial Inquiries & Submissions',
      subtitle: 'Pitch a story or reach our technical desk.',
      body: (
        <div className="space-y-4 text-sm leading-relaxed text-stone-700 dark:text-stone-300">
          <p>
            We welcome technical drafts, essays on distributed systems, interface design case studies, and engineering philosophy.
          </p>
          <div className="p-4 rounded-xl bg-stone-100 dark:bg-stone-800 text-stone-900 dark:text-stone-100 font-mono text-xs space-y-1">
            <div>Desk: desk@blogsphere.dev</div>
            <div>Submissions: pitches@blogsphere.dev</div>
            <div>PGP Key: 0x9B84_2026_ED01</div>
          </div>
          <p className="text-xs text-stone-500">
            All submitted drafts are peer-reviewed by domain specialists before publication.
          </p>
        </div>
      )
    },
    privacy: {
      title: 'Privacy Policy',
      subtitle: 'How we respect your attention and personal telemetry.',
      body: (
        <div className="space-y-4 text-sm leading-relaxed text-stone-700 dark:text-stone-300">
          <p>
            At {settings.projectName}, we hold a radical respect for reader privacy. We do not operate third-party tracking pixels, behavioural profiling networks, or invasive analytics.
          </p>
          <h4 className="font-editorial text-base font-bold text-stone-900 dark:text-stone-100 pt-2">
            Information We Process
          </h4>
          <p>
            - <strong>Comments</strong>: The name and optional email you choose to provide when posting a public response.<br/>
            - <strong>Subscribers</strong>: Your email address, solely used to deliver the Sunday Dispatch. Never sold, never rented.<br/>
            - <strong>Reading Telemetry</strong>: Basic aggregated view counters to calculate publication resonance.
          </p>
        </div>
      )
    },
    terms: {
      title: 'Terms of Service',
      subtitle: 'Guidelines for reading, commenting, and syndicating our publications.',
      body: (
        <div className="space-y-4 text-sm leading-relaxed text-stone-700 dark:text-stone-300">
          <p>
            By accessing or reading {settings.projectName}, you agree to engage in constructive, intellectual discourse.
          </p>
          <p>
            <strong>Content Ownership</strong>: Original essays remain the intellectual property of their respective authors. Code snippets provided within publications are distributed under the permissive MIT License for educational and technical use.
          </p>
          <p>
            <strong>Community Standards</strong>: Harassment, spam, commercial solicitation, and defamatory statements will be removed by editorial moderators.
          </p>
        </div>
      )
    }
  }[page];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-stone-950/60 backdrop-blur-xs">
      <div className="w-full max-w-lg p-6 sm:p-8 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 shadow-xl">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="font-editorial text-2xl font-bold text-stone-900 dark:text-stone-100">
              {contentMap.title}
            </h3>
            <p className="text-xs text-stone-500 mt-0.5">{contentMap.subtitle}</p>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 text-stone-400 hover:text-stone-700 dark:hover:text-stone-200 rounded-lg"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="py-2">
          {contentMap.body}
        </div>

        <div className="mt-6 pt-4 border-t border-stone-100 dark:border-stone-800 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 text-xs font-semibold text-white bg-stone-900 dark:bg-stone-100 dark:text-stone-950 rounded-xl"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
