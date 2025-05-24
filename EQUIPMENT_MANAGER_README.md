# Equipment Manager Agent

A specialist-level AI agent for managing fitness and exercise equipment across different locations and settings. The Equipment Manager operates as a sub-agent under the Health Manager in the 3-level hierarchical agent architecture.

## 🏗️ Position in Hierarchy

```
🎯 Director of Agents (Level 1)
└── 🏥 Health Manager (Level 2)
    ├── 👨‍🍳 Personal Chef (Level 3)
    └── 🔧 Equipment Manager (Level 3) ← This Agent
```

## 🎯 Purpose & Capabilities

The Equipment Manager agent specializes in:

- **Equipment Inventory Management**: Track equipment across multiple locations
- **Equipment Group Organization**: Organize by location (home gym, office, gym, etc.)
- **Equipment Addition**: Add new equipment with automatic categorization
- **Equipment Recommendations**: Suggest equipment based on fitness goals
- **Location-Based Tracking**: Manage equipment by specific locations

## 🔄 Converted from n8n

This agent was converted from an n8n workflow that included:
- OpenAI Chat Model (gpt-4o-mini)
- Supabase integration for equipment data
- Dynamic parameter extraction with $fromAI()
- Equipment group and item management

**Original n8n Capabilities Preserved:**
- Get equipment groups filtered by health area
- Get equipment items by group
- Create new equipment items
- AI-driven parameter extraction

## 🗄️ Database Schema

The Equipment Manager integrates with these Supabase tables:

### `equipment_groups`
- `id` - Unique identifier
- `group_name` - Name of the equipment group (e.g., "Home Gym", "Office")
- `description` - Optional description
- `area` - Health area ID for filtering (uses same ID as other health agents)

### `equipment_items`
- `id` - Unique identifier
- `item_name` - Name of the equipment item
- `item_description` - Detailed description
- `equipment_group` - Foreign key to equipment_groups

## 🛠️ Core Functions

### Equipment Viewing
```python
# Get all equipment groups
groups = equipment_manager.get_equipment_groups()

# Get equipment items by group
items = equipment_manager.get_equipment_items(group_id)

# Get equipment by group name
group, items = equipment_manager.get_equipment_by_group_name("Home Gym")
```

### Equipment Addition
```python
# Add new equipment item
success = equipment_manager.add_equipment_item(
    item_name="Kettlebell 20kg",
    item_description="Cast iron kettlebell for strength training",
    equipment_group_id="group_uuid"
)
```

### Chat Interface
```python
# Chat with automatic equipment detection
response, equipment_added = equipment_manager.chat(
    "I bought a new set of dumbbells for my home gym"
)
```

## 🔀 Routing & Integration

### Automatic Routing Keywords

The Equipment Manager handles requests containing:
- `equipment`, `gym equipment`, `weights`, `dumbbells`
- `treadmill`, `bike`, `home gym`, `office gym`
- `gear`, `machine`, `barbell`, `kettlebell`
- `yoga mat`, `bench`, `rack`
- `add equipment`, `buy equipment`, `new equipment`
- `equipment list`, `what equipment`

### Integration Flow

1. **User Query**: "What equipment do I have at home?"
2. **Director**: Routes to Health Manager (domain-level)
3. **Health Manager**: Routes to Equipment Manager (specialist-level)
4. **Equipment Manager**: Provides equipment inventory
5. **Response Path**: Equipment Manager → Health Manager → Director → User

## 🎛️ Usage Examples

### Viewing Equipment
```
User: "What gym equipment do I have?"
Equipment Manager: Shows all equipment across all groups

User: "Show me my home gym equipment"
Equipment Manager: Shows only home gym equipment group

User: "What equipment groups do you have?"
Equipment Manager: Lists all available equipment groups
```

### Adding Equipment
```
User: "I bought a new kettlebell for my home gym"
Equipment Manager: Detects addition intent, asks for details if needed

User: "Add 20kg barbell to my office gym setup"
Equipment Manager: Adds with automatic group detection

Auto-format detection:
**EQUIPMENT_ADD:**
- item_name: 20kg Olympic Barbell
- item_description: Standard Olympic barbell for strength training
- equipment_group_id: office-gym-uuid
```

### Equipment Recommendations
```
User: "What equipment should I get for strength training?"
Equipment Manager: Provides recommendations based on goals and space

User: "I have limited space, what's essential?"
Equipment Manager: Suggests space-efficient equipment options
```

## 🚀 Getting Started

### 1. Ensure Database Setup
Make sure your Supabase instance has the required tables:
```sql
-- Equipment Groups table
CREATE TABLE equipment_groups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    group_name TEXT NOT NULL,
    description TEXT,
    area UUID NOT NULL
);

-- Equipment Items table  
CREATE TABLE equipment_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    item_name TEXT NOT NULL,
    item_description TEXT,
    equipment_group UUID REFERENCES equipment_groups(id)
);
```

### 2. Initialize Through Health Manager
```python
from health_manager_agent import HealthManagerAgent

# Equipment Manager is automatically initialized as sub-agent
health_manager = HealthManagerAgent()

# Test equipment routing
response, metadata = health_manager.chat("Show me my equipment")
```

### 3. Use Through Director (Recommended)
```python
from director_of_agents import DirectorOfAgents

director = DirectorOfAgents()
response, metadata = director.chat("What weights do I have at home?")

# Check routing
print(f"Routed to: {metadata.get('domain_metadata', {}).get('routed_to')}")
```

## 🧪 Testing

Run the Equipment Manager test suite:
```bash
python3 test_equipment_manager.py
```

**Test Coverage:**
- ✅ Standalone Equipment Manager functionality
- ✅ Integration with Health Manager
- ✅ Routing through Director of Agents
- ✅ Equipment addition detection
- ✅ Database integration
- ✅ Error handling

## 🔧 Configuration

### Environment Variables
Uses same configuration as other agents:
```
OPENAI_API_KEY=your_openai_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### Health Area ID
Defaults to the same health area ID used by other health agents:
`536ade3b-2f55-4f91-ada8-5ff851caf43f`

## 📊 Metadata & Tracking

### Response Metadata
```python
{
    "handled_by": "equipment_manager",
    "equipment_added": True,  # When equipment is added
    "conversation_memory": 4,  # Messages in memory
    "health_area_id": "uuid"
}
```

### Equipment Addition Tracking
The agent automatically detects and logs when equipment is added:
- Extracts equipment details from natural language
- Validates required fields (name, description, group)
- Returns boolean flag in response metadata
- Updates database automatically

## 🎯 Agent Capabilities

```python
{
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
    "conversation_memory": 10,
    "health_area_id": "536ade3b-2f55-4f91-ada8-5ff851caf43f"
}
```

## 🔮 Future Enhancements

### Planned Features
- **Equipment Maintenance Tracking**: Schedule and track equipment maintenance
- **Usage Analytics**: Track equipment usage patterns and frequency
- **Workout Integration**: Connect equipment with workout routines
- **Purchase Recommendations**: Smart equipment purchase suggestions
- **Condition Monitoring**: Track equipment condition and replacement needs

### Fitness Trainer Integration
When the Fitness Trainer agent is added:
- **Workout-Equipment Matching**: Automatically suggest equipment for workouts
- **Progressive Equipment Planning**: Equipment recommendations for fitness progression
- **Space-Optimized Workouts**: Workouts based on available equipment

## 🎨 CLI Integration

The Equipment Manager is fully integrated into the Director CLI:

```
🎯 Director of Agents
└── 🏥 Health Manager
    ├── 👨‍🍳 Personal Chef
    └── 🔧 Equipment Manager

Domain Management:
• 🏥 Health - nutrition, fitness, wellness, equipment, medical
```

### CLI Routing Display
```
🎯 Director [📋 Routed to Health Manager → Equipment Manager] [🔧 Equipment Added]: 
I've connected you with your Equipment Manager specialist...
```

## 🏆 Success Metrics

- ✅ **Seamless Integration**: Works within 3-level hierarchy
- ✅ **Intelligent Routing**: Automatic equipment query detection
- ✅ **Database Integration**: Full CRUD operations on equipment data
- ✅ **Natural Language Processing**: Understands equipment addition intents
- ✅ **Memory Management**: Maintains conversation context
- ✅ **Error Handling**: Graceful failure handling
- ✅ **Extensible Design**: Ready for fitness trainer integration

The Equipment Manager demonstrates how n8n workflows can be successfully converted into sophisticated, hierarchical AI agent architectures while preserving functionality and adding intelligent coordination capabilities. 