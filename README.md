# Location Risk Assessment - AI Analysis System

This project provides comprehensive **Location Risk Assessment** capabilities, combining deep research with professional risk analysis for buildings, locations, and assets using advanced AI agents.

## Features

### 🔬 Deep Research Agent
- Comprehensive multi-level research with configurable breadth and depth
- Systematic analysis across multiple aspects of a location/building
- Detailed report generation with structured methodology
- Built as a Semantic Kernel plugin for maximum reusability

### � Risk Assessment Agent
- Professional risk analysis across multiple categories:
  - Structural & Engineering risks
  - Environmental & Natural Disaster risks
  - Safety & Security risks
  - Financial & Economic risks
  - Regulatory & Legal risks
  - Operational & Business risks
- Evidence-based risk evaluation with likelihood and impact scoring
- Actionable recommendations and mitigation strategies

### 💾 File Saving Functionality
- Automatic saving of complete analysis reports
- Markdown format with professional structure
- Sanitized filenames with timestamps
- Organized in "researches" directory
- Complete research + risk assessment in single file

## Recent Updates

This solution has been **completely modernized** with:
- **Semantic Kernel 1.37.0** (latest version)
- **ChatCompletionAgent** instead of deprecated AzureAIAgent
- **Location Risk Assessment** - Professional risk analysis system
- **File Saving** - Automatic report generation in markdown format
- **Two-stage analysis** - Deep research followed by risk assessment
- **Modern plugin architecture** for better modularity
- **Simplified deployment** without complex Azure AI Foundry dependencies

## Usage

### Running the Application

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the application
python3 location_searches_main.py
```

### How It Works

1. **Input**: Enter any location, building, or asset to analyze
2. **Stage 1**: Deep Research Agent performs comprehensive research
3. **Stage 2**: Risk Assessment Agent analyzes potential risks
4. **Output**: Complete analysis saved to markdown file in "researches" directory

### Example Inputs

- `"Empire State Building, New York"`
- `"Downtown Seattle office building at 1st and Pike"`
- `"Residential area in Miami Beach, Florida"`
- `"Industrial facility in Houston, Texas"`
- `"Microsoft Office The Circle, Zürich"`

### Output Files

Analysis reports are automatically saved as:
```
researches/Location_Name_YYYYMMDD_HHMMSS.md
```

Example: `Statue_of_Liberty,_New_York_20250922_151537.md`

## Deep Research Plugin

The Deep Research Plugin provides comprehensive research capabilities:

### `deep_research(query, breadth, depth)`
- **query**: Research topic or question
- **breadth**: Number of research aspects to explore (1-10, default: 3)
- **depth**: Number of research iterations per aspect (1-5, default: 2)

## Risk Assessment Plugin

The Risk Assessment Plugin provides professional risk analysis:

### `assess_risks(location_info)`
- **location_info**: Detailed research information about the location
- **Returns**: Comprehensive risk analysis across 6 categories
- **Output**: Structured risk assessment with evidence and recommendations

## File Management

### Automatic Saving
- All analysis reports automatically saved to `researches/` directory
- Files named with sanitized location name + timestamp
- Complete markdown format with headers and structure

### Filename Sanitization
- Removes invalid characters for safe file naming
- Replaces spaces and special characters with underscores
- Preserves readability while ensuring cross-platform compatibility

## Configuration

Set the following environment variables in your `.env` file:

```bash
# For Azure OpenAI (used by both Deep Research and Risk Assessment)
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
AZURE_OPENAI_API_KEY=your_api_key

# Optional: For Bing Search (if using search functionality)
BING_SEARCH_API_KEY=your_bing_api_key_here
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables in `.env` file

3. Run the application:
```bash
source .venv/bin/activate
python3 location_searches_main.py
```

## File Structure

```
12-location-searches-agentic/
├── location_searches_main.py       # Main application with risk assessment
├── deep_research_plugin.py         # Deep Research Plugin with ChatCompletionAgent
├── risk_agent.py                   # Risk Assessment Plugin
├── researches/                     # Auto-generated analysis reports
│   └── *.md                        # Saved analysis files
├── test_deep_research.py           # Comprehensive test suite
├── requirements.txt                # Updated dependencies with SK 1.37.0
├── .env                            # Environment variables
└── README.md                       # This file
```

## Analysis Methodology

The application uses a systematic two-stage approach:

### Stage 1: Deep Research
1. **Outline Generation**: Creates multiple research aspects based on the location
2. **Iterative Research**: Performs multiple research iterations for each aspect
3. **Comprehensive Analysis**: Synthesizes findings across all aspects and iterations
4. **Report Generation**: Creates structured reports with methodology notes

### Stage 2: Risk Assessment
1. **Risk Identification**: Analyzes potential risks across 6 key categories
2. **Evidence Evaluation**: Reviews research data for risk indicators
3. **Impact Assessment**: Evaluates likelihood and severity of identified risks


### Research Aspects Covered

- Current state and overview
- Recent developments and trends  
- Key challenges and opportunities
- Future implications and predictions
- Expert opinions and analysis
- Technical aspects and specifications
- Economic and market impact
- Social and cultural effects
- Regulatory and legal considerations
- Comparative analysis and alternatives

### Risk Categories Analyzed

1. **🏗️ Structural & Engineering** - Building integrity, materials, maintenance
2. **🌍 Environmental & Natural Disaster** - Climate risks, weather threats
3. **🚨 Safety & Security** - Personnel safety, security threats, access control
4. **💰 Financial & Economic** - Cost risks, market factors, funding issues
5. **🏛️ Regulatory & Legal** - Compliance, legal requirements, policy changes
6. **🚀 Operational & Business** - Operational disruptions, business continuity

## Testing

Test the individual components:

```bash
# Test Deep Research Plugin
python3 test_deep_research.py

# Test the complete application
source .venv/bin/activate
echo "Test Location" | python3 location_searches_main.py
```

The test suite includes:
- Direct plugin function testing
- Agent-based integration testing
- Individual function validation
- Error handling verification

