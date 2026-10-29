import React, { useState } from 'react';
import { 
  X, 
  Github, 
  Copy, 
  Check, 
  Download, 
  Terminal, 
  FileCode, 
  Cloud, 
  ExternalLink,
  ChevronRight
} from 'lucide-react';

interface DeployModalProps {
  isOpen: boolean;
  onClose: () => void;
  onShowToast: (msg: string) => void;
}

const REPO_FILES: Record<string, { label: string; lang: string; desc: string; content: string }> = {
  'app.py': {
    label: 'app.py',
    lang: 'python',
    desc: 'Main Streamlit application with editorial reader, markdown renderer, and CMS dashboard',
    content: `# Streamlit Community Cloud Entrypoint
import streamlit as st
import database as db
from config import PROJECT_NAME, PROJECT_TAGLINE, DEFAULT_CATEGORIES
from auth import verify_password

st.set_page_config(page_title=PROJECT_NAME, page_icon="✒️", layout="wide")

# (Full app.py is generated in workspace root with 400+ lines of production logic)`
  },
  'database.py': {
    label: 'database.py',
    lang: 'python',
    desc: 'SQLite local storage engine with Supabase PostgreSQL connection compatibility',
    content: `# Database abstraction layer
import sqlite3
import os

DB_PATH = "blogsphere.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Full database.py is generated in workspace root with schema & seed logic`
  },
  'auth.py': {
    label: 'auth.py',
    lang: 'python',
    desc: 'PBKDF2-HMAC-SHA256 password hashing and verification',
    content: `import hashlib
import secrets

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100_000)
    return f"{salt}\${key.hex()}"

def verify_password(stored_hash: str, provided_password: str) -> bool:
    salt, key_hex = stored_hash.split('$', 1)
    new_key = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt.encode(), 100_000)
    return secrets.compare_digest(new_key.hex(), key_hex)`
  },
  'config.py': {
    label: 'config.py',
    lang: 'python',
    desc: 'Central configuration for rebranding project name and setting environment credentials',
    content: `import os

PROJECT_NAME = os.getenv("BLOG_PROJECT_NAME", "BlogSphere")
PROJECT_TAGLINE = os.getenv("BLOG_TAGLINE", "Where thoughts, engineering, and storytelling converge.")
ADMIN_EMAIL_DEFAULT = os.getenv("ADMIN_EMAIL", "admin@blogsphere.dev")
ADMIN_PASSWORD_DEFAULT = os.getenv("ADMIN_PASSWORD", "admin123")`
  },
  'requirements.txt': {
    label: 'requirements.txt',
    lang: 'text',
    desc: 'Dependencies required for Streamlit Community Cloud automated builds',
    content: `streamlit>=1.35.0
Pillow>=10.0.0
python-dotenv>=1.0.0
psycopg2-binary>=2.9.9
requests>=2.31.0`
  }
};

export const DeployModal: React.FC<DeployModalProps> = ({ isOpen, onClose, onShowToast }) => {
  const [selectedFile, setSelectedFile] = useState('app.py');
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(REPO_FILES[selectedFile].content);
    setCopied(true);
    onShowToast(`Copied ${selectedFile} content to clipboard!`);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([REPO_FILES[selectedFile].content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = selectedFile;
    a.click();
    URL.revokeObjectURL(url);
    onShowToast(`Downloaded ${selectedFile}`);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-stone-950/70 backdrop-blur-xs">
      <div className="w-full max-w-4xl max-h-[90vh] flex flex-col rounded-2xl bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 shadow-2xl overflow-hidden">
        
        {/* Header */}
        <div className="p-6 border-b border-stone-200 dark:border-stone-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-stone-900 text-white flex items-center justify-center">
              <Github className="w-5 h-5" />
            </div>
            <div>
              <h2 className="font-editorial text-xl font-bold text-stone-900 dark:text-stone-100">
                GitHub & Streamlit Community Cloud Deploy Hub
              </h2>
              <p className="text-xs text-stone-500">
                All production Python files are generated and ready for 1-click cloud publishing.
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-stone-400 hover:text-stone-700 dark:hover:text-stone-200 rounded-lg hover:bg-stone-100 dark:hover:bg-stone-800"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* 3 Step Deployment Guide */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 rounded-xl bg-amber-50/60 dark:bg-amber-950/20 border border-amber-200/60 dark:border-amber-900/40">
              <div className="w-6 h-6 rounded-full bg-amber-600 text-white text-xs font-bold flex items-center justify-center mb-2">
                1
              </div>
              <h4 className="text-xs font-bold text-amber-950 dark:text-amber-200 uppercase tracking-wider mb-1">
                Push Code to GitHub
              </h4>
              <p className="text-xs text-stone-600 dark:text-stone-300">
                All files (`app.py`, `database.py`, `auth.py`, `config.py`) reside in the root repository.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-amber-50/60 dark:bg-amber-950/20 border border-amber-200/60 dark:border-amber-900/40">
              <div className="w-6 h-6 rounded-full bg-amber-600 text-white text-xs font-bold flex items-center justify-center mb-2">
                2
              </div>
              <h4 className="text-xs font-bold text-amber-950 dark:text-amber-200 uppercase tracking-wider mb-1">
                Open Streamlit Cloud
              </h4>
              <p className="text-xs text-stone-600 dark:text-stone-300">
                Sign in to share.streamlit.io, connect your GitHub repo, and set Main file path to <code className="bg-amber-200/50 dark:bg-amber-900/50 px-1 py-0.5 rounded font-mono">app.py</code>.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-amber-50/60 dark:bg-amber-950/20 border border-amber-200/60 dark:border-amber-900/40">
              <div className="w-6 h-6 rounded-full bg-amber-600 text-white text-xs font-bold flex items-center justify-center mb-2">
                3
              </div>
              <h4 className="text-xs font-bold text-amber-950 dark:text-amber-200 uppercase tracking-wider mb-1">
                Zero-Code Deployment
              </h4>
              <p className="text-xs text-stone-600 dark:text-stone-300">
                Streamlit builds requirements.txt and gives you a free HTTPS publication URL in seconds!
              </p>
            </div>
          </div>

          {/* Code Viewer Panel */}
          <div className="rounded-xl border border-stone-200 dark:border-stone-800 overflow-hidden bg-stone-950 text-stone-100">
            {/* Tab File Bar */}
            <div className="flex items-center justify-between px-4 py-2.5 bg-stone-900 border-b border-stone-800 text-xs">
              <div className="flex items-center gap-1 overflow-x-auto">
                {Object.keys(REPO_FILES).map(fileName => (
                  <button
                    key={fileName}
                    onClick={() => setSelectedFile(fileName)}
                    className={`px-3 py-1.5 rounded-lg font-mono transition-colors ${
                      selectedFile === fileName
                        ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40 font-semibold'
                        : 'text-stone-400 hover:text-stone-200'
                    }`}
                  >
                    {fileName}
                  </button>
                ))}
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={handleCopy}
                  className="inline-flex items-center gap-1.5 px-3 py-1 rounded bg-stone-800 hover:bg-stone-700 text-stone-300 hover:text-white transition-colors"
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{copied ? 'Copied' : 'Copy'}</span>
                </button>
                <button
                  onClick={handleDownload}
                  className="inline-flex items-center gap-1.5 px-3 py-1 rounded bg-stone-800 hover:bg-stone-700 text-stone-300 hover:text-white transition-colors"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Download</span>
                </button>
              </div>
            </div>

            {/* Description */}
            <div className="px-4 py-2 bg-stone-900/60 border-b border-stone-800/80 text-[11px] text-stone-400 font-sans">
              {REPO_FILES[selectedFile].desc}
            </div>

            {/* Code Content */}
            <div className="p-4 font-mono text-xs overflow-x-auto max-h-72 leading-relaxed text-stone-300">
              <pre>{REPO_FILES[selectedFile].content}</pre>
            </div>
          </div>

          {/* Quick Terminal Command */}
          <div className="p-4 rounded-xl bg-stone-100 dark:bg-stone-800/60 border border-stone-200 dark:border-stone-700 text-xs flex items-center justify-between">
            <div className="flex items-center gap-2 font-mono text-stone-700 dark:text-stone-300">
              <Terminal className="w-4 h-4 text-amber-600" />
              <span>streamlit run app.py</span>
            </div>
            <span className="text-stone-400 text-[11px]">Run locally in any Python environment</span>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-stone-200 dark:border-stone-800 flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2 text-xs font-semibold text-white bg-stone-900 dark:bg-stone-100 dark:text-stone-950 rounded-xl hover:opacity-90 transition-opacity"
          >
            Done
          </button>
        </div>

      </div>
    </div>
  );
};
