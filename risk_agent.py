"""
Risk Assessment Agent Module

This module contains the RiskAssessmentPlugin and agent creation functionality
for performing comprehensive risk analysis on locations, buildings, and assets.
"""

import os
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import kernel_function
from azure.identity import AzureCliCredential
from typing import Annotated


class RiskAssessmentPlugin:
    """A Plugin to perform comprehensive risk assessment analysis"""
    
    def __init__(self):
        """Initialize the Risk Assessment Plugin"""
        pass
    
    @kernel_function(description="Performs comprehensive risk assessment analysis for locations, buildings, or assets")
    async def assess_risks(self,
                          research_data: Annotated[str, "Research data or information about the location/building to assess"],
                          location: Annotated[str, "The specific location, building, or asset being assessed"] = "",
                          risk_categories: Annotated[str, "Specific risk categories to focus on (optional)"] = "") -> str:
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
            # Create risk assessment agent
            risk_agent = ChatCompletionAgent(
                name="RiskAssessmentAnalyst",
                instructions="""You are an expert risk assessment analyst. Analyze the provided research data and perform a comprehensive risk assessment.

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

Format your response with clear headings and bullet points. Be specific and actionable based on the research data provided.""",
                service=AzureChatCompletion(
                    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                    api_version="2024-02-01",
                    credential=AzureCliCredential(),
                )
            )
            
            # Create chat history and add the assessment request
            chat_history = ChatHistory()
            prompt = f"""Please perform a comprehensive risk assessment for: {location}

Based on this research data:
{research_data}

Focus on: {risk_categories if risk_categories else 'all risk categories'}

Provide a detailed risk analysis."""
            
            chat_history.add_user_message(prompt)
            
            # Get the AI response
            responses = []
            async for message in risk_agent.invoke(chat_history):
                responses.append(message)
            
            # Extract and return the assessment content
            assessment_content = ""
            for message in responses:
                assessment_content += str(message.content)
            
            return assessment_content.strip()
            
        except Exception as e:
            return f"❌ Error during risk assessment: {str(e)}\nPlease check your Azure OpenAI configuration."


async def create_risk_assessment_agent() -> ChatCompletionAgent:
    """
    Create and configure the risk assessment agent using ChatCompletionAgent
    
    Returns:
        ChatCompletionAgent: Configured risk assessment agent
    """
    
    # Initialize kernel and Azure OpenAI service
    kernel = Kernel()
    
    # Configure Azure OpenAI chat completion service
    azure_chat_completion = AzureChatCompletion(
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version="2024-02-01",
    )
    kernel.add_service(azure_chat_completion)
    
    # Add the risk assessment plugin to the kernel
    kernel.add_plugin(RiskAssessmentPlugin(), "RiskAssessmentPlugin")
    
    # Create the chat completion agent with specialized risk assessment instructions
    risk_agent = ChatCompletionAgent(
        service_id="azure_chat_completion",
        kernel=kernel,
        name="RiskAssessmentAgent",
        instructions="""You are an expert risk assessment analyst with deep expertise in evaluating various types of risks for locations, buildings, and assets. Your role is to provide comprehensive, actionable risk assessments based on research data.

## Your Core Competencies:

### 🏗️ **Structural & Engineering Risks**
- Building integrity and structural soundness
- Foundation and seismic vulnerabilities
- Material degradation and aging infrastructure
- Construction quality and code compliance

### 🌍 **Environmental & Natural Disaster Risks**
- Climate change impacts and extreme weather
- Flood zones, earthquake zones, wildfire areas
- Air and water quality concerns
- Environmental contamination risks

### 🚨 **Safety & Security Risks**
- Crime rates and security vulnerabilities
- Emergency response capabilities
- Fire safety and evacuation procedures
- Accessibility and safety compliance

### 💰 **Financial & Economic Risks**
- Property value volatility
- Insurance costs and availability
- Market conditions and economic trends
- Regulatory and compliance costs

### 🏛️ **Regulatory & Legal Risks**
- Zoning and land use restrictions
- Building codes and permit requirements
- Environmental regulations
- Liability and legal exposure

### 🚀 **Operational & Business Risks**
- Supply chain and logistics vulnerabilities
- Technology and infrastructure dependencies
- Human factors and staffing risks
- Business continuity considerations

## Your Analysis Framework:

When provided with research data about a location or building, you must:

1. **SYSTEMATIC EVALUATION**: Analyze the research data across all risk categories
2. **RISK QUANTIFICATION**: Assign risk levels (Critical/High/Medium/Low) with clear justification
3. **IMPACT ASSESSMENT**: Evaluate potential consequences and likelihood
4. **INTERCONNECTED RISKS**: Identify how risks may compound or interact
5. **TEMPORAL CONSIDERATIONS**: Assess both immediate and long-term risks

## Your Response Structure:

### 📊 **Executive Risk Summary**
- Overall risk rating
- Top 3 critical risks

### 🔍 **Detailed Risk Analysis**
For each risk category:
- **Risk Level**: Critical/High/Medium/Low
- **Likelihood**: Probability of occurrence
- **Impact**: Potential consequences
- **Evidence**: Supporting data from research

## Guidelines:

- **Be Objective**: Base assessments on data and evidence
- **Be Specific**: Provide concrete, actionable recommendations
- **Be Comprehensive**: Cover all relevant risk categories
- **Be Practical**: Consider feasibility and cost-effectiveness
- **Be Clear**: Use clear risk ratings and plain language
- **Be Balanced**: Don't overstate or understate risks

Always provide professional, thorough, and actionable risk assessments that help users make informed decisions about locations, buildings, and assets."""
    )

    return risk_agent