"""
Risk Assessment Agent Module

This module contains the RiskAssessmentPlugin and agent creation functionality
for performing comprehensive risk analysis on locations, buildings, and assets.
Uses OpenAI Azure API with function calling.
"""

import os
import json
import logging
from typing import Dict, Any
import openai
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class RiskAssessmentPlugin:
    """An OpenAI-based plugin to perform comprehensive risk assessment analysis"""
    
    def __init__(self):
        """Initialize the Risk Assessment Plugin"""
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Risk Assessment Plugin initialized")
        
        # Initialize OpenAI client
        self._credential = AzureCliCredential()
        self.client = openai.AsyncAzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_ad_token_provider=lambda: self._credential.get_token("https://cognitiveservices.azure.com/.default").token,
            api_version="2024-02-01"
        )
    
    async def assess_risks(self, research_data: str, location: str = "", risk_categories: str = "") -> str:
        """
        Perform comprehensive risk assessment based on research data
        
        Args:
            research_data: Research findings about the location/building
            location: Name or description of the location being assessed
            risk_categories: Specific risk categories to focus on
            
        Returns:
            Detailed risk assessment report
        """
        try:
            logger.info(f"Starting risk assessment for: '{location}'")
            
            # Create system message for risk assessment
            system_message = """You are an expert risk assessment analyst. Analyze the provided research data and perform a comprehensive risk assessment.

Evaluate risks across these categories:
🏗️ **Structural & Engineering Risks**
🌍 **Environmental & Natural Disaster Risks**  
🚨 **Safety & Security Risks**
💰 **Financial & Economic Risks**
🏛️ **Regulatory & Legal Risks**
🚀 **Operational & Business Risks**

For each relevant risk category, provide:
- **Risk Level**: Critical/High/Medium/Low
- **Likelihood**: Probability of occurrence  
- **Impact**: Potential consequences
- **Evidence**: Supporting data from research
- **Key Concerns**: Specific issues identified

Format your response with clear headings and bullet points. Be specific and actionable based on the research data provided."""

            # Create the assessment prompt
            prompt = f"""Please perform a comprehensive risk assessment for: {location}

Based on this research data:
{research_data}

Focus on: {risk_categories if risk_categories else 'all risk categories'}

Provide a detailed risk analysis."""
            
            # Make OpenAI API call
            response = await self.client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Extract and return the assessment content
            assessment_content = response.choices[0].message.content
            
            logger.info(f"Risk assessment completed for: '{location}'")
            
            return assessment_content.strip()
            
        except Exception as e:
            logger.error(f"Error in risk assessment: {e}")
            return f"❌ Error during risk assessment: {str(e)}\nPlease check your Azure OpenAI configuration."


# Function definitions for OpenAI function calling
def get_risk_assessment_functions():
    """Get function definitions for OpenAI function calling"""
    return [
        {
            "type": "function",
            "function": {
                "name": "assess_risks",
                "description": "Performs comprehensive risk assessment analysis for locations, buildings, or assets",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "research_data": {
                            "type": "string",
                            "description": "Research data or information about the location/building to assess"
                        },
                        "location": {
                            "type": "string",
                            "description": "The specific location, building, or asset being assessed",
                            "default": ""
                        },
                        "risk_categories": {
                            "type": "string",
                            "description": "Specific risk categories to focus on (optional)",
                            "default": ""
                        }
                    },
                    "required": ["research_data"]
                }
            }
        }
    ]


# Helper class for creating risk assessment agent using OpenAI
class RiskAssessmentAgent:
    """
    An OpenAI-based risk assessment agent with function calling capabilities
    """
    
    def __init__(self):
        """Initialize the risk assessment agent with OpenAI client"""
        self._credential = AzureCliCredential()
        self.client = openai.AsyncAzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_ad_token_provider=lambda: self._credential.get_token("https://cognitiveservices.azure.com/.default").token,
            api_version="2024-02-01"
        )
        self.plugin = RiskAssessmentPlugin()
        self.system_message = """You are an expert risk assessment analyst with deep expertise in evaluating various types of risks for locations, buildings, and assets. Your role is to provide comprehensive, actionable risk assessments based on research data.

You have access to risk assessment functions that can help you analyze locations and buildings. When a user asks for risk assessment, you should:

1. Use the assess_risks function to perform comprehensive analysis
2. Provide detailed risk analysis covering:
   - Structural & Engineering Risks
   - Environmental & Natural Disaster Risks  
   - Safety & Security Risks
   - Financial & Economic Risks
   - Regulatory & Legal Risks
   - Operational & Business Risks

Always provide professional, thorough, and actionable risk assessments that help users make informed decisions about locations, buildings, and assets."""

    async def chat(self, message: str) -> str:
        """
        Chat with the risk assessment agent, which can call risk assessment functions as needed
        
        Args:
            message: The user's message or risk assessment request
            
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
                tools=get_risk_assessment_functions(),
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
                    if function_name == "assess_risks":
                        function_response = await self.plugin.assess_risks(
                            research_data=function_args.get("research_data"),
                            location=function_args.get("location", ""),
                            risk_categories=function_args.get("risk_categories", "")
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


def create_risk_assessment_agent() -> RiskAssessmentAgent:
    """
    Create and configure the risk assessment agent using OpenAI
    
    Returns:
        RiskAssessmentAgent: Configured risk assessment agent
    """
    return RiskAssessmentAgent()