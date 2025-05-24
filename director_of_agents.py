"""
Director of Agents
The highest-level agent coordinator that manages multiple domain managers including the Health Manager Agent.
Routes requests across different life domains and coordinates complex multi-domain tasks.
"""

import os
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple, Union
from dotenv import load_dotenv
from supabase import create_client, Client
from openai import OpenAI

# Import our domain managers
from health_manager_agent import HealthManagerAgent

class DirectorOfAgents:
    """
    Director of Agents - the top-level coordinator for all AI assistants.
    
    This agent provides:
    - High-level request routing across different life domains
    - Multi-domain task coordination
    - Overall strategy and goal alignment
    - Cross-domain insights and analytics
    - Executive decision making for complex requests
    """
    
    def __init__(self, 
                 openai_api_key: Optional[str] = None,
                 supabase_url: Optional[str] = None, 
                 supabase_key: Optional[str] = None):
        """
        Initialize the Director of Agents.
        
        Args:
            openai_api_key: OpenAI API key (uses env var if not provided)
            supabase_url: Supabase URL (uses env var if not provided)  
            supabase_key: Supabase key (uses env var if not provided)
        """
        # Load environment variables if not provided
        load_dotenv()
        
        # Initialize OpenAI client
        api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required")
        self.openai_client = OpenAI(api_key=api_key)
        
        # Initialize Supabase client (for cross-domain analytics)
        url = supabase_url or os.getenv("SUPABASE_URL")
        key = supabase_key or os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("Supabase URL and key are required")
        self.supabase: Client = create_client(url, key)
        
        # Conversation memory
        self.conversation_history = []
        self.max_memory = 20  # Keep more messages for complex multi-domain discussions
        
        # Initialize domain managers
        self.domain_managers = {}
        self._initialize_domain_managers()
        
        # Domain routing keywords
        self.domain_routing = {
            'health_manager': [
                'health', 'meal', 'food', 'eat', 'cook', 'recipe', 'nutrition', 'calories',
                'protein', 'carbs', 'fats', 'breakfast', 'lunch', 'dinner', 'snack',
                'diet', 'weight', 'fitness', 'exercise', 'workout', 'medical', 'wellness',
                'blood pressure', 'heart rate', 'sleep', 'vitals', 'goals', 'chef',
                'equipment', 'gym equipment', 'weights', 'dumbbells', 'treadmill', 'home gym',
                'office gym', 'gear', 'machine', 'barbell', 'kettlebell', 'yoga mat'
            ],
            # Future domain managers
            'finance_manager': [
                'money', 'budget', 'finance', 'investment', 'savings', 'expense',
                'bank', 'credit', 'debt', 'payment', 'income', 'tax', 'financial'
            ],
            'productivity_manager': [
                'task', 'schedule', 'calendar', 'project', 'deadline', 'meeting',
                'todo', 'productivity', 'time', 'organization', 'work', 'planning'
            ],
            'learning_manager': [
                'learn', 'study', 'education', 'course', 'skill', 'knowledge',
                'training', 'development', 'book', 'research', 'tutorial'
            ]
        }
        
        # Cross-domain coordination patterns
        self.multi_domain_patterns = {
            'health_and_finance': ['meal budget', 'grocery cost', 'gym membership', 'health insurance'],
            'health_and_productivity': ['meal prep time', 'workout schedule', 'health goals planning'],
            'finance_and_productivity': ['budget planning', 'investment research', 'financial goals']
        }
    
    def _initialize_domain_managers(self):
        """Initialize all available domain managers"""
        try:
            # Initialize Health Manager
            self.domain_managers['health_manager'] = HealthManagerAgent(
                openai_api_key=os.getenv("OPENAI_API_KEY"),
                supabase_url=os.getenv("SUPABASE_URL"),
                supabase_key=os.getenv("SUPABASE_KEY")
            )
            print("✅ Health Manager initialized")
        except Exception as e:
            print(f"❌ Failed to initialize Health Manager: {e}")
        
        # Placeholder for future domain managers
        # self.domain_managers['finance_manager'] = FinanceManagerAgent(...)
        # self.domain_managers['productivity_manager'] = ProductivityManagerAgent(...)
        # self.domain_managers['learning_manager'] = LearningManagerAgent(...)
    
    def route_to_domain_manager(self, user_message: str) -> Optional[str]:
        """Determine which domain manager should handle the request"""
        message_lower = user_message.lower()
        
        # Check for multi-domain patterns first
        for pattern_name, keywords in self.multi_domain_patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                return 'multi_domain'  # Requires coordination
        
        # Check single domain routing
        domain_scores = {}
        for domain_name, keywords in self.domain_routing.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > 0:
                domain_scores[domain_name] = score
        
        # Return domain with highest score
        if domain_scores:
            return max(domain_scores, key=domain_scores.get)
        
        return None  # Handle at Director level
    
    def detect_multi_domain_request(self, user_message: str) -> List[str]:
        """Detect if a request involves multiple domains"""
        message_lower = user_message.lower()
        involved_domains = []
        
        for domain_name, keywords in self.domain_routing.items():
            if any(keyword in message_lower for keyword in keywords):
                involved_domains.append(domain_name)
        
        return involved_domains if len(involved_domains) > 1 else []
    
    def create_system_prompt(self) -> str:
        """Create the system prompt for the Director of Agents"""
        available_managers = list(self.domain_managers.keys())
        
        return f"""You are the Director of Agents - the highest-level AI coordinator responsible for managing a comprehensive network of specialized AI assistants and coordinating complex multi-domain tasks.

You oversee these domain managers:
{', '.join(available_managers)}

Your core responsibilities:
1. **Strategic Coordination**: Route requests to appropriate domain managers
2. **Multi-Domain Integration**: Handle requests that span multiple life domains
3. **Executive Decision Making**: Make high-level decisions about resource allocation and priorities
4. **Cross-Domain Analytics**: Provide insights that connect different aspects of the user's life
5. **Goal Alignment**: Ensure all domain activities align with user's overall life objectives

Domain Management:
- **Health Manager**: Oversees nutrition (Personal Chef), equipment management, fitness, wellness tracking, health goals
- **Finance Manager**: Budget, investments, expenses, financial planning (future)
- **Productivity Manager**: Tasks, scheduling, project management, time optimization (future)
- **Learning Manager**: Skill development, education, knowledge acquisition (future)

When to route vs handle directly:
- **Route to Domain Manager**: Specific domain requests (health, finance, productivity, learning)
- **Handle Directly**: 
  - Multi-domain coordination ("Plan my week considering health and budget")
  - High-level life strategy ("What should I prioritize this month?")
  - Cross-domain insights ("How do my health and productivity goals relate?")
  - Executive decisions requiring multiple domain input

Multi-Domain Coordination Examples:
- "Plan healthy meals within my budget" → Coordinate Health + Finance
- "Schedule workouts around my work meetings" → Coordinate Health + Productivity
- "Learn cooking while meeting nutrition goals" → Coordinate Learning + Health

Communication Style:
- Executive and strategic perspective
- Acknowledge domain expertise when routing
- Provide high-level coordination for complex requests
- Use data from multiple domains for comprehensive insights
- Focus on overall life optimization and goal alignment

When routing, explain the strategic decision and what value the domain manager will provide. When handling directly, provide executive-level guidance that considers the full picture."""

    def get_cross_domain_insights(self) -> Dict[str, Any]:
        """Generate insights that span multiple domains"""
        insights = {
            "timestamp": datetime.now().isoformat(),
            "domain_statuses": {},
            "cross_domain_opportunities": [],
            "integration_suggestions": []
        }
        
        # Collect status from each domain manager
        for domain_name, manager in self.domain_managers.items():
            if hasattr(manager, 'get_agent_capabilities'):
                insights["domain_statuses"][domain_name] = {
                    "available": True,
                    "capabilities": manager.get_agent_capabilities()
                }
                
                # Get domain-specific insights
                if domain_name == 'health_manager' and hasattr(manager, 'get_health_dashboard'):
                    health_dashboard = manager.get_health_dashboard()
                    insights["domain_statuses"][domain_name]["dashboard"] = health_dashboard
        
        # Add cross-domain opportunities
        if 'health_manager' in self.domain_managers:
            insights["cross_domain_opportunities"].extend([
                "Meal prep scheduling optimization",
                "Health goal financial planning",
                "Fitness learning curriculum"
            ])
        
        return insights
    
    def handle_multi_domain_request(self, user_message: str, involved_domains: List[str]) -> Tuple[str, Dict[str, Any]]:
        """Handle requests that require coordination across multiple domains"""
        responses = {}
        
        # Collect input from relevant domain managers
        for domain in involved_domains:
            if domain in self.domain_managers:
                try:
                    if domain == 'health_manager':
                        response, metadata = self.domain_managers[domain].chat(user_message)
                        responses[domain] = {
                            "response": response,
                            "metadata": metadata
                        }
                except Exception as e:
                    responses[domain] = {"error": str(e)}
        
        # Synthesize cross-domain response
        synthesis_prompt = f"""
        User Request: {user_message}
        
        Domain Responses:
        {json.dumps(responses, indent=2)}
        
        As the Director of Agents, synthesize these domain responses into a comprehensive, coordinated response that addresses the multi-domain nature of the request. Focus on integration, prioritization, and strategic guidance.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.create_system_prompt()},
                    {"role": "user", "content": synthesis_prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            coordinated_response = response.choices[0].message.content
            
            metadata = {
                "handled_by": "director_of_agents",
                "coordination_type": "multi_domain",
                "involved_domains": involved_domains,
                "domain_responses": responses
            }
            
            return coordinated_response, metadata
            
        except Exception as e:
            return f"Error coordinating multi-domain response: {e}", {"error": str(e)}
    
    def add_to_memory(self, role: str, content: str):
        """Add message to conversation memory"""
        self.conversation_history.append({"role": role, "content": content})
        
        # Keep only the last max_memory messages
        if len(self.conversation_history) > self.max_memory:
            self.conversation_history = self.conversation_history[-self.max_memory:]
    
    def clear_memory(self):
        """Clear conversation memory for all agents"""
        self.conversation_history = []
        # Clear domain manager memories
        for manager in self.domain_managers.values():
            if hasattr(manager, 'clear_memory'):
                manager.clear_memory()
    
    def chat(self, user_message: str) -> Tuple[str, Dict[str, Any]]:
        """
        Main chat function for the Director of Agents.
        
        Args:
            user_message: The user's message/question
            
        Returns:
            Tuple of (assistant_response, metadata_dict)
        """
        # Add user message to memory
        self.add_to_memory("user", user_message)
        
        # Check for multi-domain requests
        involved_domains = self.detect_multi_domain_request(user_message)
        
        if involved_domains:
            response, metadata = self.handle_multi_domain_request(user_message, involved_domains)
            self.add_to_memory("assistant", response)
            return response, metadata
        
        # Determine target domain manager
        target_domain = self.route_to_domain_manager(user_message)
        
        metadata = {
            "routed_to": target_domain,
            "handled_by": "director_of_agents",
            "domain_response": None
        }
        
        # Route to domain manager if appropriate
        if target_domain and target_domain in self.domain_managers:
            try:
                if target_domain == 'health_manager':
                    response, domain_metadata = self.domain_managers[target_domain].chat(user_message)
                    metadata["domain_response"] = response
                    metadata["domain_metadata"] = domain_metadata
                    metadata["handled_by"] = target_domain
                    
                    # Create executive coordination response
                    exec_response = f"I'm coordinating with your {target_domain.replace('_', ' ').title()} for this request.\n\n**Strategic Coordination:**\n{response}"
                    
                    self.add_to_memory("assistant", exec_response)
                    return exec_response, metadata
                
                # Handle other domain managers when available
                else:
                    response = f"I would coordinate with your {target_domain.replace('_', ' ').title()}, but that domain manager is not yet available. Let me provide executive-level guidance instead."
            
            except Exception as e:
                response = f"There was an issue coordinating with your {target_domain.replace('_', ' ').title()}. Let me handle this at the executive level."
        
        # Handle at Director level
        metadata["handled_by"] = "director_of_agents"
        
        # Build messages for OpenAI
        messages = [
            {"role": "system", "content": self.create_system_prompt()}
        ]
        
        # Add cross-domain context for strategic queries
        if any(word in user_message.lower() for word in ['strategy', 'overview', 'priorities', 'plan', 'coordinate', 'integrate']):
            cross_domain_context = self.get_cross_domain_insights()
            messages.append({"role": "system", "content": f"Cross-Domain Context:\n{json.dumps(cross_domain_context, indent=2)}"})
        
        # Add conversation history
        messages.extend(self.conversation_history)
        
        try:
            # Get response from OpenAI
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=1500,
                temperature=0.7
            )
            
            assistant_response = response.choices[0].message.content
            
            # Add assistant response to memory
            self.add_to_memory("assistant", assistant_response)
            
            return assistant_response, metadata
            
        except Exception as e:
            error_msg = f"Error in executive decision making: {e}"
            return error_msg, metadata
    
    def get_agent_capabilities(self) -> Dict[str, Any]:
        """Return comprehensive capabilities across all managed agents"""
        domain_capabilities = {}
        for name, manager in self.domain_managers.items():
            if hasattr(manager, 'get_agent_capabilities'):
                domain_capabilities[name] = manager.get_agent_capabilities()
        
        return {
            "name": "Director of Agents",
            "description": "Executive-level AI coordinator managing comprehensive life assistance",
            "capabilities": [
                "strategic_coordination",
                "multi_domain_integration",
                "executive_decision_making",
                "cross_domain_analytics",
                "goal_alignment",
                "resource_prioritization"
            ],
            "domain_managers": domain_capabilities,
            "tools": [
                "route_to_domain_manager",
                "handle_multi_domain_request",
                "get_cross_domain_insights",
                "detect_multi_domain_request"
            ],
            "data_sources": ["cross_domain_analytics", "supabase_integration"],
            "ai_model": "gpt-4o-mini",
            "agent_type": "executive_coordinator",
            "hierarchy_level": "top"
        }
    
    def get_conversation_summary(self) -> str:
        """Get comprehensive conversation summary including all domain interactions"""
        if not self.conversation_history:
            return "No conversation history"
        
        # Create executive summary
        recent_messages = self.conversation_history[-8:]  # More context for executive decisions
        summary_parts = []
        
        for msg in recent_messages:
            role = "User" if msg["role"] == "user" else "Director"
            content = msg["content"][:200] + "..." if len(msg["content"]) > 200 else msg["content"]
            summary_parts.append(f"{role}: {content}")
        
        # Add domain manager status
        active_domains = [name for name, manager in self.domain_managers.items() if manager]
        summary_parts.append(f"\nActive Domain Managers: {', '.join(active_domains)}")
        
        return "\n".join(summary_parts)
    
    def get_executive_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive executive dashboard across all domains"""
        dashboard = {
            "director_status": "active",
            "domain_managers": {},
            "cross_domain_insights": self.get_cross_domain_insights(),
            "last_updated": datetime.now().isoformat()
        }
        
        # Collect dashboards from each domain manager
        for name, manager in self.domain_managers.items():
            if hasattr(manager, 'get_health_dashboard') and name == 'health_manager':
                dashboard["domain_managers"][name] = manager.get_health_dashboard()
            elif hasattr(manager, 'get_agent_capabilities'):
                dashboard["domain_managers"][name] = {
                    "capabilities": manager.get_agent_capabilities(),
                    "status": "active"
                }
        
        return dashboard
    
    def delegate_to_health_manager(self, message: str) -> Tuple[str, Dict[str, Any]]:
        """Directly delegate to the Health Manager"""
        if 'health_manager' in self.domain_managers:
            return self.domain_managers['health_manager'].chat(message)
        else:
            return "Health Manager not available", {}
    
    def coordinate_domains(self, request: str, domains: List[str]) -> str:
        """Coordinate a specific request across multiple domains"""
        coordination_results = {}
        
        for domain in domains:
            if domain in self.domain_managers:
                try:
                    response, metadata = self.domain_managers[domain].chat(request)
                    coordination_results[domain] = response
                except Exception as e:
                    coordination_results[domain] = f"Error: {e}"
        
        return f"Coordinated response across {', '.join(domains)}:\n" + \
               "\n".join([f"{domain}: {response}" for domain, response in coordination_results.items()]) 