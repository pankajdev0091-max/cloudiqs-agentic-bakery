'use client';

import Header from '@/components/Header';
import Dashboard from '@/components/Dashboard';

export default function DashboardPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header title="Dashboard" subtitle="Overview of your agent fleet" />
      <div className="flex-1 p-4 lg:p-8">
        <Dashboard />
      </div>
    </div>
  );
}
