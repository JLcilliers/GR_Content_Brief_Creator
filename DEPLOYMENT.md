# Deployment Guide - Streamlit Community Cloud

This guide walks you through deploying the Content Brief Creator as a web application on Streamlit Community Cloud (100% free hosting).

## Prerequisites

1. **GitHub Account** - Your code must be in a GitHub repository
2. **Streamlit Account** - Sign up at [share.streamlit.io](https://share.streamlit.io) (free, uses GitHub login)
3. **AI Provider API Key** - At least one of:
   - OpenAI API key
   - Anthropic (Claude) API key
   - Perplexity API key
   - Mistral API key

## Step 1: Prepare Your Repository

Ensure these files are committed to your GitHub repository:
- ✅ `app.py` - Main Streamlit application
- ✅ `requirements.txt` - Python dependencies
- ✅ `.streamlit/config.toml` - Streamlit configuration
- ✅ `.streamlit/secrets.toml.example` - Example secrets file
- ✅ `.gitignore` - Excludes secrets from git

## Step 2: Deploy to Streamlit Community Cloud

### 2.1 Sign In
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign in with GitHub"
3. Authorize Streamlit to access your GitHub account

### 2.2 Create New App
1. Click "New app" button
2. Select your repository: `GR_Content_Brief_Creator`
3. Select branch: `main`
4. Set main file path: `app.py`
5. Click "Deploy!"

### 2.3 Configure Secrets
**CRITICAL:** Add your API keys before the app finishes deploying

1. Click "Advanced settings" (or go to app settings after deployment)
2. Click "Secrets" in the left sidebar
3. Paste your API keys in TOML format:

```toml
# Add at least one AI provider API key
OPENAI_API_KEY = "sk-..."
CLAUDE_API_KEY = "sk-ant-..."
PERPLEXITY_API_KEY = "pplx-..."
MISTRAL_API_KEY = "..."

# Optional: Set default provider
DEFAULT_AI_PROVIDER = "openai"
```

4. Click "Save"
5. The app will automatically restart with your secrets

## Step 3: Access Your Web App

Your app will be available at:
```
https://[your-app-name].streamlit.app
```

Example: `https://content-brief-creator.streamlit.app`

## Step 4: Share with Others

✅ **Anyone can use your deployed app without needing API keys**
- You configure the API keys once in Streamlit secrets
- Users just visit the URL and start creating briefs
- All API costs are charged to your configured keys

## Features Available in Web App

✅ **Multi-AI Provider Support**
- OpenAI GPT-4o
- Claude 3.5 Sonnet
- Perplexity Sonar Large
- Mistral Large

✅ **Client Profile Management**
- Create and save client profiles
- Load existing clients
- Manage multiple clients

✅ **Content Brief Generation**
- Input topic and keywords
- Select AI provider
- Generate professional briefs

✅ **Export Options**
- Download as Word document (.docx)
- Professional formatting
- Timestamped filenames

## Updating Your App

Streamlit Community Cloud automatically redeploys when you push to GitHub:

1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update app"
   git push origin main
   ```
3. App automatically redeploys in ~1-2 minutes

## Troubleshooting

### App won't start
- **Check logs** in Streamlit Cloud dashboard
- **Verify secrets** are configured correctly
- **Check requirements.txt** has all dependencies

### "No AI provider API keys found"
- Go to app settings → Secrets
- Add at least one API key in TOML format
- Save and restart app

### Import errors
- Check `requirements.txt` has correct versions
- Try redeploying the app
- Check Python version compatibility

### API errors
- Verify API keys are valid
- Check API key has credits/quota
- Try different AI provider

## Cost Management

**Streamlit hosting:** FREE forever
**API costs:** Depends on usage
- OpenAI GPT-4o: ~$0.01-0.03 per brief
- Claude 3.5 Sonnet: ~$0.01-0.02 per brief
- Perplexity: ~$0.005-0.01 per brief
- Mistral: ~$0.002-0.008 per brief

**Tips to minimize costs:**
- Use Mistral for budget-friendly briefs
- Monitor API usage in provider dashboards
- Set up usage alerts in provider accounts
- Consider rate limiting for public apps

## Security Best Practices

✅ **DO:**
- Store API keys only in Streamlit secrets
- Use `.gitignore` to exclude `.env` and `secrets.toml`
- Monitor API usage regularly
- Rotate API keys periodically

❌ **DON'T:**
- Commit API keys to GitHub
- Share your Streamlit app secrets
- Use production API keys for testing
- Ignore usage alerts

## Advanced: Supabase Integration (Coming Soon)

Supabase will enable:
- Persistent client profile storage
- User authentication
- Multi-user support
- Profile sharing across team

Documentation will be updated when Supabase integration is complete.

## Support

- **Streamlit Docs:** [docs.streamlit.io](https://docs.streamlit.io)
- **GitHub Issues:** [Your repo]/issues
- **Streamlit Community:** [discuss.streamlit.io](https://discuss.streamlit.io)

---

**Your web app is now live! 🚀**

Share the URL with anyone who needs to create content briefs.
