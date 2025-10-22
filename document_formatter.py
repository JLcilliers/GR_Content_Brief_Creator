"""
Document Formatter
Creates formatted Word documents from content brief data.
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from typing import Dict
import os
from datetime import datetime


class DocumentFormatter:
    """Formats content briefs into Word documents with consistent styling."""
    
    def __init__(self):
        self.font_name = "Poppins"
        self.body_size = 12
        self.heading_size = 14
    
    def create_brief_document(self, brief_data: Dict, output_dir: str = "output_briefs") -> str:
        """Create a formatted Word document from brief data."""
        
        doc = Document()
        
        # Set default font for the document
        style = doc.styles['Normal']
        font = style.font
        font.name = self.font_name
        font.size = Pt(self.body_size)
        
        # Header
        self._add_header(doc, brief_data)
        
        # Add each section
        self._add_section(doc, "1. Page Type Identification", brief_data.get("page_type", ""))
        self._add_section(doc, "2. Page Title", brief_data.get("page_title", ""))
        self._add_section(doc, "3. Meta Description", brief_data.get("meta_description", ""))
        self._add_section(doc, "4. Target URL", brief_data.get("target_url", ""))
        self._add_section(doc, "5. H1 Heading", brief_data.get("h1", ""))
        self._add_section(doc, "6. Summary Bullets", brief_data.get("summary_bullets", ""))
        self._add_section(doc, "7. Internal Linking", brief_data.get("internal_links", ""))
        self._add_section(doc, "8. Audience Definition", brief_data.get("audience", ""))
        self._add_section(doc, "9. CTA / Path", brief_data.get("cta", ""))
        self._add_section(doc, "10. Restrictions", brief_data.get("restrictions", ""))
        self._add_section(doc, "11. Requirements", brief_data.get("requirements", ""))
        self._add_section(doc, "12. Suggested Headings & Key Points (+ FAQ)", brief_data.get("headings_faq", ""))
        
        # Save the document
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        client_name = brief_data.get("client_name", "Client").replace(" ", "_")
        topic = brief_data.get("topic", "Topic").replace(" ", "_")[:30]  # Limit length
        
        filename = f"{client_name}_{topic}_{timestamp}.docx"
        filepath = os.path.join(output_dir, filename)
        
        doc.save(filepath)
        
        return filepath
    
    def _add_header(self, doc: Document, brief_data: Dict):
        """Add the header section with client name, topic, site, and keywords."""
        
        # Main title
        title = f"{brief_data.get('client_name', '')} - {brief_data.get('topic', '')} - Content Brief"
        p = doc.add_paragraph(title)
        p.runs[0].font.size = Pt(16)
        p.runs[0].font.bold = True
        p.runs[0].font.name = self.font_name
        p.runs[0].font.color.rgb = RGBColor(0, 51, 102)  # Dark blue
        p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        
        # Site
        p = doc.add_paragraph(f"Site: {brief_data.get('site', '')}")
        p.runs[0].font.name = self.font_name
        p.runs[0].font.size = Pt(self.body_size)
        
        # Primary keyword
        p = doc.add_paragraph(f"Primary keyword: {brief_data.get('primary_kw', '')}")
        p.runs[0].font.name = self.font_name
        p.runs[0].font.size = Pt(self.body_size)
        
        # Secondary keywords
        p = doc.add_paragraph(f"Secondary keywords: {brief_data.get('secondary_kws', '')}")
        p.runs[0].font.name = self.font_name
        p.runs[0].font.size = Pt(self.body_size)
        
        # Add spacing
        doc.add_paragraph()
    
    def _add_section(self, doc: Document, section_title: str, content: str):
        """Add a section with heading and content."""
        
        # Section heading
        p = doc.add_paragraph(section_title)
        p.runs[0].font.size = Pt(self.heading_size)
        p.runs[0].font.bold = True
        p.runs[0].font.name = self.font_name
        p.runs[0].font.color.rgb = RGBColor(51, 102, 153)  # Medium blue
        
        # Content
        # Split content into paragraphs and preserve formatting
        content_lines = content.split('\n')
        for line in content_lines:
            if line.strip():  # Skip empty lines
                p = doc.add_paragraph(line)
                p.runs[0].font.name = self.font_name
                p.runs[0].font.size = Pt(self.body_size)
            else:
                doc.add_paragraph()  # Add blank line
        
        # Add spacing after section
        doc.add_paragraph()
    
    def set_font(self, font_name: str):
        """Change the font name."""
        self.font_name = font_name
    
    def set_body_size(self, size: int):
        """Change the body font size."""
        self.body_size = size
    
    def set_heading_size(self, size: int):
        """Change the heading font size."""
        self.heading_size = size
