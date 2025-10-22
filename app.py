"""
Streamlit Web Application for Content Brief Creator
Hosted on GitHub and deployable to Streamlit Community Cloud
"""

import streamlit as st
import os
from dotenv import load_dotenv
from ai_provider import AIProvider
from brief_generator import BriefGenerator
from document_formatter import DocumentFormatter
from datetime import datetime
import io

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Content Brief Creator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'client_data' not in st.session_state:
        st.session_state.client_data = None
    if 'generated_brief' not in st.session_state:
        st.session_state.generated_brief = None
    if 'selected_provider' not in st.session_state:
        st.session_state.selected_provider = None

def display_header():
    """Display application header"""
    st.markdown('<p class="main-header">📝 Content Brief Creator</p>', unsafe_allow_html=True)
    st.markdown("Generate professional, AI-powered content briefs with customizable client profiles")
    st.markdown("---")

def sidebar_client_management():
    """Sidebar for client profile management"""
    st.sidebar.title("🏢 Client Profiles")
    
    # TODO: Will integrate with Supabase
    # For now, use session state
    
    tab1, tab2 = st.sidebar.tabs(["Load Client", "Create Client"])
    
    with tab1:
        st.info("Supabase integration coming soon!")
        # Temporary manual input
        if st.button("Use Demo Client"):
            st.session_state.client_data = {
                "name": "Demo Client",
                "industry": "Technology",
                "target_audience": "Tech professionals and enthusiasts",
                "brand_voice": "Professional yet approachable",
                "content_goals": "Educate and engage our audience",
                "website": "https://example.com"
            }
            st.success("Demo client loaded!")
    
    with tab2:
        st.subheader("Create New Client")
        with st.form("new_client_form"):
            client_name = st.text_input("Client Name*")
            industry = st.text_input("Industry*")
            target_audience = st.text_area("Target Audience*")
            brand_voice = st.text_area("Brand Voice & Tone*")
            content_goals = st.text_area("Content Goals*")
            website = st.text_input("Website URL")
            
            submitted = st.form_submit_button("Save Client")
            if submitted:
                if client_name and industry and target_audience and brand_voice and content_goals:
                    st.session_state.client_data = {
                        "name": client_name,
                        "industry": industry,
                        "target_audience": target_audience,
                        "brand_voice": brand_voice,
                        "content_goals": content_goals,
                        "website": website
                    }
                    st.success(f"✅ Client '{client_name}' created!")
                else:
                    st.error("Please fill in all required fields")

def main_content():
    """Main content area for brief generation"""
    
    # Check if client is selected
    if st.session_state.client_data is None:
        st.warning("⚠️ Please load or create a client profile from the sidebar first")
        return
    
    # Display current client
    st.success(f"**Current Client:** {st.session_state.client_data['name']}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Brief Details")
        
        # Brief input form
        with st.form("brief_form"):
            topic = st.text_input(
                "Content Topic*",
                placeholder="e.g., The Future of Artificial Intelligence"
            )
            
            primary_kw = st.text_input(
                "Primary Keyword*",
                placeholder="e.g., artificial intelligence"
            )
            
            secondary_kws_input = st.text_area(
                "Secondary Keywords (comma-separated)*",
                placeholder="e.g., machine learning, AI ethics, automation"
            )
            
            # AI Provider selection
            available_providers = AIProvider.list_available_providers()
            
            if not available_providers:
                st.error("❌ No AI provider API keys found. Please configure at least one provider in your secrets.")
                return
            
            provider = st.selectbox(
                "AI Provider*",
                options=available_providers,
                format_func=lambda x: {
                    'openai': '🤖 OpenAI GPT-4o',
                    'claude': '🧠 Claude 3.5 Sonnet',
                    'perplexity': '🔍 Perplexity Sonar',
                    'mistral': '⚡ Mistral Large'
                }.get(x, x.upper())
            )
            
            submitted = st.form_submit_button("🚀 Generate Brief", type="primary")
            
            if submitted:
                if topic and primary_kw and secondary_kws_input:
                    # Parse secondary keywords
                    secondary_kws = [kw.strip() for kw in secondary_kws_input.split(',') if kw.strip()]
                    
                    with st.spinner(f'Generating content brief with {provider.upper()}...'):
                        try:
                            # Initialize brief generator
                            brief_generator = BriefGenerator(provider=provider)
                            
                            # Generate brief
                            brief_data = brief_generator.generate_brief(
                                client_data=st.session_state.client_data,
                                topic=topic,
                                primary_kw=primary_kw,
                                secondary_kws=secondary_kws
                            )
                            
                            st.session_state.generated_brief = brief_data
                            st.session_state.selected_provider = provider
                            st.success("✅ Brief generated successfully!")
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Error generating brief: {str(e)}")
                else:
                    st.error("Please fill in all required fields")
    
    with col2:
        st.subheader("ℹ️ Tips")
        st.info("""
        **Topic**: Clear, specific title for your content
        
        **Primary Keyword**: Main SEO target
        
        **Secondary Keywords**: Related terms to include (2-5 recommended)
        
        **AI Providers**:
        - GPT-4o: Best all-rounder
        - Claude: Great for long-form
        - Perplexity: Research-focused
        - Mistral: Fast & efficient
        """)

def display_generated_brief():
    """Display the generated brief"""
    if st.session_state.generated_brief:
        st.markdown("---")
        st.subheader("📄 Generated Content Brief")
        
        brief = st.session_state.generated_brief
        
        # Display brief sections
        col1, col2 = st.columns([3, 1])
        
        with col1:
            with st.expander("📌 Brief Overview", expanded=True):
                st.markdown(f"**Topic:** {brief.get('topic', 'N/A')}")
                st.markdown(f"**Primary Keyword:** {brief.get('primary_keyword', 'N/A')}")
                st.markdown(f"**Secondary Keywords:** {', '.join(brief.get('secondary_keywords', []))}")
                st.markdown(f"**Generated with:** {st.session_state.selected_provider.upper()}")
            
            with st.expander("🎯 Target Audience", expanded=True):
                st.markdown(brief.get('target_audience', 'N/A'))
            
            with st.expander("📝 Content Outline", expanded=True):
                st.markdown(brief.get('outline', 'N/A'))
            
            with st.expander("🔑 Key Points", expanded=True):
                st.markdown(brief.get('key_points', 'N/A'))
            
            with st.expander("💡 Content Recommendations", expanded=True):
                st.markdown(brief.get('recommendations', 'N/A'))
            
            with st.expander("🎨 Tone & Style", expanded=True):
                st.markdown(brief.get('tone_style', 'N/A'))
        
        with col2:
            st.markdown("### 💾 Export")
            
            # Generate Word document
            if st.button("📄 Download as Word Doc", type="primary"):
                try:
                    formatter = DocumentFormatter()
                    
                    # Create document in memory
                    doc = formatter.create_document(
                        client_name=st.session_state.client_data['name'],
                        brief_data=brief
                    )
                    
                    # Save to BytesIO
                    doc_bytes = io.BytesIO()
                    doc.save(doc_bytes)
                    doc_bytes.seek(0)
                    
                    # Create filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"brief_{brief.get('topic', 'untitled').replace(' ', '_')}_{timestamp}.docx"
                    
                    # Download button
                    st.download_button(
                        label="⬇️ Click to Download",
                        data=doc_bytes,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                    
                except Exception as e:
                    st.error(f"Error creating document: {str(e)}")
            
            if st.button("🔄 Generate New Brief"):
                st.session_state.generated_brief = None
                st.rerun()

def main():
    """Main application function"""
    init_session_state()
    display_header()
    sidebar_client_management()
    main_content()
    display_generated_brief()

if __name__ == "__main__":
    main()
