#!/usr/bin/env python3
"""
Test script for the Deep Research Plugin

This script demonstrates how to use the Deep Research Plugin
with different parameters and scenarios.
"""

import asyncio
import os
from deep_research_plugin import DeepResearchPlugin, create_deep_research_agent
from semantic_kernel.contents import ChatHistory

async def test_deep_research_plugin():
    """Test the Deep Research Plugin functionality"""
    
    print("🧪 Testing Deep Research Plugin")
    print("=" * 50)
    
    # Test 1: Direct Plugin Testing
    print("\n📋 Test 1: Direct Plugin Usage")
    print("-" * 30)
    plugin = DeepResearchPlugin()
    
    result1 = await plugin.quick_research("artificial intelligence trends")
    print("Quick research result length:", len(result1))
    print("First 200 characters:", result1[:200] + "...")
    
    # Test 2: Plugin with custom parameters
    print("\n📋 Test 2: Deep Research with Custom Parameters")
    print("-" * 30)
    result2 = await plugin.deep_research("renewable energy", breadth=3, depth=2)
    print("Deep research result length:", len(result2))
    print("First 200 characters:", result2[:200] + "...")
    
    # Test 3: Agent-based testing (if environment is configured)
    print("\n📋 Test 3: Agent-based Testing")
    print("-" * 30)
    
    if os.getenv("AZURE_OPENAI_ENDPOINT") and os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"):
        try:
            agent = await create_deep_research_agent()
            chat_history = ChatHistory()
            chat_history.add_user_message("Quick research on blockchain technology")
            
            response = await agent.invoke(chat_history)
            print("Agent response received:")
            for message in response:
                print("Message length:", len(message.content))
                print("First 200 characters:", message.content[:200] + "...")
        except Exception as e:
            print(f"Agent test failed (expected if Azure OpenAI not configured): {e}")
    else:
        print("Skipping agent test - Azure OpenAI environment variables not set")
    
    print("\n✅ All tests completed successfully!")

async def test_plugin_functions():
    """Test individual plugin functions"""
    
    print("\n🔬 Testing Individual Plugin Functions")
    print("=" * 50)
    
    plugin = DeepResearchPlugin()
    
    # Test research outline generation
    outline = await plugin._generate_research_outline("machine learning", 4)
    print(f"\nResearch outline for 'machine learning' (4 aspects):")
    for i, aspect in enumerate(outline, 1):
        print(f"  {i}. {aspect}")
    
    # Test iterative research
    research_results = await plugin._perform_iterative_research("AI ethics", outline[:2], 2)
    print(f"\nIterative research results:")
    for aspect, findings in research_results.items():
        print(f"\nAspect: {aspect}")
        print(f"  Findings: {len(findings)} items")
        for finding in findings[:2]:  # Show first 2 findings
            print(f"    - {finding}")

if __name__ == "__main__":
    asyncio.run(test_deep_research_plugin())
    asyncio.run(test_plugin_functions())