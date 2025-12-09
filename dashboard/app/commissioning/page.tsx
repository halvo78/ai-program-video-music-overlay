'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  CheckCircle2,
  XCircle,
  AlertTriangle,
  RefreshCw,
  Play,
  Pause,
  Clock,
  Cpu,
  Database,
  Globe,
  Shield,
  Zap,
  Bot,
  Server,
  Wifi,
  WifiOff,
  Activity,
  BarChart3,
  Code,
  FileCode,
  Terminal,
  Bug,
  Sparkles,
  Eye,
  Network,
  HardDrive,
  MemoryStick,
  Gauge,
  ChevronRight,
  ChevronDown,
  ExternalLink,
  Copy,
  Download,
  Filter,
  Search,
  Settings,
  Layers,
  GitBranch,
  TestTube,
  Rocket,
  Target,
  Award,
  TrendingUp,
  AlertCircle,
  Info,
} from 'lucide-react'
import Sidebar from '@/components/layout/Sidebar'
import Header from '@/components/layout/Header'
import Card, { CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import Button from '@/components/ui/Button'
import { api } from '@/lib/api'

// Test categories
const testCategories = [
  {
    id: 'api',
    name: 'API Endpoints',
    icon: Globe,
    tests: [
      { name: 'Health Check', endpoint: '/health', status: 'passed', time: 45 },
      { name: 'Status Endpoint', endpoint: '/status', status: 'passed', time: 123 },
      { name: 'Create Video', endpoint: '/api/create', status: 'passed', time: 892 },
      { name: 'Get Agents', endpoint: '/api/agents', status: 'passed', time: 67 },
      { name: 'Social Publish', endpoint: '/api/social/publish', status: 'warning', time: 2340 },
    ],
  },
  {
    id: 'agents',
    name: 'AI Agents',
    icon: Bot,
    tests: [
      { name: 'Orchestrator Agent', status: 'passed', time: 156 },
      { name: 'Video Generation Agent', status: 'passed', time: 234 },
      { name: 'Music Generation Agent', status: 'passed', time: 189 },
      { name: 'Image Generation Agent', status: 'passed', time: 145 },
      { name: 'Voice Agent', status: 'passed', time: 98 },
      { name: 'Content Analysis Agent', status: 'passed', time: 112 },
      { name: 'Editing Agent', status: 'passed', time: 167 },
      { name: 'Optimization Agent', status: 'passed', time: 89 },
      { name: 'Analytics Agent', status: 'passed', time: 134 },
      { name: 'Safety Agent', status: 'passed', time: 78 },
    ],
  },
  {
    id: 'providers',
    name: 'AI Providers',
    icon: Cpu,
    tests: [
      { name: 'Together.ai Connection', status: 'passed', time: 234 },
      { name: 'HuggingFace API', status: 'passed', time: 189 },
      { name: 'FLUX Image Generation', status: 'passed', time: 456 },
      { name: 'OpenAI Integration', status: 'passed', time: 167 },
      { name: 'Replicate Models', status: 'warning', time: 1890 },
    ],
  },
  {
    id: 'social',
    name: 'Social Media',
    icon: Network,
    tests: [
      { name: 'TikTok API', status: 'passed', time: 345 },
      { name: 'Instagram API', status: 'passed', time: 289 },
      { name: 'YouTube API', status: 'passed', time: 234 },
      { name: 'Twitter/X API', status: 'passed', time: 178 },
      { name: 'Facebook API', status: 'failed', time: 0 },
    ],
  },
  {
    id: 'database',
    name: 'Database',
    icon: Database,
    tests: [
      { name: 'PostgreSQL Connection', status: 'passed', time: 23 },
      { name: 'Redis Cache', status: 'passed', time: 12 },
      { name: 'Query Performance', status: 'passed', time: 45 },
      { name: 'Data Integrity', status: 'passed', time: 234 },
    ],
  },
  {
    id: 'security',
    name: 'Security',
    icon: Shield,
    tests: [
      { name: 'API Authentication', status: 'passed', time: 89 },
      { name: 'Rate Limiting', status: 'passed', time: 156 },
      { name: 'Input Validation', status: 'passed', time: 67 },
      { name: 'CORS Configuration', status: 'passed', time: 34 },
      { name: 'SSL/TLS', status: 'passed', time: 12 },
    ],
  },
]

// System metrics
const systemMetrics = [
  { name: 'CPU Usage', value: 23, unit: '%', icon: Cpu, color: 'cyan' },
  { name: 'Memory', value: 4.2, unit: 'GB', icon: MemoryStick, color: 'violet' },
  { name: 'Disk I/O', value: 156, unit: 'MB/s', icon: HardDrive, color: 'fuchsia' },
  { name: 'Network', value: 89, unit: 'Mbps', icon: Wifi, color: 'emerald' },
]

// Status badge component
function StatusBadge({ status }: { status: string }) {
  const config = {
    passed: { icon: CheckCircle2, color: 'emerald', text: 'Passed' },
    failed: { icon: XCircle, color: 'red', text: 'Failed' },
    warning: { icon: AlertTriangle, color: 'amber', text: 'Warning' },
    running: { icon: RefreshCw, color: 'blue', text: 'Running' },
    pending: { icon: Clock, color: 'gray', text: 'Pending' },
  }[status] || { icon: AlertCircle, color: 'gray', text: status }

  const Icon = config.icon

  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-${config.color}-500/20 text-${config.color}-400`}>
      <Icon className={`w-3 h-3 ${status === 'running' ? 'animate-spin' : ''}`} />
      {config.text}
    </span>
  )
}

// Test category card
function TestCategoryCard({ category, isExpanded, onToggle }: any) {
  const Icon = category.icon
  const passedCount = category.tests.filter((t: any) => t.status === 'passed').length
  const failedCount = category.tests.filter((t: any) => t.status === 'failed').length
  const warningCount = category.tests.filter((t: any) => t.status === 'warning').length
  const totalTime = category.tests.reduce((sum: number, t: any) => sum + t.time, 0)

  const overallStatus = failedCount > 0 ? 'failed' : warningCount > 0 ? 'warning' : 'passed'

  return (
    <motion.div
      layout
      className={`rounded-2xl border transition-all ${
        overallStatus === 'passed'
          ? 'bg-emerald-500/5 border-emerald-500/20'
          : overallStatus === 'warning'
          ? 'bg-amber-500/5 border-amber-500/20'
          : 'bg-red-500/5 border-red-500/20'
      }`}
    >
      {/* Header */}
      <motion.button
        onClick={onToggle}
        className="w-full p-5 flex items-center justify-between text-left"
      >
        <div className="flex items-center gap-4">
          <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${
            overallStatus === 'passed'
              ? 'bg-emerald-500/20'
              : overallStatus === 'warning'
              ? 'bg-amber-500/20'
              : 'bg-red-500/20'
          }`}>
            <Icon className={`w-6 h-6 ${
              overallStatus === 'passed'
                ? 'text-emerald-400'
                : overallStatus === 'warning'
                ? 'text-amber-400'
                : 'text-red-400'
            }`} />
          </div>
          <div>
            <h3 className="font-semibold text-lg">{category.name}</h3>
            <p className="text-sm text-white/50">
              {category.tests.length} tests • {totalTime}ms total
            </p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-3 text-sm">
            {passedCount > 0 && (
              <span className="flex items-center gap-1 text-emerald-400">
                <CheckCircle2 className="w-4 h-4" />
                {passedCount}
              </span>
            )}
            {warningCount > 0 && (
              <span className="flex items-center gap-1 text-amber-400">
                <AlertTriangle className="w-4 h-4" />
                {warningCount}
              </span>
            )}
            {failedCount > 0 && (
              <span className="flex items-center gap-1 text-red-400">
                <XCircle className="w-4 h-4" />
                {failedCount}
              </span>
            )}
          </div>
          <motion.div
            animate={{ rotate: isExpanded ? 180 : 0 }}
            transition={{ duration: 0.2 }}
          >
            <ChevronDown className="w-5 h-5 text-white/40" />
          </motion.div>
        </div>
      </motion.button>

      {/* Expanded content */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="px-5 pb-5">
              <div className="space-y-2">
                {category.tests.map((test: any, i: number) => (
                  <motion.div
                    key={test.name}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.03 * i }}
                    className="flex items-center justify-between p-3 rounded-xl bg-white/5"
                  >
                    <div className="flex items-center gap-3">
                      <div className={`w-2 h-2 rounded-full ${
                        test.status === 'passed' ? 'bg-emerald-400' :
                        test.status === 'warning' ? 'bg-amber-400' : 'bg-red-400'
                      }`} />
                      <span className="font-medium">{test.name}</span>
                      {test.endpoint && (
                        <code className="text-xs text-white/40 bg-white/10 px-2 py-0.5 rounded">
                          {test.endpoint}
                        </code>
                      )}
                    </div>
                    <div className="flex items-center gap-4">
                      <span className="text-sm text-white/50">{test.time}ms</span>
                      <StatusBadge status={test.status} />
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}

// Metric card
function MetricCard({ metric }: any) {
  const Icon = metric.icon
  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      className="p-4 rounded-xl bg-white/5 border border-white/10"
    >
      <div className="flex items-center justify-between mb-3">
        <Icon className={`w-5 h-5 text-${metric.color}-400`} />
        <span className="text-xs text-white/40">{metric.name}</span>
      </div>
      <p className="text-2xl font-bold">
        {metric.value}
        <span className="text-sm text-white/50 ml-1">{metric.unit}</span>
      </p>
      <div className="mt-2 h-1.5 bg-white/10 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${Math.min(metric.value, 100)}%` }}
          transition={{ duration: 1, ease: 'easeOut' }}
          className={`h-full bg-gradient-to-r from-${metric.color}-500 to-${metric.color}-400 rounded-full`}
        />
      </div>
    </motion.div>
  )
}

export default function CommissioningPage() {
  const [expandedCategories, setExpandedCategories] = useState<string[]>(['api'])
  const [isRunning, setIsRunning] = useState(false)
  const [lastRun, setLastRun] = useState<Date | null>(null)
  const [filter, setFilter] = useState<'all' | 'passed' | 'failed' | 'warning'>('all')

  const toggleCategory = (id: string) => {
    setExpandedCategories(prev =>
      prev.includes(id) ? prev.filter(c => c !== id) : [...prev, id]
    )
  }

  const runAllTests = async () => {
    setIsRunning(true)
    // Simulate test run
    await new Promise(resolve => setTimeout(resolve, 3000))
    setIsRunning(false)
    setLastRun(new Date())
  }

  // Calculate overall stats
  const allTests = testCategories.flatMap(c => c.tests)
  const totalTests = allTests.length
  const passedTests = allTests.filter(t => t.status === 'passed').length
  const failedTests = allTests.filter(t => t.status === 'failed').length
  const warningTests = allTests.filter(t => t.status === 'warning').length
  const successRate = Math.round((passedTests / totalTests) * 100)

  // Filter categories
  const filteredCategories = filter === 'all'
    ? testCategories
    : testCategories.map(cat => ({
        ...cat,
        tests: cat.tests.filter(t => t.status === filter)
      })).filter(cat => cat.tests.length > 0)

  return (
    <div className="flex min-h-screen bg-[#0a0a0f]">
      <Sidebar />

      <main className="flex-1 overflow-auto">
        <Header title="Commissioning" subtitle="System validation and testing" />

        <div className="p-6 space-y-6">
          {/* Hero Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-emerald-600/20 via-cyan-600/10 to-violet-600/20 border border-white/10 p-8"
          >
            {/* Animated background */}
            <div className="absolute inset-0">
              <motion.div
                className="absolute w-96 h-96 rounded-full bg-emerald-500/20 blur-3xl"
                animate={{
                  scale: [1, 1.2, 1],
                  opacity: [0.3, 0.5, 0.3],
                }}
                transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
                style={{ top: '-20%', right: '10%' }}
              />
            </div>

            <div className="relative z-10">
              <div className="flex items-center justify-between mb-8">
                <div>
                  <div className="flex items-center gap-3 mb-2">
                    <h1 className="text-3xl font-display font-bold">
                      System Commissioning
                    </h1>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                      successRate >= 90
                        ? 'bg-emerald-500/20 text-emerald-400'
                        : successRate >= 70
                        ? 'bg-amber-500/20 text-amber-400'
                        : 'bg-red-500/20 text-red-400'
                    }`}>
                      {successRate}% Success Rate
                    </span>
                  </div>
                  <p className="text-white/60">
                    {lastRun
                      ? `Last run: ${lastRun.toLocaleString()}`
                      : 'Run tests to validate system integrity'}
                  </p>
                </div>
                <div className="flex gap-3">
                  <Button
                    variant="glass"
                    leftIcon={<Download className="w-4 h-4" />}
                  >
                    Export Report
                  </Button>
                  <Button
                    variant="gradient"
                    leftIcon={isRunning ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
                    onClick={runAllTests}
                    disabled={isRunning}
                  >
                    {isRunning ? 'Running Tests...' : 'Run All Tests'}
                  </Button>
                </div>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-4 gap-4">
                {[
                  { label: 'Total Tests', value: totalTests, icon: TestTube, color: 'violet' },
                  { label: 'Passed', value: passedTests, icon: CheckCircle2, color: 'emerald' },
                  { label: 'Warnings', value: warningTests, icon: AlertTriangle, color: 'amber' },
                  { label: 'Failed', value: failedTests, icon: XCircle, color: 'red' },
                ].map((stat, i) => (
                  <motion.div
                    key={stat.label}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 * i }}
                    className="p-5 rounded-2xl bg-white/5 backdrop-blur-sm border border-white/10"
                  >
                    <div className="flex items-center gap-3 mb-3">
                      <div className={`w-10 h-10 rounded-xl bg-${stat.color}-500/20 flex items-center justify-center`}>
                        <stat.icon className={`w-5 h-5 text-${stat.color}-400`} />
                      </div>
                    </div>
                    <p className="text-3xl font-bold mb-1">{stat.value}</p>
                    <p className="text-sm text-white/50">{stat.label}</p>
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.div>

          {/* System Metrics */}
          <div>
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Gauge className="w-5 h-5 text-cyan-400" />
              System Metrics
            </h2>
            <div className="grid grid-cols-4 gap-4">
              {systemMetrics.map((metric, i) => (
                <motion.div
                  key={metric.name}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.05 * i }}
                >
                  <MetricCard metric={metric} />
                </motion.div>
              ))}
            </div>
          </div>

          {/* Filter Bar */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Filter className="w-4 h-4 text-white/40" />
              {['all', 'passed', 'warning', 'failed'].map((f) => (
                <Button
                  key={f}
                  variant={filter === f ? 'primary' : 'ghost'}
                  size="sm"
                  onClick={() => setFilter(f as any)}
                >
                  {f.charAt(0).toUpperCase() + f.slice(1)}
                </Button>
              ))}
            </div>
            <div className="flex items-center gap-3">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-white/40" />
                <input
                  type="text"
                  placeholder="Search tests..."
                  className="pl-10 pr-4 py-2 bg-white/5 border border-white/10 rounded-xl text-sm focus:outline-none focus:border-violet-500/50 w-64"
                />
              </div>
              <Button variant="ghost" size="sm" leftIcon={<Settings className="w-4 h-4" />}>
                Configure
              </Button>
            </div>
          </div>

          {/* Test Categories */}
          <div className="space-y-4">
            {filteredCategories.map((category, i) => (
              <motion.div
                key={category.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.05 * i }}
              >
                <TestCategoryCard
                  category={category}
                  isExpanded={expandedCategories.includes(category.id)}
                  onToggle={() => toggleCategory(category.id)}
                />
              </motion.div>
            ))}
          </div>

          {/* Quick Actions */}
          <div className="grid md:grid-cols-3 gap-4">
            {[
              {
                title: 'Generate Report',
                description: 'Create detailed PDF report of all test results',
                icon: FileCode,
                gradient: 'from-violet-500 to-fuchsia-600',
              },
              {
                title: 'View Logs',
                description: 'Access detailed system and error logs',
                icon: Terminal,
                gradient: 'from-cyan-500 to-blue-600',
              },
              {
                title: 'Debug Mode',
                description: 'Enable verbose logging for troubleshooting',
                icon: Bug,
                gradient: 'from-amber-500 to-orange-600',
              },
            ].map((action, i) => (
              <motion.button
                key={action.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 * i }}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="p-5 rounded-2xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all text-left group"
              >
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${action.gradient} flex items-center justify-center mb-4`}>
                  <action.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="font-semibold mb-1">{action.title}</h3>
                <p className="text-sm text-white/50">{action.description}</p>
                <ChevronRight className="w-5 h-5 text-white/20 group-hover:text-white/40 mt-3 transition-colors" />
              </motion.button>
            ))}
          </div>
        </div>
      </main>
    </div>
  )
}
