"""
Deep Research Plugin Module

This module contains the DeepResearchPlugin for performing comprehensive
multi-level research using Azure OpenAI services in a Semantic Kernel framework.
"""

import os
import asyncio
import logging
import datetime
from typing import List, Optional, Dict, Any, Annotated

from azure.identity import AzureCliCredential
from semantic_kernel.functions import kernel_function
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents import ChatHistory

from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class DeepResearchPlugin:
    """A Semantic Kernel Plugin for performing deep, multi-level research on topics"""
    
    def __init__(self):
        """Initialize the Deep Research Plugin"""
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Deep Research Plugin initialized")

    @kernel_function(description="Performs comprehensive deep research on a topic with multiple research iterations")
    async def deep_research(self,
                           query: Annotated[str, "The research topic or question to investigate thoroughly"],
                           breadth: Annotated[int, "Number of research aspects to explore (default: 3)"] = 3,
                           depth: Annotated[int, "Number of research iterations to perform (default: 2)"] = 2) -> str:
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

    @kernel_function(description="Performs quick research on a topic with preset parameters for faster results")
    async def quick_research(self,
                            query: Annotated[str, "The research topic or question to investigate"]) -> str:
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
            # Create outline generation agent using proper SK 1.37.0 pattern
            outline_agent = ChatCompletionAgent(
                name="OutlineGenerator",
                instructions=f"""You are a research planning specialist. Generate {breadth} specific research aspects for comprehensive analysis of: {query}

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

Focus on practical, investigatable aspects that would provide valuable insights.""",
                service=AzureChatCompletion(
                    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                    api_version="2024-02-01",
                    credential=AzureCliCredential(),
                )
            )
            
            # Create chat history and request the outline
            chat_history = ChatHistory()
            chat_history.add_user_message(f"Generate {breadth} specific research aspects for comprehensive analysis of: {query}")
            
            # Get the AI response
            responses = []
            async for message in outline_agent.invoke(chat_history):
                responses.append(message)
            
            # Extract and parse the response
            outline_content = ""
            for message in responses:
                outline_content += str(message.content) + "\n"
            
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
            # Create research agent using proper SK 1.37.0 pattern
            research_agent = ChatCompletionAgent(
                name="AspectResearcher",
                instructions=f"""You are a specialized research analyst conducting iteration {iteration} research on: {aspect}

Provide a detailed, factual analysis focusing on:
- Current state and recent developments
- Key facts, statistics, and data points
- Important trends and patterns
- Challenges and opportunities
- Expert insights and analysis
- Future implications

Format your response as clear, actionable bullet points with specific details.
Be thorough, factual, and provide valuable insights that go beyond general statements.
Focus on concrete information and actionable intelligence.""",
                service=AzureChatCompletion(
                    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                    api_version="2024-02-01",
                    credential=AzureCliCredential(),
                )
            )
            
            # Create chat history and add the research request
            chat_history = ChatHistory()
            chat_history.add_user_message(f"Research and analyze: {aspect}. Provide detailed findings for iteration {iteration}.")
            
            # Get the AI response
            responses = []
            async for message in research_agent.invoke(chat_history):
                responses.append(message)
            
            # Extract the content from the response
            research_content = ""
            for message in responses:
                research_content += str(message.content) + "\n"
            
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


# Helper function to create deep research agent using SK 1.37.0 pattern
def create_deep_research_agent() -> ChatCompletionAgent:
    """
    Create and configure the deep research agent using proper SK 1.37.0 pattern
    
    Returns:
        ChatCompletionAgent: Configured deep research agent
    """
    
    # Create the chat completion agent
    deep_research_agent = ChatCompletionAgent(
        name="DeepResearchAgent",
        instructions="""You are an expert deep research agent capable of performing comprehensive, multi-level research on any topic.

When a user asks you to research something, provide detailed, factual analysis focusing on:
- Current state and recent developments
- Key facts, statistics, and data points
- Important trends and patterns
- Challenges and opportunities
- Expert insights and analysis
- Future implications

Always provide well-structured, detailed reports with clear insights.
Be thorough, factual, and provide valuable analysis that goes beyond surface-level information.
Your research should be comprehensive, well-organized, and actionable.""",
        service=AzureChatCompletion(
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version="2024-02-01",
            credential=AzureCliCredential(),
        )
    )

    return deep_research_agent