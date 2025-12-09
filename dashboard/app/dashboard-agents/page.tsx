'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Bot,
  Play,
  Pause,
  RefreshCw,
  CheckCircle2,
  XCircle,
  Clock,
  Zap,
  Search,
  Filter,
  Grid,
  List,
  Settings,
  Download,
  Eye,
  Code,
  Sparkles,
  Globe,
  Shield,
  Video,
  Image,
  Music,
  Type,
  Layers,
  BarChart3,
  Share2,
  Mic,
  Wand2,
  ChevronRight,
  ChevronDown,
  Activity,
  TrendingUp,
  AlertCircle,
  Info,
} from 'lucide-react';
import Link from 'next/link';

// Agent category configuration
const AGENT_CATEGORIES = {
  mcp_tool_management: {
    name: 'MCP & Tool Management',
    icon: Settings,
    color: 'blue',
    count: 8,
  },
  deep_research: {
    name: 'Deep Research & Open Source',
    icon: Code,
    color: 'purple',
    count: 8,
  },
  proof_validation: {
    name: 'Proof & Validation',
    icon: Shield,
    color: 'green',
    count: 6,
  },
  graphics_design: {
    name: 'Graphics & Design',
    icon: Image,
    color: 'pink',
    count: 6,
  },
  ui_ux: {
    name: 'UI/UX',
    icon: Layers,
    color: 'indigo',
    count: 6,
  },
  website_analysis: {
    name: 'Website Analysis & Copying',
    icon: Globe,
    color: 'orange',
    count: 6,
  },
  video_specific: {
    name: 'Video-Specific',
    icon: Video,
    color: 'red',
    count: 6,
  },
  development: {
    name: 'Development & Commissioning',
    icon: Zap,
    color: 'yellow',
    count: 4,
  },
  invideo_specialized: {
    name: 'InVideo.io Specialized',
    icon: Sparkles,
    color: 'cyan',
    count: 2,
  },
};

interface Agent {
  id: string;
  name: string;
  category: string;
  status: 'idle' | 'running' | 'completed' | 'error';
  last_run?: string;
  success_rate: number;
  total_runs: number;
}

export default function DashboardAgentsPage() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set());
  const [runningAgents, setRunningAgents] = useState<Set<string>>(new Set());

  // Fetch agents on mount
  useEffect(() => {
    fetchAgents();
    // Poll for updates every 5 seconds
    const interval = setInterval(fetchAgents, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchAgents = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/dashboard/agents');
      const data = await response.json();
      
      // Transform API response to Agent format
      const agentsList: Agent[] = Object.entries(data.agents || {}).map(([id, agent]: [string, any]) => ({
        id,
        name: agent.name || id.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
        category: agent.category || 'Unknown',
        status: agent.status || 'idle',
        last_run: null,
        success_rate: 0,
        total_runs: 0,
      }));
      
      setAgents(agentsList);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch agents:', error);
      setLoading(false);
    }
  };

  const runAgent = async (agentId: string) => {
    setRunningAgents(prev => new Set(prev).add(agentId));
    try {
      const response = await fetch(`http://localhost:8000/api/dashboard/agents/${agentId}/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ parameters: {}, timeout: 300 }),
      });
      const result = await response.json();
      console.log('Agent started:', result);
      
      // Refresh agents after a delay
      setTimeout(fetchAgents, 2000);
    } catch (error) {
      console.error('Failed to run agent:', error);
    } finally {
      setTimeout(() => {
        setRunningAgents(prev => {
          const next = new Set(prev);
          next.delete(agentId);
          return next;
        });
      }, 2000);
    }
  };

  const toggleCategory = (category: string) => {
    setExpandedCategories(prev => {
      const next = new Set(prev);
      if (next.has(category)) {
        next.delete(category);
      } else {
        next.add(category);
      }
      return next;
    });
  };

  // Filter agents
  const filteredAgents = agents.filter(agent => {
    const matchesSearch = agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         agent.id.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = !selectedCategory || agent.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  // Group agents by category
  const agentsByCategory = filteredAgents.reduce((acc, agent) => {
    const category = agent.category;
    if (!acc[category]) acc[category] = [];
    acc[category].push(agent);
    return acc;
  }, {} as Record<string, Agent[]>);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="w-8 h-8 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">Loading agents...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="container py-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard Agents</h1>
              <p className="text-gray-600">Manage all 50 specialized agents</p>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={() => setViewMode(viewMode === 'grid' ? 'list' : 'grid')}
                className="p-2 rounded-lg border border-gray-200 hover:bg-gray-50"
              >
                {viewMode === 'grid' ? <List className="w-5 h-5" /> : <Grid className="w-5 h-5" />}
              </button>
              <button
                onClick={fetchAgents}
                className="p-2 rounded-lg border border-gray-200 hover:bg-gray-50"
              >
                <RefreshCw className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Search and Filters */}
          <div className="flex items-center gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search agents..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <select
              value={selectedCategory || ''}
              onChange={(e) => setSelectedCategory(e.target.value || null)}
              className="px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Categories</option>
              {Object.entries(AGENT_CATEGORIES).map(([key, cat]) => (
                <option key={key} value={cat.name}>{cat.name}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Stats Bar */}
      <div className="bg-white border-b border-gray-200">
        <div className="container py-4">
          <div className="grid grid-cols-4 gap-6">
            <div>
              <p className="text-sm text-gray-600 mb-1">Total Agents</p>
              <p className="text-2xl font-bold text-gray-900">50</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Active</p>
              <p className="text-2xl font-bold text-green-600">
                {agents.filter(a => a.status === 'running').length}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Idle</p>
              <p className="text-2xl font-bold text-gray-600">
                {agents.filter(a => a.status === 'idle').length}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Categories</p>
              <p className="text-2xl font-bold text-blue-600">9</p>
            </div>
          </div>
        </div>
      </div>

      {/* Agents by Category */}
      <div className="container py-8">
        {Object.entries(AGENT_CATEGORIES).map(([categoryKey, category]) => {
          const categoryAgents = agentsByCategory[category.name] || [];
          if (categoryAgents.length === 0 && selectedCategory) return null;
          
          const isExpanded = expandedCategories.has(categoryKey);
          const Icon = category.icon;

          return (
            <motion.div
              key={categoryKey}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-6"
            >
              <div className="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
                {/* Category Header */}
                <button
                  onClick={() => toggleCategory(categoryKey)}
                  className="w-full flex items-center justify-between p-6 hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <div className={`w-12 h-12 rounded-xl bg-${category.color}-50 flex items-center justify-center`}>
                      <Icon className={`w-6 h-6 text-${category.color}-600`} />
                    </div>
                    <div className="text-left">
                      <h2 className="text-xl font-bold text-gray-900">{category.name}</h2>
                      <p className="text-sm text-gray-600">{categoryAgents.length} agents</p>
                    </div>
                  </div>
                  {isExpanded ? (
                    <ChevronDown className="w-5 h-5 text-gray-400 rotate-180 transition-transform" />
                  ) : (
                    <ChevronRight className="w-5 h-5 text-gray-400 transition-transform" />
                  )}
                </button>

                {/* Agents List */}
                <AnimatePresence>
                  {isExpanded && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      className="overflow-hidden"
                    >
                      <div className="p-6 pt-0">
                        {categoryAgents.length > 0 ? (
                          <div className={viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4' : 'space-y-3'}>
                            {categoryAgents.map((agent) => (
                              <AgentCard
                                key={agent.id}
                                agent={agent}
                                onRun={() => runAgent(agent.id)}
                                isRunning={runningAgents.has(agent.id)}
                              />
                            ))}
                          </div>
                        ) : (
                          <div className="text-center py-8 text-gray-500">
                            No agents found in this category
                          </div>
                        )}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* InVideo.io Special Actions */}
      <div className="container pb-8">
        <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl p-8 text-white">
          <h2 className="text-2xl font-bold mb-4">InVideo.io Specialized Tools</h2>
          <p className="text-blue-100 mb-6">Analyze and replicate InVideo.io website structure</p>
          <div className="flex gap-4">
            <Link
              href="/dashboard-agents/invideo-analyzer"
              className="px-6 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
            >
              Analyze InVideo.io
            </Link>
            <Link
              href="/dashboard-agents/invideo-copier"
              className="px-6 py-3 bg-blue-600/20 text-white border-2 border-white rounded-lg font-semibold hover:bg-blue-600/30 transition-colors"
            >
              Copy to Next.js
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

// Agent Card Component
function AgentCard({ agent, onRun, isRunning }: { agent: Agent; onRun: () => void; isRunning: boolean }) {
  const statusColors = {
    idle: 'bg-gray-100 text-gray-600',
    running: 'bg-blue-100 text-blue-600',
    completed: 'bg-green-100 text-green-600',
    error: 'bg-red-100 text-red-600',
  };

  const statusIcons = {
    idle: Clock,
    running: RefreshCw,
    completed: CheckCircle2,
    error: XCircle,
  };

  const StatusIcon = statusIcons[agent.status];

  return (
    <motion.div
      whileHover={{ y: -2 }}
      className="bg-white border border-gray-200 rounded-xl p-4 hover:shadow-md transition-shadow"
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h3 className="font-semibold text-gray-900 mb-1">{agent.name}</h3>
          <p className="text-xs text-gray-500">{agent.id}</p>
        </div>
        <div className={`px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1 ${statusColors[agent.status]}`}>
          <StatusIcon className={`w-3 h-3 ${agent.status === 'running' ? 'animate-spin' : ''}`} />
          {agent.status}
        </div>
      </div>

      <div className="flex items-center justify-between">
        <div className="text-xs text-gray-600">
          {agent.total_runs > 0 && (
            <span>Success: {Math.round(agent.success_rate * 100)}%</span>
          )}
        </div>
        <button
          onClick={onRun}
          disabled={isRunning || agent.status === 'running'}
          className="px-3 py-1.5 bg-blue-600 text-white text-xs font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1"
        >
          {isRunning || agent.status === 'running' ? (
            <>
              <RefreshCw className="w-3 h-3 animate-spin" />
              Running
            </>
          ) : (
            <>
              <Play className="w-3 h-3" />
              Run
            </>
          )}
        </button>
      </div>
    </motion.div>
  );
}
