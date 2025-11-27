# EcoHome Energy Advisor

An AI-powered energy optimization agent that helps customers reduce electricity costs and environmental impact through personalized recommendations.

## Project Overview

EcoHome is a smart-home energy start-up that helps customers with solar panels, electric vehicles, and smart thermostats optimize their energy usage. The Energy Advisor agent provides personalized recommendations about when to run devices to minimize costs and carbon footprint.

### Key Features

- **Weather Integration**: Uses weather forecasts to predict solar generation
- **Dynamic Pricing**: Considers time-of-day electricity prices for cost optimization
- **Historical Analysis**: Queries past energy usage patterns for personalized advice
- **RAG Pipeline**: Retrieves relevant energy-saving tips and best practices
- **Multi-device Optimization**: Handles EVs, HVAC, appliances, and solar systems
- **Cost Calculations**: Provides specific savings estimates and ROI analysis

## Project Structure

```
ecohome_starter/
├── models/
│   ├── __init__.py
│   └── energy.py              # Database models for energy data
├── data/
│   └── documents/
│       ├── tip_device_best_practices.txt
│       └── tip_energy_savings.txt
├── agent.py                   # Main Energy Advisor agent
├── tools.py                   # Agent tools (weather, pricing, database, RAG)
├── requirements.txt           # Python dependencies
├── 01_db_setup.ipynb         # Database setup and sample data
├── 02_rag_setup.ipynb        # RAG pipeline setup
├── 03_run_and_evaluate.ipynb # Agent testing and evaluation
└── README.md                  # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file with your API keys:

```bash
VOCAREUM_API_KEY=your_vocareum_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Notebooks

Execute the notebooks in order:

1. **01_db_setup.ipynb** - Set up the database and populate with sample data
2. **02_rag_setup.ipynb** - Configure the RAG pipeline for energy tips
3. **03_agent_evaluation.ipynb** - Test and evaluate the agent
4. **03_run_and_evaluate.ipynb** - Run and evaluate the agent with example scenarios

> Persona-friendly tip: You can pass a system-level `context` when invoking the agent to reflect your household. The notebooks include a sample night-shift persona (Odaiba, Tokyo, heavy GPU compute 22:00-06:00). Swap this out with your own patterns (work hours, comfort temps, battery preferences, EV flexibility).

## Agent Capabilities

### Tools Available

- **Weather Forecast**: Get hourly weather predictions and solar irradiance
- **Electricity Pricing**: Access time-of-day pricing data
- **Energy Usage Query**: Retrieve historical consumption data
- **Solar Generation Query**: Get past solar production data
- **Energy Tips Search**: Find relevant energy-saving recommendations
- **Savings Calculator**: Compute potential cost savings

### Example Questions

The Energy Advisor can answer questions like:

- "When should I charge my electric car tomorrow to minimize cost and maximize solar power?"
- "What temperature should I set my thermostat on Wednesday afternoon if electricity prices spike?"
- "Suggest three ways I can reduce energy use based on my usage history."
- "How much can I save by running my dishwasher during off-peak hours?"
- "I run GPU jobs at night—how should I adjust HVAC and EV charging tomorrow?"

## Database Schema

### Energy Usage Table
- `timestamp`: When the energy was consumed
- `consumption_kwh`: Amount of energy used
- `device_type`: Type of device (EV, HVAC, appliance)
- `device_name`: Specific device name
- `cost_usd`: Cost at time of usage

### Solar Generation Table
- `timestamp`: When the energy was generated
- `generation_kwh`: Amount of solar energy produced
- `weather_condition`: Weather during generation
- `temperature_c`: Temperature at time of generation
- `solar_irradiance`: Solar irradiance level

## Agent Instructions (implemented in 03_run_and_evaluate.ipynb)
- Who: EcoHome Energy Advisor for smart homes with solar, EVs, HVAC, storage; default persona = night-shift engineer in Odaiba (changeable via `context`).
- What: Understand question + context → pull weather, TOU prices, usage/solar history, and tips → propose schedules + savings.
- How: Use tools (`get_weather_forecast`, `get_electricity_prices`, `query_energy_usage`, `query_solar_generation`, `get_recent_energy_summary`, `search_energy_tips`, `calculate_energy_savings`), avoid guessing, cite data, quantify costs/savings, keep responses concise and actionable.

## Key Technologies

- **LangChain**: Agent framework and tool integration
- **LangGraph**: Agent orchestration and workflow
- **ChromaDB**: Vector database for document retrieval
- **SQLAlchemy**: Database ORM and management
- **OpenAI**: LLM and embeddings
- **SQLite**: Local database storage

## Evaluation & Testing
- `03_run_and_evaluate.ipynb` now includes:
  - A crafted system prompt with persona guidance
  - 10 diverse test cases (EV, HVAC, appliances, solar, pricing, ROI, night compute)
  - Heuristic evaluation of responses (accuracy/relevance/completeness/usefulness) and tool usage checks
  - A generated report summarizing averages and per-test feedback

## Knowledge Base & RAG
- Added five new tip files in `data/documents/` (HVAC, smart automation, renewable integration, seasonal management, energy storage) to enrich RAG responses.
- Vector store auto-builds on first use; subsequent runs reuse `data/vectorstore/`.
- For VOC credentials: `.env` uses `OPENAI_API_KEY`/`OPENAI_API_BASE`; code routes both chat and embeddings through a helper to ensure the key is passed as a plain string (OpenAI client set explicitly for sync calls).

## Getting Started

1. Clone this repository
2. Install the required dependencies
3. Set up your environment variables
4. Run the notebooks in sequence
5. Test the agent with your own questions

## Contributing

This is a learning project. Feel free to:
- Add new tools and capabilities
- Improve the evaluation metrics
- Enhance the RAG pipeline
- Add more sophisticated optimization algorithms

## License

This project is for educational purposes as part of the Udacity Course 2 curriculum.
