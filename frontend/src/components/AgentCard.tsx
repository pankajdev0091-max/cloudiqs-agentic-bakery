'use client';

import Link from 'next/link';
import {
  Monitor,
  TrendingUp,
  Headphones,
  Calculator,
  BookOpen,
  Star,
  MessageCircle,
  Settings,
  Bot,
} from 'lucide-react';

const iconMap: Record<string, React.ComponentType<{ className?: string }>> = {
  Monitor,
  TrendingUp,
  HeadphonesIcon: Headphones,
  Calculator,
  BookOpen,
  Bot,
};

const typeColors: Record<string, string> = {
  'IT Support': 'bg-blue-500/10 text-blue-400 border-blue-500/20',
  Sales: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
  'Customer Service': 'bg-purple-500/10 text-purple-400 border-purple-500/20',
  Finance: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
  Knowledge: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20',
};

interface AgentCardProps {
  id: string;
  name: string;
  type: string;
  description: string;
  status: string;
  model: string;
  conversations: number;
  rating: number;
  icon: string;
  compact?: boolean;
}

export default function AgentCard({
  id,
  name,
  type,
  description,
  status,
  model,
  conversations,
  rating,
  icon,
  compact = false,
}: AgentCardProps) {
  const IconComponent = iconMap[icon] || Bot;
  const typeColor = typeColors[type] || 'bg-slate-500/10 text-slate-400 border-slate-500/20';

  if (compact) {
    return (
      <Link
        href={`/chat/${id}`}
        className="glass-card p-4 hover:border-slate-700 transition-smooth group cursor-pointer block"
      >
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-slate-800 flex items-center justify-center group-hover:bg-amber-500/10 transition-smooth">
            <IconComponent className="w-5 h-5 text-slate-400 group-hover:text-amber-400 transition-smooth" />
          </div>
          <div className="min-w-0 flex-1">
            <h3 className="text-sm font-medium text-white truncate">{name}</h3>
            <p className="text-xs text-slate-500">{type}</p>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-2 h-2 rounded-full bg-emerald-500" />
          </div>
        </div>
      </Link>
    );
  }

  return (
    <div className="glass-card p-5 hover:border-slate-700 transition-smooth group">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 rounded-xl bg-slate-800 flex items-center justify-center group-hover:bg-amber-500/10 transition-smooth">
            <IconComponent className="w-5 h-5 text-slate-400 group-hover:text-amber-400 transition-smooth" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-white">{name}</h3>
            <span className={`inline-block mt-1 text-[10px] font-medium px-2 py-0.5 rounded-full border ${typeColor}`}>
              {type}
            </span>
          </div>
        </div>
        <div className="flex items-center gap-1.5">
          <div className={`w-2 h-2 rounded-full ${status === 'active' ? 'bg-emerald-500' : 'bg-slate-600'}`} />
          <span className="text-[11px] text-slate-500 capitalize">{status}</span>
        </div>
      </div>

      {/* Description */}
      <p className="text-sm text-slate-400 mb-4 line-clamp-2 leading-relaxed">{description}</p>

      {/* Model badge */}
      <div className="mb-4">
        <span className="text-[10px] text-slate-500 bg-slate-800 px-2 py-1 rounded-md font-mono">
          {model}
        </span>
      </div>

      {/* Metrics */}
      <div className="flex items-center gap-4 mb-4 text-xs text-slate-500">
        <div className="flex items-center gap-1.5">
          <MessageCircle className="w-3.5 h-3.5" />
          <span>{conversations.toLocaleString()} chats</span>
        </div>
        <div className="flex items-center gap-1.5">
          <Star className="w-3.5 h-3.5 text-amber-500" />
          <span>{rating}</span>
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-2">
        <Link
          href={`/chat/${id}`}
          className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-amber-500 hover:bg-amber-400 text-slate-950 rounded-lg text-sm font-medium transition-smooth"
        >
          <MessageCircle className="w-4 h-4" />
          Chat
        </Link>
        <button className="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-sm transition-smooth">
          <Settings className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
