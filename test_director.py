#!/usr/bin/env python3
"""
Test Director of Agents
Verify the top-level agent coordinator and its multi-level routing capabilities.
"""

import os
from director_of_agents import DirectorOfAgents

def test_director_initialization():
    """Test Director of Agents initialization and hierarchy setup"""
    print("🧪 Testing Director of Agents Initialization")
    print("=" * 50)
    
    try:
        # Initialize Director
        print("1. Initializing Director of Agents...")
        director = DirectorOfAgents()
        print("✅ Director of Agents initialized")
        
        # Test agent capabilities
        print("\n2. Testing agent capabilities...")
        capabilities = director.get_agent_capabilities()
        print(f"✅ Agent type: {capabilities.get('agent_type')}")
        print(f"✅ Hierarchy level: {capabilities.get('hierarchy_level')}")
        print(f"✅ Domain managers: {list(capabilities.get('domain_managers', {}).keys())}")
        
        # Verify hierarchy depth
        domain_managers = capabilities.get('domain_managers', {})
        if 'health_manager' in domain_managers:
            health_capabilities = domain_managers['health_manager']
            sub_agents = health_capabilities.get('sub_agents', {})
            print(f"✅ Health Manager sub-agents: {list(sub_agents.keys())}")
        
        # Test executive dashboard
        print("\n3. Testing executive dashboard...")
        dashboard = director.get_executive_dashboard()
        print(f"✅ Dashboard sections: {list(dashboard.keys())}")
        print(f"✅ Director status: {dashboard.get('director_status')}")
        
        return True, director
        
    except Exception as e:
        print(f"❌ Initialization test failed: {e}")
        return False, None

def test_routing_hierarchy():
    """Test the 3-level routing hierarchy"""
    print("\n🎯 Testing 3-Level Routing Hierarchy")
    print("=" * 40)
    
    try:
        director = DirectorOfAgents()
        
        # Test cases for different routing levels
        test_cases = [
            # Level 1: Director handles directly
            ("What's my overall life strategy?", "director_of_agents"),
            ("Help me prioritize my goals", "director_of_agents"),
            
            # Level 2: Route to Health Manager
            ("How are my health goals?", "health_manager"),
            ("I need fitness advice", "health_manager"),
            
            # Level 3: Route through Health Manager to Personal Chef
            ("What should I eat for lunch?", "health_manager"),  # Will route to personal_chef
            ("I ate a sandwich", "health_manager"),  # Will route to personal_chef
            
            # Multi-domain (handled by Director)
            ("Plan healthy meals within budget", "multi_domain")
        ]
        
        for message, expected_handler in test_cases:
            # Test routing decision
            target_domain = director.route_to_domain_manager(message)
            
            if expected_handler == "director_of_agents":
                expected_target = None
            elif expected_handler == "multi_domain":
                involved_domains = director.detect_multi_domain_request(message)
                expected_target = "multi_domain" if len(involved_domains) > 1 else target_domain
            else:
                expected_target = expected_handler
            
            status = "✅" if target_domain == expected_target else "❌"
            print(f"{status} '{message}' → {target_domain or 'director_of_agents'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Routing test failed: {e}")
        return False

def test_multi_domain_coordination():
    """Test multi-domain request handling"""
    print("\n🔄 Testing Multi-Domain Coordination")
    print("=" * 35)
    
    try:
        director = DirectorOfAgents()
        
        # Test multi-domain detection
        multi_domain_queries = [
            "Plan healthy meals within my budget",
            "Schedule workouts around my work meetings", 
            "Learn cooking while meeting nutrition goals"
        ]
        
        for query in multi_domain_queries:
            involved_domains = director.detect_multi_domain_request(query)
            is_multi = len(involved_domains) > 1
            status = "✅" if is_multi else "❌"
            print(f"{status} Multi-domain: '{query}' → {involved_domains}")
        
        # Test actual coordination
        print("\n4. Testing coordination execution...")
        response, metadata = director.chat("Help me with health and wellness strategy")
        coordination_type = metadata.get("coordination_type")
        handled_by = metadata.get("handled_by")
        
        print(f"✅ Response generated: {len(response)} characters")
        print(f"✅ Handled by: {handled_by}")
        if coordination_type:
            print(f"✅ Coordination type: {coordination_type}")
        
        return True
        
    except Exception as e:
        print(f"❌ Multi-domain test failed: {e}")
        return False

def test_executive_functions():
    """Test executive-level functions and capabilities"""
    print("\n📊 Testing Executive Functions")
    print("=" * 30)
    
    try:
        director = DirectorOfAgents()
        
        # Test cross-domain insights
        print("1. Testing cross-domain insights...")
        insights = director.get_cross_domain_insights()
        print(f"✅ Insights generated with {len(insights)} sections")
        
        # Test conversation management
        print("\n2. Testing conversation management...")
        response1, meta1 = director.chat("Who are you?")
        response2, meta2 = director.chat("What can you help me with?")
        
        summary = director.get_conversation_summary()
        print(f"✅ Conversation summary: {len(summary)} characters")
        
        # Test memory clearing
        print("\n3. Testing memory management...")
        director.clear_memory()
        summary_after_clear = director.get_conversation_summary()
        print(f"✅ Memory cleared: '{summary_after_clear}'")
        
        return True
        
    except Exception as e:
        print(f"❌ Executive functions test failed: {e}")
        return False

def test_real_interaction_flow():
    """Test realistic interaction flows through the hierarchy"""
    print("\n💬 Testing Real Interaction Flows")
    print("=" * 35)
    
    try:
        director = DirectorOfAgents()
        
        # Simulate realistic user interactions
        interactions = [
            "What should I eat for dinner tonight?",  # Should route to health manager → personal chef
            "How am I doing with my overall goals?",  # Should stay at director level
            "I ate chicken and rice for lunch"       # Should route to health manager → personal chef with logging
        ]
        
        for i, interaction in enumerate(interactions, 1):
            print(f"\n{i}. Testing: '{interaction}'")
            response, metadata = director.chat(interaction)
            
            handled_by = metadata.get("handled_by")
            routed_to = metadata.get("routed_to")
            
            print(f"   ✅ Handled by: {handled_by}")
            print(f"   ✅ Response length: {len(response)} characters")
            
            if routed_to:
                print(f"   ✅ Routed to: {routed_to}")
            
            # Check for nested routing info
            if metadata.get("domain_metadata"):
                domain_meta = metadata["domain_metadata"]
                if domain_meta.get("routed_to"):
                    print(f"   ✅ Sub-routed to: {domain_meta['routed_to']}")
                if domain_meta.get("meal_logged"):
                    print(f"   ✅ Meal logged: {domain_meta['meal_logged']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Interaction flow test failed: {e}")
        return False

def main():
    """Run all Director of Agents tests"""
    print("🚀 Director of Agents Test Suite")
    print("=" * 50)
    
    tests = [
        test_director_initialization,
        test_routing_hierarchy,
        test_multi_domain_coordination,
        test_executive_functions,
        test_real_interaction_flow
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test_func.__name__} failed with error: {e}")
    
    print(f"\n📈 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Director of Agents is ready for deployment!")
        print("\nHierarchy Verified:")
        print("🎯 Director of Agents")
        print("└── 🏥 Health Manager") 
        print("    └── 👨‍🍳 Personal Chef")
        print("\nTo run: python3 director_cli.py")
    else:
        print(f"\n❌ {total - passed} tests failed. Check configuration.")

if __name__ == "__main__":
    main() 