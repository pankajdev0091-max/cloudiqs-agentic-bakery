'use client';

import { useEffect, useState } from 'react';
import {
  Bot,
  MessageCircle,
  Clock,
  ThumbsUp,
  ArrowUpRight,
  ArrowDownRight,
  Activity,
  Zap,
} from 'lucide-react';
import AgentCard from './AgentCard';
import { DEMO_AGENTS } from '@/lib/agents';

interface StatCard {
  label: string;
  value: string;
  change: string;
  trend: 'up' | 'down';
  icon: React.ComponentType<{ className?: string }>;
  color: string;
}

const stats: StatCard[] = [
  {
    label: 'Total Agents',
    value: '5',
    change: '+2 this month',
    trend: 'up',
    icon: Bot,
    color: 'from-amber-500 to-orange-600',
  },
  {
    label: 'Active Conversations',
    value: '142',
    change: '+23% vs last week',
    trend: 'up',
    icon: MessageCircle,
    color: 'from-indigo-500 to-purple-600',
  },
  {
    label: 'Avg Response Time',
    value: '1.2s',
    change: '-0.3s improvement',
    trend: 'down',
    icon: Clock,
    color: 'from-emerald-500 to-teal-600',
  },
  {
    label: 'Satisfaction Rate',
    value: '96.4%',
    change: '+1.2% vs last month',
    trend: 'up',
    icon: ThumbsUp,
    color: 'from-pink-500 to-rose-600',
  },
];

const recentActivity = [
  {
    id: 1,
    agent: 'IT Helpdesk Assistant',
    action: 'Resolved password reset for john.doe@company.com',
    time: '2 min ago',
    type: 'success',
  },
  {
    id: 2,
    agent: 'Sales Qualification Agent',
    action: 'Qualified new lead: Acme Corp ($50K ARR potential)',
    time: '5 min ago',
    type: 'info',
  },
  {
    id: 3,
    agent: 'Customer Service Agent',
    action: 'Escalated order #4521 complaint to human agent',
    time: '12 min ago',
    type: 'warning',
  },
  {
    id: 4,
    agent: 'Finance Assistant',
    action: 'Generated Q4 runway analysis report',
    time: '18 min ago',
    type: 'success',
  },
  {
    id: 5,
    agent: 'Knowledge Base Agent',
    action: 'Answered API documentation query for deployment guide',
    time: '25 min ago',
    type: 'info',
  },
  {
    id: 6,
    agent: 'IT Helpdesk Assistant',
    action: 'Created ticket #8934 for VPN connectivity issue',
    time: '31 min ago',
    type: 'info',
  },
];

const activityTypeStyles: Record<string, string> = {
  success: 'bg-emerald-500',
  info: 'bg-blue-500',
  warning: 'bg-amber-500',
};

export default function Dashboard() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <div className="space-y-6">
      {/* Welcome banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900 to-amber-950/30 border border-slate-800 p-6 lg:p-8">
        <div className="relative z-10">
          <div className="flex items-center gap-2 mb-2">
            <Zap className="w-5 h-5 text-amber-500" />
            <span className="text-xs font-medium text-amber-500 uppercase tracking-wider">
              AWS AgentCore
            </span>
          </div>
          <h2 className="text-2xl lg:text-3xl font-bold text-white mb-2">
            Agentic AI Bakery Dashboard
          </h2>
          <p className="text-slate-400 text-sm lg:text-base max-w-xl">
            Monitor and manage your Strands Agents fleet. Deploy intelligent agents
            that handle customer inquiries, qualify leads, and automate workflows.
          </p>
        </div>
        {/* Decorative grid */}
        <div className="absolute top-0 right-0 w-64 h-full opacity-5">
          <div className="grid grid-cols-8 gap-2 p-4 h-full">
            {Array.from({ length: 64 }).map((_, i) => (
              <div key={i} className="w-full aspect-square bg-amber-500 rounded-sm" />
            ))}
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div
              key={stat.label}
              className={`glass-card p-5 transition-smooth hover:border-slate-700 ${
                mounted ? 'animate-fade-in' : ''
              }`}
            >
              <div className="flex items-start justify-between mb-3">
                <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${stat.color} flex items-center justify-center`}>
                  <Icon className="w-5 h-5 text-white" />
                </div>
                <div className={`flex items-center gap-1 text-xs ${
                  stat.trend === 'up' ? 'text-emerald-400' : 'text-emerald-400'
                }`}>
                  {stat.trend === 'up' ? (
                    <ArrowUpRight className="w-3 h-3" />
                  ) : (
                    <ArrowDownRight className="w-3 h-3" />
                  )}
                </div>
              </div>
              <p className="text-2xl font-bold text-white mb-1">{stat.value}</p>
              <p className="text-xs text-slate-500">{stat.label}</p>
              <p className="text-[11px] text-slate-600 mt-1">{stat.change}</p>
            </div>
          );
        })}
      </div>

      {/* Two column layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Quick Access Agents */}
        <div className="lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-base font-semibold text-white">Quick Access</h3>
            <a href="/agents" className="text-xs text-amber-500 hover:text-amber-400 transition-smooth">
              View all agents
            </a>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {DEMO_AGENTS.slice(0, 4).map((agent) => (
              <AgentCard key={agent.id} {...agent} compact />
            ))}
          </div>
        </div>

        {/* Recent Activity */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-base font-semibold text-white flex items-center gap-2">
              <Activity className="w-4 h-4 text-slate-500" />
              Recent Activity
            </h3>
          </div>
          <div className="glass-card divide-y divide-slate-800">
            {recentActivity.map((item) => (
              <div key={item.id} className="px-4 py-3 hover:bg-slate-800/50 transition-smooth">
                <div className="flex items-start gap-3">
                  <div className={`w-1.5 h-1.5 rounded-full mt-2 flex-shrink-0 ${activityTypeStyles[item.type]}`} />
                  <div className="min-w-0 flex-1">
                    <p className="text-xs font-medium text-slate-300 mb-0.5">{item.agent}</p>
                    <p className="text-xs text-slate-500 line-clamp-2">{item.action}</p>
                    <p className="text-[10px] text-slate-600 mt-1">{item.time}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
