import React, { useState, useEffect } from 'react';
import { 
  Save, 
  Eye, 
  FileText, 
  Image as ImageIcon, 
  Tag, 
  Folder, 
  Bold, 
  Italic, 
  Heading1, 
  Heading2, 
  Quote, 
  Code, 
  List, 
  ListOrdered, 
  Link as LinkIcon, 
  Sparkles,
  Upload,
  ArrowLeft,
  CheckCircle2
} from 'lucide-react';
import { Post, PostStatus, SiteSettings } from '../types.ts';

interface PostEditorProps {
  initialPost?: Post | null;
  settings: SiteSettings;
  onSave: (postData: Omit<Post, 'id' | 'createdAt' | 'updatedAt' | 'views' | 'likes'>, existingId?: string) => void;
  onCancel: () => void;
  onShowToast: (msg: string) => void;
}

const CURATED_IMAGE_PRESETS = [
  { name: 'Systems & Space', url: 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80' },
  { name: 'Modern Code & Data', url: 'https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=1200&q=80' },
  { name: 'Clean Editorial Desk', url: 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=1200&q=80' },
  { name: 'Neural Flow', url: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1200&q=80' },
  { name: 'Architecture & Steel', url: 'https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=1200&q=80' },
  { name: 'Minimalist Hardware', url: 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200&q=80' }
];

export const PostEditor: React.FC<PostEditorProps> = ({
  initialPost,
  settings,
  onSave,
  onCancel,
  onShowToast
}) => {
  const [title, setTitle] = useState(initialPost?.title || '');
  const [subtitle, setSubtitle] = useState(initialPost?.subtitle || '');
  const [slug, setSlug] = useState(initialPost?.slug || '');
  const [content, setContent] = useState(initialPost?.content || '');
  const [excerpt, setExcerpt] = useState(initialPost?.excerpt || '');
  const [category, setCategory] = useState(initialPost?.category || settings.categories[0]);
  const [customCategory, setCustomCategory] = useState('');
  const [tagsInput, setTagsInput] = useState(initialPost?.tags?.join(', ') || '');
  const [status, setStatus] = useState<PostStatus>(initialPost?.status || 'published');
  const [isFeatured, setIsFeatured] = useState(initialPost?.isFeatured || false);
  const [featuredImage, setFeaturedImage] = useState(
    initialPost?.featuredImage || CURATED_IMAGE_PRESETS[0].url
  );
  const [activeTab, setActiveTab] = useState<'edit' | 'preview'>('edit');
  const [authorName, setAuthorName] = useState(initialPost?.authorName || settings.authorName);

  // Auto-generate slug when title changes (unless manual override or editing existing)
  useEffect(() => {
    if (!initialPost && title) {
      const generated = title
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/(^-|-$)/g, '');
      setSlug(generated);
    }
  }, [title, initialPost]);

  // Insert markdown helper at cursor position
  const insertFormatting = (before: string, after: string = '', defaultText: string = '') => {
    const textarea = document.getElementById('markdown-editor-textarea') as HTMLTextAreaElement;
    if (!textarea) return;

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const selected = content.substring(start, end) || defaultText;
    const replacement = `${before}${selected}${after}`;

    const newContent = content.substring(0, start) + replacement + content.substring(end);
    setContent(newContent);

    setTimeout(() => {
      textarea.focus();
      textarea.setSelectionRange(start + before.length, start + before.length + selected.length);
    }, 10);
  };

  // Handle local image file upload (converts to persistent Base64 Data URL)
  const handleImageFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (file.size > 4 * 1024 * 1024) {
      onShowToast("Image size exceeds 4MB limit.");
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
      if (typeof reader.result === 'string') {
        setFeaturedImage(reader.result);
        onShowToast("Featured image uploaded and converted successfully!");
      }
    };
    reader.readAsDataURL(file);
  };

  // Submit Handler
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      onShowToast("Please enter an article title.");
      return;
    }
    if (!content.trim()) {
      onShowToast("Please provide article content.");
      return;
    }

    // Calculate reading time
    const words = content.trim().split(/\s+/).length;
    const readTime = Math.max(1, Math.round(words / 200));

    // Prepare tags
    const tags = tagsInput
      .split(',')
      .map(t => t.trim())
      .filter(Boolean);

    const chosenCat = customCategory.trim() ? customCategory.trim() : category;

    // Generate auto-excerpt if empty
    const finalExcerpt = excerpt.trim() || 
      content.replace(/[#*`>]/g, '').trim().slice(0, 160) + '...';

    onSave({
      title: title.trim(),
      subtitle: subtitle.trim(),
      slug: slug.trim() || title.toLowerCase().replace(/[^a-z0-9]+/g, '-'),
      content: content.trim(),
      excerpt: finalExcerpt,
      featuredImage: featuredImage.trim(),
      category: chosenCat,
      tags,
      status,
      isFeatured,
      readTime,
      publishedAt: initialPost?.publishedAt || new Date().toISOString(),
      authorName: authorName.trim() || settings.authorName,
      authorAvatar: settings.authorAvatar,
      authorRole: 'Editorial Desk'
    }, initialPost?.id);
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8">
      {/* Top Header & Navigation */}
      <div className="flex flex-wrap items-center justify-between gap-4 mb-8 pb-4 border-b border-stone-200 dark:border-stone-800">
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={onCancel}
            className="p-2 text-stone-500 hover:text-stone-900 dark:hover:text-white rounded-lg hover:bg-stone-100 dark:hover:bg-stone-800 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div>
            <h1 className="font-editorial text-2xl font-bold text-stone-900 dark:text-stone-100">
              {initialPost ? 'Edit Publication' : 'Compose New Publication'}
            </h1>
            <p className="text-xs text-stone-500">
              {initialPost ? `Updating story: ${initialPost.title}` : 'Drafting new story with real-time markdown preview'}
            </p>
          </div>
        </div>

        {/* Tab Switcher & Quick Save */}
        <div className="flex items-center gap-3">
          <div className="flex items-center bg-stone-200/60 dark:bg-stone-800 p-1 rounded-xl text-xs font-medium">
            <button
              type="button"
              onClick={() => setActiveTab('edit')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-colors ${
                activeTab === 'edit'
                  ? 'bg-white dark:bg-stone-700 text-stone-900 dark:text-white shadow-xs'
                  : 'text-stone-600 dark:text-stone-400'
              }`}
            >
              <FileText className="w-3.5 h-3.5" />
              <span>Editor</span>
            </button>
            <button
              type="button"
              onClick={() => setActiveTab('preview')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-colors ${
                activeTab === 'preview'
                  ? 'bg-white dark:bg-stone-700 text-stone-900 dark:text-white shadow-xs'
                  : 'text-stone-600 dark:text-stone-400'
              }`}
            >
              <Eye className="w-3.5 h-3.5" />
              <span>Live Preview</span>
            </button>
          </div>

          <button
            type="button"
            onClick={handleSubmit}
            className="inline-flex items-center gap-2 px-5 py-2 text-xs font-semibold text-white bg-amber-600 hover:bg-amber-700 rounded-xl shadow-sm transition-colors"
          >
            <Save className="w-4 h-4" />
            <span>{status === 'draft' ? 'Save Draft' : 'Publish Story'}</span>
          </button>
        </div>
      </div>

      {activeTab === 'edit' ? (
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Main Title & Subtitle */}
          <div className="p-6 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200/80 dark:border-stone-800 space-y-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-stone-500 mb-1.5">
                Article Title *
              </label>
              <input
                type="text"
                required
                placeholder="e.g. The Architecture of Calm Software"
                value={title}
                onChange={e => setTitle(e.target.value)}
                className="w-full text-xl sm:text-2xl font-editorial font-bold px-4 py-3 rounded-xl bg-stone-50 dark:bg-stone-800/80 border border-stone-200 dark:border-stone-700 text-stone-900 dark:text-white placeholder-stone-400 focus:outline-none focus:ring-2 focus:ring-amber-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-stone-500 mb-1.5">
                Subtitle / Deck (Optional)
              </label>
              <input
                type="text"
                placeholder="A compelling one-sentence hook expanding on the title"
                value={subtitle}
                onChange={e => setSubtitle(e.target.value)}
                className="w-full text-sm px-4 py-2.5 rounded-xl bg-stone-50 dark:bg-stone-800/80 border border-stone-200 dark:border-stone-700 text-stone-900 dark:text-white placeholder-stone-400 focus:outline-none focus:ring-2 focus:ring-amber-500"
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-stone-500 mb-1.5">
                  URL Slug
                </label>
                <div className="flex items-center rounded-xl bg-stone-50 dark:bg-stone-800/80 border border-stone-200 dark:border-stone-700 px-3 py-2 text-xs">
                  <span className="text-stone-400 font-mono">/story/</span>
                  <input
                    type="text"
                    value={slug}
                    onChange={e => setSlug(e.target.value)}
                    className="w-full bg-transparent text-stone-800 dark:text-stone-200 font-mono focus:outline-none ml-1"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-stone-500 mb-1.5">
                  Author Byline
                </label>
                <input
                  type="text"
                  value={authorName}
                  onChange={e => setAuthorName(e.target.value)}
                  className="w-full text-xs px-3 py-2 rounded-xl bg-stone-50 dark:bg-stone-800/80 border border-stone-200 dark:border-stone-700 text-stone-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-amber-500"
                />
              </div>
            </div>
          </div>

          {/* Classification & Status Row */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Category */}
            <div className="p-5 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200/80 dark:border-stone-800">
              <label className="block text-xs font-semibold uppercase tracking-wider text-stone-500 mb-2">
                Category
              </label>
              <select
                value={category}
                onChange={e => {
                  setCategory(e.target.value);
                  setCustomCategory('');
                }}
                className="w-full text-xs px-3 py-2.5 rounded-xl bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 text-stone-800 dark:text-stone-200 focus:outline-none focus:ring-2 focus:ring-amber-500 mb-2"
              >
                {settings.categories.map(c => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
              <input
                type="text"
                placeholder="Or create new category..."
                value={customCategory}
                onChange={e => setCustomCategory(e.target.value)}
                className="w-full text-xs px-3 py-1.5 rounded-lg bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 text-stone-800 dark:text-stone-200 focus:outline-none focus:ring-2 focus:ring-amber-500"
              />
            </div>

            {/* Publication Status & Featured */}
            <div className="p-5 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200/80 dark:border-stone-800">
              <label className="block text-xs font-semibold uppercase tracking-wider text-stone-500 mb-2">
                Publish Status
              </label>
              <div className="flex gap-2 mb-3">
                {(['published', 'draft', 'scheduled'] as PostStatus[]).map(st => (
                  <button
                    key={st}
                    type="button"
                    onClick={() => setStatus(st)}
                    className={`flex-1 py-1.5 text-xs font-semibold uppercase rounded-lg border transition-all ${
                      status === st
                        ? 'bg-amber-600 text-white border-amber-600 shadow-xs'
                        : 'bg-stone-50 dark:bg-stone-800 text-stone-600 dark:text-stone-400 border-stone-200 dark:border-stone-700'
                    }`}
                  >
                    {st}
                  </button>
                ))}
              </div>
              <label className="flex items-center gap-2 cursor-pointer pt-1">
                <input
                  type="checkbox"
                  checked={isFeatured}
                  onChange={e => setIsFeatured(e.target.checked)}
                  className="rounded text-amber-600 focus:ring-amber-500 w-4 h-4"
                />
                <span className="text-xs font-medium text-stone-700 dark:text-stone-300">
                  Feature on Homepage Hero
                </span>
              </label>
            </div>

            {/* Tags & Topics */}
            <div className="p-5 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200/80 dark:border-stone-800">
              <label className="block text-xs font-semibold uppercase tracking-wider text-stone-500 mb-2">
                Tags & Topics
              </label>
              <input
                type="text"
                placeholder="Python, Systems, Design"
                value={tagsInput}
                onChange={e => setTagsInput(e.target.value)}
                className="w-full text-xs px-3 py-2.5 rounded-xl bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 text-stone-800 dark:text-stone-200 focus:outline-none focus:ring-2 focus:ring-amber-500 mb-2"
              />
              <p className="text-[11px] text-stone-400">Separate multiple tags with commas.</p>
            </div>
          </div>

          {/* Featured Image Management */}
          <div className="p-6 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200/80 dark:border-stone-800 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-sm font-semibold text-stone-900 dark:text-stone-100 flex items-center gap-1.5">
                  <ImageIcon className="w-4 h-4 text-amber-600" />
                  <span>Featured Image Workflow</span>
                </h3>
                <p className="text-xs text-stone-500">Provide an image URL, pick from editorial presets, or upload a file directly.</p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-12 gap-4 items-center">
              {/* Image Preview */}
              <div className="md:col-span-4 relative rounded-xl overflow-hidden aspect-[16/10] bg-stone-100 dark:bg-stone-800 border border-stone-200 dark:border-stone-700">
                <img
                  src={featuredImage}
                  alt="Featured Preview"
                  className="w-full h-full object-cover"
                  onError={() => setFeaturedImage(CURATED_IMAGE_PRESETS[0].url)}
                />
              </div>

              {/* URL & Upload Inputs */}
              <div className="md:col-span-8 space-y-3">
                <div>
                  <label className="block text-xs font-medium text-stone-600 dark:text-stone-400 mb-1">
                    Image URL (Cloudinary, Supabase, or Unsplash)
                  </label>
                  <input
                    type="url"
                    value={featuredImage}
                    onChange={e => setFeaturedImage(e.target.value)}
                    placeholder="https://images.unsplash.com/..."
                    className="w-full text-xs px-3.5 py-2.5 rounded-xl bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 text-stone-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-amber-500"
                  />
                </div>

                <div className="flex items-center gap-3">
                  <label className="cursor-pointer inline-flex items-center gap-2 px-3 py-1.5 text-xs font-semibold text-stone-700 dark:text-stone-200 bg-stone-100 dark:bg-stone-800 hover:bg-stone-200 dark:hover:bg-stone-700 rounded-lg border border-stone-300/70 dark:border-stone-700 transition-colors">
                    <Upload className="w-3.5 h-3.5" />
                    <span>Upload from Computer</span>
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImageFileUpload}
                      className="hidden"
                    />
                  </label>
                  <span className="text-[11px] text-stone-400">Stores as persistent data directly in browser database.</span>
                </div>

                {/* Preset Chips */}
                <div>
                  <span className="text-[11px] font-medium text-stone-500 block mb-1.5">Editorial Presets:</span>
                  <div className="flex flex-wrap gap-1.5">
                    {CURATED_IMAGE_PRESETS.map((p, idx) => (
                      <button
                        key={idx}
                        type="button"
                        onClick={() => setFeaturedImage(p.url)}
                        className={`text-[11px] px-2.5 py-1 rounded-md border transition-colors ${
                          featuredImage === p.url
                            ? 'bg-amber-100 border-amber-300 text-amber-900 dark:bg-amber-950 dark:border-amber-800 dark:text-amber-300 font-medium'
                            : 'bg-stone-50 dark:bg-stone-800 border-stone-200 dark:border-stone-700 text-stone-600 dark:text-stone-400 hover:bg-stone-100'
                        }`}
                      >
                        {p.name}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Excerpt */}
          <div className="p-5 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200/80 dark:border-stone-800">
            <label className="block text-xs font-semibold uppercase tracking-wider text-stone-500 mb-1.5">
              Excerpt / Briefing (Used for cards and search summaries)
            </label>
            <textarea
              rows={2}
              placeholder="A concise summary of the article's core insight..."
              value={excerpt}
              onChange={e => setExcerpt(e.target.value)}
              className="w-full text-xs p-3 rounded-xl bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 text-stone-800 dark:text-stone-200 focus:outline-none focus:ring-2 focus:ring-amber-500"
            />
          </div>

          {/* Markdown Content Editor */}
          <div className="p-6 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200/80 dark:border-stone-800 space-y-3">
            <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-stone-200 dark:border-stone-800">
              <label className="text-xs font-semibold uppercase tracking-wider text-stone-500">
                Article Body (Markdown) *
              </label>

              {/* Formatting Toolbar */}
              <div className="flex flex-wrap items-center gap-1 bg-stone-100 dark:bg-stone-800 p-1 rounded-lg">
                <button
                  type="button"
                  onClick={() => insertFormatting('**', '**', 'bold text')}
                  className="p-1.5 rounded hover:bg-stone-200 dark:hover:bg-stone-700 text-stone-700 dark:text-stone-300"
                  title="Bold"
                >
                  <Bold className="w-3.5 h-3.5" />
                </button>
                <button
                  type="button"
                  onClick={() => insertFormatting('*', '*', 'italic text')}
                  className="p-1.5 rounded hover:bg-stone-200 dark:hover:bg-stone-700 text-stone-700 dark:text-stone-300"
                  title="Italic"
                >
                  <Italic className="w-3.5 h-3.5" />
                </button>
                <button
                  type="button"
                  onClick={() => insertFormatting('## ', '', 'Section Heading')}
                  className="p-1.5 rounded hover:bg-stone-200 dark:hover:bg-stone-700 text-stone-700 dark:text-stone-300"
                  title="Heading 2"
                >
                  <Heading1 className="w-3.5 h-3.5" />
                </button>
                <button
                  type="button"
                  onClick={() => insertFormatting('### ', '', 'Sub-section')}
                  className="p-1.5 rounded hover:bg-stone-200 dark:hover:bg-stone-700 text-stone-700 dark:text-stone-300"
                  title="Heading 3"
                >
                  <Heading2 className="w-3.5 h-3.5" />
                </button>
                <button
                  type="button"
                  onClick={() => insertFormatting('> ', '', 'Thoughtful quote')}
                  className="p-1.5 rounded hover:bg-stone-200 dark:hover:bg-stone-700 text-stone-700 dark:text-stone-300"
                  title="Blockquote"
                >
                  <Quote className="w-3.5 h-3.5" />
                </button>
                <button
                  type="button"
                  onClick={() => insertFormatting('```python\n', '\n```', '# Python code here')}
                  className="p-1.5 rounded hover:bg-stone-200 dark:hover:bg-stone-700 text-stone-700 dark:text-stone-300"
                  title="Code Block"
                >
                  <Code className="w-3.5 h-3.5" />
                </button>
                <button
                  type="button"
                  onClick={() => insertFormatting('- ', '', 'Bullet item')}
                  className="p-1.5 rounded hover:bg-stone-200 dark:hover:bg-stone-700 text-stone-700 dark:text-stone-300"
                  title="List"
                >
                  <List className="w-3.5 h-3.5" />
                </button>
                <button
                  type="button"
                  onClick={() => insertFormatting('1. ', '', 'Numbered item')}
                  className="p-1.5 rounded hover:bg-stone-200 dark:hover:bg-stone-700 text-stone-700 dark:text-stone-300"
                  title="Numbered List"
                >
                  <ListOrdered className="w-3.5 h-3.5" />
                </button>
                <button
                  type="button"
                  onClick={() => insertFormatting('[', '](https://example.com)', 'Link label')}
                  className="p-1.5 rounded hover:bg-stone-200 dark:hover:bg-stone-700 text-stone-700 dark:text-stone-300"
                  title="Link"
                >
                  <LinkIcon className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>

            <textarea
              id="markdown-editor-textarea"
              rows={16}
              required
              value={content}
              onChange={e => setContent(e.target.value)}
              placeholder="Write your story using Markdown. Supports ## Headings, > quotes, ```code blocks, lists, and images."
              className="w-full font-mono text-sm leading-relaxed p-4 rounded-xl bg-stone-50 dark:bg-stone-800/80 border border-stone-200 dark:border-stone-700 text-stone-900 dark:text-stone-100 placeholder-stone-400 focus:outline-none focus:ring-2 focus:ring-amber-500"
            />
          </div>

          {/* Submit Actions */}
          <div className="flex items-center justify-end gap-3 pt-4">
            <button
              type="button"
              onClick={onCancel}
              className="px-5 py-2.5 text-xs font-semibold text-stone-600 dark:text-stone-400 hover:bg-stone-100 dark:hover:bg-stone-800 rounded-xl transition-colors"
            >
              Discard Changes
            </button>
            <button
              type="submit"
              className="inline-flex items-center gap-2 px-6 py-2.5 text-xs font-semibold text-white bg-amber-600 hover:bg-amber-700 rounded-xl shadow-md transition-colors"
            >
              <Save className="w-4 h-4" />
              <span>{initialPost ? 'Update Publication' : 'Save & Publish Story'}</span>
            </button>
          </div>
        </form>
      ) : (
        /* LIVE PREVIEW TAB */
        <div className="p-8 sm:p-12 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 shadow-sm">
          <div className="max-w-3xl mx-auto">
            <div className="flex items-center gap-2 text-xs font-medium text-amber-700 dark:text-amber-400 uppercase mb-3">
              <span>{customCategory || category}</span>
              <span aria-hidden="true">·</span>
              <span>Preview Mode</span>
            </div>
            <h1 className="font-editorial text-3xl sm:text-5xl font-bold tracking-tight text-stone-900 dark:text-stone-100 mb-4">
              {title || 'Untitled Article'}
            </h1>
            {subtitle && (
              <p className="font-editorial text-xl italic text-stone-600 dark:text-stone-300 mb-6">
                {subtitle}
              </p>
            )}

            {featuredImage && (
              <div className="rounded-xl overflow-hidden my-6">
                <img src={featuredImage} alt="Preview" className="w-full h-auto max-h-[400px] object-cover" />
              </div>
            )}

            <div className="prose-editorial text-base sm:text-lg">
              {content ? (
                content.split('\n\n').map((p, i) => {
                  if (p.startsWith('## ')) {
                    return <h2 key={i} className="font-editorial text-2xl font-bold mt-6 mb-3">{p.replace('## ', '')}</h2>;
                  }
                  if (p.startsWith('> ')) {
                    return <blockquote key={i} className="border-l-4 border-amber-500 pl-4 py-1 italic my-4 bg-amber-50/50 dark:bg-amber-950/20">{p.replace('> ', '')}</blockquote>;
                  }
                  return <p key={i} className="my-3 text-stone-700 dark:text-stone-300 leading-relaxed">{p}</p>;
                })
              ) : (
                <p className="text-stone-400 italic">No content written yet...</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
