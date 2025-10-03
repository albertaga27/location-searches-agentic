#!/usr/bin/env python3
"""
Test script for the refactored OpenAI-based Deep Research Plugin

This script demonstrates how to use the Deep Research Plugin
with OpenAI function calling instead of Semantic Kernel.
"""

import asyncio
import os
from deep_research_plugin import DeepResearchPlugin, DeepResearchAgent, create_deep_research_agent


async def test_openai_deep_research():
    """Test the OpenAI-based Deep Research Plugin functionality"""
    
    print("🚀 Testing OpenAI-based Deep Research Plugin")
    print("=" * 50)
    
    # Test 1: Direct Plugin Testing
    print("\n📋 Test 1: Direct Plugin Usage")
    print("-" * 30)
    plugin = DeepResearchPlugin()
    
    try:
        result1 = await plugin.quick_research("artificial intelligence trends")
        print("✅ Quick research completed!")
        print("Result length:", len(result1))
        print("First 200 characters:", result1[:200] + "...")
    except Exception as e:
        print(f"❌ Quick research failed: {e}")
    
    # Test 2: Plugin with custom parameters
    print("\n📋 Test 2: Deep Research with Custom Parameters")
    print("-" * 30)
    try:
        result2 = await plugin.deep_research("renewable energy", breadth=3, depth=2)
        print("✅ Deep research completed!")
        print("Result length:", len(result2))
        print("First 200 characters:", result2[:200] + "...")
    except Exception as e:
        print(f"❌ Deep research failed: {e}")
    
    # Test 3: Agent-based testing with function calling
    print("\n📋 Test 3: Agent with Function Calling")
    print("-" * 30)
    
    if os.getenv("AZURE_OPENAI_ENDPOINT") and os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"):
        try:
            agent = create_deep_research_agent()
            
            # Test function calling with a research request
            response = await agent.chat("Please perform a quick research on blockchain technology trends")
            print("✅ Agent function calling completed!")
            print("Response length:", len(response))
            print("First 300 characters:", response[:300] + "...")
            
            # Test direct conversation
            response2 = await agent.chat("What are the main benefits of using AI in healthcare?")
            print("\n✅ Direct conversation completed!")
            print("Response length:", len(response2))
            print("First 300 characters:", response2[:300] + "...")
            
        except Exception as e:
            print(f"❌ Agent testing failed: {e}")
    else:
        print("⚠️  Azure OpenAI configuration not found. Skipping agent test.")
        print("Please ensure AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT_NAME are set.")


async def test_function_calling_scenarios():
    """Test various function calling scenarios"""
    
    print("\n🔧 Testing Function Calling Scenarios")
    print("=" * 50)
    
    if not (os.getenv("AZURE_OPENAI_ENDPOINT") and os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")):
        print("⚠️  Azure OpenAI configuration not found. Skipping function calling tests.")
        return
    
    agent = create_deep_research_agent()
    
    # Test scenarios that should trigger function calls
    scenarios = [
        "Research the latest trends in quantum computing",
        "I need a comprehensive analysis of electric vehicle adoption",
        "Can you do a quick research on sustainable energy solutions?",
        "Perform deep research on cybersecurity challenges with 4 aspects and 3 iterations",
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📝 Scenario {i}: {scenario}")
        print("-" * 40)
        try:
            response = await agent.chat(scenario)
            print("✅ Response received!")
            print("Length:", len(response))
            print("Preview:", response[:150] + "..." if len(response) > 150 else response)
        except Exception as e:
            print(f"❌ Scenario {i} failed: {e}")


async def main():
    """Main test function"""
    print("🧪 OpenAI-based Deep Research Plugin Test Suite")
    print("=" * 60)
    
    # Run basic plugin tests
    await test_openai_deep_research()
    
    # Run function calling tests
    await test_function_calling_scenarios()
    
    print("\n" + "=" * 60)
    print("🏁 Test suite completed!")


if __name__ == "__main__":
    asyncio.run(main())