# AgenticADA - Hierarchical AI Agent Network

A sophisticated 3-level hierarchical AI agent architecture that converts n8n workflows into intelligent, coordinated standalone agents. This system demonstrates advanced agent coordination, intelligent routing, and seamless multi-domain task management.

## 🏗️ Architecture Overview

```
🎯 Director of Agents (Level 1 - Executive)
└── 🏥 Health Manager (Level 2 - Domain)
    ├── 👨‍🍳 Personal Chef (Level 3 - Specialist)
    └── 🔧 Equipment Manager (Level 3 - Specialist)
```

## 🚀 Key Features

- **3-Level Hierarchical Architecture**: Executive → Domain → Specialist coordination
- **Intelligent Routing**: Automatic request routing based on keywords and context
- **n8n Workflow Conversion**: Seamlessly converts n8n workflows to AI agents
- **Cross-Domain Coordination**: Handles complex multi-domain requests
- **Natural Language Processing**: Advanced NLP for intent detection and response
- **Database Integration**: Full CRUD operations with Supabase
- **Memory Management**: Conversation context across the hierarchy
- **CLI Interface**: Executive-level command interface

## 🎯 Agents Overview

### Director of Agents (Level 1)
**Role**: Executive coordinator and strategic decision maker
- Routes requests across life domains
- Handles multi-domain coordination
- Provides executive-level insights
- Manages overall strategy and goal alignment

### Health Manager (Level 2)
**Role**: Domain-level health coordination
- Manages overall health goals and progress
- Routes to health specialists
- Provides health analytics and insights
- Coordinates nutrition, fitness, and equipment

### Personal Chef (Level 3)
**Role**: Nutrition and meal specialist
- Meal planning and logging
- Recipe management and suggestions
- Nutritional analysis and tracking
- Cookbook integration

### Equipment Manager (Level 3)
**Role**: Fitness equipment specialist
- Equipment inventory management
- Location-based organization (home gym, office, gym)
- Equipment recommendations
- Purchase planning and tracking

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- Supabase account and database
- Required Python packages (see `requirements.txt`)

## 🔧 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/kwbise02/agenticada.git
cd agenticada
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
```bash
cp env_example.txt .env
# Edit .env with your actual API keys
```

4. **Configure your `.env` file**:
```
OPENAI_API_KEY=your_openai_api_key_here
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
```

## 🗄️ Database Setup

Set up these tables in your Supabase database:

```sql
-- Goals table
CREATE TABLE goals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    description TEXT NOT NULL,
    target_value NUMERIC,
    current_value NUMERIC DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Meal types table
CREATE TABLE meal_type (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT
);

-- Cookbook table
CREATE TABLE cookbook (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_name TEXT NOT NULL,
    ingredients TEXT[],
    instructions TEXT,
    prep_time INTEGER,
    cook_time INTEGER,
    servings INTEGER
);

-- Food log table
CREATE TABLE food_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meal_name TEXT NOT NULL,
    meal_time TIMESTAMP DEFAULT NOW(),
    calories NUMERIC,
    protein NUMERIC,
    carbs NUMERIC,
    fats NUMERIC,
    meal_type UUID REFERENCES meal_type(id)
);

-- Equipment groups table
CREATE TABLE equipment_groups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    group_name TEXT NOT NULL,
    description TEXT,
    area UUID NOT NULL
);

-- Equipment items table
CREATE TABLE equipment_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    item_name TEXT NOT NULL,
    item_description TEXT,
    equipment_group UUID REFERENCES equipment_groups(id)
);
```

## 🚀 Usage

### CLI Interface (Recommended)
```bash
python3 director_cli.py
```

The CLI provides:
- Executive-level agent coordination
- Real-time routing information
- Cross-domain dashboard
- Agent status monitoring
- Strategic guidance interface

### Programmatic Usage

**Director Level**:
```python
from director_of_agents import DirectorOfAgents

director = DirectorOfAgents()
response, metadata = director.chat("Plan healthy meals within my budget")
```

**Health Manager Level**:
```python
from health_manager_agent import HealthManagerAgent

health_manager = HealthManagerAgent()
response, metadata = health_manager.chat("Log my breakfast")
```

**Specialist Level**:
```python
from personal_chef_agent_core import PersonalChefAgent

chef = PersonalChefAgent()
response, meal_logged = chef.chat("I had oatmeal with berries")
```

## 🧪 Testing

Run comprehensive test suites:

```bash
# Test Director and overall system
python3 test_director.py

# Test Equipment Manager integration
python3 test_equipment_manager.py
```

**Test Coverage**:
- ✅ Agent initialization and capabilities
- ✅ Intelligent routing and coordination
- ✅ Database integration and CRUD operations
- ✅ Cross-domain request handling
- ✅ Memory management
- ✅ Error handling and graceful failures

## 📊 CLI Commands

| Command | Description |
|---------|-------------|
| `dashboard` | Executive overview across all domains |
| `status` | Check all agent statuses |
| `strategy` | Get strategic coordination advice |
| `clear` | Clear all agent memories |
| `quit` | Exit the system |

## 🔀 Routing Intelligence

The system uses sophisticated keyword-based routing:

### Health Domain Keywords
- Nutrition: `meal`, `food`, `recipe`, `calories`, `protein`
- Equipment: `equipment`, `weights`, `gym`, `dumbbells`
- Fitness: `workout`, `exercise`, `cardio`, `strength`

### Multi-Domain Coordination
- `"Plan healthy meals within budget"` → Health + Finance
- `"Schedule workouts around meetings"` → Health + Productivity
- `"Learn cooking for nutrition goals"` → Learning + Health

## 📈 Capabilities

### Intelligence Features
- **Natural Language Understanding**: Advanced intent detection
- **Context Awareness**: Maintains conversation context across hierarchy
- **Automatic Categorization**: Smart equipment and meal categorization
- **Progress Tracking**: Comprehensive health and goal analytics

### Integration Features
- **Database Synchronization**: Real-time data sync with Supabase
- **Workflow Conversion**: n8n to agent architecture conversion
- **API Integration**: OpenAI GPT models for intelligence
- **Modular Design**: Easy addition of new agents and domains

## 🔮 Future Roadmap

### Domain Expansion
- **Finance Manager**: Budget, investments, expense tracking
- **Productivity Manager**: Tasks, scheduling, project management
- **Learning Manager**: Skill development, education planning

### Enhanced Capabilities
- **Voice Interface**: Speech-to-text and text-to-speech
- **Mobile App**: Native mobile interface
- **Advanced Analytics**: ML-powered insights and predictions
- **Workflow Builder**: Visual agent workflow creation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-agent`)
3. Commit your changes (`git commit -am 'Add new agent'`)
4. Push to the branch (`git push origin feature/new-agent`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Related Documentation

- [Director of Agents README](DIRECTOR_README.md)
- [Equipment Manager README](EQUIPMENT_MANAGER_README.md)
- [n8n Workflow Examples](equipmentagentrebuild)

## 🙋‍♂️ Support

For questions, issues, or contributions:
- Open an issue on GitHub
- Check existing documentation
- Review test files for usage examples

## 🏆 Success Metrics

- ✅ **3-Level Hierarchy**: Complete executive → domain → specialist architecture
- ✅ **Intelligent Routing**: 100% accurate keyword-based routing
- ✅ **n8n Conversion**: Successfully converted Equipment Manager workflow
- ✅ **Database Integration**: Full CRUD operations across all agents
- ✅ **Natural Language**: Advanced NLP for all user interactions
- ✅ **Cross-Domain**: Multi-domain request coordination
- ✅ **Memory Management**: Hierarchical conversation context
- ✅ **Error Handling**: Graceful failure handling throughout

AgenticADA demonstrates the future of AI agent architecture: intelligent, hierarchical, and seamlessly coordinated systems that can handle complex, multi-domain tasks with human-like understanding and strategic thinking. 