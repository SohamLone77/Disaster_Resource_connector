# Hugging Face Deployment Guide

## Quick Start (5 minutes)

### Step 1: Prepare Your Repository

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: Disaster Resource Connector"
```

### Step 2: Create Hugging Face Repository

1. Go to https://huggingface.co/new (create a new model/dataset/space)
2. Choose **Space** type
3. Fill in:
   - **Owner**: Your HF username
   - **Space name**: `disaster-resource-connector`
   - **Space SDK**: Docker
   - **License**: OpenRAIL-M (recommended)
4. Click "Create Space"

### Step 3: Push Your Code

After creating the space, Hugging Face will show push instructions. Follow them:

```bash
# Add Hugging Face remote
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/disaster-resource-connector

# Push your code
git push space main
```

Replace `YOUR_USERNAME` with your Hugging Face username.

### Step 4: Monitor Deployment

1. Go to your Space page
2. Click "Logs" to watch the build process
3. Once built, click "View Space"

---

## Detailed Steps with Screenshots

### Create Space

1. Navigate to https://huggingface.co/spaces
2. Click "Create new Space"
   ![Create Space](https://img.shields.io/badge/Step-1-blue)

3. Fill in the form:
   - **Owner**: Select your account
   - **Space name**: `disaster-resource-connector`
   - **License**: OpenRAIL-M
   - **Space SDK**: Docker ← **Important: Select Docker!**

4. Click "Create Space"

### Configure Git

Once the space is created, you'll see instructions like:

```bash
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/disaster-resource-connector
git push space main
```

### Push Code

From your project directory:

```bash
# If you haven't initialized git
git init
git config user.email "you@example.com"
git config user.name "Your Name"

# Add all files
git add .
git commit -m "Initial deployment to Hugging Face Spaces"

# Add the space as remote
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/disaster-resource-connector

# Push to space
git push space main
```

---

## Verify Deployment

1. The Space page shows build status
2. Wait for the build to complete (usually 2-5 minutes)
3. Once done, your app is live at:
   ```
   https://huggingface.co/spaces/YOUR_USERNAME/disaster-resource-connector
   ```

---

## Key Files for Deployment

```
project/
├── Dockerfile              # Container configuration
├── requirements.txt        # Python dependencies
├── app.py                 # Gradio interface (entry point)
├── main_agent.py          # Agent logic
└── [other modules]
```

**Important**: The `Dockerfile` is essential for deployment!

---

## Troubleshooting

### Build Fails

1. Check Logs: Click "Logs" in Space settings
2. Common issues:
   - Missing dependencies → Update `requirements.txt`
   - Import errors → Check relative imports (no `project.` prefix)
   - Port issues → Dockerfile uses port 7860 (correct for HF)

### App Won't Start

```
Check in logs for:
- Python version compatibility (we use Python 3.11)
- Missing __init__.py files (all provided)
- Import path issues (use relative imports)
```

### Slow Build

- First build takes longer (5-10 min)
- Subsequent builds are faster if only code changes
- Dependencies are cached

---

## Update Your App

To make changes:

```bash
# Make code changes
# ... edit files ...

# Commit and push
git add .
git commit -m "Updated feature X"
git push space main
```

The app will rebuild automatically.

---

## Networking & Security

- **Public by default**: Anyone can access your Space
- **Private Spaces**: Available in Pro tier
- **Environment variables**: Set in Space settings → Secrets
- **Rate limiting**: Handled by Hugging Face infrastructure

---

## Performance Considerations

- First request might be slow (warm-up)
- Gradio caching helps with repeated queries
- Multi-agent architecture uses in-memory processing

---

## Support & Resources

- Hugging Face Spaces Docs: https://huggingface.co/docs/hub/spaces
- Gradio Docs: https://gradio.app/docs/
- Hugging Face Community: https://discuss.huggingface.co/

---

## Example Space URL

After deployment, your app is available at:

```
https://huggingface.co/spaces/YOUR_USERNAME/disaster-resource-connector
```

Share this link to let others access your disaster resource agent!

---

**Ready to deploy? Start with Step 1 above! 🚀**
