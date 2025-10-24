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
from supabase_client_manager import SupabaseClientManager
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
    if 'client_manager' not in st.session_state:
        try:
            st.session_state.client_manager = SupabaseClientManager()
        except Exception as e:
            st.session_state.client_manager = None
            st.sidebar.error(f"⚠️ Supabase connection error: {str(e)}")

def display_header():
    """Display application header"""
    st.markdown('<p class="main-header">📝 Content Brief Creator</p>', unsafe_allow_html=True)
    st.markdown("Generate professional, AI-powered content briefs with customizable client profiles")
    st.markdown("---")

def sidebar_client_management():
    """Sidebar for client profile management"""
    st.sidebar.title("🏢 Client Profiles")
    
    # Check if Supabase is connected
    if st.session_state.client_manager is None:
        st.sidebar.error("❌ Supabase not connected. Check your SUPABASE_URL and SUPABASE_KEY in .env file.")
        return
    
    tab1, tab2 = st.sidebar.tabs(["Load Client", "Create Client"])
    
    with tab1:
        st.subheader("Load Existing Client")
        
        # Get list of clients from Supabase
        try:
            client_list = st.session_state.client_manager.list_clients()
            
            if client_list:
                selected_client = st.selectbox(
                    "Select a client:",
                    options=client_list,
                    key="client_selector"
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📂 Load Client", use_container_width=True):
                        client_data = st.session_state.client_manager.get_client(selected_client)
                        if client_data:
                            st.session_state.client_data = client_data
                            st.success(f"✅ Loaded: {selected_client}")
                            st.rerun()
                        else:
                            st.error("Failed to load client")
                
                with col2:
                    if st.button("🗑️ Delete", use_container_width=True):
                        if st.session_state.client_manager.delete_client(selected_client):
                            st.success(f"Deleted: {selected_client}")
                            if st.session_state.client_data and st.session_state.client_data.get('client_name') == selected_client:
                                st.session_state.client_data = None
                            st.rerun()
                        else:
                            st.error("Failed to delete client")
            else:
                st.info("📭 No clients found. Create one in the 'Create Client' tab.")
                
        except Exception as e:
            st.error(f"Error loading clients: {str(e)}")
    
    with tab2:
        st.subheader("Create New Client")
        with st.form("new_client_form"):
            client_name = st.text_input("Client Name*")
            industry = st.text_input("Industry*")
            target_audience = st.text_area("Target Audience*")
            brand_voice = st.text_area("Brand Voice & Tone*")
            content_goals = st.text_area("Content Goals*")
            website = st.text_input("Website URL")
            
            # Content restrictions and requirements
            st.markdown("### Content Guidelines")
            things_to_avoid = st.text_area(
                "❌ Things to Avoid",
                placeholder="Topics, keywords, or content types to avoid (one per line)",
                help="Enter content restrictions, sensitive topics, or keywords to avoid"
            )
            things_must_include = st.text_area(
                "✅ Things Must Include",
                placeholder="Required elements, topics, or keywords (one per line)",
                help="Enter mandatory mentions, required topics, or must-have elements"
            )
            
            submitted = st.form_submit_button("💾 Save Client")
            if submitted:
                if client_name and industry and target_audience and brand_voice and content_goals:
                    # Check if client already exists
                    if st.session_state.client_manager.client_exists(client_name):
                        st.error(f"❌ Client '{client_name}' already exists!")
                    else:
                        # Process things to avoid and must include
                        avoid_list = [item.strip() for item in things_to_avoid.split('\n') if item.strip()] if things_to_avoid else []
                        must_include_list = [item.strip() for item in things_must_include.split('\n') if item.strip()] if things_must_include else []
                        
                        # Create client data
                        client_data = {
                            "client_name": client_name,
                            "site": website if website else "",
                            "industry": industry,
                            "target_audience": target_audience,
                            "brand_voice": brand_voice,
                            "content_goals": content_goals,
                            "restrictions": {
                                "legal": [],
                                "brand": avoid_list,
                                "seo": [],
                                "content_integrity": []
                            },
                            "requirements": {
                                "word_count": None,
                                "tone": brand_voice,
                                "mandatory_mentions": must_include_list,
                                "readability_score": "",
                                "schema_required": False,
                                "images_required": 0,
                                "cta_required": True,
                                "internal_links_min": 6
                            }
                        }
                        
                        # Save to Supabase
                        try:
                            if st.session_state.client_manager.create_client(client_name, client_data):
                                st.session_state.client_data = client_data
                                st.success(f"✅ Client '{client_name}' created and saved to Supabase!")
                                st.rerun()
                            else:
                                st.error("Failed to save client to database")
                        except Exception as e:
                            st.error(f"Error saving client: {str(e)}")
                else:
                    st.error("⚠️ Please fill in all required fields")

def main_content():
    """Main content area for brief generation"""
    
    # Check if client is selected
    if st.session_state.client_data is None:
        st.warning("⚠️ Please load or create a client profile from the sidebar first")
        return
    
    # Display current client
    st.success(f"**Current Client:** {st.session_state.client_data['client_name']}")
    
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
                    'grok': '✨ Grok (xAI)',
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
        - Grok: Real-time insights
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
                st.markdown(f"**Client:** {brief.get('client_name', 'N/A')}")
                st.markdown(f"**Site:** {brief.get('site', 'N/A')}")
                st.markdown(f"**Topic:** {brief.get('topic', 'N/A')}")
                st.markdown(f"**Primary Keyword:** {brief.get('primary_kw', 'N/A')}")
                st.markdown(f"**Secondary Keywords:** {brief.get('secondary_kws', 'N/A')}")
                st.markdown(f"**Generated with:** {st.session_state.selected_provider.upper()}")
            
            with st.expander("📍 Page Type", expanded=False):
                st.markdown(brief.get('page_type', 'N/A'))
            
            with st.expander("📄 Page Title", expanded=False):
                st.markdown(brief.get('page_title', 'N/A'))
            
            with st.expander("📝 Meta Description", expanded=False):
                st.markdown(brief.get('meta_description', 'N/A'))
            
            with st.expander("🔗 Target URL", expanded=False):
                st.markdown(brief.get('target_url', 'N/A'))
            
            with st.expander("🎯 H1 Heading", expanded=False):
                st.markdown(brief.get('h1', 'N/A'))
            
            with st.expander("📋 Summary Bullets", expanded=False):
                st.markdown(brief.get('summary_bullets', 'N/A'))
            
            with st.expander("🔗 Internal Links", expanded=False):
                st.markdown(brief.get('internal_links', 'N/A'))
            
            with st.expander("👥 Audience", expanded=False):
                st.markdown(brief.get('audience', 'N/A'))
            
            with st.expander("📣 CTA / Path", expanded=False):
                st.markdown(brief.get('cta', 'N/A'))
            
            with st.expander("🚫 Restrictions", expanded=False):
                st.markdown(brief.get('restrictions', 'N/A'))
            
            with st.expander("✅ Requirements", expanded=False):
                st.markdown(brief.get('requirements', 'N/A'))
            
            with st.expander("📑 Headings & FAQ", expanded=False):
                st.markdown(brief.get('headings_faq', 'N/A'))
        
        with col2:
            st.markdown("### 💾 Export")
            
            # Generate Word document
            if st.button("📄 Download as Word Doc", type="primary"):
                try:
                    formatter = DocumentFormatter()
                    
                    # Create document and save to temp file
                    doc_path = formatter.create_brief_document(
                        brief_data=brief,
                        output_dir="temp_output"
                    )
                    
                    # Read the saved document into memory
                    with open(doc_path, 'rb') as f:
                        doc_bytes_data = f.read()
                    
                    # Clean up temp file and directory
                    import os
                    import shutil
                    os.remove(doc_path)
                    if os.path.exists("temp_output") and not os.listdir("temp_output"):
                        shutil.rmtree("temp_output")
                    
                    # Create BytesIO object for download
                    doc_bytes = io.BytesIO(doc_bytes_data)
                    
                    # Create filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    client_name = brief.get('client_name', 'Client').replace(' ', '_')
                    topic = brief.get('topic', 'untitled').replace(' ', '_')[:30]
                    filename = f"{client_name}_{topic}_{timestamp}.docx"
                    
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
