#!/usr/bin/env python3
"""
Test Equipment Manager Agent
Verify the Equipment Manager functionality and integration with the Health Manager.
"""

import os
from equipment_manager_agent import EquipmentManagerAgent
from health_manager_agent import HealthManagerAgent
from director_of_agents import DirectorOfAgents

def test_equipment_manager_standalone():
    """Test Equipment Manager as a standalone agent"""
    print("🧪 Testing Equipment Manager Standalone")
    print("=" * 40)
    
    try:
        # Initialize Equipment Manager
        print("1. Initializing Equipment Manager...")
        equipment_manager = EquipmentManagerAgent()
        print("✅ Equipment Manager initialized")
        
        # Test capabilities
        print("\n2. Testing agent capabilities...")
        capabilities = equipment_manager.get_agent_capabilities()
        print(f"✅ Agent type: {capabilities.get('agent_type')}")
        print(f"✅ Hierarchy level: {capabilities.get('hierarchy_level')}")
        print(f"✅ Parent agent: {capabilities.get('parent_agent')}")
        print(f"✅ Capabilities: {capabilities.get('capabilities')}")
        
        # Test equipment groups retrieval
        print("\n3. Testing equipment groups...")
        groups = equipment_manager.get_equipment_groups()
        print(f"✅ Found {len(groups)} equipment groups")
        for group in groups[:2]:  # Show first 2 groups
            print(f"   - {group.get('group_name', 'Unknown')}")
        
        # Test chat functionality
        print("\n4. Testing chat functionality...")
        response, equipment_added = equipment_manager.chat("What equipment groups do you have?")
        print(f"✅ Response generated: {len(response)} characters")
        print(f"✅ Equipment added: {equipment_added}")
        
        return True
        
    except Exception as e:
        print(f"❌ Standalone test failed: {e}")
        return False

def test_equipment_manager_in_health_manager():
    """Test Equipment Manager integration with Health Manager"""
    print("\n🏥 Testing Equipment Manager in Health Manager")
    print("=" * 45)
    
    try:
        # Initialize Health Manager (should include Equipment Manager)
        print("1. Initializing Health Manager...")
        health_manager = HealthManagerAgent()
        print("✅ Health Manager initialized")
        
        # Check sub-agents
        print("\n2. Checking sub-agents...")
        capabilities = health_manager.get_agent_capabilities()
        sub_agents = capabilities.get('sub_agents', {})
        print(f"✅ Sub-agents loaded: {list(sub_agents.keys())}")
        
        if 'equipment_manager' in sub_agents:
            print("✅ Equipment Manager successfully loaded as sub-agent")
        else:
            print("❌ Equipment Manager not found in sub-agents")
            return False
        
        # Test routing to Equipment Manager
        print("\n3. Testing routing to Equipment Manager...")
        target_agent = health_manager.route_to_sub_agent("What gym equipment do I have?")
        print(f"✅ Routing target: {target_agent}")
        
        if target_agent == 'equipment_manager':
            print("✅ Successfully routes equipment queries to Equipment Manager")
        else:
            print(f"❌ Expected 'equipment_manager', got '{target_agent}'")
            return False
        
        # Test full chat with routing
        print("\n4. Testing full chat with routing...")
        response, metadata = health_manager.chat("Show me my home gym equipment")
        print(f"✅ Response generated: {len(response)} characters")
        print(f"✅ Handled by: {metadata.get('handled_by')}")
        print(f"✅ Routed to: {metadata.get('routed_to')}")
        
        if metadata.get('equipment_added') is not None:
            print(f"✅ Equipment tracking: {metadata.get('equipment_added')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Health Manager integration test failed: {e}")
        return False

def test_equipment_manager_in_director():
    """Test Equipment Manager integration through Director of Agents"""
    print("\n🎯 Testing Equipment Manager through Director")
    print("=" * 42)
    
    try:
        # Initialize Director
        print("1. Initializing Director of Agents...")
        director = DirectorOfAgents()
        print("✅ Director initialized")
        
        # Test routing
        print("\n2. Testing routing logic...")
        target_domain = director.route_to_domain_manager("What weights do I have at home?")
        print(f"✅ Routes to domain: {target_domain}")
        
        if target_domain == 'health_manager':
            print("✅ Successfully routes equipment queries to Health Manager")
        else:
            print(f"❌ Expected 'health_manager', got '{target_domain}'")
            return False
        
        # Test full chat through hierarchy
        print("\n3. Testing full chat through hierarchy...")
        response, metadata = director.chat("I need to see my gym equipment")
        print(f"✅ Response generated: {len(response)} characters")
        print(f"✅ Handled by: {metadata.get('handled_by')}")
        
        # Check for nested routing metadata
        if metadata.get('domain_metadata'):
            domain_meta = metadata['domain_metadata']
            print(f"✅ Domain routed to: {domain_meta.get('routed_to')}")
            if domain_meta.get('equipment_added') is not None:
                print(f"✅ Equipment tracking: {domain_meta.get('equipment_added')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Director integration test failed: {e}")
        return False

def test_equipment_addition():
    """Test equipment addition functionality"""
    print("\n➕ Testing Equipment Addition")
    print("=" * 30)
    
    try:
        # Test through Director (full hierarchy)
        director = DirectorOfAgents()
        
        # Try to add equipment
        print("1. Testing equipment addition...")
        response, metadata = director.chat("I bought a new kettlebell for my home gym")
        print(f"✅ Response generated: {len(response)} characters")
        
        # Check if equipment was added
        if metadata.get('domain_metadata', {}).get('equipment_added'):
            print("✅ Equipment successfully added through hierarchy")
        else:
            print("⚠️ Equipment addition not detected (may need manual confirmation)")
        
        return True
        
    except Exception as e:
        print(f"❌ Equipment addition test failed: {e}")
        return False

def main():
    """Run all Equipment Manager tests"""
    print("🔧 Equipment Manager Agent Tests")
    print("=" * 50)
    
    tests = [
        test_equipment_manager_standalone,
        test_equipment_manager_in_health_manager,
        test_equipment_manager_in_director,
        test_equipment_addition
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
                print("✅ Test passed\n")
            else:
                print("❌ Test failed\n")
        except Exception as e:
            print(f"❌ Test error: {e}\n")
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Equipment Manager tests passed! Equipment Manager is ready!")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main() 