export interface DemoAgent {
  id: string;
  name: string;
  type: string;
  description: string;
  status: string;
  model: string;
  conversations: number;
  rating: number;
  icon: string;
  tools: string[];
  suggestedPrompts: string[];
}

export const DEMO_AGENTS: DemoAgent[] = [
  {
    id: 'it-helpdesk',
    name: 'IT Helpdesk Assistant',
    type: 'IT Support',
    description:
      'Handles password resets, ticket management, and system status inquiries. Integrates with ServiceNow and Active Directory.',
    status: 'active',
    model: 'Claude 3.5 Sonnet',
    conversations: 1247,
    rating: 4.8,
    icon: 'Monitor',
    tools: ['Password Reset', 'Ticket Creation', 'System Status Check', 'Knowledge Base Search'],
    suggestedPrompts: [
      'I need to reset my password',
      'Check the status of ticket #4521',
      'Is the VPN service running?',
      'How do I set up two-factor authentication?',
    ],
  },
  {
    id: 'sales-assistant',
    name: 'Sales Assistant Agent',
    type: 'Sales',
    description:
      'Qualifies leads, provides pricing information, and schedules product demos. Connects with Salesforce and Calendly.',
    status: 'active',
    model: 'Claude 3.5 Sonnet',
    conversations: 856,
    rating: 4.6,
    icon: 'TrendingUp',
    tools: ['Lead Scoring', 'CRM Lookup', 'Demo Scheduling', 'Pricing Calculator'],
    suggestedPrompts: [
      'I want to learn about your enterprise plan',
      'Can you schedule a demo for next week?',
      'What integrations do you support?',
      'We have a team of 50, what would pricing look like?',
    ],
  },
  {
    id: 'customer-service',
    name: 'Customer Service Agent',
    type: 'Customer Service',
    description:
      'Manages orders, handles complaints, and provides product support. Integrated with order management and CRM systems.',
    status: 'active',
    model: 'Claude 3 Opus',
    conversations: 2341,
    rating: 4.9,
    icon: 'HeadphonesIcon',
    tools: ['Order Lookup', 'Refund Processing', 'Complaint Escalation', 'Product Recommendations'],
    suggestedPrompts: [
      'Where is my order #12345?',
      'I want to return a product',
      "I'm not satisfied with my recent purchase",
      'Can you recommend a similar product?',
    ],
  },
  {
    id: 'finance-advisor',
    name: 'Finance Advisor',
    type: 'Finance',
    description:
      'Analyzes burn rate, calculates runway, and provides financial forecasts. Connects to accounting systems and databases.',
    status: 'active',
    model: 'Claude 3.5 Sonnet',
    conversations: 432,
    rating: 4.7,
    icon: 'Calculator',
    tools: ['Burn Rate Calculator', 'Runway Analysis', 'Revenue Forecasting', 'Expense Tracker'],
    suggestedPrompts: [
      'What is our current burn rate?',
      'Calculate our runway at current spending',
      'Show me the revenue forecast for Q4',
      'Break down expenses by department',
    ],
  },
  {
    id: 'knowledge-base',
    name: 'Knowledge Base Agent',
    type: 'Knowledge',
    description:
      'Searches documentation, answers technical questions from the knowledge base. Uses RAG with vector search.',
    status: 'active',
    model: 'Claude 3 Haiku',
    conversations: 3120,
    rating: 4.5,
    icon: 'BookOpen',
    tools: ['Vector Search', 'Document Retrieval', 'Code Search', 'API Reference Lookup'],
    suggestedPrompts: [
      'How do I deploy to production?',
      'What is the API rate limit?',
      'Show me the authentication documentation',
      'How do I configure webhooks?',
    ],
  },
];

export function getAgentById(id: string): DemoAgent | undefined {
  return DEMO_AGENTS.find((agent) => agent.id === id);
}

export function generateMockResponse(agentId: string, userMessage: string): string {
  const msg = userMessage.toLowerCase();

  switch (agentId) {
    case 'it-helpdesk':
      if (msg.includes('password') || msg.includes('reset')) {
        return `I can help you with your password reset. I've initiated the process through Active Directory.\n\n**Steps to complete:**\n1. You'll receive a verification email at your registered address\n2. Click the secure link within 15 minutes\n3. Set a new password (minimum 12 characters, including uppercase, lowercase, number, and special character)\n\nYour temporary access token has been generated. Would you like me to create a support ticket for tracking purposes?`;
      }
      if (msg.includes('ticket') || msg.includes('status')) {
        return `I've looked up the information in ServiceNow.\n\n**Ticket #4521 Status:**\n- **Status:** In Progress\n- **Priority:** Medium\n- **Assigned to:** Sarah Chen (Infrastructure Team)\n- **Last Updated:** 2 hours ago\n- **ETA:** Resolution expected within 4 hours\n\nThe team is currently investigating the network latency issue reported. Would you like me to add a comment or escalate the priority?`;
      }
      if (msg.includes('vpn') || msg.includes('service') || msg.includes('running')) {
        return `Here's the current system status:\n\n| Service | Status | Uptime |\n|---------|--------|--------|\n| VPN Gateway | **Operational** | 99.97% |\n| Email Server | **Operational** | 99.99% |\n| SSO/Auth | **Operational** | 100% |\n| Dev Environments | **Degraded** | 98.2% |\n\n**Note:** Dev environments are experiencing slightly elevated response times due to scheduled maintenance. Expected resolution: 6:00 PM EST.\n\nWould you like me to set up an alert for when all services are fully operational?`;
      }
      return `I'm the IT Helpdesk Assistant, powered by AWS AgentCore. I can help you with:\n\n- **Password resets** and account recovery\n- **Ticket management** (create, update, check status)\n- **System status** monitoring\n- **Technical troubleshooting**\n\nI have access to ServiceNow, Active Directory, and our monitoring dashboards. How can I assist you today?`;

    case 'sales-assistant':
      if (msg.includes('pricing') || msg.includes('plan') || msg.includes('enterprise') || msg.includes('cost')) {
        return `Great question! Here's an overview of our enterprise offering:\n\n**Enterprise Plan - Starting at $299/month**\n- Up to 100 agent deployments\n- Unlimited conversations\n- Priority support (< 1hr response time)\n- Custom model fine-tuning\n- SOC 2 Type II compliance\n- SSO & SAML integration\n- Dedicated account manager\n\n**Volume Discounts Available:**\n- 50+ seats: 15% discount\n- 100+ seats: 25% discount\n- 500+ seats: Custom pricing\n\nI'd love to understand your use case better. How many team members would be using the platform? I can prepare a tailored proposal.`;
      }
      if (msg.includes('demo') || msg.includes('schedule')) {
        return `I'd be happy to set up a demo for you!\n\n**Available Demo Slots (Next Week):**\n- Tuesday, 10:00 AM EST\n- Wednesday, 2:00 PM EST\n- Thursday, 11:00 AM EST\n- Friday, 3:00 PM EST\n\nEach demo is 30 minutes and includes:\n1. Platform overview and architecture\n2. Live agent deployment demonstration\n3. Integration walkthrough\n4. Q&A session\n\nWhich time works best for you? I'll also need your email to send the calendar invite.`;
      }
      if (msg.includes('integration') || msg.includes('connect')) {
        return `We support a comprehensive set of integrations:\n\n**CRM:** Salesforce, HubSpot, Pipedrive\n**Communication:** Slack, Microsoft Teams, Discord\n**Ticketing:** Jira, ServiceNow, Zendesk\n**Cloud:** AWS, Azure, GCP\n**Data:** Snowflake, BigQuery, Redshift\n**Auth:** Okta, Auth0, Azure AD\n\n**API & Custom:**\n- REST API with webhook support\n- GraphQL endpoint\n- Custom connector SDK\n- Terraform provider\n\nAll integrations are included in the Enterprise plan. Would you like a deeper dive into any specific integration?`;
      }
      return `Welcome! I'm the Sales Qualification Agent. I can help you with:\n\n- **Pricing information** for our plans\n- **Demo scheduling** with our solutions team\n- **Feature comparisons** and integration details\n- **Custom proposals** for enterprise needs\n\nWhat brings you to CloudiQS today? I'd love to learn more about your team's needs.`;

    case 'customer-service':
      if (msg.includes('order') || msg.includes('where') || msg.includes('tracking')) {
        return `I've located your order details:\n\n**Order #12345**\n- **Status:** Shipped - In Transit\n- **Carrier:** FedEx Express\n- **Tracking:** 7891234567890\n- **Estimated Delivery:** Tomorrow, Oct 30 by 5:00 PM\n- **Current Location:** Distribution Center, Memphis TN\n\n**Order Items:**\n1. CloudiQS Pro License (Annual) - $599.00\n2. Premium Support Add-on - $149.00\n\n**Total:** $748.00\n\nThe package is on schedule for delivery. Would you like me to set up delivery notifications?`;
      }
      if (msg.includes('return') || msg.includes('refund')) {
        return `I can help you with the return process.\n\n**Our Return Policy:**\n- 30-day money-back guarantee on all plans\n- No questions asked for the first 14 days\n- Prorated refund available after 14 days\n\n**To initiate your return, I need:**\n1. Your order number\n2. Reason for return (helps us improve)\n\nOnce submitted, refunds are processed within 3-5 business days to your original payment method.\n\nWould you like to proceed with the return?`;
      }
      if (msg.includes('not satisfied') || msg.includes('complaint') || msg.includes('unhappy') || msg.includes('problem')) {
        return `I'm sorry to hear about your experience. Your satisfaction is our top priority.\n\nLet me help resolve this right away. I've created an escalation ticket:\n\n**Case #ESC-2847**\n- **Priority:** High\n- **Status:** Assigned to Senior Support\n- **Expected Response:** Within 2 hours\n\n**Immediate actions I can take:**\n1. Issue a service credit to your account\n2. Connect you with a senior support specialist\n3. Provide a temporary workaround\n\nCould you share more details about what happened? I want to make sure we address the root cause.`;
      }
      return `Hello! I'm the Customer Service Agent. I'm here to help with:\n\n- **Order tracking** and delivery updates\n- **Returns and refunds** processing\n- **Product support** and troubleshooting\n- **Account management**\n\nI have access to your order history and account details. How can I make your experience better today?`;

    case 'finance-advisor':
      if (msg.includes('burn rate') || msg.includes('spending')) {
        return `Here's your current burn rate analysis:\n\n**Monthly Burn Rate: $127,450**\n\n**Breakdown by Category:**\n| Category | Monthly | % of Total |\n|----------|---------|------------|\n| Salaries & Benefits | $82,000 | 64.3% |\n| Cloud Infrastructure | $18,200 | 14.3% |\n| Software & Tools | $8,750 | 6.9% |\n| Office & Operations | $6,500 | 5.1% |\n| Marketing | $7,000 | 5.5% |\n| Other | $5,000 | 3.9% |\n\n**Trend:** Burn rate increased 3.2% from last month, primarily due to two new engineering hires.\n\nWould you like me to project the impact on runway?`;
      }
      if (msg.includes('runway')) {
        return `**Runway Analysis**\n\n**Current Cash Position:** $2,847,000\n**Monthly Burn Rate:** $127,450\n**Current Runway:** 22.3 months\n\n**Scenario Analysis:**\n| Scenario | Monthly Burn | Runway |\n|----------|-------------|--------|\n| Current | $127,450 | 22.3 months |\n| +2 Hires | $142,450 | 20.0 months |\n| +5 Hires | $164,950 | 17.3 months |\n| 10% Cost Reduction | $114,705 | 24.8 months |\n\n**Recommendation:** At current burn, you have comfortable runway through Q2 2028. If planning to raise Series B in Q3 2027, you have an 8-month buffer.\n\nWould you like me to generate a detailed forecast report?`;
      }
      if (msg.includes('revenue') || msg.includes('forecast')) {
        return `**Q4 Revenue Forecast**\n\n**Projected Revenue: $485,000** (+18% QoQ)\n\n**Monthly Breakdown:**\n- October: $152,000 (actual: $148,500)\n- November: $162,000 (projected)\n- December: $171,000 (projected)\n\n**Revenue by Stream:**\n| Stream | Q4 Forecast | Growth |\n|--------|-------------|--------|\n| SaaS Subscriptions | $342,000 | +22% |\n| Professional Services | $98,000 | +8% |\n| Support Plans | $45,000 | +15% |\n\n**Key Drivers:**\n- 3 enterprise deals in pipeline (weighted: $89K)\n- Annual renewals: 94% retention rate\n- New product tier launch expected Nov 15\n\nShall I drill down into any specific revenue stream?`;
      }
      return `I'm the Finance Assistant, connected to your accounting systems. I can help with:\n\n- **Burn rate analysis** and expense tracking\n- **Runway calculations** with scenario modeling\n- **Revenue forecasting** and pipeline analysis\n- **Department budget breakdowns**\n\nAll data is pulled in real-time from your connected financial systems. What would you like to analyze?`;

    case 'knowledge-base':
      if (msg.includes('deploy') || msg.includes('production')) {
        return `# Deployment Guide\n\nHere's the production deployment process from our documentation:\n\n## Prerequisites\n- AWS CLI configured with appropriate IAM permissions\n- Docker 20.10+ installed\n- Terraform 1.5+ (for infrastructure)\n\n## Steps\n\n**1. Build the container:**\n\`\`\`bash\ndocker build -t cloudiqs-api:latest .\n\`\`\`\n\n**2. Push to ECR:**\n\`\`\`bash\naws ecr get-login-password | docker login --username AWS --password-stdin $ECR_REPO\ndocker push $ECR_REPO/cloudiqs-api:latest\n\`\`\`\n\n**3. Deploy with Terraform:**\n\`\`\`bash\ncd infrastructure/\nterraform plan -var-file=prod.tfvars\nterraform apply -var-file=prod.tfvars\n\`\`\`\n\n**4. Verify:**\n\`\`\`bash\ncurl https://api.cloudiqs.com/api/health\n\`\`\`\n\nSee also: [CI/CD Pipeline Guide], [Rollback Procedures]\n\nWould you like details on any specific step?`;
      }
      if (msg.includes('api') || msg.includes('rate limit')) {
        return `# API Rate Limits\n\nFrom the API Reference documentation:\n\n| Plan | Requests/min | Requests/day | Concurrent |\n|------|-------------|-------------|------------|\n| Free | 20 | 1,000 | 2 |\n| Pro | 100 | 50,000 | 10 |\n| Enterprise | 500 | Unlimited | 50 |\n\n## Rate Limit Headers\nEvery response includes:\n\`\`\`\nX-RateLimit-Limit: 100\nX-RateLimit-Remaining: 95\nX-RateLimit-Reset: 1698590400\n\`\`\`\n\n## Handling Rate Limits\nWhen exceeded, you'll receive:\n\`\`\`json\n{\n  "error": "rate_limit_exceeded",\n  "retry_after": 30\n}\n\`\`\`\n\n**Best Practice:** Implement exponential backoff starting at 1 second, max 5 retries.\n\nNeed help with implementation? I can provide code examples in Python, Node.js, or Go.`;
      }
      if (msg.includes('auth') || msg.includes('authentication')) {
        return `# Authentication Documentation\n\nCloudIQS supports multiple authentication methods:\n\n## API Key Authentication\n\`\`\`bash\ncurl -H "Authorization: Bearer YOUR_API_KEY" \\\n     https://api.cloudiqs.com/api/agents\n\`\`\`\n\n## OAuth 2.0 / OIDC\nSupported providers:\n- AWS Cognito\n- Okta\n- Auth0\n- Azure AD\n\n**Configuration:**\n\`\`\`json\n{\n  "auth": {\n    "provider": "cognito",\n    "user_pool_id": "us-east-1_xxxxx",\n    "client_id": "your-client-id",\n    "scopes": ["openid", "profile", "email"]\n  }\n}\n\`\`\`\n\n## Service-to-Service (IAM)\nFor AWS services, use IAM roles with SigV4 signing.\n\n## Token Refresh\nAccess tokens expire after 1 hour. Use the refresh token flow:\n\`\`\`\nPOST /auth/refresh\n{ "refresh_token": "..." }\n\`\`\`\n\nSee: [Security Best Practices], [RBAC Configuration]`;
      }
      return `I'm the Knowledge Base Agent, powered by RAG with vector search across your documentation.\n\nI can help you find information about:\n- **Deployment guides** and infrastructure setup\n- **API reference** and rate limits\n- **Authentication** and security configuration\n- **Troubleshooting** common issues\n- **Architecture** decisions and design patterns\n\nWhat topic are you looking for?`;

    default:
      return `Thank you for your message. I'm processing your request using AWS AgentCore and Strands Agents. How can I help you further?`;
  }
}
