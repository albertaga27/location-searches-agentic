#!/usr/bin/env python3
"""
Simple usage example for the OpenAI-based Deep Research Plugin

This demonstrates the basic usage patterns for the refactored plugin.
"""

import asyncio
import os
from deep_research_plugin import DeepResearchPlugin, create_deep_research_agent


async def simple_plugin_usage():
    """Demonstrate simple plugin usage"""
    print("🔍 Simple Plugin Usage Example")
    print("=" * 40)
    
    # Create plugin instance
    plugin = DeepResearchPlugin()
    
    # Quick research
    print("Performing quick research...")
    result = await plugin.quick_research("machine learning applications in healthcare")
    print("Research completed!\n")
    print(result)


async def agent_with_function_calling():
    """Demonstrate agent with function calling"""
    print("\n🤖 Agent with Function Calling Example")
    print("=" * 40)
    
    # Create agent
    agent = create_deep_research_agent()
    
    # Chat with the agent - this may trigger function calling
    print("Chatting with research agent...")
    response = await agent.chat("I need detailed research on renewable energy trends, please analyze 3 key aspects")
    print("Agent response:\n")
    print(response)


async def main():
    """Main example function"""
    if not (os.getenv("AZURE_OPENAI_ENDPOINT") and os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")):
        print("❌ Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT_NAME environment variables")
        return
    
    try:
        # Run simple plugin usage
        await simple_plugin_usage()
        
        # Run agent with function calling
        await agent_with_function_calling()
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())