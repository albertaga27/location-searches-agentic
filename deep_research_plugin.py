"""
Deep Research Plugin Module

This module contains the DeepResearchPlugin for performing comprehensive
multi-level research using OpenAI API with function calling.
"""

import os
import asyncio
import logging
import datetime
import json
from typing import List, Optional, Dict, Any

from azure.identity import AzureCliCredential
import openai

from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class DeepResearchPlugin:
    """An OpenAI-based plugin for performing deep, multi-level research on topics"""
    
    def __init__(self):
        """Initialize the Deep Research Plugin"""
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Deep Research Plugin initialized")
        
        # Initialize OpenAI client
        self._credential = AzureCliCredential()
        self.client = openai.AsyncAzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_ad_token_provider=lambda: self._credential.get_token("https://cognitiveservices.azure.com/.default").token,
            api_version="2024-02-01"
        )
        
    async def deep_research(self, query: str, breadth: int = 3, depth: int = 2) -> str:
        """
        Perform comprehensive deep research on a given topic
        
        Args:
            query: The research topic or question
            breadth: Number of research aspects to explore (1-10)
            depth: Number of research iterations (1-5)
            
        Returns:
            Comprehensive research report in markdown format
        """
        try:
            # Validate parameters
            breadth = max(1, min(10, breadth))
            depth = max(1, min(5, depth))
            
            logger.info(f"Starting deep research on: '{query}' (breadth: {breadth}, depth: {depth})")
            
            # Generate research outline
            research_outline = await self._generate_research_outline(query, breadth)
            
            # Perform iterative research
            research_results = await self._perform_iterative_research(query, research_outline, depth)
            
            # Generate final comprehensive report
            final_report = await self._generate_final_report(query, research_results, breadth, depth)
            
            logger.info(f"Deep research completed on: '{query}'")
            
            return final_report
            
        except Exception as e:
            logger.error(f"Error in deep research: {e}")
            return f"❌ Deep research failed: {str(e)}"

    async def quick_research(self, query: str) -> str:
        """
        Perform quick research with preset parameters for faster results
        
        Args:
            query: The research topic or question
            
        Returns:
            Research summary in markdown format
        """
        return await self.deep_research(query, breadth=2, depth=1)

    async def _generate_research_outline(self, query: str, breadth: int) -> List[str]:
        """Generate an AI-powered research outline with multiple aspects to explore"""
        
        try:
            # Create system message for outline generation
            system_message = f"""You are a research planning specialist. Generate {breadth} specific research aspects for comprehensive analysis of: {query}

Create focused research areas that are:
- Specific and actionable
- Comprehensive and covering different dimensions
- Relevant to the topic
- Suitable for detailed investigation

Format your response as a numbered list of research aspects, each on a new line.
Example format:
1. [Specific research aspect]
2. [Another specific research aspect]
etc.

Focus on practical, investigatable aspects that would provide valuable insights."""
            
            # Make OpenAI API call
            response = await self.client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"Generate {breadth} specific research aspects for comprehensive analysis of: {query}"}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract the response content
            outline_content = response.choices[0].message.content
            
            # Parse the numbered list into individual aspects
            aspects = []
            lines = outline_content.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                    # Remove numbering and clean up the aspect
                    aspect = line.split('.', 1)[-1].strip() if '.' in line else line.lstrip('-•').strip()
                    if aspect:
                        aspects.append(aspect)
            
            # Ensure we have the requested number of aspects
            if len(aspects) < breadth:
                # Fallback to generic aspects if parsing failed
                generic_aspects = [
                    f"Current state and overview of {query}",
                    f"Recent developments and trends in {query}",
                    f"Key challenges and opportunities in {query}",
                    f"Future implications and predictions for {query}",
                    f"Expert opinions and analysis on {query}",
                    f"Technical aspects and specifications of {query}",
                    f"Economic and market impact of {query}",
                    f"Social and cultural effects of {query}",
                    f"Regulatory and legal considerations for {query}",
                    f"Comparative analysis and alternatives to {query}"
                ]
                aspects.extend(generic_aspects[len(aspects):breadth])
            
            return aspects[:breadth]
            
        except Exception as e:
            logger.error(f"Error generating research outline: {e}")
            # Fallback to generic aspects
            aspects = [
                f"Current state and overview of {query}",
                f"Recent developments and trends in {query}",
                f"Key challenges and opportunities in {query}",
                f"Future implications and predictions for {query}",
                f"Expert opinions and analysis on {query}",
                f"Technical aspects and specifications of {query}",
                f"Economic and market impact of {query}",
                f"Social and cultural effects of {query}",
                f"Regulatory and legal considerations for {query}",
                f"Comparative analysis and alternatives to {query}"
            ]
            return aspects[:breadth]

    async def _perform_iterative_research(self, query: str, outline: List[str], depth: int) -> Dict[str, List[str]]:
        """Perform iterative research on each aspect"""
        
        research_results = {}
        
        for aspect in outline:
            research_results[aspect] = []
            
            # Perform multiple iterations of research
            for iteration in range(depth):
                # Get research findings for this aspect and iteration
                findings = await self._research_aspect(aspect, iteration + 1)
                research_results[aspect].extend(findings)
                
                # Add some delay to simulate research time
                await asyncio.sleep(0.1)
        
        return research_results

    async def _research_aspect(self, aspect: str, iteration: int) -> List[str]:
        """Perform actual AI-powered research for a specific aspect"""
        
        try:
            # Create system message for research
            system_message = f"""You are a specialized research analyst conducting iteration {iteration} research on: {aspect}

Provide a detailed, factual analysis focusing on:
- Current state and recent developments
- Key facts, statistics, and data points
- Important trends and patterns
- Challenges and opportunities
- Expert insights and analysis
- Future implications

Format your response as clear, actionable bullet points with specific details.
Be thorough, factual, and provide valuable insights that go beyond general statements.
Focus on concrete information and actionable intelligence."""
            
            # Make OpenAI API call
            response = await self.client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"Research and analyze: {aspect}. Provide detailed findings for iteration {iteration}."}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            # Extract the content from the response
            research_content = response.choices[0].message.content
            
            # Format the findings as a list
            findings = [
                f"Research iteration {iteration} for {aspect}:",
                research_content.strip()
            ]
            
            return findings
            
        except Exception as e:
            logger.error(f"Error in _research_aspect: {e}")
            # Fallback to indicate the error
            return [
                f"Research iteration {iteration} for {aspect}:",
                f"❌ Error occurred during research: {str(e)}",
                "Please check your Azure OpenAI configuration and try again."
            ]

    async def _generate_final_report(self, query: str, research_results: Dict[str, List[str]], breadth: int, depth: int) -> str:
        """Generate a comprehensive final research report"""
        
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        report = f"""# Deep Research Report: {query}

**Research Date:** {current_date}  
**Research Scope:** {breadth} aspects explored with {depth} iterations each  
**Total Research Points:** {len(research_results) * depth}

## Executive Summary

This comprehensive research report presents findings from a multi-dimensional analysis of **{query}**. The research was conducted across {breadth} key aspects with {depth} iterations of investigation for each area, providing a thorough understanding of the topic.

## Research Methodology

- **Breadth:** {breadth} key aspects identified and investigated
- **Depth:** {depth} research iterations per aspect
- **Approach:** Systematic multi-level analysis with iterative refinement
- **Coverage:** Comprehensive examination of current state, trends, challenges, and future implications

## Detailed Findings

"""
        
        # Add detailed findings for each aspect
        for i, (aspect, findings) in enumerate(research_results.items(), 1):
            report += f"### {i}. {aspect}\n\n"
            
            for finding in findings:
                report += f"{finding}\n\n"
            
            report += "---\n\n"

        # Add methodology notes
        report += f"""## Sources and Methodology Notes

- Research conducted using systematic multi-aspect analysis
- Findings synthesized from {len(research_results)} research areas
- Each area investigated through {depth} iterative research cycles
- Report generated on {current_date}

---

*This report was generated using the Deep Research Plugin for comprehensive topic analysis.*
"""

        return report


# Function definitions for OpenAI function calling
def get_research_functions():
    """Get function definitions for OpenAI function calling"""
    return [
        {
            "type": "function",
            "function": {
                "name": "deep_research",
                "description": "Performs comprehensive deep research on a topic with multiple research iterations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The research topic or question to investigate thoroughly"
                        },
                        "breadth": {
                            "type": "integer",
                            "description": "Number of research aspects to explore (default: 3)",
                            "minimum": 1,
                            "maximum": 10,
                            "default": 3
                        },
                        "depth": {
                            "type": "integer", 
                            "description": "Number of research iterations to perform (default: 2)",
                            "minimum": 1,
                            "maximum": 5,
                            "default": 2
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "quick_research",
                "description": "Performs quick research on a topic with preset parameters for faster results",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The research topic or question to investigate"
                        }
                    },
                    "required": ["query"]
                }
            }
        }
    ]


# Helper class for creating deep research agent using OpenAI
class DeepResearchAgent:
    """
    An OpenAI-based research agent with function calling capabilities
    """
    
    def __init__(self):
        """Initialize the deep research agent with OpenAI client"""
        self._credential = AzureCliCredential()
        self.client = openai.AsyncAzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_ad_token_provider=lambda: self._credential.get_token("https://cognitiveservices.azure.com/.default").token,
            api_version="2024-02-01"
        )
        self.plugin = DeepResearchPlugin()
        self.system_message = """You are an expert deep research agent capable of performing comprehensive, multi-level research on any topic.

You have access to research functions that can help you provide detailed analysis. When a user asks you to research something, you should:

1. Use the appropriate research function (deep_research for comprehensive analysis, quick_research for faster results)
2. Provide detailed, factual analysis focusing on:
   - Current state and recent developments
   - Key facts, statistics, and data points
   - Important trends and patterns
   - Challenges and opportunities
   - Expert insights and analysis
   - Future implications

Always provide well-structured, detailed reports with clear insights.
Be thorough, factual, and provide valuable analysis that goes beyond surface-level information.
Your research should be comprehensive, well-organized, and actionable."""

    async def chat(self, message: str) -> str:
        """
        Chat with the agent, which can call research functions as needed
        
        Args:
            message: The user's message or research request
            
        Returns:
            Agent response as a string
        """
        try:
            messages = [
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": message}
            ]
            
            # First call to potentially trigger function calling
            response = await self.client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                messages=messages,
                tools=get_research_functions(),
                tool_choice="auto",
                temperature=0.7,
                max_tokens=2000
            )
            
            response_message = response.choices[0].message
            
            # Check if the model wants to call a function
            if response_message.tool_calls:
                # Add the assistant's response to messages
                messages.append({
                    "role": "assistant", 
                    "content": response_message.content,
                    "tool_calls": response_message.tool_calls
                })
                
                # Execute each function call
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Call the appropriate function
                    if function_name == "deep_research":
                        function_response = await self.plugin.deep_research(
                            query=function_args.get("query"),
                            breadth=function_args.get("breadth", 3),
                            depth=function_args.get("depth", 2)
                        )
                    elif function_name == "quick_research":
                        function_response = await self.plugin.quick_research(
                            query=function_args.get("query")
                        )
                    else:
                        function_response = f"Unknown function: {function_name}"
                    
                    # Add function response to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": function_response
                    })
                
                # Get final response from the model
                final_response = await self.client.chat.completions.create(
                    model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                    messages=messages,
                    temperature=0.7,
                    max_tokens=2000
                )
                
                return final_response.choices[0].message.content
            else:
                # No function call needed, return the direct response
                return response_message.content
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return f"❌ Chat failed: {str(e)}"


def create_deep_research_agent() -> DeepResearchAgent:
    """
    Create and configure the deep research agent using OpenAI
    
    Returns:
        DeepResearchAgent: Configured deep research agent
    """
    return DeepResearchAgent()