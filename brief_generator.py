"""
AI Content Brief Generator
Generates comprehensive content briefs using multiple AI providers.
"""

from typing import Dict, List, Optional
from ai_provider import AIProvider


class BriefGenerator:
    """Generates content briefs using AI based on client profiles."""
    
    def __init__(self, provider: Optional[str] = None):
        """
        Initialize brief generator with specified AI provider.
        
        Args:
            provider: AI provider name ('openai', 'claude', 'perplexity', 'mistral')
                     If None, uses DEFAULT_AI_PROVIDER from .env
        """
        self.ai_provider = AIProvider(provider)
    
    def generate_brief(
        self,
        client_data: Dict,
        topic: str,
        primary_kw: str,
        secondary_kws: List[str]
    ) -> Dict[str, str]:
        """Generate a complete content brief."""
        
        brief_sections = {}
        
        # System instruction for absolute mode
        system_instruction = self._get_system_instruction()
        
        # Generate each section
        print("Generating Page Type...")
        brief_sections["page_type"] = self._generate_page_type(
            system_instruction, client_data, topic, primary_kw, secondary_kws
        )
        
        print("Generating Page Title...")
        brief_sections["page_title"] = self._generate_page_title(
            system_instruction, client_data, topic, primary_kw, secondary_kws
        )
        
        print("Generating Meta Description...")
        brief_sections["meta_description"] = self._generate_meta_description(
            system_instruction, client_data, topic, primary_kw, secondary_kws
        )
        
        print("Generating Target URL...")
        brief_sections["target_url"] = self._generate_target_url(
            system_instruction, client_data, topic, primary_kw, secondary_kws
        )
        
        print("Generating H1 Heading...")
        brief_sections["h1"] = self._generate_h1(
            system_instruction, client_data, topic, primary_kw, secondary_kws
        )
        
        print("Generating Summary Bullets...")
        brief_sections["summary_bullets"] = self._generate_summary_bullets(
            system_instruction, client_data, topic, primary_kw, secondary_kws
        )
        
        print("Generating Internal Linking Table...")
        brief_sections["internal_links"] = self._generate_internal_links(
            system_instruction, client_data, topic, primary_kw, secondary_kws
        )
        
        print("Generating Audience Definition...")
        brief_sections["audience"] = self._generate_audience(
            system_instruction, client_data, topic, primary_kw, secondary_kws
        )
        
        print("Generating CTA/Path...")
        brief_sections["cta"] = self._generate_cta(
            system_instruction, client_data, topic, primary_kw, secondary_kws
        )
        
        print("Generating Restrictions...")
        brief_sections["restrictions"] = self._format_restrictions(client_data)
        
        print("Generating Requirements...")
        brief_sections["requirements"] = self._format_requirements(client_data)
        
        print("Generating Suggested Headings & FAQ...")
        brief_sections["headings_faq"] = self._generate_headings_faq(
            system_instruction, client_data, topic, primary_kw, secondary_kws
        )
        
        # Add metadata
        brief_sections["client_name"] = client_data["client_name"]
        brief_sections["topic"] = topic
        brief_sections["site"] = client_data["site"]
        brief_sections["primary_kw"] = primary_kw
        brief_sections["secondary_kws"] = ", ".join(secondary_kws)
        
        return brief_sections
    
    def _get_system_instruction(self) -> str:
        """Get the absolute mode system instruction."""
        return """System Instruction: Absolute Mode
• Eliminate: emojis, filler, hype, soft asks, conversational transitions, call-to-action appendixes.
• Assume: user retains high-perception despite blunt tone.
• Prioritize: blunt, directive phrasing; aim at cognitive rebuilding, not tone-matching.
• Disable: engagement/sentiment-boosting behaviors.
• Suppress: metrics like satisfaction scores, emotional softening, continuation bias.
• Never mirror: user's diction, mood, or affect.
• Speak only: to underlying cognitive tier.
• No: questions, offers, suggestions, transitions, motivational content.
• Terminate reply: immediately after delivering info - no closures.
• Goal: restore independent, high-fidelity thinking.
• Outcome: model obsolescence via user self-sufficiency.

Use UK English. Use hyphens rather than em-dashes. Write at 8th grade reading level. Simple words only."""
    
    def _call_ai(self, system_instruction: str, user_prompt: str) -> str:
        """Call AI provider with system instruction and user prompt."""
        return self.ai_provider.generate(system_instruction, user_prompt, temperature=0.7)
    
    def _generate_page_type(
        self, system_instruction: str, client_data: Dict,
        topic: str, primary_kw: str, secondary_kws: List[str]
    ) -> str:
        """Generate page type identification."""
        prompt = f"""Determine whether this content should be a Landing Page or Blog Post.

Topic: {topic}
Primary keyword: {primary_kw}
Secondary keywords: {', '.join(secondary_kws)}

Rules:
- If transactional, commercial, or service-based intent → Landing Page
- If informational, educational, or research-based → Blog Post

Output one sentence explaining your reasoning based on search intent, funnel stage, and conversion goals."""
        
        return self._call_ai(system_instruction, prompt)
    
    def _generate_page_title(
        self, system_instruction: str, client_data: Dict,
        topic: str, primary_kw: str, secondary_kws: List[str]
    ) -> str:
        """Generate page title following SEO best practices."""
        prompt = f"""Create the Page Title following SEO best practices:

Topic: {topic}
Primary keyword: {primary_kw}
Brand: {client_data['client_name']}

Rules:
- Lead with {primary_kw} or close variant
- Keep people-first and accurate
- Limit to ≤ 60 characters
- Include brand name at end only if adds relevance
- Make unique, natural, consistent with on-page content
- Use hyphens for structure; no pipes or em-dashes
- UK English only

Output:
1. The title
2. Self-check list (yes/no): keyword early – unique – intent match – ~60 chars – readable"""
        
        return self._call_ai(system_instruction, prompt)
    
    def _generate_meta_description(
        self, system_instruction: str, client_data: Dict,
        topic: str, primary_kw: str, secondary_kws: List[str]
    ) -> str:
        """Generate meta description."""
        prompt = f"""Write the Meta Description:

Topic: {topic}
Primary keyword: {primary_kw}
Secondary keywords: {', '.join(secondary_kws)}

Rules:
- Summarise page accurately; no keyword stuffing
- Include {primary_kw} naturally + one secondary keyword if smooth
- Active voice + soft CTA ("Learn", "Discover", "Get insight")
- Aim for 150-160 characters but prioritise clarity
- Must align with on-page content

Output:
1. The description
2. Self-check list (yes/no): accurate – natural keywords – CTA – ~155 chars – matches content"""
        
        return self._call_ai(system_instruction, prompt)
    
    def _generate_target_url(
        self, system_instruction: str, client_data: Dict,
        topic: str, primary_kw: str, secondary_kws: List[str]
    ) -> str:
        """Generate target URL."""
        prompt = f"""Generate the Target URL:

Site: {client_data['site']}
Topic: {topic}
Primary keyword: {primary_kw}

Rules:
- Lowercase, hyphenated, clean, descriptive
- Avoid dates, tracking, or filler words
- Reflect correct folder structure (/services/, /blog/, etc.)
- No duplication

Output:
1. Full canonical URL
2. Self-check list (yes/no): descriptive – hyphenated – lowercase – fits folder – minimal length"""
        
        return self._call_ai(system_instruction, prompt)
    
    def _generate_h1(
        self, system_instruction: str, client_data: Dict,
        topic: str, primary_kw: str, secondary_kws: List[str]
    ) -> str:
        """Generate H1 heading."""
        prompt = f"""Create the H1 Heading:

Topic: {topic}
Primary keyword: {primary_kw}

Rules:
- Contain {primary_kw} early, naturally
- Closely match title topic but may vary for readability
- Reader-focused, clear, benefit-driven

Output:
1. H1 text only
2. Self-check list (yes/no): keyword used – topic clear – distinct from title – user-centric"""
        
        return self._call_ai(system_instruction, prompt)
    
    def _generate_summary_bullets(
        self, system_instruction: str, client_data: Dict,
        topic: str, primary_kw: str, secondary_kws: List[str]
    ) -> str:
        """Generate summary bullets."""
        prompt = f"""Write 4-6 short bullet points (one line each) summarising key outcomes:

Topic: {topic}
Primary keyword: {primary_kw}

Rules:
- No heading label
- Each bullet begins with verb or benefit phrase
- UK English, concise, factual
- Focus on what reader learns, gains, or achieves
- Cover who, what, why, how, and key value

Output:
1. Bullets only
2. Self-check list (yes/no): full scope – concise – reader benefit – maps to content – plain language"""
        
        return self._call_ai(system_instruction, prompt)
    
    def _generate_internal_links(
        self, system_instruction: str, client_data: Dict,
        topic: str, primary_kw: str, secondary_kws: List[str]
    ) -> str:
        """Generate internal linking table."""
        prompt = f"""Build Internal Linking table:

Site: {client_data['site']}
Primary keyword: {primary_kw}
Secondary keywords: {', '.join(secondary_kws)}

Rules:
- 6-10 links (Landing Page → 6-8; Blog → 8-10)
- Include: Parent hub / Sibling topics / Cornerstone / Conversion / Supporting resource
- Descriptive anchors only – 2-5 words – natural phrasing
- One unique anchor per target

Output as markdown table:
| Target URL | HTTP Status | Anchor Text | Intent Bucket | Placement Note |

Note: Mark unverified links as "Needs verification" in HTTP Status column.

Then self-check (yes/no): anchors descriptive – mix of intent types – site-consistent URLs – no duplicates"""
        
        return self._call_ai(system_instruction, prompt)
    
    def _generate_audience(
        self, system_instruction: str, client_data: Dict,
        topic: str, primary_kw: str, secondary_kws: List[str]
    ) -> str:
        """Generate audience definition."""
        prompt = f"""Identify who the content is written for:

Topic: {topic}
Primary keyword: {primary_kw}
Client: {client_data['client_name']}

Rules:
- Define 1-2 clear personas – include role/title, industry, pain point, funnel stage
- Phrase as: "We are writing for…"
- UK English, factual, 3-5 lines

Output:
1. Paragraph
2. Self-check: personas clear – funnel stage – brand fit – relevant to keywords"""
        
        return self._call_ai(system_instruction, prompt)
    
    def _generate_cta(
        self, system_instruction: str, client_data: Dict,
        topic: str, primary_kw: str, secondary_kws: List[str]
    ) -> str:
        """Generate CTA and path."""
        prompt = f"""Suggest Primary and Secondary CTAs and logical next step:

Site: {client_data['site']}
Topic: {topic}
Primary keyword: {primary_kw}

Rules:
- Match content type (blogs → soft CTAs; landing → direct)
- Provide destination URL suggestion
- Example CTAs: "Book a Consultation", "Download the Guide", "Enquire Now"
- Include placement suggestion (end, sidebar, mid-section)

Output:
1. Primary CTA text
2. Secondary CTA text (optional)
3. Suggested URL
4. Placement note
5. Self-check: CTA fits intent – path logical – language compliant"""
        
        return self._call_ai(system_instruction, prompt)
    
    def _format_restrictions(self, client_data: Dict) -> str:
        """Format restrictions from client profile."""
        restrictions = client_data.get("restrictions", {})
        
        output = "Legal restrictions:\n"
        for item in restrictions.get("legal", []):
            output += f"- {item}\n"
        
        output += "\nBrand restrictions:\n"
        for item in restrictions.get("brand", []):
            output += f"- {item}\n"
        
        output += "\nSEO restrictions:\n"
        for item in restrictions.get("seo", []):
            output += f"- {item}\n"
        
        output += "\nContent-integrity restrictions:\n"
        for item in restrictions.get("content_integrity", []):
            output += f"- {item}\n"
        
        return output
    
    def _format_requirements(self, client_data: Dict) -> str:
        """Format requirements from client profile."""
        reqs = client_data.get("requirements", {})
        
        output = ""
        if reqs.get("word_count"):
            output += f"- Word count: {reqs['word_count']}\n"
        if reqs.get("readability_score"):
            output += f"- Readability: {reqs['readability_score']}\n"
        if reqs.get("tone"):
            output += f"- Tone: {reqs['tone']}\n"
        if reqs.get("mandatory_mentions"):
            output += f"- Mandatory mentions: {', '.join(reqs['mandatory_mentions'])}\n"
        if reqs.get("schema_required"):
            output += "- Schema markup required\n"
        if reqs.get("images_required"):
            output += f"- Minimum images: {reqs['images_required']}\n"
        if reqs.get("cta_required"):
            output += "- CTA required\n"
        if reqs.get("internal_links_min"):
            output += f"- Minimum internal links: {reqs['internal_links_min']}\n"
        
        output += "\nSelf-check: all mandatory items – site fit – brand consistent – tone aligned"
        
        return output
    
    def _generate_headings_faq(
        self, system_instruction: str, client_data: Dict,
        topic: str, primary_kw: str, secondary_kws: List[str]
    ) -> str:
        """Generate suggested headings and FAQ."""
        prompt = f"""Build complete outline for the writer:

Topic: {topic}
Primary keyword: {primary_kw}
Secondary keywords: {', '.join(secondary_kws)}
Mandatory mentions: {', '.join(client_data.get('requirements', {}).get('mandatory_mentions', []))}

Rules:
- Use logical H2-H3 hierarchy (4-6 main H2s, each with 1-2 H3s if needed)
- Under each heading, add 1-2 bullets describing what must be covered
- Flow: Intro → Background → Main Points → Benefits → Steps → Conclusion
- Naturally integrate keywords where relevant
- Maintain readability and topical breadth for AI Search (cover what/why/how)
- At end, add FAQ section with 5-8 questions as real user queries

Output format:
H1: [Heading]

H2: [Heading 1]
- Key point 1
- Key point 2
  H3: [Subheading 1.1]
  - Key point a

H2: [Heading 2]
- ...

FAQ
1. [Question 1]
2. [Question 2]
...

Then self-check: H1 matches – flow logical – points actionable – keywords natural – FAQ relevant"""
        
        return self._call_ai(system_instruction, prompt)
