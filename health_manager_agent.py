"""
Health Manager Agent
A top-level health management agent that coordinates multiple health-related sub-agents.
Manages overall health goals, tracks progress, and routes requests to appropriate specialists.
"""

import os
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple, Union
from dotenv import load_dotenv
from supabase import create_client, Client
from openai import OpenAI

# Import our sub-agents
from personal_chef_agent_core import PersonalChefAgent
from equipment_manager_agent import EquipmentManagerAgent

class HealthManagerAgent:
    """
    Health Manager AI Agent - orchestrates comprehensive health management.
    
    This agent provides:
    - Overall health goal coordination
    - Progress tracking across multiple health domains
    - Sub-agent management (Personal Chef, Fitness Trainer, etc.)
    - Health analytics and insights
    - Personalized health recommendations
    """
    
    def __init__(self, 
                 openai_api_key: Optional[str] = None,
                 supabase_url: Optional[str] = None, 
                 supabase_key: Optional[str] = None,
                 health_area_id: Optional[str] = None):
        """
        Initialize the Health Manager Agent.
        
        Args:
            openai_api_key: OpenAI API key (uses env var if not provided)
            supabase_url: Supabase URL (uses env var if not provided)
            supabase_key: Supabase key (uses env var if not provided)
            health_area_id: Health area ID for filtering goals (uses default if not provided)
        """
        # Load environment variables if not provided
        load_dotenv()
        
        # Initialize OpenAI client
        api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required")
        self.openai_client = OpenAI(api_key=api_key)
        
        # Initialize Supabase client
        url = supabase_url or os.getenv("SUPABASE_URL")
        key = supabase_key or os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("Supabase URL and key are required")
        self.supabase: Client = create_client(url, key)
        
        # Conversation memory
        self.conversation_history = []
        self.max_memory = 15  # Keep more messages for complex health discussions
        
        # Health area ID
        self.health_area_id = health_area_id or "536ade3b-2f55-4f91-ada8-5ff851caf43f"
        
        # Initialize sub-agents
        self.sub_agents = {}
        self._initialize_sub_agents()
        
        # Agent routing keywords
        self.agent_routing = {
            'personal_chef': [
                'meal', 'food', 'eat', 'cook', 'recipe', 'nutrition', 'calories', 
                'protein', 'carbs', 'fats', 'breakfast', 'lunch', 'dinner', 'snack',
                'hungry', 'diet', 'cookbook', 'ingredient', 'log meal'
            ],
            'equipment_manager': [
                'equipment', 'gym equipment', 'weights', 'dumbbells', 'treadmill',
                'bike', 'home gym', 'office gym', 'gear', 'machine', 'barbell',
                'kettlebell', 'yoga mat', 'bench', 'rack', 'add equipment',
                'buy equipment', 'new equipment', 'equipment list', 'what equipment'
            ],
            # Future sub-agents can be added here
            'fitness_trainer': [
                'workout', 'exercise', 'cardio', 'strength', 'training',
                'fitness', 'muscle', 'weight lifting', 'run', 'jog'
            ],
            'health_tracker': [
                'weight', 'blood pressure', 'heart rate', 'sleep', 'steps',
                'vitals', 'measurement', 'progress', 'tracking'
            ]
        }
    
    def _initialize_sub_agents(self):
        """Initialize all available sub-agents"""
        try:
            # Initialize Personal Chef Agent
            self.sub_agents['personal_chef'] = PersonalChefAgent(
                openai_api_key=os.getenv("OPENAI_API_KEY"),
                supabase_url=os.getenv("SUPABASE_URL"),
                supabase_key=os.getenv("SUPABASE_KEY"),
                health_area_id=self.health_area_id
            )
            print("✅ Personal Chef Agent initialized")
        except Exception as e:
            print(f"❌ Failed to initialize Personal Chef Agent: {e}")
        
        try:
            # Initialize Equipment Manager Agent
            self.sub_agents['equipment_manager'] = EquipmentManagerAgent(
                openai_api_key=os.getenv("OPENAI_API_KEY"),
                supabase_url=os.getenv("SUPABASE_URL"),
                supabase_key=os.getenv("SUPABASE_KEY"),
                health_area_id=self.health_area_id
            )
            print("✅ Equipment Manager Agent initialized")
        except Exception as e:
            print(f"❌ Failed to initialize Equipment Manager Agent: {e}")
        
        # Placeholder for future sub-agents
        # self.sub_agents['fitness_trainer'] = FitnessTrainerAgent(...)
        # self.sub_agents['health_tracker'] = HealthTrackerAgent(...)
    
    def get_all_health_goals(self) -> List[Dict]:
        """Get all health goals across different areas"""
        try:
            response = self.supabase.table("goals").select("*").execute()
            return response.data
        except Exception as e:
            return []
    
    def get_health_progress(self) -> Dict[str, Any]:
        """Get comprehensive health progress across all domains"""
        try:
            # Get recent meals for nutrition analysis
            recent_meals = self.supabase.table("food_log").select("*").gte(
                "meal_time", (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            ).execute()
            
            # Calculate nutrition totals for the week
            total_calories = sum(meal.get('calories', 0) for meal in recent_meals.data)
            total_protein = sum(meal.get('protein', 0) for meal in recent_meals.data)
            total_carbs = sum(meal.get('carbs', 0) for meal in recent_meals.data)
            total_fats = sum(meal.get('fats', 0) for meal in recent_meals.data)
            
            return {
                "nutrition": {
                    "weekly_calories": total_calories,
                    "weekly_protein": total_protein,
                    "weekly_carbs": total_carbs,
                    "weekly_fats": total_fats,
                    "meals_logged": len(recent_meals.data),
                    "daily_avg_calories": total_calories / 7 if total_calories > 0 else 0
                },
                "goals": self.get_all_health_goals(),
                "period": "last_7_days"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def route_to_sub_agent(self, user_message: str) -> Optional[str]:
        """Determine which sub-agent should handle the request"""
        message_lower = user_message.lower()
        
        # Check each agent's keywords
        for agent_name, keywords in self.agent_routing.items():
            if any(keyword in message_lower for keyword in keywords):
                return agent_name
        
        return None
    
    def create_system_prompt(self) -> str:
        """Create the system prompt for the Health Manager agent"""
        available_agents = list(self.sub_agents.keys())
        
        return f"""You are a Health Manager AI assistant. You are the top-level health coordinator responsible for managing a user's overall health and wellness journey.

You have access to these specialized sub-agents:
{', '.join(available_agents)}

Your primary responsibilities:
1. **Health Goal Coordination**: Help users set, track, and achieve comprehensive health goals
2. **Progress Monitoring**: Analyze progress across nutrition, fitness, sleep, and other health metrics
3. **Agent Routing**: Determine when to delegate specific tasks to sub-agents vs handling them yourself
4. **Health Insights**: Provide holistic health analysis and recommendations
5. **Lifestyle Coaching**: Offer guidance on sustainable health habits

When to route to sub-agents:
- **Personal Chef**: Food, meals, nutrition tracking, cooking, recipes, dietary questions
- **Equipment Manager**: Equipment inventory, gym equipment, home gym setup, equipment recommendations
- **Fitness Trainer**: Workouts, exercise plans, fitness goals (when available)
- **Health Tracker**: Vital signs, measurements, progress tracking (when available)

When to handle yourself:
- Overall health strategy and goal setting
- Cross-domain health insights (nutrition + fitness + sleep)
- Health education and general wellness advice
- Motivational support and accountability
- Complex health decisions requiring multiple perspectives

Communication style:
- Be supportive and encouraging
- Use data-driven insights when available
- Acknowledge when routing to specialists
- Provide holistic perspective on health decisions

If routing to a sub-agent, explain why and what they'll help with. If handling the request yourself, provide comprehensive health management guidance."""

    def handle_health_analysis(self, context: str = "") -> str:
        """Provide comprehensive health analysis and insights"""
        progress = self.get_health_progress()
        goals = self.get_all_health_goals()
        
        analysis_parts = []
        
        # Nutrition analysis
        if progress.get("nutrition"):
            nutrition = progress["nutrition"]
            analysis_parts.append(f"""
**Nutrition Analysis (Last 7 Days):**
- Total Calories: {nutrition['weekly_calories']:,}
- Daily Average: {nutrition['daily_avg_calories']:.0f} calories
- Protein: {nutrition['weekly_protein']}g | Carbs: {nutrition['weekly_carbs']}g | Fats: {nutrition['weekly_fats']}g
- Meals Logged: {nutrition['meals_logged']}
""")
        
        # Goals analysis
        if goals:
            analysis_parts.append(f"**Active Health Goals:** {len(goals)} goals tracked")
            for goal in goals[:3]:  # Show first 3 goals
                analysis_parts.append(f"- {goal.get('description', 'Goal')}")
        
        return "\n".join(analysis_parts) if analysis_parts else "No health data available for analysis."
    
    def add_to_memory(self, role: str, content: str):
        """Add message to conversation memory"""
        self.conversation_history.append({"role": role, "content": content})
        
        # Keep only the last max_memory messages
        if len(self.conversation_history) > self.max_memory:
            self.conversation_history = self.conversation_history[-self.max_memory:]
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.conversation_history = []
        # Also clear sub-agent memories
        for agent in self.sub_agents.values():
            if hasattr(agent, 'clear_memory'):
                agent.clear_memory()
    
    def chat(self, user_message: str) -> Tuple[str, Dict[str, Any]]:
        """
        Main chat function for the Health Manager Agent.
        
        Args:
            user_message: The user's message/question
            
        Returns:
            Tuple of (assistant_response, metadata_dict)
        """
        # Add user message to memory
        self.add_to_memory("user", user_message)
        
        # Determine if we should route to a sub-agent
        target_agent = self.route_to_sub_agent(user_message)
        
        metadata = {
            "routed_to": target_agent,
            "handled_by": "health_manager",
            "sub_agent_response": None,
            "meal_logged": False,
            "equipment_added": False
        }
        
        # Route to sub-agent if appropriate
        if target_agent and target_agent in self.sub_agents:
            try:
                if target_agent == 'personal_chef':
                    response, meal_logged = self.sub_agents[target_agent].chat(user_message)
                    metadata["sub_agent_response"] = response
                    metadata["meal_logged"] = meal_logged
                    metadata["handled_by"] = target_agent
                    
                    # Create a coordination response
                    coord_response = f"I've connected you with your Personal Chef specialist for this request.\n\n**Personal Chef Response:**\n{response}"
                    
                    # Add to our memory
                    self.add_to_memory("assistant", coord_response)
                    return coord_response, metadata
                
                elif target_agent == 'equipment_manager':
                    response, equipment_added = self.sub_agents[target_agent].chat(user_message)
                    metadata["sub_agent_response"] = response
                    metadata["equipment_added"] = equipment_added
                    metadata["handled_by"] = target_agent
                    
                    # Create a coordination response
                    coord_response = f"I've connected you with your Equipment Manager specialist for this request.\n\n**Equipment Manager Response:**\n{response}"
                    
                    # Add to our memory
                    self.add_to_memory("assistant", coord_response)
                    return coord_response, metadata
                
                # Handle other sub-agents when available
                else:
                    response = f"I would route this to your {target_agent.replace('_', ' ').title()} specialist, but that agent is not yet available. Let me help you with general health guidance instead."
            
            except Exception as e:
                response = f"There was an issue connecting to your {target_agent.replace('_', ' ').title()} specialist. Let me help you directly."
        
        # Handle the request ourselves
        metadata["handled_by"] = "health_manager"
        
        # Build messages for OpenAI
        messages = [
            {"role": "system", "content": self.create_system_prompt()}
        ]
        
        # Add health context for complex queries
        if any(word in user_message.lower() for word in ['progress', 'analysis', 'goals', 'overview', 'summary']):
            health_context = self.handle_health_analysis()
            messages.append({"role": "system", "content": f"Current Health Context:\n{health_context}"})
        
        # Add conversation history
        messages.extend(self.conversation_history)
        
        try:
            # Get response from OpenAI
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=1200,
                temperature=0.7
            )
            
            assistant_response = response.choices[0].message.content
            
            # Add assistant response to memory
            self.add_to_memory("assistant", assistant_response)
            
            return assistant_response, metadata
            
        except Exception as e:
            error_msg = f"Error communicating with OpenAI: {e}"
            return error_msg, metadata
    
    def get_agent_capabilities(self) -> Dict[str, Any]:
        """Return a description of this agent's capabilities for the agent network"""
        sub_agent_caps = {}
        for name, agent in self.sub_agents.items():
            if hasattr(agent, 'get_agent_capabilities'):
                sub_agent_caps[name] = agent.get_agent_capabilities()
        
        return {
            "name": "Health Manager Agent",
            "description": "Top-level health coordination and management system",
            "capabilities": [
                "health_goal_coordination",
                "progress_monitoring", 
                "agent_routing",
                "health_insights",
                "lifestyle_coaching",
                "cross_domain_analysis"
            ],
            "sub_agents": sub_agent_caps,
            "tools": [
                "get_all_health_goals",
                "get_health_progress",
                "route_to_sub_agent",
                "handle_health_analysis"
            ],
            "data_sources": ["supabase_health_db"],
            "ai_model": "gpt-4o-mini",
            "agent_type": "coordinator"
        }
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation including sub-agent interactions"""
        if not self.conversation_history:
            return "No conversation history"
        
        # Create a comprehensive summary
        recent_messages = self.conversation_history[-6:]  # Last 6 messages
        summary_parts = []
        
        for msg in recent_messages:
            role = "User" if msg["role"] == "user" else "Health Manager"
            content = msg["content"][:150] + "..." if len(msg["content"]) > 150 else msg["content"]
            summary_parts.append(f"{role}: {content}")
        
        # Add sub-agent status
        active_agents = [name for name, agent in self.sub_agents.items() if agent]
        summary_parts.append(f"\nActive Sub-Agents: {', '.join(active_agents)}")
        
        return "\n".join(summary_parts)
    
    def delegate_to_chef(self, message: str) -> Tuple[str, bool]:
        """Directly delegate to the Personal Chef agent"""
        if 'personal_chef' in self.sub_agents:
            return self.sub_agents['personal_chef'].chat(message)
        else:
            return "Personal Chef agent not available", False
    
    def get_health_dashboard(self) -> Dict[str, Any]:
        """Get a comprehensive health dashboard"""
        progress = self.get_health_progress()
        goals = self.get_all_health_goals()
        
        # Get sub-agent statuses
        agent_status = {}
        for name, agent in self.sub_agents.items():
            agent_status[name] = {
                "available": agent is not None,
                "capabilities": agent.get_agent_capabilities() if hasattr(agent, 'get_agent_capabilities') else {}
            }
        
        return {
            "health_progress": progress,
            "goals": goals,
            "sub_agents": agent_status,
            "last_updated": datetime.now().isoformat()
        } 