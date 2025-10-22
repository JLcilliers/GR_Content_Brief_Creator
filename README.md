# Content Brief Creator - Web Application

An AI-powered web application for generating consistent, professionally-formatted content briefs by pulling from customizable client profiles. Access it through your browser with support for multiple AI providers including OpenAI, Claude, Perplexity, and Mistral.

🌐 **[Access the Web App](https://share.streamlit.io)** (Coming soon - see [Deployment Guide](DEPLOYMENT.md))

## Features

- **🌐 Web-Based Interface**: Access from any browser - no installation required for end users
- **👥 Client Profile Management**: Create, view, and manage client-specific information through an intuitive UI
- **🤖 Multi-AI Provider Support**: Choose between OpenAI GPT-4o, Claude 3.5 Sonnet, Perplexity Sonar, or Mistral Large
- **⚡ Real-Time Brief Generation**: Automatically generates comprehensive 12-section content briefs
- **📄 Professional Formatting**: Every brief follows consistent structure with Poppins font styling
- **⬇️ Instant Download**: Download formatted .docx files directly from the browser
- **🔐 Secure API Key Management**: Built-in secrets management through Streamlit Cloud
- **💾 Persistent Storage**: Supabase integration for client data (coming soon)
- **📱 Responsive Design**: Works on desktop, tablet, and mobile devices

## Brief Sections

Each generated brief includes:

1. Page Type (Landing Page vs Blog Post)
2. Page Title (SEO-optimized, ≤60 characters)
3. Meta Description (150-160 characters with CTA)
4. Target URL Structure
5. H1 Heading (Reader-focused with keyword integration)
6. Summary Bullets (4-6 key outcome points)
7. Internal Links Table (6-10 strategic links)
8. Target Audience (1-2 personas with pain points)
9. Call-to-Action (Primary and secondary CTAs)
10. Client Restrictions (Legal, brand, SEO, content integrity)
11. Client Requirements (Word count, tone, mandatory mentions, etc.)
12. Headings & FAQ (H2/H3 hierarchy + 5-8 FAQ questions)

## Quick Start

### Option 1: Use the Hosted Web App (Recommended)

1. **Access the app**: Visit the deployed web application URL (coming soon)
2. **Select AI Provider**: Choose your preferred AI provider from the sidebar
3. **Create/Load Client**: Create a new client profile or load an existing one
4. **Generate Brief**: Enter topic and keywords, then click "Generate Brief"
5. **Download**: Download the formatted Word document

No installation required! All you need is a web browser.

### Option 2: Run Locally for Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/JLcilliers/GR_Content_Brief_Creator.git
   cd GR_Content_Brief_Creator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys**:
   - Copy `.env.example` to `.env`
   - Add at least one AI provider API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     CLAUDE_API_KEY=your_claude_api_key_here
     PERPLEXITY_API_KEY=your_perplexity_api_key_here
     MISTRAL_API_KEY=your_mistral_api_key_here
     
     DEFAULT_AI_PROVIDER=openai
     ```

4. **Run the web app locally**:
   ```bash
   streamlit run app.py
   ```
   
   The app will open in your browser at `http://localhost:8501`

### Option 3: Deploy Your Own Instance

See the complete [Deployment Guide](DEPLOYMENT.md) for step-by-step instructions on deploying to Streamlit Community Cloud (free forever).

## Using the Web Application

### Creating a Client Profile

1. **Sidebar Navigation**: Use the "Client Management" section in the left sidebar
2. **Create New Client**: Click the expander and fill in:
   - Client name
   - Website URL
   - Client information
   - Restrictions (legal, brand, SEO, content integrity)
   - Requirements (word count, tone, mandatory mentions, etc.)
3. **Save**: Profile is automatically saved and available for selection

### Generating a Content Brief

1. **Load Client**: Select a client from the "Load Existing Client" dropdown
2. **Choose AI Provider**: Select from available providers (OpenAI, Claude, Perplexity, Mistral)
3. **Enter Details**:
   - Content topic
   - Primary keyword
   - Secondary keywords (comma-separated)
4. **Generate**: Click "Generate Brief" button
5. **Review**: Brief appears below with all 12 sections
6. **Download**: Click "Download Brief as .docx" to get formatted document

### Managing Existing Clients

- **View**: Select a client to see their full profile details
- **Update**: Edit any client information (coming soon)
- **Delete**: Remove client profiles (coming soon)

## Web App Architecture

```
Content Brief Creator/
├── app.py                  # Main Streamlit web application
├── brief_generator.py      # AI brief generation logic
├── ai_provider.py          # Multi-provider abstraction layer
├── client_manager.py       # Client CRUD operations
├── document_formatter.py   # Word document creation
├── requirements.txt        # Python dependencies
├── .streamlit/
│   ├── config.toml        # Streamlit theme configuration
│   └── secrets.toml       # API keys (git-ignored)
├── .env.example           # Environment template for local dev
├── .gitignore             # Git ignore rules
├── DEPLOYMENT.md          # Deployment guide
├── clients/               # Client profiles (JSON files)
└── README.md             # This file
```

## Client Profile Structure

Client profiles are stored as JSON files. Each profile contains:

```json
{
  "client_name": "Example Client",
  "site": "https://example.com",
  "information": "General information about the client...",
  "restrictions": {
    "legal": ["Do not provide legal advice"],
    "brand": ["Use 'we' not 'our team'"],
    "seo": ["Avoid keyword stuffing"],
    "content_integrity": ["No unverified statistics"]
  },
  "requirements": {
    "word_count": "800-1200 words",
    "readability_score": "8th grade level",
    "tone": "Professional, approachable",
    "mandatory_mentions": ["Service A", "Service B"],
    "sections_to_include": ["Introduction", "Benefits", "How it Works"],
    "cta_preference": "Contact us for a free consultation"
  }
}
```

## Document Formatting

- **Font**: Poppins (12pt body text, 14pt headings)
- **Colors**: 
  - Main title: Dark blue (RGB 0, 51, 102)
  - Section headings: Medium blue (RGB 51, 102, 153)
- **Language**: UK English
- **Punctuation**: Hyphens (not em-dashes)
- **Reading Level**: 8th grade

## Writing Style

All briefs follow "Absolute Mode" principles:
- No emojis, filler words, or conversational fluff
- Blunt, directive phrasing
- Outcome-focused language
- SEO best practices integrated throughout

## Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **AI Providers**: OpenAI, Anthropic, Perplexity, Mistral
- **Document Generation**: python-docx
- **Hosting**: Streamlit Community Cloud (free tier)
- **Database**: Supabase (coming soon)

## Requirements

### For End Users (Web App)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection

### For Developers (Local Development)
- Python 3.8+
- At least one AI provider API key
- Dependencies listed in `requirements.txt`

## Dependencies

```
python-docx>=1.1.0
openai>=1.0.0
anthropic>=0.18.0
requests>=2.31.0
python-dotenv>=1.0.0
streamlit>=1.28.0
supabase>=2.0.0
```

## Deployment

### Streamlit Community Cloud (Recommended)

**Advantages:**
- ✅ Free forever
- ✅ Automatic deployments from GitHub
- ✅ Built-in secrets management
- ✅ Custom domain support
- ✅ No server management required

**Quick Deploy:**
1. Push code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect repository and deploy
4. Add API keys in app settings

See the complete [Deployment Guide](DEPLOYMENT.md) for detailed instructions.

### Local Development Server

```bash
# Run locally
streamlit run app.py

# Run with custom port
streamlit run app.py --server.port 8080

# Run with file watching disabled
streamlit run app.py --server.fileWatcherType none
```

## Troubleshooting

### Web App Issues

**"No AI providers available"**
- Ensure API keys are configured in Streamlit secrets (deployed app)
- Check `.env` file for local development
- Verify at least one API key is valid

**"Failed to generate brief"**
- Check internet connection
- Verify selected AI provider has valid API key and credits
- Try switching to a different AI provider
- Check browser console for detailed error messages

**"Client profile not loading"**
- Ensure client profiles exist in the `clients/` directory
- Check JSON file format is valid
- Refresh the page

### Local Development Issues

**"Module not found: streamlit"**
```bash
pip install -r requirements.txt
```

**"Port already in use"**
```bash
streamlit run app.py --server.port 8502
```

**"API key not found"**
- Verify `.env` file exists in project root
- Check API key format (no quotes, no spaces)
- Restart Streamlit after changing `.env`

## Coming Soon

- ✨ Supabase integration for persistent client storage
- 👥 Multi-user support with authentication
- 📊 Usage analytics and brief history
- ✏️ In-app client profile editing
- 🔄 Brief versioning and revision history
- 📧 Email delivery of generated briefs

## CLI Mode (Legacy)

The original CLI interface is still available via `main.py`:

```bash
python main.py
```

However, the web application (`app.py`) is now the recommended interface for all users.

## Contributing

This is a private repository for Ghost Rank's content production workflow. For issues or feature requests, please contact the development team.

## License

This project is proprietary software for internal use.

## Author

Created for Ghost Rank content production workflow.

---

**Need Help?** See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment instructions or open an issue in the repository.
