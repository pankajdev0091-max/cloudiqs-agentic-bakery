'use client';

import Header from '@/components/Header';
import {
  BarChart3,
  TrendingUp,
  Clock,
  Users,
  MessageCircle,
  Star,
  ArrowUpRight,
} from 'lucide-react';
import { DEMO_AGENTS } from '@/lib/agents';

const weeklyData = [
  { day: 'Mon', conversations: 245, satisfaction: 96 },
  { day: 'Tue', conversations: 312, satisfaction: 97 },
  { day: 'Wed', conversations: 287, satisfaction: 95 },
  { day: 'Thu', conversations: 356, satisfaction: 98 },
  { day: 'Fri', conversations: 298, satisfaction: 96 },
  { day: 'Sat', conversations: 134, satisfaction: 94 },
  { day: 'Sun', conversations: 98, satisfaction: 95 },
];

const maxConversations = Math.max(...weeklyData.map((d) => d.conversations));

export default function AnalyticsPage() {
  const totalConversations = DEMO_AGENTS.reduce((sum, a) => sum + a.conversations, 0);
  const avgRating = (
    DEMO_AGENTS.reduce((sum, a) => sum + a.rating, 0) / DEMO_AGENTS.length
  ).toFixed(1);

  return (
    <div className="flex flex-col min-h-screen">
      <Header title="Analytics" subtitle="Performance metrics and insights" />

      <div className="flex-1 p-4 lg:p-8 space-y-6">
        {/* Summary cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="glass-card p-5">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-9 h-9 rounded-lg bg-indigo-500/10 flex items-center justify-center">
                <MessageCircle className="w-4 h-4 text-indigo-400" />
              </div>
              <div>
                <p className="text-xs text-slate-500">Total Conversations</p>
                <p className="text-xl font-bold text-white">{totalConversations.toLocaleString()}</p>
              </div>
            </div>
            <div className="flex items-center gap-1 text-xs text-emerald-400">
              <ArrowUpRight className="w-3 h-3" />
              <span>+18.2% from last month</span>
            </div>
          </div>

          <div className="glass-card p-5">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-9 h-9 rounded-lg bg-amber-500/10 flex items-center justify-center">
                <Star className="w-4 h-4 text-amber-400" />
              </div>
              <div>
                <p className="text-xs text-slate-500">Avg Satisfaction</p>
                <p className="text-xl font-bold text-white">{avgRating}/5.0</p>
              </div>
            </div>
            <div className="flex items-center gap-1 text-xs text-emerald-400">
              <ArrowUpRight className="w-3 h-3" />
              <span>+0.3 from last month</span>
            </div>
          </div>

          <div className="glass-card p-5">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-9 h-9 rounded-lg bg-emerald-500/10 flex items-center justify-center">
                <Clock className="w-4 h-4 text-emerald-400" />
              </div>
              <div>
                <p className="text-xs text-slate-500">Avg Response Time</p>
                <p className="text-xl font-bold text-white">1.2s</p>
              </div>
            </div>
            <div className="flex items-center gap-1 text-xs text-emerald-400">
              <ArrowUpRight className="w-3 h-3" />
              <span>-0.3s improvement</span>
            </div>
          </div>

          <div className="glass-card p-5">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-9 h-9 rounded-lg bg-purple-500/10 flex items-center justify-center">
                <Users className="w-4 h-4 text-purple-400" />
              </div>
              <div>
                <p className="text-xs text-slate-500">Resolution Rate</p>
                <p className="text-xl font-bold text-white">94.7%</p>
              </div>
            </div>
            <div className="flex items-center gap-1 text-xs text-emerald-400">
              <ArrowUpRight className="w-3 h-3" />
              <span>+2.1% from last month</span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Weekly Conversations Chart */}
          <div className="lg:col-span-2 glass-card p-6">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-base font-semibold text-white flex items-center gap-2">
                  <BarChart3 className="w-4 h-4 text-slate-500" />
                  Weekly Conversations
                </h3>
                <p className="text-xs text-slate-500 mt-0.5">Last 7 days</p>
              </div>
              <div className="flex items-center gap-4 text-xs">
                <div className="flex items-center gap-1.5">
                  <div className="w-2.5 h-2.5 rounded-sm bg-amber-500" />
                  <span className="text-slate-500">Conversations</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <div className="w-2.5 h-2.5 rounded-sm bg-emerald-500" />
                  <span className="text-slate-500">Satisfaction %</span>
                </div>
              </div>
            </div>

            {/* Simple bar chart */}
            <div className="flex items-end gap-3 h-48">
              {weeklyData.map((d) => (
                <div key={d.day} className="flex-1 flex flex-col items-center gap-2">
                  <div className="w-full flex flex-col items-center gap-1 flex-1 justify-end">
                    <span className="text-[10px] text-slate-500">{d.conversations}</span>
                    <div
                      className="w-full bg-amber-500/20 rounded-t-md relative overflow-hidden"
                      style={{
                        height: `${(d.conversations / maxConversations) * 100}%`,
                        minHeight: '8px',
                      }}
                    >
                      <div className="absolute inset-0 bg-gradient-to-t from-amber-500/40 to-amber-500/10" />
                    </div>
                  </div>
                  <span className="text-[11px] text-slate-600">{d.day}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Agent Performance Ranking */}
          <div className="glass-card p-6">
            <div className="flex items-center gap-2 mb-4">
              <TrendingUp className="w-4 h-4 text-slate-500" />
              <h3 className="text-base font-semibold text-white">Agent Rankings</h3>
            </div>
            <div className="space-y-3">
              {[...DEMO_AGENTS]
                .sort((a, b) => b.rating - a.rating)
                .map((agent, index) => (
                  <div key={agent.id} className="flex items-center gap-3 p-2.5 rounded-lg hover:bg-slate-800/50 transition-smooth">
                    <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                      index === 0
                        ? 'bg-amber-500/20 text-amber-400'
                        : index === 1
                        ? 'bg-slate-400/20 text-slate-300'
                        : index === 2
                        ? 'bg-amber-700/20 text-amber-600'
                        : 'bg-slate-800 text-slate-500'
                    }`}>
                      {index + 1}
                    </span>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-white truncate">{agent.name}</p>
                      <p className="text-[10px] text-slate-500">{agent.conversations.toLocaleString()} conversations</p>
                    </div>
                    <div className="flex items-center gap-1">
                      <Star className="w-3 h-3 text-amber-500" />
                      <span className="text-xs font-medium text-white">{agent.rating}</span>
                    </div>
                  </div>
                ))}
            </div>
          </div>
        </div>

        {/* Agent breakdown table */}
        <div className="glass-card overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-800">
            <h3 className="text-base font-semibold text-white">Agent Performance Breakdown</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-800">
                  <th className="text-left text-xs font-medium text-slate-500 uppercase tracking-wider px-6 py-3">
                    Agent
                  </th>
                  <th className="text-left text-xs font-medium text-slate-500 uppercase tracking-wider px-6 py-3">
                    Type
                  </th>
                  <th className="text-right text-xs font-medium text-slate-500 uppercase tracking-wider px-6 py-3">
                    Conversations
                  </th>
                  <th className="text-right text-xs font-medium text-slate-500 uppercase tracking-wider px-6 py-3">
                    Rating
                  </th>
                  <th className="text-right text-xs font-medium text-slate-500 uppercase tracking-wider px-6 py-3">
                    Model
                  </th>
                  <th className="text-center text-xs font-medium text-slate-500 uppercase tracking-wider px-6 py-3">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {DEMO_AGENTS.map((agent) => (
                  <tr key={agent.id} className="hover:bg-slate-800/30 transition-smooth">
                    <td className="px-6 py-4">
                      <span className="text-sm font-medium text-white">{agent.name}</span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-xs text-slate-400">{agent.type}</span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <span className="text-sm text-white">{agent.conversations.toLocaleString()}</span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex items-center justify-end gap-1">
                        <Star className="w-3 h-3 text-amber-500" />
                        <span className="text-sm text-white">{agent.rating}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <span className="text-xs text-slate-500 font-mono">{agent.model}</span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex justify-center">
                        <span className="flex items-center gap-1.5 text-xs text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full">
                          <div className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                          Active
                        </span>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
