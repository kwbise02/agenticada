#!/usr/bin/env python3
"""
Director of Agents CLI Interface
Executive-level interface for the top-tier agent coordinator.
"""

import os
from director_of_agents import DirectorOfAgents

def main():
    """Main CLI interface for the Director of Agents"""
    print("🎯 Director of Agents")
    print("=" * 60)
    print("I'm your executive AI coordinator managing your entire agent network!")
    print("\nAgent Hierarchy:")
    print("🎯 Director of Agents (You are here)")
    print("└── 🏥 Health Manager")
    print("    ├── 👨‍🍳 Personal Chef")
    print("    └── 🔧 Equipment Manager")
    print("\nDomain Management:")
    print("• 🏥 Health - nutrition, fitness, wellness, equipment, medical")
    print("• 💰 Finance - budget, investments, expenses (coming soon)")
    print("• 📋 Productivity - tasks, scheduling, projects (coming soon)")
    print("• 📚 Learning - education, skills, development (coming soon)")
    print("\nSpecial Commands:")
    print("• 'quit' - exit the system")
    print("• 'clear' - clear all agent memories")
    print("• 'dashboard' - executive overview across all domains")
    print("• 'status' - check all agent statuses")
    print("• 'strategy' - get strategic coordination advice")
    print("-" * 60)
    
    # Initialize the Director of Agents
    try:
        director = DirectorOfAgents()
        print("✅ Director of Agents initialized successfully!")
        
        # Show agent hierarchy status
        capabilities = director.get_agent_capabilities()
        domain_managers = capabilities.get("domain_managers", {})
        print(f"✅ Domain Managers loaded: {list(domain_managers.keys())}")
        
        for domain_name, domain_info in domain_managers.items():
            sub_agents = domain_info.get("sub_agents", {})
            if sub_agents:
                print(f"   └── {domain_name}: {list(sub_agents.keys())}")
        
    except Exception as e:
        print(f"❌ Failed to initialize Director of Agents: {e}")
        return
    
    print()
    
    while True:
        try:
            user_input = input("Executive: ").strip()
            
            if user_input.lower() == 'quit':
                print("🎯 Thank you for using the Director of Agents!")
                print("Your agent network is always ready to assist you.")
                break
            
            if user_input.lower() == 'clear':
                director.clear_memory()
                print("🧹 All agent memories cleared across the entire network!")
                continue
            
            if user_input.lower() == 'dashboard':
                dashboard = director.get_executive_dashboard()
                print("\n📊 Executive Dashboard")
                print("=" * 40)
                
                # Director status
                print(f"🎯 Director Status: {dashboard.get('director_status', 'unknown').upper()}")
                
                # Domain manager summaries
                domain_managers = dashboard.get("domain_managers", {})
                print(f"\n🏢 Domain Managers ({len(domain_managers)}):")
                
                for domain_name, domain_data in domain_managers.items():
                    print(f"\n   🏥 {domain_name.replace('_', ' ').title()}:")
                    
                    if domain_name == 'health_manager' and 'health_progress' in domain_data:
                        health_progress = domain_data['health_progress']
                        if health_progress.get('nutrition'):
                            nutrition = health_progress['nutrition']
                            print(f"      📈 Weekly Calories: {nutrition.get('weekly_calories', 0):,}")
                            print(f"      🍽️ Meals Logged: {nutrition.get('meals_logged', 0)}")
                        
                        goals = domain_data.get('goals', [])
                        print(f"      🎯 Active Goals: {len(goals)}")
                    
                    # Show sub-agents
                    sub_agents = domain_data.get('sub_agents', {})
                    if sub_agents:
                        print(f"      🤖 Sub-Agents: {list(sub_agents.keys())}")
                
                # Cross-domain insights
                insights = dashboard.get("cross_domain_insights", {})
                opportunities = insights.get("cross_domain_opportunities", [])
                if opportunities:
                    print(f"\n🔄 Cross-Domain Opportunities:")
                    for opp in opportunities[:3]:
                        print(f"   • {opp}")
                
                print()
                continue
            
            if user_input.lower() == 'status':
                print("\n🔍 Agent Network Status")
                print("-" * 30)
                
                capabilities = director.get_agent_capabilities()
                domain_managers = capabilities.get("domain_managers", {})
                
                for domain_name, domain_info in domain_managers.items():
                    status_icon = "✅" if domain_info else "❌"
                    print(f"{status_icon} {domain_name.replace('_', ' ').title()}")
                    
                    sub_agents = domain_info.get("sub_agents", {})
                    for sub_name, sub_info in sub_agents.items():
                        sub_status = "✅" if sub_info else "❌"
                        print(f"   {sub_status} {sub_name.replace('_', ' ').title()}")
                
                print()
                continue
            
            if user_input.lower() == 'strategy':
                strategic_input = "Provide strategic guidance on optimizing my life across health, productivity, and personal development goals."
                user_input = strategic_input
                print(f"🎯 Strategic Query: {strategic_input}")
            
            if not user_input:
                continue
            
            # Get response from Director
            response, metadata = director.chat(user_input)
            
            # Display response with routing/coordination info
            routing_info = ""
            if metadata.get("routed_to"):
                if metadata.get("coordination_type") == "multi_domain":
                    involved = metadata.get("involved_domains", [])
                    routing_info = f" [🔄 Multi-Domain: {', '.join(involved)}]"
                elif metadata["handled_by"] != "director_of_agents":
                    routing_info = f" [📋 Routed to {metadata['handled_by'].replace('_', ' ').title()}]"
                    
                    # Check for nested routing (e.g., to Personal Chef via Health Manager)
                    if metadata.get("domain_metadata", {}).get("routed_to"):
                        nested_route = metadata["domain_metadata"]["routed_to"]
                        routing_info += f" → {nested_route.replace('_', ' ').title()}"
                        
                        if metadata["domain_metadata"].get("meal_logged"):
                            routing_info += " [🍽️ Meal Logged]"
                        
                        if metadata["domain_metadata"].get("equipment_added"):
                            routing_info += " [🔧 Equipment Added]"
            
            print(f"🎯 Director{routing_info}: {response}")
            print()
            
        except KeyboardInterrupt:
            print("\n🎯 Executive session ended. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Executive Error: {e}")
            print()

if __name__ == "__main__":
    main() 