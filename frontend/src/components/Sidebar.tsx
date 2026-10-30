'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  Bot,
  BarChart3,
  ChevronLeft,
  ChevronRight,
  Zap,
  Menu,
  X,
} from 'lucide-react';

const navItems = [
  { href: '/', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/agents', label: 'Agents', icon: Bot },
  { href: '/analytics', label: 'Analytics', icon: BarChart3 },
];

export default function Sidebar() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  const isActive = (href: string) => {
    if (href === '/') return pathname === '/';
    return pathname.startsWith(href);
  };

  const sidebarContent = (
    <div className="flex flex-col h-full">
      {/* Brand */}
      <div className="px-4 py-6 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center flex-shrink-0">
            <Zap className="w-5 h-5 text-white" />
          </div>
          {!collapsed && (
            <div className="min-w-0">
              <h1 className="text-lg font-bold text-white tracking-tight leading-tight">
                CloudiQS
              </h1>
              <p className="text-[11px] text-amber-500 font-medium tracking-wide uppercase">
                Agentic AI Bakery
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              onClick={() => setMobileOpen(false)}
              className={`
                flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium
                transition-smooth group relative
                ${
                  active
                    ? 'bg-amber-500/10 text-amber-400'
                    : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                }
              `}
            >
              {active && (
                <div className="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-5 bg-amber-500 rounded-r-full" />
              )}
              <Icon className={`w-5 h-5 flex-shrink-0 ${active ? 'text-amber-400' : 'text-slate-500 group-hover:text-white'}`} />
              {!collapsed && <span>{item.label}</span>}
            </Link>
          );
        })}
      </nav>

      {/* Collapse toggle (desktop only) */}
      <div className="hidden lg:block px-3 py-2 border-t border-slate-800">
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="flex items-center gap-3 px-3 py-2 rounded-lg text-slate-500 hover:text-white hover:bg-slate-800 transition-smooth w-full text-sm"
        >
          {collapsed ? (
            <ChevronRight className="w-4 h-4" />
          ) : (
            <>
              <ChevronLeft className="w-4 h-4" />
              <span>Collapse</span>
            </>
          )}
        </button>
      </div>

      {/* Powered by AWS */}
      <div className="px-4 py-4 border-t border-slate-800">
        {!collapsed ? (
          <div className="flex items-center gap-2 text-[11px] text-slate-600">
            <div className="w-5 h-5 rounded bg-slate-800 flex items-center justify-center text-[9px] font-bold text-amber-500">
              aws
            </div>
            <span>Powered by AWS AgentCore</span>
          </div>
        ) : (
          <div className="flex justify-center">
            <div className="w-5 h-5 rounded bg-slate-800 flex items-center justify-center text-[9px] font-bold text-amber-500">
              aws
            </div>
          </div>
        )}
      </div>
    </div>
  );

  return (
    <>
      {/* Mobile hamburger */}
      <button
        onClick={() => setMobileOpen(true)}
        className="lg:hidden fixed top-4 left-4 z-50 p-2 rounded-lg bg-slate-800 text-white"
      >
        <Menu className="w-5 h-5" />
      </button>

      {/* Mobile overlay */}
      {mobileOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/60 z-40"
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* Mobile sidebar */}
      <aside
        className={`
          lg:hidden fixed inset-y-0 left-0 z-50 w-64 bg-slate-900 border-r border-slate-800
          transform transition-transform duration-300
          ${mobileOpen ? 'translate-x-0' : '-translate-x-full'}
        `}
      >
        <button
          onClick={() => setMobileOpen(false)}
          className="absolute top-4 right-4 p-1 text-slate-400 hover:text-white"
        >
          <X className="w-5 h-5" />
        </button>
        {sidebarContent}
      </aside>

      {/* Desktop sidebar */}
      <aside
        className={`
          hidden lg:flex flex-col flex-shrink-0 bg-slate-900 border-r border-slate-800 h-screen sticky top-0
          transition-all duration-300
          ${collapsed ? 'w-[68px]' : 'w-60'}
        `}
      >
        {sidebarContent}
      </aside>
    </>
  );
}
