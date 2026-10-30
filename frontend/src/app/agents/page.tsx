'use client';

import { useState, useMemo } from 'react';
import Header from '@/components/Header';
import AgentCard from '@/components/AgentCard';
import { DEMO_AGENTS } from '@/lib/agents';
import { Search, Plus, Filter } from 'lucide-react';

const CATEGORIES = ['All', 'Customer Service', 'Sales', 'IT Support', 'Finance', 'Knowledge'];

export default function AgentsPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState('All');

  const filteredAgents = useMemo(() => {
    return DEMO_AGENTS.filter((agent) => {
      const matchesSearch =
        agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        agent.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        agent.type.toLowerCase().includes(searchQuery.toLowerCase());

      const matchesCategory =
        activeCategory === 'All' || agent.type === activeCategory;

      return matchesSearch && matchesCategory;
    });
  }, [searchQuery, activeCategory]);

  return (
    <div className="flex flex-col min-h-screen">
      <Header title="Agents" subtitle="Manage and deploy your AI agent fleet" />

      <div className="flex-1 p-4 lg:p-8 space-y-6">
        {/* Controls bar */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          {/* Search */}
          <div className="relative w-full sm:w-80">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
            <input
              type="text"
              placeholder="Search agents..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 bg-slate-900 border border-slate-800 rounded-xl text-sm text-white placeholder-slate-500 focus:border-amber-500/50 focus:ring-2 focus:ring-amber-500/20 transition-smooth"
            />
          </div>

          {/* Deploy button */}
          <button className="flex items-center gap-2 px-4 py-2.5 bg-amber-500 hover:bg-amber-400 text-slate-950 rounded-xl text-sm font-medium transition-smooth whitespace-nowrap">
            <Plus className="w-4 h-4" />
            Deploy New Agent
          </button>
        </div>

        {/* Category filters */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1">
          <Filter className="w-4 h-4 text-slate-600 flex-shrink-0" />
          {CATEGORIES.map((category) => (
            <button
              key={category}
              onClick={() => setActiveCategory(category)}
              className={`
                px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-smooth
                ${
                  activeCategory === category
                    ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                    : 'text-slate-500 hover:text-white hover:bg-slate-800 border border-transparent'
                }
              `}
            >
              {category}
            </button>
          ))}
        </div>

        {/* Agent count */}
        <div className="flex items-center justify-between">
          <p className="text-xs text-slate-500">
            Showing {filteredAgents.length} of {DEMO_AGENTS.length} agents
          </p>
        </div>

        {/* Agents grid */}
        {filteredAgents.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {filteredAgents.map((agent) => (
              <AgentCard key={agent.id} {...agent} />
            ))}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-16 text-center">
            <div className="w-16 h-16 rounded-2xl bg-slate-800 flex items-center justify-center mb-4">
              <Search className="w-8 h-8 text-slate-600" />
            </div>
            <h3 className="text-base font-medium text-white mb-1">No agents found</h3>
            <p className="text-sm text-slate-500">
              Try adjusting your search or filter criteria
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
