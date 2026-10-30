'use client';

import { useParams } from 'next/navigation';
import { useState } from 'react';
import {
  ArrowLeft,
  Bot,
  Wrench,
  Info,
  ChevronRight,
  Hash,
  Monitor,
  TrendingUp,
  Headphones,
  Calculator,
  BookOpen,
} from 'lucide-react';
import Link from 'next/link';
import ChatInterface from '@/components/ChatInterface';
import { getAgentById } from '@/lib/agents';

const iconMap: Record<string, React.ComponentType<{ className?: string }>> = {
  Monitor,
  TrendingUp,
  HeadphonesIcon: Headphones,
  Calculator,
  BookOpen,
  Bot,
};

const typeColors: Record<string, string> = {
  'IT Support': 'bg-blue-500/10 text-blue-400',
  Sales: 'bg-emerald-500/10 text-emerald-400',
  'Customer Service': 'bg-purple-500/10 text-purple-400',
  Finance: 'bg-amber-500/10 text-amber-400',
  Knowledge: 'bg-cyan-500/10 text-cyan-400',
};

export default function ChatPage() {
  const params = useParams();
  const agentId = params.agentId as string;
  const agent = getAgentById(agentId);
  const [sidePanelOpen, setSidePanelOpen] = useState(true);

  if (!agent) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen text-center p-8">
        <div className="w-16 h-16 rounded-2xl bg-slate-800 flex items-center justify-center mb-4">
          <Bot className="w-8 h-8 text-slate-600" />
        </div>
        <h2 className="text-xl font-semibold text-white mb-2">Agent Not Found</h2>
        <p className="text-sm text-slate-500 mb-4">
          The agent &quot;{agentId}&quot; could not be found.
        </p>
        <Link
          href="/agents"
          className="flex items-center gap-2 px-4 py-2 bg-amber-500 hover:bg-amber-400 text-slate-950 rounded-xl text-sm font-medium transition-smooth"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Agents
        </Link>
      </div>
    );
  }

  const IconComponent = iconMap[agent.icon] || Bot;
  const typeColor = typeColors[agent.type] || 'bg-slate-500/10 text-slate-400';

  return (
    <div className="flex h-screen">
      {/* Side panel */}
      <div
        className={`
          hidden lg:flex flex-col border-r border-slate-800 bg-slate-900/50
          transition-all duration-300 flex-shrink-0
          ${sidePanelOpen ? 'w-72' : 'w-0 overflow-hidden'}
        `}
      >
        <div className="p-4 border-b border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <Link
              href="/agents"
              className="flex items-center gap-1.5 text-xs text-slate-500 hover:text-white transition-smooth"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              All Agents
            </Link>
            <button
              onClick={() => setSidePanelOpen(false)}
              className="p-1 rounded text-slate-500 hover:text-white hover:bg-slate-800 transition-smooth"
            >
              <ChevronRight className="w-4 h-4 rotate-180" />
            </button>
          </div>

          {/* Agent info */}
          <div className="flex items-center gap-3 mb-3">
            <div className="w-11 h-11 rounded-xl bg-slate-800 flex items-center justify-center">
              <IconComponent className="w-5 h-5 text-amber-500" />
            </div>
            <div>
              <h2 className="text-sm font-semibold text-white">{agent.name}</h2>
              <span className={`inline-block mt-0.5 text-[10px] font-medium px-2 py-0.5 rounded-full ${typeColor}`}>
                {agent.type}
              </span>
            </div>
          </div>

          <p className="text-xs text-slate-500 leading-relaxed">{agent.description}</p>
        </div>

        {/* Status */}
        <div className="px-4 py-3 border-b border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-500">Status</span>
            <div className="flex items-center gap-1.5">
              <div className="w-2 h-2 rounded-full bg-emerald-500" />
              <span className="text-xs text-emerald-400 capitalize">{agent.status}</span>
            </div>
          </div>
          <div className="flex items-center justify-between mt-2">
            <span className="text-xs text-slate-500">Model</span>
            <span className="text-xs text-slate-300 font-mono">{agent.model}</span>
          </div>
          <div className="flex items-center justify-between mt-2">
            <span className="text-xs text-slate-500">Conversations</span>
            <span className="text-xs text-slate-300">{agent.conversations.toLocaleString()}</span>
          </div>
        </div>

        {/* Tools */}
        <div className="px-4 py-3 border-b border-slate-800">
          <div className="flex items-center gap-1.5 mb-3">
            <Wrench className="w-3.5 h-3.5 text-slate-500" />
            <span className="text-xs font-medium text-slate-400">Available Tools</span>
          </div>
          <div className="space-y-1.5">
            {agent.tools.map((tool) => (
              <div
                key={tool}
                className="flex items-center gap-2 px-2.5 py-1.5 bg-slate-800/50 rounded-lg"
              >
                <Hash className="w-3 h-3 text-slate-600" />
                <span className="text-xs text-slate-400">{tool}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Session info */}
        <div className="px-4 py-3 mt-auto border-t border-slate-800">
          <div className="flex items-center gap-1.5 mb-2">
            <Info className="w-3.5 h-3.5 text-slate-600" />
            <span className="text-[10px] text-slate-600">Session Info</span>
          </div>
          <p className="text-[10px] text-slate-700 font-mono break-all">
            New session started
          </p>
        </div>
      </div>

      {/* Collapsed panel toggle */}
      {!sidePanelOpen && (
        <button
          onClick={() => setSidePanelOpen(true)}
          className="hidden lg:flex items-center justify-center w-8 border-r border-slate-800 bg-slate-900/50 hover:bg-slate-800 transition-smooth"
        >
          <ChevronRight className="w-4 h-4 text-slate-500" />
        </button>
      )}

      {/* Chat area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Mobile header */}
        <div className="lg:hidden flex items-center gap-3 px-4 py-3 border-b border-slate-800 bg-slate-900/50">
          <Link
            href="/agents"
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-smooth"
          >
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div className="w-8 h-8 rounded-lg bg-slate-800 flex items-center justify-center">
            <IconComponent className="w-4 h-4 text-amber-500" />
          </div>
          <div>
            <h2 className="text-sm font-medium text-white">{agent.name}</h2>
            <div className="flex items-center gap-1">
              <div className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
              <span className="text-[10px] text-slate-500">Online</span>
            </div>
          </div>
        </div>

        <ChatInterface agent={agent} />
      </div>
    </div>
  );
}
