"""
Equipment Manager Agent
A specialist agent for managing gym and fitness equipment.
Handles equipment viewing, adding, and organization by equipment groups (home gym, office, gym, etc.).
"""

import os
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv
from supabase import create_client, Client
from openai import OpenAI

class EquipmentManagerAgent:
    """
    Equipment Manager AI Agent for equipment tracking and management.
    
    This agent provides:
    - Equipment inventory management across different locations
    - Equipment group organization (home gym, office, gym, etc.)
    - Equipment recommendations and suggestions
    - Equipment condition and maintenance tracking
    - Integration with health and fitness goals
    """
    
    def __init__(self, 
                 openai_api_key: Optional[str] = None,
                 supabase_url: Optional[str] = None, 
                 supabase_key: Optional[str] = None,
                 health_area_id: Optional[str] = None):
        """
        Initialize the Equipment Manager Agent.
        
        Args:
            openai_api_key: OpenAI API key (uses env var if not provided)
            supabase_url: Supabase URL (uses env var if not provided)
            supabase_key: Supabase key (uses env var if not provided)
            health_area_id: Health area ID for filtering equipment groups (uses default if not provided)
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
        
    def get_equipment_groups(self) -> List[Dict]:
        """Get all equipment groups for the health area from Supabase"""
        try:
            response = self.supabase.table("equipment_groups").select("*").eq("area", self.health_area_id).execute()
            return response.data
        except Exception as e:
            return []
    
    def get_equipment_items(self, equipment_group_id: Optional[str] = None) -> List[Dict]:
        """Get equipment items, optionally filtered by equipment group"""
        try:
            query = self.supabase.table("equipment_items").select("*")
            if equipment_group_id:
                query = query.eq("equipment_group", equipment_group_id)
            response = query.execute()
            return response.data
        except Exception as e:
            return []
    
    def add_equipment_item(self, item_name: str, item_description: str, equipment_group_id: str) -> bool:
        """Add a new equipment item to the specified equipment group"""
        try:
            data = {
                "item_name": item_name.strip(),
                "item_description": item_description.strip(),
                "equipment_group": equipment_group_id.strip()
            }
            
            response = self.supabase.table("equipment_items").insert(data).execute()
            return True
        except Exception as e:
            return False
    
    def get_equipment_by_group_name(self, group_name: str) -> Tuple[Optional[Dict], List[Dict]]:
        """Get equipment group and its items by group name"""
        try:
            # Get equipment groups
            groups = self.get_equipment_groups()
            
            # Find matching group (case insensitive)
            matching_group = None
            for group in groups:
                if group.get('group_name', '').lower() == group_name.lower():
                    matching_group = group
                    break
            
            if not matching_group:
                return None, []
            
            # Get items for this group
            items = self.get_equipment_items(matching_group['id'])
            return matching_group, items
        except Exception as e:
            return None, []
    
    def get_current_date_time(self) -> str:
        """Get current date and time"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S CST")
    
    def create_system_prompt(self) -> str:
        """Create the system prompt for the Equipment Manager agent"""
        return """You are an Equipment Manager AI assistant. Your role is to help users manage their fitness and exercise equipment across different locations and settings.

You have access to the following tools and data:
1. Equipment groups (home gym, office, gym, etc.) organized by health area
2. Equipment items within each group
3. Ability to add new equipment items
4. Equipment organization and categorization

Key capabilities:
- View equipment by location/group (home gym, office, gym, etc.)
- Add new equipment items with descriptions
- Organize equipment by categories and locations
- Provide equipment recommendations based on fitness goals
- Help plan equipment purchases and setup

IMPORTANT: When a user wants to add equipment, you should:
1. Ask for details if needed (equipment name, description, location/group)
2. Identify the correct equipment group
3. Respond with an equipment addition format like this:

**EQUIPMENT_ADD:**
- item_name: [equipment name]
- item_description: [detailed description]
- equipment_group_id: [group ID]

Equipment Groups Context:
- Home Gym: Personal equipment at home
- Office: Equipment available at workplace
- Gym: Commercial gym equipment
- Outdoor: Parks, trails, outdoor fitness areas

Communication style:
- Be helpful and encouraging about fitness equipment
- Focus on practical equipment solutions
- Consider space, budget, and fitness goals
- Provide equipment maintenance and usage tips
- Ask clarifying questions when needed"""

    def extract_equipment_add_from_response(self, response: str) -> Optional[Dict]:
        """Extract equipment addition information from assistant response"""
        # Look for EQUIPMENT_ADD pattern
        equipment_add_pattern = r'\*\*EQUIPMENT_ADD:\*\*(.*?)(?=\n\n|\Z)'
        match = re.search(equipment_add_pattern, response, re.DOTALL)
        
        if not match:
            return None
        
        equipment_add_text = match.group(1)
        
        # Extract individual fields
        patterns = {
            'item_name': r'item_name:\s*(.+?)(?=\n-|\Z)',
            'item_description': r'item_description:\s*(.+?)(?=\n-|\Z)',
            'equipment_group_id': r'equipment_group_id:\s*(.+?)(?=\n-|\Z)',
        }
        
        equipment_data = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, equipment_add_text, re.IGNORECASE)
            if match:
                equipment_data[key] = match.group(1).strip()
        
        # Validate we have all required fields
        required_fields = ['item_name', 'item_description', 'equipment_group_id']
        if all(field in equipment_data for field in required_fields):
            return equipment_data
        
        return None
    
    def format_tool_response(self, tool_name: str, data: Any) -> str:
        """Format tool response data for context"""
        if tool_name == "equipment_groups":
            if not data:
                return "No equipment groups found."
            
            groups_text = "Available Equipment Groups:\n"
            for group in data:
                groups_text += f"- {group.get('group_name', 'Unknown')} (ID: {group.get('id', 'Unknown')})\n"
                if group.get('description'):
                    groups_text += f"  Description: {group['description']}\n"
            return groups_text
        
        elif tool_name == "equipment_items":
            if not data:
                return "No equipment items found."
            
            items_text = "Equipment Items:\n"
            for item in data:
                items_text += f"- {item.get('item_name', 'Unknown')}\n"
                if item.get('item_description'):
                    items_text += f"  Description: {item['item_description']}\n"
            return items_text
        
        elif tool_name == "equipment_by_group":
            group, items = data
            if not group:
                return "Equipment group not found."
            
            result = f"Equipment Group: {group.get('group_name', 'Unknown')}\n"
            if group.get('description'):
                result += f"Description: {group['description']}\n"
            
            result += f"\nEquipment Items ({len(items)}):\n"
            if items:
                for item in items:
                    result += f"- {item.get('item_name', 'Unknown')}\n"
                    if item.get('item_description'):
                        result += f"  Description: {item['item_description']}\n"
            else:
                result += "No equipment items in this group yet.\n"
            
            return result
        
        return str(data)
    
    def determine_tools_needed(self, user_message: str) -> List[str]:
        """Determine which tools are needed based on user message"""
        message_lower = user_message.lower()
        tools_needed = []
        
        # Equipment group viewing
        if any(keyword in message_lower for keyword in ['groups', 'locations', 'categories', 'where', 'group']):
            tools_needed.append("equipment_groups")
        
        # Equipment item viewing
        if any(keyword in message_lower for keyword in ['equipment', 'items', 'what equipment', 'show me', 'list']):
            # Check if they're asking about a specific group
            groups = self.get_equipment_groups()
            for group in groups:
                group_name = group.get('group_name', '').lower()
                if group_name in message_lower:
                    tools_needed.append(f"equipment_by_group:{group_name}")
                    break
            else:
                # No specific group mentioned, show all equipment
                tools_needed.append("equipment_items")
        
        # Equipment addition
        if any(keyword in message_lower for keyword in ['add', 'new', 'buy', 'got', 'purchased', 'bought']):
            tools_needed.append("equipment_groups")  # Need to know available groups
        
        return tools_needed if tools_needed else ["equipment_groups"]  # Default to showing groups
    
    def gather_context(self, tools_needed: List[str]) -> str:
        """Gather context using the needed tools"""
        context_parts = []
        
        for tool in tools_needed:
            if tool == "equipment_groups":
                groups = self.get_equipment_groups()
                context_parts.append(self.format_tool_response("equipment_groups", groups))
            
            elif tool == "equipment_items":
                items = self.get_equipment_items()
                context_parts.append(self.format_tool_response("equipment_items", items))
            
            elif tool.startswith("equipment_by_group:"):
                group_name = tool.split(":", 1)[1]
                group, items = self.get_equipment_by_group_name(group_name)
                context_parts.append(self.format_tool_response("equipment_by_group", (group, items)))
        
        return "\n\n".join(context_parts)
    
    def add_to_memory(self, role: str, content: str):
        """Add message to conversation memory"""
        self.conversation_history.append({"role": role, "content": content})
        if len(self.conversation_history) > self.max_memory * 2:  # *2 for user/assistant pairs
            self.conversation_history = self.conversation_history[-self.max_memory * 2:]
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.conversation_history = []
    
    def chat(self, user_message: str, auto_add_equipment: bool = True) -> Tuple[str, bool]:
        """
        Chat with the Equipment Manager agent.
        
        Args:
            user_message: User's message
            auto_add_equipment: Whether to automatically add equipment when detected
            
        Returns:
            Tuple of (response, equipment_added)
        """
        # Add user message to memory
        self.add_to_memory("user", user_message)
        
        # Determine what tools/context we need
        tools_needed = self.determine_tools_needed(user_message)
        
        # Gather context
        context = self.gather_context(tools_needed)
        
        # Create messages for OpenAI
        messages = [
            {"role": "system", "content": self.create_system_prompt()},
            {"role": "system", "content": f"Current context:\n{context}"},
            {"role": "system", "content": f"Current date/time: {self.get_current_date_time()}"}
        ]
        
        # Add conversation history
        messages.extend(self.conversation_history)
        
        try:
            # Get response from OpenAI
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            assistant_response = response.choices[0].message.content
            
            # Add assistant response to memory
            self.add_to_memory("assistant", assistant_response)
            
            # Check for equipment addition
            equipment_added = False
            if auto_add_equipment:
                equipment_data = self.extract_equipment_add_from_response(assistant_response)
                if equipment_data:
                    success = self.add_equipment_item(
                        equipment_data['item_name'],
                        equipment_data['item_description'],
                        equipment_data['equipment_group_id']
                    )
                    equipment_added = success
            
            return assistant_response, equipment_added
            
        except Exception as e:
            error_response = f"I apologize, but I encountered an error: {str(e)}"
            self.add_to_memory("assistant", error_response)
            return error_response, False
    
    def get_agent_capabilities(self) -> Dict[str, Any]:
        """Get agent capabilities and status"""
        return {
            "agent_type": "equipment_manager",
            "hierarchy_level": 3,
            "parent_agent": "health_manager",
            "capabilities": [
                "equipment_inventory_management",
                "equipment_group_organization", 
                "equipment_addition",
                "equipment_recommendations",
                "location_based_equipment_tracking"
            ],
            "data_sources": ["equipment_groups", "equipment_items"],
            "conversation_memory": len(self.conversation_history),
            "health_area_id": self.health_area_id
        }
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation"""
        if not self.conversation_history:
            return "No conversation history yet."
        
        # Count equipment-related interactions
        equipment_queries = sum(1 for msg in self.conversation_history 
                              if msg["role"] == "user" and 
                              any(word in msg["content"].lower() for word in ["equipment", "gym", "add", "show"]))
        
        return f"Equipment management session with {len(self.conversation_history)//2} exchanges. " \
               f"Equipment-related queries: {equipment_queries}" 