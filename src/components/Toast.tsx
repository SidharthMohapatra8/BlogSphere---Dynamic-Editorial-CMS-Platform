import React, { useEffect } from 'react';
import { CheckCircle2, X } from 'lucide-react';

interface ToastProps {
  message: string | null;
  onClose: () => void;
}

export const Toast: React.FC<ToastProps> = ({ message, onClose }) => {
  useEffect(() => {
    if (!message) return;
    const timer = setTimeout(() => {
      onClose();
    }, 3500);
    return () => clearTimeout(timer);
  }, [message, onClose]);

  if (!message) return null;

  return (
    <div className="fixed bottom-6 right-6 z-50 flex items-center gap-2.5 px-4 py-3 rounded-xl bg-stone-900 text-white dark:bg-stone-100 dark:text-stone-950 shadow-2xl border border-stone-800 dark:border-stone-200 animate-in fade-in slide-in-from-bottom-3 duration-200 text-xs font-medium">
      <CheckCircle2 className="w-4 h-4 text-amber-500 dark:text-amber-600 flex-shrink-0" />
      <span>{message}</span>
      <button onClick={onClose} className="ml-2 text-stone-400 hover:text-white dark:hover:text-black">
        <X className="w-3.5 h-3.5" />
      </button>
    </div>
  );
};
