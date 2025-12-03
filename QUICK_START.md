# 🚀 Quick Start Guide - Deploy to Hugging Face in 5 Minutes

## Step 1: Clone & Setup (1 min)

```bash
# Navigate to project
cd c:\Users\SOHAM\OneDrive\Desktop\Courses\Disaster_Agent\project

# Initialize git
git init
git config user.email "your@email.com"
git config user.name "Your Name"
git add .
git commit -m "Initial commit: Disaster Resource Connector"
```

## Step 2: Create Hugging Face Space (2 min)

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Fill in the form:
   - **Owner**: Your username
   - **Space name**: `disaster-resource-connector`
   - **License**: OpenRAIL-M
   - **Space SDK**: **Docker** ← ⭐ Important!
4. Click **"Create Space"**

## Step 3: Push Your Code (1 min)

Copy the command from your new Space page and run it:

```bash
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/disaster-resource-connector
git push space main
```

Replace `YOUR_USERNAME` with your Hugging Face username.

## Step 4: Wait for Deployment (1 min)

1. Go to your Space page
2. Click **"Logs"** to watch the build
3. Wait for "Build complete" ✓
4. Click **"View Space"**

## Step 5: Test It! ✓

The app is now live at:
```
https://huggingface.co/spaces/YOUR_USERNAME/disaster-resource-connector
```

Try these test queries:
- "I need shelter after the hurricane"
- "Where can I find food and water?"
- "Medical assistance needed urgently"
- "How do I apply for FEMA aid?"

---

## What Changed from Original?

| Aspect | Before | After |
|--------|--------|-------|
| **Framework** | Flask (REST API) | Gradio (Web UI) |
| **Interface** | cURL/HTTP requests | Web form + examples |
| **Imports** | `from project.agents...` | `from agents...` |
| **Port** | 5000 | 7860 |
| **Logging** | File only | Console + optional file |
| **Deployment** | Manual | Automatic Docker build |

---

## If Something Goes Wrong

### Build fails?
- Click "Logs" in Space settings
- Check error messages
- Common fix: Update `requirements.txt`

### App won't start?
- Verify `Dockerfile` exists
- Check `app.py` has no syntax errors
- Ensure all imports are relative (no `project.` prefix)

### Can't see the interface?
- Give it 30 seconds to load
- Refresh the page
- Check Space status is "Running"

### Need more help?
- See `HF_DEPLOYMENT_GUIDE.md` (detailed guide)
- See `DEPLOYMENT_CHECKLIST.md` (verification checklist)
- See `HUGGING_FACE_CONFIG.md` (configuration details)

---

## Local Testing First (Optional)

Before uploading, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Open browser to http://localhost:7860
```

---

## Success! 🎉

Your Disaster Resource Connector is now:
- ✓ Live on the internet
- ✓ Accessible 24/7
- ✓ Shareable with anyone
- ✓ Automatically scaled by Hugging Face

Share the link with others to help during disasters!

---

## Next Steps (Optional)

1. **Connect real APIs** - Replace mock data with real disaster resources
2. **Add authentication** - Require login for certain features
3. **Deploy updates** - Just push to git, HF rebuilds automatically
4. **Monitor usage** - Check Space settings for analytics

---

## Key Files Reference

- **`app.py`** - Main Gradio interface
- **`Dockerfile`** - Container configuration
- **`requirements.txt`** - Python dependencies
- **`README.md`** - Full project documentation

---

## Support Resources

- Hugging Face Spaces: https://huggingface.co/docs/hub/spaces
- Gradio Documentation: https://www.gradio.app/
- This repo has detailed guides in:
  - `HF_DEPLOYMENT_GUIDE.md`
  - `DEPLOYMENT_CHECKLIST.md`
  - `HUGGING_FACE_CONFIG.md`

---

**You're all set! Deploy now and start helping people find disaster resources! 💪**
