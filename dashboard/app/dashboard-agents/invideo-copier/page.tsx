'use client';

import { useState, useEffect, Suspense } from 'react';
import { motion } from 'framer-motion';
import {
  Sparkles,
  Code,
  Download,
  RefreshCw,
  CheckCircle2,
  FileText,
  Folder,
  Settings,
  Play,
} from 'lucide-react';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';

function InVideoCopierContent() {
  const searchParams = useSearchParams();
  const [analysisId, setAnalysisId] = useState<string | null>(null);

  useEffect(() => {
    if (searchParams) {
      setAnalysisId(searchParams.get('analysis_id'));
    }
  }, [searchParams]);

  const [framework, setFramework] = useState('nextjs');
  const [outputPath, setOutputPath] = useState('./invideo-replica');
  const [includeAssets, setIncludeAssets] = useState(true);
  const [copying, setCopying] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleCopy = async () => {
    setCopying(true);
    try {
      const response = await fetch('http://localhost:8000/api/dashboard/invideo/copy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          analysis_id: analysisId,
          framework,
          output_path: outputPath,
          include_assets: includeAssets,
        }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Copy failed:', error);
    } finally {
      setCopying(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container py-8">
        {/* Header */}
        <div className="mb-8">
          <Link href="/dashboard-agents" className="text-blue-600 hover:text-blue-700 mb-4 inline-block">
            ← Back to Agents
          </Link>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">InVideo.io Copier</h1>
          <p className="text-gray-600">Create a Next.js replica of InVideo.io based on analysis</p>
        </div>

        {/* Configuration */}
        <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 mb-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Copy Configuration</h2>
          
          <div className="space-y-4">
            {analysisId && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p className="text-sm text-blue-700">
                  <strong>Analysis ID:</strong> {analysisId}
                </p>
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Framework</label>
              <select
                value={framework}
                onChange={(e) => setFramework(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="nextjs">Next.js</option>
                <option value="react">React</option>
                <option value="vue">Vue.js</option>
                <option value="svelte">Svelte</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Output Path</label>
              <input
                type="text"
                value={outputPath}
                onChange={(e) => setOutputPath(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="./invideo-replica"
              />
            </div>

            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={includeAssets}
                onChange={(e) => setIncludeAssets(e.target.checked)}
                className="rounded"
              />
              <span className="text-sm text-gray-700">Include Assets (images, fonts, etc.)</span>
            </label>

            <button
              onClick={handleCopy}
              disabled={copying}
              className="w-full btn-primary flex items-center justify-center gap-2"
            >
              {copying ? (
                <>
                  <RefreshCw className="w-5 h-5 animate-spin" />
                  Copying...
                </>
              ) : (
                <>
                  <Code className="w-5 h-5" />
                  Generate Next.js Replica
                </>
              )}
            </button>
          </div>
        </div>

        {/* Results */}
        {result && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6"
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-gray-900">Copy Results</h2>
              <div className="flex items-center gap-2 text-green-600">
                <CheckCircle2 className="w-5 h-5" />
                <span className="font-medium">Completed</span>
              </div>
            </div>

            <div className="grid md:grid-cols-3 gap-6 mb-6">
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <FileText className="w-5 h-5 text-gray-600" />
                  <span className="text-sm font-medium text-gray-700">Files Created</span>
                </div>
                <p className="text-2xl font-bold text-gray-900">{result.files_created || 0}</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <Code className="w-5 h-5 text-gray-600" />
                  <span className="text-sm font-medium text-gray-700">Components</span>
                </div>
                <p className="text-2xl font-bold text-gray-900">{result.components_created || 0}</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <Folder className="w-5 h-5 text-gray-600" />
                  <span className="text-sm font-medium text-gray-700">Pages</span>
                </div>
                <p className="text-2xl font-bold text-gray-900">{result.pages_created || 0}</p>
              </div>
            </div>

            <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
              <p className="text-sm text-green-700">
                <strong>Output Path:</strong> {result.output_path}
              </p>
              <p className="text-sm text-green-700 mt-1">
                Styles replicated: {result.styles_replicated ? 'Yes' : 'No'}
              </p>
            </div>

            <div className="flex gap-4">
              <button className="btn-primary flex items-center gap-2">
                <Download className="w-5 h-5" />
                Download Project
              </button>
              <button className="btn-secondary flex items-center gap-2">
                <Play className="w-5 h-5" />
                Preview
              </button>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}

export default function InVideoCopierPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="w-8 h-8 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    }>
      <InVideoCopierContent />
    </Suspense>
  );
}
