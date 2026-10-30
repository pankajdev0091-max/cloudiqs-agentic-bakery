const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export interface Agent {
  id: string;
  name: string;
  type: string;
  description: string;
  status: string;
  model: string;
  conversations: number;
  rating: number;
  icon: string;
  tools?: string[];
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  agentId?: string;
}

export interface DashboardStats {
  totalAgents: number;
  activeConversations: number;
  avgResponseTime: string;
  satisfactionRate: number;
}

export interface AgentMetrics {
  totalConversations: number;
  avgResponseTime: number;
  satisfactionRate: number;
  peakHours: string[];
  topTopics: string[];
}

async function fetchWithTimeout(url: string, options?: RequestInit, timeout = 5000): Promise<Response> {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    clearTimeout(id);
    return response;
  } catch (error) {
    clearTimeout(id);
    throw error;
  }
}

export async function fetchAgents(): Promise<Agent[]> {
  try {
    const response = await fetchWithTimeout(`${API_BASE}/api/agents`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch {
    throw new Error('Failed to fetch agents');
  }
}

export async function fetchAgent(id: string): Promise<Agent> {
  try {
    const response = await fetchWithTimeout(`${API_BASE}/api/agents/${id}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch {
    throw new Error('Failed to fetch agent');
  }
}

export async function sendMessage(
  agentId: string,
  message: string,
  sessionId: string
): Promise<{ message: string; session_id: string }> {
  try {
    const response = await fetchWithTimeout(
      `${API_BASE}/api/chat`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          agent_id: agentId,
          message,
          session_id: sessionId,
        }),
      },
      30000
    );
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch {
    throw new Error('Failed to send message');
  }
}

export async function fetchConversation(sessionId: string): Promise<ChatMessage[]> {
  try {
    const response = await fetchWithTimeout(`${API_BASE}/api/conversations/${sessionId}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch {
    throw new Error('Failed to fetch conversation');
  }
}

export async function fetchAgentMetrics(agentId: string): Promise<AgentMetrics> {
  try {
    const response = await fetchWithTimeout(`${API_BASE}/api/agents/${agentId}/metrics`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch {
    throw new Error('Failed to fetch agent metrics');
  }
}

export async function fetchDashboardStats(): Promise<DashboardStats> {
  try {
    const response = await fetchWithTimeout(`${API_BASE}/api/dashboard/stats`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch {
    throw new Error('Failed to fetch dashboard stats');
  }
}
