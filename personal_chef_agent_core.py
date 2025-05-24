"""
Personal Chef Agent Core
A reusable agent class for meal planning, nutrition tracking, and cooking assistance.
Designed for integration into larger agent networks.
"""

import os
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv
from supabase import create_client, Client
from openai import OpenAI

class PersonalChefAgent:
    """
    Personal Chef AI Agent for meal planning, nutrition tracking, and cooking assistance.
    
    This agent provides:
    - Intelligent meal suggestions based on health goals
    - Automatic meal logging with nutritional tracking
    - Recipe management and cookbook access
    - Health goal integration
    - Conversation memory
    """
    
    def __init__(self, 
                 openai_api_key: Optional[str] = None,
                 supabase_url: Optional[str] = None, 
                 supabase_key: Optional[str] = None,
                 health_area_id: Optional[str] = None):
        """
        Initialize the Personal Chef Agent.
        
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
        self.max_memory = 10  # Keep last 10 messages
        
        # Health area ID from the n8n config or provided
        self.health_area_id = health_area_id or "536ade3b-2f55-4f91-ada8-5ff851caf43f"
        
    def get_health_goals(self) -> List[Dict]:
        """Get health goals from Supabase"""
        try:
            response = self.supabase.table("goals").select("*").eq("area", self.health_area_id).execute()
            return response.data
        except Exception as e:
            return []
    
    def get_meal_types(self) -> List[Dict]:
        """Get all meal types from Supabase"""
        try:
            response = self.supabase.table("meal_type").select("*").execute()
            return response.data
        except Exception as e:
            return []
    
    def get_cookbook(self, meal_type_id: Optional[str] = None) -> List[Dict]:
        """Get cookbook recipes, optionally filtered by meal type"""
        try:
            query = self.supabase.table("cookbook").select("*")
            if meal_type_id:
                query = query.eq("meal_type", meal_type_id)
            response = query.execute()
            return response.data
        except Exception as e:
            return []
    
    def log_meal(self, meal_details: str, calories: int, protein: int, carbs: int, fats: int, meal_time: Optional[str] = None) -> bool:
        """Log a meal to the food_log table"""
        try:
            if not meal_time:
                meal_time = datetime.now().isoformat()
            
            data = {
                "meal_details": meal_details,
                "calories": int(calories),
                "protein": int(protein),
                "carbs": int(carbs),
                "fats": int(fats),
                "meal_time": meal_time
            }
            
            response = self.supabase.table("food_log").insert(data).execute()
            return True
        except Exception as e:
            return False
    
    def get_meals_for_today(self) -> List[Dict]:
        """Get all meals logged for today"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            response = self.supabase.table("food_log").select("*").gte("meal_time", today).execute()
            return response.data
        except Exception as e:
            return []
    
    def get_meals_last_3_days(self) -> List[Dict]:
        """Get meals from the last 3 days"""
        try:
            three_days_ago = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
            response = self.supabase.table("food_log").select("*").gte("meal_time", three_days_ago).execute()
            return response.data
        except Exception as e:
            return []
    
    def get_current_date_time(self) -> str:
        """Get current date and time"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S CST")
    
    def create_system_prompt(self) -> str:
        """Create the system prompt for the Personal Chef agent"""
        return """You are a Personal Chef AI assistant. Your role is to help users with meal planning, nutrition tracking, and cooking advice based on their health goals and preferences.

You have access to the following tools and data:
1. Health goals for the user
2. Available meal types (breakfast, lunch, dinner, snacks, etc.)
3. A cookbook with recipes
4. Ability to log meals with nutritional information
5. Recent meal history

Key capabilities:
- Suggest meals based on health goals and available recipes
- Help track nutritional information (calories, protein, carbs, fats)
- Log meals when users eat something
- Review recent eating patterns
- Provide cooking advice and recipe modifications

IMPORTANT: When a user tells you they ate something or want to log a meal, you should:
1. Ask for details if needed (ingredients, portions, cooking method)
2. Calculate or estimate the nutritional values
3. Respond with a meal logging format like this:

**MEAL_LOG:**
- meal_details: [detailed description]
- calories: [number]
- protein: [number in grams]
- carbs: [number in grams] 
- fats: [number in grams]
- meal_time: [current timestamp]

Be helpful, encouraging, and focused on the user's health and nutrition goals. Always ask clarifying questions if you need more information to provide better assistance."""

    def extract_meal_log_from_response(self, response: str) -> Optional[Dict]:
        """Extract meal logging information from assistant response"""
        # Look for MEAL_LOG pattern
        meal_log_pattern = r'\*\*MEAL_LOG:\*\*(.*?)(?=\n\n|\Z)'
        match = re.search(meal_log_pattern, response, re.DOTALL)
        
        if not match:
            return None
        
        meal_log_text = match.group(1)
        
        # Extract individual fields
        patterns = {
            'meal_details': r'meal_details:\s*(.+?)(?=\n-|\Z)',
            'calories': r'calories:\s*(\d+)',
            'protein': r'protein:\s*(\d+)',
            'carbs': r'carbs:\s*(\d+)',
            'fats': r'fats:\s*(\d+)',
        }
        
        meal_data = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, meal_log_text, re.IGNORECASE)
            if match:
                meal_data[key] = match.group(1).strip()
        
        # Validate we have all required fields
        required_fields = ['meal_details', 'calories', 'protein', 'carbs', 'fats']
        if all(field in meal_data for field in required_fields):
            return meal_data
        
        return None
    
    def format_tool_response(self, tool_name: str, data: Any) -> str:
        """Format tool responses for the AI"""
        if not data:
            return f"{tool_name}: No data found"
        
        if isinstance(data, list):
            return f"{tool_name}:\n" + "\n".join([json.dumps(item, default=str) for item in data])
        else:
            return f"{tool_name}: {json.dumps(data, default=str)}"
    
    def determine_tools_needed(self, user_message: str) -> List[str]:
        """Determine which tools might be needed based on user message"""
        tools_needed = []
        
        message_lower = user_message.lower()
        
        # Always get current date for context
        tools_needed.append("current_date")
        
        # Keywords that suggest different tools
        if any(word in message_lower for word in ["goal", "health", "target", "objective"]):
            tools_needed.append("health_goals")
        
        if any(word in message_lower for word in ["meal type", "breakfast", "lunch", "dinner", "snack"]):
            tools_needed.append("meal_types")
        
        if any(word in message_lower for word in ["recipe", "cook", "how to make", "cookbook", "dish"]):
            tools_needed.append("cookbook")
        
        if any(word in message_lower for word in ["today", "eaten today", "meals today"]):
            tools_needed.append("meals_today")
        
        if any(word in message_lower for word in ["recent", "last few days", "past days", "history"]):
            tools_needed.append("meals_recent")
        
        return tools_needed
    
    def gather_context(self, tools_needed: List[str]) -> str:
        """Gather context from various tools"""
        context_parts = []
        
        if "current_date" in tools_needed:
            current_time = self.get_current_date_time()
            context_parts.append(f"Current date/time: {current_time}")
        
        if "health_goals" in tools_needed:
            goals = self.get_health_goals()
            context_parts.append(self.format_tool_response("Health Goals", goals))
        
        if "meal_types" in tools_needed:
            meal_types = self.get_meal_types()
            context_parts.append(self.format_tool_response("Available Meal Types", meal_types))
        
        if "cookbook" in tools_needed:
            cookbook = self.get_cookbook()
            context_parts.append(self.format_tool_response("Cookbook Recipes", cookbook))
        
        if "meals_today" in tools_needed:
            today_meals = self.get_meals_for_today()
            context_parts.append(self.format_tool_response("Today's Meals", today_meals))
        
        if "meals_recent" in tools_needed:
            recent_meals = self.get_meals_last_3_days()
            context_parts.append(self.format_tool_response("Recent Meals (Last 3 Days)", recent_meals))
        
        return "\n\n".join(context_parts)
    
    def add_to_memory(self, role: str, content: str):
        """Add message to conversation memory"""
        self.conversation_history.append({"role": role, "content": content})
        
        # Keep only the last max_memory messages
        if len(self.conversation_history) > self.max_memory:
            self.conversation_history = self.conversation_history[-self.max_memory:]
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.conversation_history = []
    
    def chat(self, user_message: str, auto_log_meals: bool = True) -> Tuple[str, bool]:
        """
        Main chat function for interacting with the Personal Chef Agent.
        
        Args:
            user_message: The user's message/question
            auto_log_meals: Whether to automatically log meals when detected
            
        Returns:
            Tuple of (assistant_response, meal_logged_successfully)
        """
        # Add user message to memory
        self.add_to_memory("user", user_message)
        
        # Determine what tools/context we need
        tools_needed = self.determine_tools_needed(user_message)
        
        # Gather relevant context
        context = self.gather_context(tools_needed)
        
        # Build messages for OpenAI
        messages = [
            {"role": "system", "content": self.create_system_prompt()}
        ]
        
        # Add context if available
        if context:
            messages.append({"role": "system", "content": f"Current context:\n{context}"})
        
        # Add conversation history
        messages.extend(self.conversation_history)
        
        try:
            # Get response from OpenAI
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            assistant_response = response.choices[0].message.content
            
            # Check if we need to log a meal
            meal_logged = False
            if auto_log_meals:
                meal_data = self.extract_meal_log_from_response(assistant_response)
                
                if meal_data:
                    success = self.log_meal(
                        meal_details=meal_data['meal_details'],
                        calories=int(meal_data['calories']),
                        protein=int(meal_data['protein']),
                        carbs=int(meal_data['carbs']),
                        fats=int(meal_data['fats'])
                    )
                    
                    if success:
                        meal_logged = True
                        assistant_response += "\n\n✅ **Meal logged successfully!**"
                    else:
                        assistant_response += "\n\n❌ **Failed to log meal. Please try again.**"
            
            # Add assistant response to memory
            self.add_to_memory("assistant", assistant_response)
            
            return assistant_response, meal_logged
            
        except Exception as e:
            error_msg = f"Error communicating with OpenAI: {e}"
            return error_msg, False
    
    # Additional utility methods for agent network integration
    def get_agent_capabilities(self) -> Dict[str, Any]:
        """Return a description of this agent's capabilities for the agent network"""
        return {
            "name": "Personal Chef Agent",
            "description": "Provides meal planning, nutrition tracking, and cooking assistance",
            "capabilities": [
                "meal_planning",
                "nutrition_tracking", 
                "recipe_suggestions",
                "health_goal_integration",
                "meal_logging"
            ],
            "tools": [
                "get_health_goals",
                "get_meal_types", 
                "get_cookbook",
                "log_meal",
                "get_meals_for_today",
                "get_meals_last_3_days"
            ],
            "data_sources": ["supabase_health_db"],
            "ai_model": "gpt-4o-mini"
        }
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation for handoff to other agents"""
        if not self.conversation_history:
            return "No conversation history"
        
        # Create a simple summary of recent interactions
        recent_messages = self.conversation_history[-4:]  # Last 4 messages
        summary_parts = []
        
        for msg in recent_messages:
            role = "User" if msg["role"] == "user" else "Chef"
            content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
            summary_parts.append(f"{role}: {content}")
        
        return "\n".join(summary_parts) 