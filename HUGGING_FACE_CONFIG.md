# Hugging Face Configuration

This directory is configured for deployment on Hugging Face Spaces using Docker.

## Quick Deploy

1. Create a new Space on HuggingFace with Docker SDK
2. Push this repository
3. Hugging Face will automatically:
   - Build the Docker image
   - Install dependencies from `requirements.txt`
   - Run `python app.py`
   - Launch Gradio on port 7860

## Key Configuration

### Dockerfile
- Uses Python 3.11 slim image
- Installs build-essential for any compiled dependencies
- Creates package __init__.py files
- Runs `python app.py` as entrypoint

### requirements.txt
- **gradio**: Web UI framework
- **transformers**: NLP models
- **torch**: Deep learning
- **numpy/pandas**: Data processing
- **requests**: HTTP library

### app.py
- Gradio interface (not Flask)
- Listens on 0.0.0.0:7860
- Includes example queries
- Caches example results

### Relative Imports
All Python imports are relative (no `project.` prefix):
```python
from agents.planner import Planner      # ✓ Correct
from core.context_engineering import ContextEngine  # ✓ Correct
# NOT from project.agents.planner import Planner  ✗ Wrong
```

### No File Logging Issues
Observability module gracefully handles read-only filesystems:
- Logs to console (always works)
- Tries file logging only if directory is writable
- Fails gracefully on Hugging Face Spaces

## Environment Variables (Optional)

Set in Space settings → Environment variables (Secrets tab):

```
API_KEY=your_key_here
LOG_LEVEL=INFO
```

Access in code:
```python
import os
api_key = os.getenv("API_KEY")
```

## Ports

Hugging Face Spaces:
- Always uses port **7860**
- Exposed automatically to public web
- No need to configure port forwarding

## Memory & Computing

Free tier:
- Shared CPU (usually Intel)
- 16GB RAM
- Suitable for this application

Upgrade available for:
- Persistent storage
- Higher CPU/GPU
- Private spaces

## Secrets Management

Don't hardcode API keys! Use Space Secrets:

1. Go to Space settings
2. "Repository secrets" tab
3. Add new secret
4. Access via `os.getenv("SECRET_NAME")`

## Monitoring

View app logs in Space settings:
- Click "Logs" tab
- See build output
- See runtime logs
- Check for errors

## Updates

To update the app:
```bash
git add .
git commit -m "Update: description"
git push space main
```

Hugging Face rebuilds automatically.

## Limitations & Workarounds

| Limitation | Workaround |
|-----------|-----------|
| No persistent file storage | Use database or cache |
| No direct GPU access (free) | Use CPU-optimized models or upgrade |
| 30-min inactivity sleep | Paid plan for always-on |
| Read-only filesystem parts | Our code handles this gracefully |

## Testing Before Deploy

```bash
# Build and run locally
docker build -t disaster-agent .
docker run -p 7860:7860 disaster-agent

# Or test directly
pip install -r requirements.txt
python app.py
```

Then visit http://localhost:7860

## File Structure

```
project/
├── Dockerfile                 # Docker container config
├── requirements.txt           # Python packages
├── app.py                    # Gradio interface (START HERE)
├── main_agent.py             # Agent logic
├── run_demo.py               # Demo script
├── README.md                 # Project docs
├── HF_DEPLOYMENT_GUIDE.md   # Deployment guide
├── DEPLOYMENT_CHECKLIST.md   # Checklist
├── .gitignore                # Git ignore rules
├── agents/
├── core/
├── memory/
└── tools/
```

## Deployment Command

After setting up HF Space:

```bash
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/disaster-resource-connector
git push space main
```

Replace YOUR_USERNAME with your Hugging Face username.

## Success Indicators

- [ ] Dockerfile builds successfully
- [ ] App starts on port 7860
- [ ] Gradio interface loads
- [ ] Example queries work
- [ ] No import errors
- [ ] No file permission errors
- [ ] Agent responds to messages

## Support

See `HF_DEPLOYMENT_GUIDE.md` for detailed instructions.

---

**Ready? Start deploying now! 🚀**
