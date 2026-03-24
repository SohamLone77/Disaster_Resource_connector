# Disaster Resource Connector 🆘

An AI-powered agent that helps people find essential resources during disaster situations, including shelter, food, medical aid, and government assistance.

## Features

- **Multi-Agent Architecture**: Planner, Worker, and Evaluator agents work together to process requests
- **Resource Discovery**: Find shelters, food distribution points, medical stations, and government aid
- **Context Understanding**: Analyzes urgency and disaster type from user input
- **Session Memory**: Maintains conversation history and caches resource data
- **Real-time Observability**: Tracks agent activities and performance metrics

## Architecture

```
app.py (Gradio Interface)
  ↓
main_agent.py (Orchestrator)
  ├── agents/
  │   ├── planner.py (Creates execution plans)
  │   ├── worker.py (Executes resource discovery)
  │   └── evaluator.py (Validates and ranks results)
  ├── core/
  │   ├── context_engineering.py (Analyzes user context)
  │   ├── observability.py (Logging and metrics)
  │   └── a2a_protocol.py (Agent-to-agent messaging)
  ├── memory/
  │   └── session_memory.py (Session and cache management)
  └── tools/
      └── tools.py (Resource data)
```

## Deployment on Hugging Face Spaces

### Option 1: Direct Deployment

1. Fork this repository to your GitHub account
2. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
3. Click "Create new Space"
4. Select:
   - **Owner**: Your Hugging Face username
   - **Space name**: `disaster-resource-connector`
   - **License**: OpenRAIL (or your choice)
   - **Space SDK**: Docker
5. Connect your GitHub repository
6. Click "Create Space"

The app will automatically deploy using the `Dockerfile`.

### Option 2: Manual Setup

1. Create a new Space on Hugging Face with **Gradio** SDK
2. Clone this repository
3. Push the code to the Space repository
4. The app will auto-deploy

## Local Development

### Prerequisites

- Python 3.8+
- pip or conda

### Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running Locally

```bash
python app.py
```

The application will launch at `http://localhost:7860`

## Usage

1. Open the Gradio interface
2. Enter your situation in the text box (e.g., "I need shelter after the hurricane")
3. Click "Find Resources" or press Enter
4. View the recommended resources with locations and descriptions

### Example Queries

- "I need shelter after the hurricane"
- "Where can I find food and water?"
- "Medical assistance needed urgently"
- "How do I apply for FEMA aid?"

## Configuration for Hugging Face

The code automatically adapts to Hugging Face environment:

- **Port**: Uses port 7860 (Hugging Face default)
- **Logging**: Only writes to console (file logging disabled on Spaces)
- **Server**: Binds to 0.0.0.0 (accessible from web)

## Project Structure

```
project/
├── app.py                 # Gradio interface (main entry point)
├── main_agent.py          # Agent orchestrator
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── agents/
│   ├── __init__.py
│   ├── planner.py        # Request planning
│   ├── worker.py         # Resource discovery
│   └── evaluator.py      # Result evaluation
├── core/
│   ├── __init__.py
│   ├── context_engineering.py  # User context analysis
│   ├── observability.py         # Logging and metrics
│   └── a2a_protocol.py          # Agent communication
├── memory/
│   ├── __init__.py
│   └── session_memory.py   # Session and cache management
└── tools/
    ├── __init__.py
    └── tools.py           # Resource data and tools
```

## Dependencies

- **gradio**: Web UI framework
- **transformers**: NLP models (for future enhancements)
- **torch**: Deep learning framework
- **numpy/pandas**: Data processing
- **requests**: HTTP requests

## Environment Variables

Currently, the application works without environment variables. All configuration is hardcoded for demo purposes. To extend with real APIs:

1. Add `.env` file with API keys
2. Update `tools/tools.py` to fetch from real APIs
3. Update requirements.txt with API client libraries

## Testing

Run test cases:

```bash
python run_demo.py
```

This will test the agent with sample queries and display results.

## Troubleshooting

### Import Errors
- Ensure you're in the project root directory
- Check that all relative imports are used (no `project.` prefix)
- Verify Python path: `echo $PYTHONPATH`

### Port Issues
- Hugging Face Spaces automatically handles port mapping
- Locally, the app uses port 7860

### Dependencies
- Update all packages: `pip install --upgrade -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

## Future Enhancements

- [ ] Integration with real disaster resource APIs
- [ ] Real-time location-based filtering
- [ ] Multi-language support
- [ ] User authentication and preferences
- [ ] SMS integration for emergency alerts
- [ ] Offline support

## License

This project is provided as-is for educational and humanitarian purposes.

## Support

For issues or questions:
1. Check the [Hugging Face Spaces documentation](https://huggingface.co/docs/hub/spaces)
2. Review logs in the Hugging Face Space interface
3. Test locally before deploying

---

**Built with ❤️ for disaster relief assistance**
=======
---
title: Disaster Resource Connector
emoji: 🌖
colorFrom: gray
colorTo: pink
sdk: gradio
sdk_version: 6.0.2
app_file: app.py
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

