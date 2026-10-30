'use client';

import { Search, Bell, User } from 'lucide-react';
import { useState } from 'react';

interface HeaderProps {
  title: string;
  subtitle?: string;
}

export default function Header({ title, subtitle }: HeaderProps) {
  const [searchOpen, setSearchOpen] = useState(false);

  return (
    <header className="sticky top-0 z-30 bg-slate-950/80 backdrop-blur-md border-b border-slate-800">
      <div className="flex items-center justify-between h-16 px-4 lg:px-8">
        {/* Left: Title */}
        <div className="pl-12 lg:pl-0">
          <h1 className="text-lg font-semibold text-white">{title}</h1>
          {subtitle && (
            <p className="text-xs text-slate-500">{subtitle}</p>
          )}
        </div>

        {/* Right: Actions */}
        <div className="flex items-center gap-2">
          {/* Search */}
          <div className={`relative transition-all duration-300 ${searchOpen ? 'w-64' : 'w-auto'}`}>
            {searchOpen ? (
              <div className="flex items-center gap-2 bg-slate-800 rounded-lg px-3 py-1.5">
                <Search className="w-4 h-4 text-slate-500" />
                <input
                  autoFocus
                  type="text"
                  placeholder="Search agents, conversations..."
                  className="bg-transparent border-none text-sm text-white placeholder-slate-500 w-full focus:outline-none focus:ring-0"
                  onBlur={() => setSearchOpen(false)}
                />
              </div>
            ) : (
              <button
                onClick={() => setSearchOpen(true)}
                className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-smooth"
              >
                <Search className="w-5 h-5" />
              </button>
            )}
          </div>

          {/* Notifications */}
          <button className="relative p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-smooth">
            <Bell className="w-5 h-5" />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-amber-500 rounded-full" />
          </button>

          {/* User */}
          <button className="flex items-center gap-2 p-1.5 rounded-lg hover:bg-slate-800 transition-smooth">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
              <User className="w-4 h-4 text-white" />
            </div>
          </button>
        </div>
      </div>
    </header>
  );
}
