'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Sparkles,
  Globe,
  Code,
  Image,
  FileText,
  Download,
  Play,
  RefreshCw,
  CheckCircle2,
  AlertCircle,
} from 'lucide-react';
import Link from 'next/link';

export default function InVideoAnalyzerPage() {
  const [url, setUrl] = useState('https://invideo.io');
  const [depth, setDepth] = useState(3);
  const [extractComponents, setExtractComponents] = useState(true);
  const [extractStyles, setExtractStyles] = useState(true);
  const [extractFeatures, setExtractFeatures] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleAnalyze = async () => {
    setAnalyzing(true);
    try {
      const response = await fetch('http://localhost:8000/api/dashboard/invideo/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          url,
          depth,
          extract_components: extractComponents,
          extract_styles: extractStyles,
          extract_features: extractFeatures,
        }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setAnalyzing(false);
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
          <h1 className="text-3xl font-bold text-gray-900 mb-2">InVideo.io Analyzer</h1>
          <p className="text-gray-600">Analyze InVideo.io structure, components, styles, and features</p>
        </div>

        {/* Configuration */}
        <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 mb-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Analysis Configuration</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Website URL</label>
              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="https://invideo.io"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Analysis Depth: {depth}
              </label>
              <input
                type="range"
                min="1"
                max="5"
                value={depth}
                onChange={(e) => setDepth(Number(e.target.value))}
                className="w-full"
              />
            </div>

            <div className="space-y-2">
              <label className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={extractComponents}
                  onChange={(e) => setExtractComponents(e.target.checked)}
                  className="rounded"
                />
                <span className="text-sm text-gray-700">Extract Components</span>
              </label>
              <label className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={extractStyles}
                  onChange={(e) => setExtractStyles(e.target.checked)}
                  className="rounded"
                />
                <span className="text-sm text-gray-700">Extract Styles</span>
              </label>
              <label className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={extractFeatures}
                  onChange={(e) => setExtractFeatures(e.target.checked)}
                  className="rounded"
                />
                <span className="text-sm text-gray-700">Extract Features</span>
              </label>
            </div>

            <button
              onClick={handleAnalyze}
              disabled={analyzing}
              className="w-full btn-primary flex items-center justify-center gap-2"
            >
              {analyzing ? (
                <>
                  <RefreshCw className="w-5 h-5 animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5" />
                  Start Analysis
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
              <h2 className="text-xl font-bold text-gray-900">Analysis Results</h2>
              <div className="flex items-center gap-2 text-green-600">
                <CheckCircle2 className="w-5 h-5" />
                <span className="font-medium">Completed</span>
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              {/* Structure */}
              <div>
                <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                  <Code className="w-5 h-5" />
                  Structure
                </h3>
                <div className="bg-gray-50 rounded-lg p-4 space-y-2">
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Pages Found:</p>
                    <p className="text-sm font-medium">{result.structure?.pages?.length || 0}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Components:</p>
                    <p className="text-sm font-medium">{result.structure?.components?.length || 0}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Routes:</p>
                    <p className="text-sm font-medium">{result.structure?.routes?.length || 0}</p>
                  </div>
                </div>
              </div>

              {/* Styles */}
              <div>
                <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                  <Image className="w-5 h-5" />
                  Styles
                </h3>
                <div className="bg-gray-50 rounded-lg p-4 space-y-2">
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Colors:</p>
                    <div className="flex gap-2">
                      {result.styles?.colors?.map((color: string, i: number) => (
                        <div
                          key={i}
                          className="w-8 h-8 rounded border border-gray-200"
                          style={{ backgroundColor: color }}
                        />
                      ))}
                    </div>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Fonts:</p>
                    <p className="text-sm font-medium">{result.styles?.fonts?.join(', ') || 'N/A'}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Features */}
            {result.features && (
              <div className="mt-6">
                <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                  <FileText className="w-5 h-5" />
                  Features Detected
                </h3>
                <div className="grid md:grid-cols-2 gap-2">
                  {result.features.map((feature: string, i: number) => (
                    <div key={i} className="bg-blue-50 text-blue-700 px-3 py-2 rounded-lg text-sm">
                      {feature}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Actions */}
            <div className="mt-6 flex gap-4">
              <Link
                href={`/dashboard-agents/invideo-copier?analysis_id=${result.analysis_id}`}
                className="btn-primary flex items-center gap-2"
              >
                <Download className="w-5 h-5" />
                Copy to Next.js
              </Link>
              <button className="btn-secondary flex items-center gap-2">
                <Download className="w-5 h-5" />
                Export Analysis
              </button>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}
