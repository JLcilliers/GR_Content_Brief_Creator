# Content Brief Creator

An AI-powered content brief generation system that creates consistent, professionally-formatted content briefs by pulling from customizable client profiles. Supports multiple AI providers including OpenAI, Claude, Perplexity, and Mistral for flexibility and reliability.

## Features

- **Client Profile Management**: Store and manage client-specific information, restrictions, and requirements
- **Multi-AI Provider Support**: Choose between OpenAI GPT-4o, Claude 3.5 Sonnet, Perplexity Sonar, or Mistral Large for brief generation
- **AI-Powered Brief Generation**: Automatically generates comprehensive 12-section content briefs
- **Consistent Formatting**: Every brief follows the same structure with Poppins font styling and professional formatting
- **Word Document Output**: Creates properly formatted .docx files ready for immediate use

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

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/JLcilliers/GR_Content_Brief_Creator.git
   cd GR_Content_Brief_Creator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your AI provider API keys**:
   - Copy `.env.example` to `.env`
   - Add at least one AI provider API key:
     ```
     # Choose one or more providers
     OPENAI_API_KEY=your_openai_api_key_here
     CLAUDE_API_KEY=your_claude_api_key_here
     PERPLEXITY_API_KEY=your_perplexity_api_key_here
     MISTRAL_API_KEY=your_mistral_api_key_here
     
     # Set default provider (optional)
     DEFAULT_AI_PROVIDER=openai
     ```

## Usage

### Running the Application

```bash
python main.py
```

### Creating a Content Brief

1. Select **"Create Brief"** from the main menu
2. **Choose an AI provider** from the available options:
   - OpenAI GPT-4o
   - Claude 3.5 Sonnet
   - Perplexity Sonar Large
   - Mistral Large
3. Choose a client from the list
4. Enter the content topic
5. Provide primary keyword
6. Add secondary keywords (comma-separated)
7. The system will:
   - Pull client profile data automatically
   - Generate all 12 brief sections using your selected AI provider
   - Create a formatted Word document in `output_briefs/`

### Managing Clients

#### List All Clients
```bash
Select "Manage Clients" → "List all clients"
```

#### Create New Client
```bash
Select "Manage Clients" → "Create new client"
```

You'll be prompted to enter:
- Client name
- Website URL
- Client information (multi-line, press Enter twice to finish)
- Restrictions (legal, brand, SEO, content integrity)
- Requirements (word count, tone, mandatory mentions, etc.)

#### View Client Details
```bash
Select "Manage Clients" → "View client details"
```

#### Update Client
```bash
Select "Manage Clients" → "Update client"
```

#### Delete Client
```bash
Select "Manage Clients" → "Delete client"
```

## Client Profile Structure

Client profiles are stored as JSON files in the `clients/` directory. Each profile contains:

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

## Output

Generated briefs are saved to `output_briefs/` with the naming convention:
```
{client_name}_{topic}_{timestamp}.docx
```

Example: `castle_surveys_measured_building_surveys_20250122_143052.docx`

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

## Project Structure

```
Content Brief Creator/
├── main.py                 # Main CLI interface
├── brief_generator.py      # AI brief generation logic
├── ai_provider.py          # AI provider abstraction layer
├── client_manager.py       # Client CRUD operations
├── document_formatter.py   # Word document creation
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .env                   # Your API keys (git-ignored)
├── .gitignore             # Git ignore rules
├── clients/               # Client profile JSON files
│   └── castle_surveys.json
└── output_briefs/         # Generated brief documents
```

## Requirements

- Python 3.8+
- At least one AI provider API key:
  - OpenAI API key (for GPT-4o)
  - Anthropic API key (for Claude 3.5 Sonnet)
  - Perplexity API key (for Sonar Large)
  - Mistral API key (for Mistral Large)
- Internet connection for API calls

## Dependencies

- python-docx >= 1.1.0
- openai >= 1.0.0
- anthropic >= 0.18.0
- requests >= 2.31.0
- python-dotenv >= 1.0.0

## Example Workflow

1. **First Time Setup**:
   ```bash
   # Install and configure
   pip install -r requirements.txt
   cp .env.example .env
   # Add at least one AI provider API key to .env
   ```

2. **Create a Client Profile**:
   ```bash
   python main.py
   # Select: Manage Clients → Create new client
   # Enter client details
   ```

3. **Generate a Brief**:
   ```bash
   python main.py
   # Select: Create Brief
   # Select AI provider (OpenAI, Claude, Perplexity, or Mistral)
   # Choose client, enter topic and keywords
   # Wait for AI generation
   # Find output in output_briefs/
   ```

## Troubleshooting

**"No AI provider API keys found"**
- Ensure `.env` file exists in project root
- Verify at least one provider API key is set correctly:
  - `OPENAI_API_KEY=your_key`
  - `CLAUDE_API_KEY=your_key`
  - `PERPLEXITY_API_KEY=your_key`
  - `MISTRAL_API_KEY=your_key`

**"No clients found"**
- Create a client profile first using the Manage Clients menu

**"Failed to generate brief"**
- Check your internet connection
- Verify your selected AI provider API key is valid and has credits/access
- Try switching to a different AI provider
- Check API error message in console for specific details

## License

This project is proprietary software for internal use.

## Author

Created for Ghost Rank content production workflow.
