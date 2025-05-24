# Director of Agents System

A sophisticated 3-level hierarchical AI agent architecture demonstrating enterprise-grade agent coordination, multi-domain management, and executive decision-making capabilities.

## 🏗️ Complete Architecture

```
🎯 Director of Agents (Executive Level)
├── 🏥 Health Manager (Domain Level)
│   └── 👨‍🍳 Personal Chef (Specialist Level)
├── 💰 Finance Manager (Future)
├── 📋 Productivity Manager (Future) 
└── 📚 Learning Manager (Future)
```

## 🎯 Executive Layer: Director of Agents

### **Role & Responsibilities**
- **Strategic Coordination**: High-level routing across life domains
- **Multi-Domain Integration**: Complex requests spanning multiple areas
- **Executive Decision Making**: Resource allocation and prioritization
- **Cross-Domain Analytics**: Comprehensive life insights
- **Goal Alignment**: Ensuring all activities support overall objectives

### **Key Capabilities**
```python
# Executive coordination across domains
"Plan healthy meals within my budget" → Health + Finance coordination
"Schedule workouts around work meetings" → Health + Productivity coordination
"Learn cooking while meeting nutrition goals" → Learning + Health coordination
```

## 🏥 Domain Layer: Health Manager

### **Role & Responsibilities**
- Health goal coordination and tracking
- Routing health requests to appropriate specialists
- Cross-health domain insights (nutrition + fitness + wellness)
- Health progress monitoring and analytics

### **Sub-Agent Management**
- **Personal Chef**: Nutrition, meals, recipes, dietary planning
- **Fitness Trainer**: Workouts, exercise planning (future)
- **Health Tracker**: Vitals, measurements, progress (future)

## 👨‍🍳 Specialist Layer: Personal Chef

### **Role & Responsibilities**
- Meal planning and nutrition tracking
- Recipe recommendations and cooking guidance
- Automatic meal logging with nutritional analysis
- Dietary guidance based on health goals

## 🚀 Intelligent Routing System

### **3-Level Routing Logic**

1. **Level 1 (Director)**: Strategic, multi-domain, high-level coordination
2. **Level 2 (Domain Manager)**: Domain-specific coordination and insights
3. **Level 3 (Specialist)**: Detailed task execution and expertise

### **Routing Examples**

| Query | Route | Handler |
|-------|--------|---------|
| "What's my life strategy?" | Director | Executive guidance |
| "How are my health goals?" | Health Manager | Health coordination |
| "What should I eat?" | Health Manager → Personal Chef | Meal planning |
| "Plan meals within budget" | Multi-Domain | Health + Finance coordination |

## 📁 System Architecture

```
director_system/
├── director_of_agents.py           # Executive coordinator
├── health_manager_agent.py         # Health domain manager  
├── personal_chef_agent_core.py     # Nutrition specialist
├── director_cli.py                 # Executive interface
├── test_director.py                # Comprehensive test suite
├── requirements.txt                # Dependencies
└── .env                           # Environment configuration
```

## 🛠️ Core Components

### **1. Director of Agents**
```python
from director_of_agents import DirectorOfAgents

# Initialize the complete hierarchy
director = DirectorOfAgents()

# Executive-level chat with intelligent routing
response, metadata = director.chat("Help me optimize my health and productivity")

# Check routing decisions
print(f"Handled by: {metadata['handled_by']}")
print(f"Coordination type: {metadata.get('coordination_type')}")
```

### **2. Multi-Domain Coordination**
```python
# Detect multi-domain requests
involved_domains = director.detect_multi_domain_request(
    "Plan healthy meal prep around my work schedule"
)
# Returns: ['health_manager', 'productivity_manager']

# Handle coordination
response, metadata = director.handle_multi_domain_request(message, involved_domains)
```

### **3. Executive Dashboard**
```python
# Comprehensive overview across all domains
dashboard = director.get_executive_dashboard()

# Contains:
# - Director status
# - Domain manager health
# - Sub-agent availability  
# - Cross-domain insights
# - Integration opportunities
```

## 🔧 Setup & Deployment

### **1. Environment Setup**
```bash
# Install dependencies
pip3 install openai supabase python-dotenv

# Configure environment
cp env_example.txt .env
# Edit .env with your API keys
```

### **2. Database Configuration**
Required Supabase tables:
- `goals` - Health and life goals with area filtering
- `meal_type` - Available meal categories
- `cookbook` - Recipe database with meal type references
- `food_log` - Nutritional tracking with calorie/macro fields

### **3. Testing**
```bash
# Run comprehensive test suite
python3 test_director.py

# Expected output:
# 🎉 All tests passed! Director of Agents is ready for deployment!
```

### **4. Launch Executive Interface**
```bash
python3 director_cli.py
```

## 💬 Usage Examples

### **Executive Commands**
```
Executive: dashboard
📊 Executive Dashboard
🎯 Director Status: ACTIVE
🏢 Domain Managers (1):
   🏥 Health Manager:
      📈 Weekly Calories: 12,500
      🍽️ Meals Logged: 15
      🤖 Sub-Agents: ['personal_chef']
```

### **Strategic Coordination**
```
Executive: strategy
🎯 Strategic Query: Provide strategic guidance on optimizing my life...

Director: As your executive AI coordinator, I recommend a holistic approach...
[Comprehensive strategic analysis across all life domains]
```

### **Intelligent Routing**
```
Executive: What should I eat for dinner?
🎯 Director [📋 Routed to Health Manager → Personal Chef]: 
I'm coordinating with your Health Manager for this request.

**Strategic Coordination:**
I've connected you with your Personal Chef specialist...
```

### **Multi-Domain Requests**
```
Executive: Plan healthy meals within my budget
🎯 Director [🔄 Multi-Domain: health_manager, finance_manager]:
I'm coordinating across your Health and Finance domains...
[Synthesized response considering both nutrition and budget constraints]
```

## 🧠 Advanced Features

### **Cross-Domain Intelligence**
- **Health + Finance**: Optimize nutrition within budget constraints
- **Health + Productivity**: Schedule wellness activities around work
- **Health + Learning**: Develop cooking skills while meeting dietary goals

### **Executive Analytics**
```python
# Get comprehensive insights across all life domains
insights = director.get_cross_domain_insights()

# Returns:
{
    "domain_statuses": {...},
    "cross_domain_opportunities": [...],
    "integration_suggestions": [...]
}
```

### **Hierarchical Memory Management**
- Director maintains executive conversation context
- Domain managers maintain domain-specific context
- Specialists maintain task-specific context
- Coordinated memory clearing across entire hierarchy

## 🔮 Future Expansion

### **Additional Domain Managers**

1. **Finance Manager**
   - Budget planning and expense tracking
   - Investment advice and portfolio management
   - Financial goal coordination

2. **Productivity Manager**
   - Task and project management
   - Calendar optimization
   - Workflow automation

3. **Learning Manager**
   - Skill development planning
   - Educational resource curation
   - Progress tracking and assessment

### **Enhanced Coordination**
- **Inter-domain workflows**: Complex processes spanning multiple domains
- **Predictive coordination**: AI-driven anticipation of multi-domain needs
- **Resource optimization**: Intelligent allocation across competing priorities

## 📊 Metadata & Analytics

### **Rich Interaction Metadata**
Every interaction returns comprehensive metadata:
```python
{
    "handled_by": "health_manager",
    "routed_to": "health_manager", 
    "coordination_type": "single_domain",
    "domain_metadata": {
        "routed_to": "personal_chef",
        "meal_logged": true,
        "sub_agent_response": "..."
    }
}
```

### **Executive Reporting**
- Request volume by domain
- Cross-domain coordination frequency
- User goal alignment tracking
- System performance analytics

## ✅ Enterprise Features

### **Scalability**
- **Horizontal**: Add new domain managers easily
- **Vertical**: Expand specialist depth within domains
- **Geographic**: Multi-region deployment support

### **Security & Privacy**
- Compartmentalized data access by domain
- Secure API key management
- Conversation privacy controls

### **Integration**
- REST API endpoints for each hierarchy level
- Webhook support for real-time coordination
- Third-party service integration framework

## 🎯 Success Metrics

The Director of Agents system demonstrates:

- ✅ **3-Level Hierarchical Routing**: Executive → Domain → Specialist
- ✅ **Multi-Domain Coordination**: Complex requests spanning multiple areas
- ✅ **Intelligent Request Analysis**: Automatic routing based on content
- ✅ **Executive Decision Making**: Strategic guidance and prioritization
- ✅ **Scalable Architecture**: Ready for additional domains and specialists
- ✅ **Rich Metadata**: Comprehensive interaction tracking
- ✅ **Memory Coordination**: Context management across hierarchy levels

## 🚀 Getting Started

1. **Run Tests**: `python3 test_director.py`
2. **Start System**: `python3 director_cli.py` 
3. **Try Commands**: `dashboard`, `status`, `strategy`
4. **Test Routing**: Ask health, finance, or productivity questions
5. **Explore Multi-Domain**: "Plan healthy meals within budget"

This system provides a foundation for building sophisticated AI agent networks that can handle complex, real-world coordination tasks across multiple life domains while maintaining clear hierarchical organization and intelligent routing capabilities. 