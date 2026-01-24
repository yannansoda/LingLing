import streamlit as st
import requests
import json
from typing import List, Dict
import os

# Page configuration
st.set_page_config(
    page_title="LingLing — for Language Learning",
    page_icon="🔔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize dark mode in session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

def get_css(dark_mode):
    """Generate CSS based on dark mode setting"""
    if dark_mode:
        # Dark mode colors
        bg_color = "#0e1117"
        text_color = "#fafafa"
        card_bg = "#1e1e1e"
        border_color = "#3d3d3d"
        input_bg = "#262730"
        input_text = "#fafafa"
        header_text = "#fafafa"
        translation_bg = "#2a2a2a"
        sidebar_bg = "#1e1e1e"
    else:
        # Light mode colors
        bg_color = "#ffffff"
        text_color = "#37352f"
        card_bg = "#f7f6f3"
        border_color = "#e9e9e7"
        input_bg = "#ffffff"
        input_text = "#37352f"
        header_text = "#37352f"
        translation_bg = "#f7f6f3"
        sidebar_bg = "#ffffff"
    
    return f"""
    <style>
    /* Main page background */
    .stApp {{
        background-color: {bg_color} !important;
    }}
    
    .main .block-container {{
        background-color: {bg_color};
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}
    
    /* All text elements */
    p, div, span, label, .stCaption {{
        color: {text_color};
    }}
    
    /* Captions */
    .stCaption {{
        color: {text_color} !important;
    }}
    
    /* Cleaner headers */
    h1 {{
        color: {header_text};
        font-weight: 600;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }}
    
    h2 {{
        color: {header_text};
        font-weight: 600;
        font-size: 1.75rem;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }}
    
    h3 {{
        color: {header_text};
        font-weight: 600;
        font-size: 1.25rem;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }}
    
    h4 {{
        color: {header_text};
    }}
    
    h5 {{
        color: {header_text};
    }}
    
    h6 {{
        color: {header_text};
    }}
    
    /* Large translation text */
    .translation-text {{
        font-size: 1.5rem;
        line-height: 1.8;
        color: {text_color};
        font-weight: 400;
        padding: 1.5rem;
        background-color: {translation_bg};
        border-radius: 8px;
        border-left: 3px solid {text_color};
        margin: 1rem 0;
    }}
    
    /* Modern input styling - FIX TEXT VISIBILITY */
    .stTextInput > div > div > input {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
        border: 1px solid {border_color};
        border-radius: 4px;
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: {input_text}80 !important;
    }}
    
    .stTextArea > div > div > textarea {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
        border: 1px solid {border_color};
        border-radius: 4px;
    }}
    
    .stTextArea > div > div > textarea::placeholder {{
        color: {input_text}80 !important;
    }}
    
    /* Select box styling */
    .stSelectbox > div > div > select {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
    }}
    
    /* Multi-select styling */
    [data-baseweb="select"] {{
        background-color: {input_bg} !important;
    }}
    
    [data-baseweb="select"] input {{
        color: {input_text} !important;
        background-color: {input_bg} !important;
    }}
    
    /* Multi-select dropdown tags/chips */
    [data-baseweb="tag"] {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
    }}
    
    /* Multi-select container */
    div[data-baseweb="select"] > div {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
    }}
    
    /* Multi-select placeholder and selected items text */
    [data-baseweb="select"] [role="combobox"],
    [data-baseweb="select"] [aria-label] {{
        color: {input_text} !important;
    }}
    
    /* Streamlit multiselect specific styling */
    .stMultiSelect > div > div {{
        background-color: {input_bg} !important;
    }}
    
    .stMultiSelect label {{
        color: {text_color} !important;
    }}
    
    /* Multiselect selected tags background */
    [data-baseweb="select"] [data-tag] {{
        background-color: {translation_bg} !important;
        color: {text_color} !important;
    }}
    
    /* Dropdown options menu/popup - the list that appears when clicking */
    [data-baseweb="popover"] {{
        background-color: {input_bg} !important;
    }}
    
    [data-baseweb="menu"] {{
        background-color: {input_bg} !important;
    }}
    
    /* Dropdown options list */
    ul[role="listbox"],
    [role="listbox"] {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
    }}
    
    /* Individual dropdown option items */
    li[role="option"],
    [role="option"] {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
    }}
    
    /* Hover state for dropdown options */
    li[role="option"]:hover,
    [role="option"]:hover {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
    }}
    
    /* Selected option in dropdown */
    li[role="option"][aria-selected="true"],
    [role="option"][aria-selected="true"] {{
        background-color: {translation_bg} !important;
        color: {text_color} !important;
    }}
    
    /* BaseWeb select dropdown menu items */
    [data-baseweb="menu"] ul,
    [data-baseweb="menu"] li {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
    }}
    
    /* Streamlit multiselect dropdown popup */
    [data-baseweb="popover"] [data-baseweb="menu"],
    [data-baseweb="popover"] [data-baseweb="menu"] ul {{
        background-color: {input_bg} !important;
    }}
    
    [data-baseweb="popover"] [data-baseweb="menu"] li {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
    }}
    
    [data-baseweb="popover"] [data-baseweb="menu"] li:hover {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
    }}
    
    /* Button styling - use gradient purple for both modes, but lighter in light mode */
    .stButton > button {{
        background-color: {("#667eea" if not dark_mode else "#667eea")} !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 4px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: background-color 0.2s;
    }}
    
    .stButton > button:hover {{
        background-color: #5568d3 !important;
        opacity: 0.9;
    }}
    
    /* CEFR level cards */
    .cefr-card {{
        text-align: center;
        padding: 0.5rem 0.75rem;
        border-radius: 5px;
        margin: 0.15rem;
        transition: transform 0.2s;
    }}
    
    .cefr-card:hover {{
        transform: translateY(-2px);
    }}
    
    /* Cleaner info boxes */
    .stAlert {{
        border-radius: 6px;
        border-left-width: 3px;
    }}
    
    /* Sidebar styling - ensure it's visible and text is readable */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
    }}
    
    /* Sidebar text colors */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] h5,
    [data-testid="stSidebar"] h6 {{
        color: {text_color} !important;
    }}
    
    /* Sidebar markdown content */
    [data-testid="stSidebar"] .stMarkdown {{
        color: {text_color} !important;
    }}
    
    /* Sidebar button text */
    [data-testid="stSidebar"] button {{
        color: {text_color if dark_mode else "#37352f"} !important;
    }}
    
    /* Sidebar toggle button text */
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] {{
        color: {text_color} !important;
    }}
    
    /* Sidebar input text */
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea {{
        color: {text_color} !important;
    }}
    
    /* Sidebar success/warning/info box text */
    [data-testid="stSidebar"] .stSuccess,
    [data-testid="stSidebar"] .stWarning,
    [data-testid="stSidebar"] .stInfo {{
        color: {text_color} !important;
    }}
    
    /* Sidebar code/pre text */
    [data-testid="stSidebar"] code,
    [data-testid="stSidebar"] pre {{
        color: {text_color} !important;
        background-color: {card_bg} !important;
    }}
    
    /* Streamlit header bar styling - fix the top rectangle */
    header[data-testid="stHeader"] {{
        background-color: {bg_color} !important;
        border-bottom: 1px solid {border_color} !important;
    }}
    
    header[data-testid="stHeader"] > div {{
        background-color: {bg_color} !important;
    }}
    
    /* Toolbar/header elements */
    .stToolbar {{
        background-color: {bg_color} !important;
    }}
    
    /* Any black rectangles or bars at top */
    div[data-testid="stToolbar"] {{
        background-color: {bg_color} !important;
    }}
    
    /* Main container background */
    section[data-testid="stMain"] {{
        background-color: {bg_color} !important;
    }}
    
    /* Toggle switch styling */
    .stToggle {{
        color: {text_color} !important;
    }}
    
    .stToggle label {{
        color: {text_color} !important;
    }}
    
    /* Success/Warning/Info/Error boxes */
    .stSuccess {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
    }}
    
    .stWarning {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
    }}
    
    .stInfo {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
    }}
    
    .stError {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
    }}
    
    /* Hide Streamlit menu and footer */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    /* Keep header visible - don't hide it so sidebar toggle button is accessible */
    /* header {{visibility: hidden;}} */
    </style>
    """

# Apply CSS based on dark mode setting
st.markdown(get_css(st.session_state.dark_mode), unsafe_allow_html=True)

# Available languages with their codes for DeepL API
LANGUAGES = {
    "English": "EN",
    "German": "DE",
    "Swedish": "SV",
    "French": "FR",
    "Spanish": "ES",
    "Italian": "IT",
    "Portuguese": "PT",
    "Russian": "RU",
    "Japanese": "JA",
    "Chinese": "ZH",
    "Dutch": "NL",
    "Polish": "PL",
    "Turkish": "TR",
    "Greek": "EL",
    "Czech": "CS",
    "Danish": "DA",
    "Finnish": "FI",
    "Norwegian": "NO",
    "Korean": "KO",
    "Arabic": "AR",
}

def get_deepl_translation(text: str, target_lang: str, api_key: str) -> str:
    """
    Translate text using DeepL Free API.
    To use: Sign up at https://www.deepl.com/pro-api?cta=header-pro-api
    Get your free API key and set it as an environment variable or in Streamlit secrets.
    Free tier: 500,000 characters/month
    """
    if not api_key or not api_key.strip():
        return "Error: API key is missing or empty"
    
    try:
        url = "https://api-free.deepl.com/v2/translate"
        headers = {
            "Authorization": f"DeepL-Auth-Key {api_key.strip()}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "text": text,
            "target_lang": target_lang
        }
        response = requests.post(url, headers=headers, data=data, timeout=10)
        
        # Check for errors before parsing JSON
        if response.status_code != 200:
            error_detail = response.text
            try:
                error_json = response.json()
                error_message = error_json.get("message", error_detail)
            except:
                error_message = error_detail
            raise Exception(f"API Error ({response.status_code}): {error_message}")
        
        result = response.json()
        if "translations" not in result or len(result["translations"]) == 0:
            raise Exception("No translations returned from API")
        
        return result["translations"][0]["text"]
    except requests.exceptions.RequestException as e:
        return f"Network error: {str(e)}"
    except Exception as e:
        return f"Translation error: {str(e)}"

def analyze_cefr_level(text: str, target_lang: str) -> Dict:
    """
    Analyze CEFR level distribution using heuristic approach.
    This is a simplified version. For production, consider using:
    - HuggingFace models (https://huggingface.co/models?search=cefr)
    - Local LLMs via Ollama
    - Custom NLP models
    
    Returns a dictionary with CEFR level distribution.
    """
    # Simple heuristic: word count, sentence complexity
    word_count = len(text.split())
    sentences = text.split('.')
    sentence_count = len([s for s in sentences if s.strip()])
    avg_words_per_sentence = word_count / max(sentence_count, 1)
    
    # Simple scoring (can be enhanced with actual NLP analysis)
    scores = {
        "A1": 0.0,
        "A2": 0.0,
        "B1": 0.0,
        "B2": 0.0,
        "C1": 0.0,
        "C2": 0.0
    }
    
    # Heuristic rules (these are simplified - real analysis would use NLP models)
    if word_count <= 5 and sentence_count <= 1:
        scores["A1"] = 0.7
        scores["A2"] = 0.3
    elif word_count <= 10 and avg_words_per_sentence <= 8:
        scores["A1"] = 0.2
        scores["A2"] = 0.5
        scores["B1"] = 0.3
    elif word_count <= 20 and avg_words_per_sentence <= 15:
        scores["A2"] = 0.2
        scores["B1"] = 0.4
        scores["B2"] = 0.3
        scores["C1"] = 0.1
    elif word_count <= 30:
        scores["B1"] = 0.2
        scores["B2"] = 0.4
        scores["C1"] = 0.3
        scores["C2"] = 0.1
    else:
        scores["B2"] = 0.2
        scores["C1"] = 0.4
        scores["C2"] = 0.4
    
    # Normalize to percentages
    total = sum(scores.values())
    if total > 0:
        scores = {k: round(v / total * 100, 1) for k, v in scores.items()}
    
    return scores

def get_difficulty_points(text: str, translation: str, target_lang: str) -> Dict[str, List[str]]:
    """
    Identify key difficulty points for learners.
    This is a simplified version. For production, consider using:
    - Grammar analysis tools
    - Word order detection
    - Vocabulary difficulty analysis
    
    Returns a dictionary with difficulty categories.
    """
    difficulties = {
        "vocabulary": [],
        "grammar": [],
        "sentence_structure": [],
        "word_order": []
    }
    
    # Simple heuristics (can be enhanced with actual NLP)
    word_count = len(text.split())
    
    # Vocabulary difficulty
    if word_count > 15:
        difficulties["vocabulary"].append(f"Contains {word_count} words - may include advanced vocabulary")
    if any(char in text for char in "äöüß"):
        difficulties["vocabulary"].append("Contains special characters that may be unfamiliar")
    
    # Grammar difficulty
    if "," in text:
        difficulties["grammar"].append("Contains clauses that may require understanding of conjunctions")
    if "?" in text or "!" in text:
        difficulties["grammar"].append("Sentence type variation (question/exclamation)")
    
    # Sentence structure
    if word_count > 10:
        difficulties["sentence_structure"].append("Longer sentence structure requires understanding of multiple clauses")
    if len(text.split('.')) > 1:
        difficulties["sentence_structure"].append("Complex sentence with multiple parts")
    
    # Word order (language-specific)
    if target_lang == "DE":  # German
        if any(word in text.lower() for word in ["der", "die", "das", "den", "dem", "des"]):
            difficulties["word_order"].append("German case system (Nominative, Accusative, Dative, Genitive)")
        if text.split()[0].lower() not in ["ich", "du", "er", "sie", "es", "wir", "ihr"]:
            difficulties["word_order"].append("Verb-second (V2) word order - verb comes second")
    elif target_lang == "SV":  # Swedish
        difficulties["word_order"].append("Verb-second word order (similar to German)")
    elif target_lang == "FR":  # French
        if "ne" in text.lower() or "pas" in text.lower():
            difficulties["word_order"].append("French negation requires 'ne...pas' around the verb")
        difficulties["word_order"].append("Adjective placement (usually after noun)")
    
    # Default messages if no specific issues found
    if not any(difficulties.values()):
        difficulties["vocabulary"].append("Beginner-friendly vocabulary level")
        difficulties["grammar"].append("Basic grammatical structures")
        difficulties["sentence_structure"].append("Simple sentence structure")
        difficulties["word_order"].append("Standard word order for this language")
    
    return difficulties

def get_cefr_explanation(level: str) -> str:
    """Get brief explanation of CEFR level."""
    explanations = {
        "A1": "Beginner - Can understand and use familiar everyday expressions",
        "A2": "Elementary - Can communicate in simple and routine tasks",
        "B1": "Intermediate - Can understand the main points of clear standard input",
        "B2": "Upper Intermediate - Can understand the main ideas of complex text",
        "C1": "Advanced - Can understand a wide range of demanding texts",
        "C2": "Proficient - Can understand with ease virtually everything"
    }
    return explanations.get(level, "Unknown level")

def main():
    # Initialize session state for API key
    if 'api_key' not in st.session_state:
        st.session_state.api_key = None
    
    # Sidebar - always show, even before API key is set
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # Dark mode toggle (always available)
        dark_mode = st.toggle(
            "🌙 Dark Mode",
            value=st.session_state.dark_mode,
            key="dark_mode_toggle"
        )
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.rerun()
        
        st.markdown("---")
        
        # API Key section - show different content based on whether key is set
        st.markdown("#### 🔑 API Key")
        
        # Check for API key in environment or secrets first
        if not st.session_state.api_key:
            env_api_key = os.getenv("DEEPL_API_KEY")
            if env_api_key:
                st.session_state.api_key = env_api_key
            else:
                # Try to get from secrets, but don't fail if secrets file doesn't exist
                try:
                    if hasattr(st, "secrets") and "DEEPL_API_KEY" in st.secrets:
                        st.session_state.api_key = st.secrets["DEEPL_API_KEY"]
                except Exception:
                    # Secrets file doesn't exist or other error - that's fine, user will input it
                    pass
        
        # Show API key status or input
        if st.session_state.api_key:
            masked_key = st.session_state.api_key[:4] + "..." + st.session_state.api_key[-4:] if len(st.session_state.api_key) > 8 else "***"
            st.success(f"✅ Configured\n`{masked_key}`")
            if st.button("Change API Key", key="change_api_key"):
                st.session_state.api_key = None
                st.rerun()
        else:
            st.warning("⚠️ API key not configured")
        
        st.markdown("---")
        st.markdown("### 📚 How to use")
        st.markdown("""
        1. Enter a sentence in any language
        2. Select one or more target languages
        3. Click 'Translate and Analyze'
        4. Explore translations and CEFR levels
        """)
    
    # Check for API key in environment or secrets first (if not already checked)
    if not st.session_state.api_key:
        env_api_key = os.getenv("DEEPL_API_KEY")
        if env_api_key:
            st.session_state.api_key = env_api_key
        else:
            # Try to get from secrets, but don't fail if secrets file doesn't exist
            try:
                if hasattr(st, "secrets") and "DEEPL_API_KEY" in st.secrets:
                    st.session_state.api_key = st.secrets["DEEPL_API_KEY"]
            except Exception:
                # Secrets file doesn't exist or other error - that's fine, user will input it
                pass
    
    # Show API key modal if not configured
    if not st.session_state.api_key:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 3rem; border-radius: 12px; margin-bottom: 2rem;">
            <h1 style="color: white; margin-bottom: 0.5rem;"> LingLing — for Language Learning</h1>
            <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem;">🔔 Translate Once, Learn Across Languages</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # API Key Input Modal
        with st.container():
            st.markdown("### 🔑 API Key Required")
            st.markdown("To get started, please enter your DeepL API key. Your key will not be stored or shared with anyone.")
            st.markdown("")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                api_key_input = st.text_input(
                    "DeepL API Key",
                    type="password",
                    help="Get a free API key at https://www.deepl.com/pro-api?cta=header-pro-api",
                    label_visibility="visible",
                    key="api_key_input"
                )
                
                if st.button("Continue", type="primary", use_container_width=True, key="submit_api_key"):
                    if api_key_input and api_key_input.strip():
                        st.session_state.api_key = api_key_input.strip()
                        st.rerun()
                    else:
                        st.error("Please enter a valid API key")
                
                st.markdown("")
                st.markdown("**Get your free API key:** [DeepL Pro API](https://www.deepl.com/pro-api?cta=header-pro-api)")
                st.caption("Free tier: 500,000 characters/month")
        
        st.stop()
    
    # Main app content (only shown if API key is set)
    # Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2.5rem; border-radius: 12px; margin-bottom: 2rem;">
        <h1 style="color: white; margin-bottom: 0.5rem;"> LingLing — for Language Learning</h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem; margin: 0;">🔔 Translate Once, Learn Across Languages</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 📝 Enter your sentence")
        input_sentence = st.text_area(
            "Sentence to translate",
            height=120,
            placeholder="Enter a sentence in any language...",
            help="Type any sentence you want to translate and analyze",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("#### 🎯 Select target languages")
        selected_languages = st.multiselect(
            "Choose languages",
            options=list(LANGUAGES.keys()),
            default=["English", "German", "Swedish"],
            help="You can select multiple languages to compare",
            label_visibility="collapsed"
        )

        # Toggle for result layout
        view_mode = st.radio(
            "How would you like to view the translations?",
            ["All languages together", "One language at a time"],
            index=0,
            horizontal=True,
            key="view_mode_layout",
        )
    
    st.markdown("")
    
    # Translate button
    if st.button("🚀 Translate and Analyze", type="primary", use_container_width=True):
        if not input_sentence.strip():
            st.error("Please enter a sentence to translate")
            return
        
        if not selected_languages:
            st.error("Please select at least one target language")
            return
        
        # Process each selected language
        with st.spinner("🔄 Translating and analyzing..."):
            results = []
            
            for lang_name in selected_languages:
                lang_code = LANGUAGES[lang_name]
                
                # Translate
                translation = get_deepl_translation(input_sentence, lang_code, st.session_state.api_key)
                
                # Check if translation failed
                translation_error = None
                if translation.startswith("Error:") or translation.startswith("Translation error:") or translation.startswith("Network error:"):
                    translation_error = translation
                    # Use original text for analysis if translation fails
                    translation = input_sentence
                elif translation.startswith("API Error"):
                    translation_error = translation
                    translation = input_sentence
                
                # Analyze CEFR (only on successful translation)
                cefr_scores = None
                # difficulties = None  # Commented out for now
                if not translation_error:
                    cefr_scores = analyze_cefr_level(translation, lang_code)
                    # Get difficulty points - COMMENTED OUT (will work on later)
                    # difficulties = get_difficulty_points(input_sentence, translation, lang_code)
                
                results.append({
                    "language": lang_name,
                    "translation": translation,
                    "translation_error": translation_error,
                    "cefr_scores": cefr_scores,
                    # "difficulties": difficulties  # Commented out
                })
        
        # Display results
        st.markdown("---")
        st.markdown("#### 🌐 Translation")

        # Helper: show all results together, with a simple responsive layout
        def show_all_results(results_list):
            count = len(results_list)
            # For many languages, use columns; otherwise stack
            if count <= 2:
                # Just stack them for maximum readability
                for i, res in enumerate(results_list):
                    if i > 0:
                        st.markdown("---")
                    display_result(res)
            else:
                # Use 2 or 3 columns depending on how many languages
                if count <= 4:
                    n_cols = 2
                elif count <= 6:
                    n_cols = 3
                else:
                    n_cols = 3

                rows = (count + n_cols - 1) // n_cols
                idx = 0
                for _ in range(rows):
                    cols = st.columns(n_cols)
                    for col in cols:
                        if idx >= count:
                            break
                        with col:
                            display_result(results_list[idx])
                        idx += 1

        # Decide how to render based on the selected view mode
        if view_mode == "All languages together" or len(results) == 1:
            show_all_results(results)
        else:
            # One language at a time: show each in its own tab
            tabs = st.tabs([f"🇺🇳 {r['language']}" for r in results])
            for tab, result in zip(tabs, results):
                with tab:
                    display_result(result)

def display_result(result: Dict):
    """Display a single result in a learner-friendly format."""
    # Get dark mode state
    dark_mode = st.session_state.get('dark_mode', False)
    text_color = "#fafafa" if dark_mode else "#37352f"
    
    st.markdown(f"#### {result['language']}")
    
    # # Translation section with larger font
    # st.markdown("#### Translation")
    
    # Check if there was a translation error
    if result.get('translation_error'):
        st.error(f"**Translation Failed:** {result['translation_error']}")
        st.warning("Please check your API key and ensure it's correctly configured.")
        return  # Skip analysis if translation failed
    
    # Display translation with larger, modern styling
    st.markdown(f"""
    <div class="translation-text">{result['translation']}</div>
    """, unsafe_allow_html=True)
    
    # CEFR Level Distribution (only show if translation succeeded)
    if result.get('cefr_scores') is None:
        return
    
    st.markdown("")
    st.markdown("##### CEFR Level Distribution")
    
    cefr_scores = result['cefr_scores']
    
    # Create columns for CEFR levels with modern colors
    cols = st.columns(6)
    cefr_levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
    # Modern, softer color palette
    colors = ["#ff6b9d", "#c0d8e0", "#ffd89b", "#95e1d3", "#a8e6cf", "#d4a5a5"]
    # Dark mode background colors
    if dark_mode:
        bg_colors = ["#2a1f25", "#1f2528", "#2a2820", "#1f2825", "#1f2823", "#2a2525"]
    else:
        bg_colors = ["#fff0f5", "#f0f8ff", "#fffef0", "#f0fff4", "#f0fff5", "#fff5f5"]
    
    for i, (level, color, bg_color) in enumerate(zip(cefr_levels, colors, bg_colors)):
        with cols[i]:
            score = cefr_scores.get(level, 0)
            st.markdown(f"""
            <div class="cefr-card" style="background-color: {bg_color}; border-left: 3px solid {color};">
                <h3 style="margin: 0.25rem 0; color: {color}; font-size: 0.9rem;">{level}</h3>
                <p style="margin: 0.5rem 0; font-size: 1.3rem; font-weight: 600; color: {text_color};">{score}%</p>
            </div>
            """, unsafe_allow_html=True)
    
    # CEFR explanations
    st.markdown("")
    st.markdown("###### Level Explanations")
    explanation_cols = st.columns(3)
    for i, level in enumerate(cefr_levels):
        with explanation_cols[i % 3]:
            if cefr_scores.get(level, 0) > 10:
                st.caption(f"**{level}**: {get_cefr_explanation(level)}")
    
    # COMMENTED OUT: Key Difficulty Points for Learners
    # This section is commented out as requested - will work on it later
    #
    # if result.get('difficulties') is None:
    #     return
    #
    # st.markdown("---")
    # st.markdown("#### 🎓 Key Difficulty Points for Learners")
    #
    # difficulties = result['difficulties']
    #
    # difficulty_cols = st.columns(2)
    #
    # with difficulty_cols[0]:
    #     st.markdown("##### 📚 Vocabulary")
    #     if difficulties["vocabulary"]:
    #         for point in difficulties["vocabulary"]:
    #             st.markdown(f"- {point}")
    #     else:
    #         st.markdown("- No major vocabulary challenges")
    #     
    #     st.markdown("##### 📖 Grammar")
    #     if difficulties["grammar"]:
    #         for point in difficulties["grammar"]:
    #             st.markdown(f"- {point}")
    #     else:
    #         st.markdown("- Basic grammatical structures")
    #
    # with difficulty_cols[1]:
    #     st.markdown("##### 🏗️ Sentence Structure")
    #     if difficulties["sentence_structure"]:
    #         for point in difficulties["sentence_structure"]:
    #             st.markdown(f"- {point}")
    #     else:
    #         st.markdown("- Simple sentence structure")
    #     
    #     st.markdown("##### 🔄 Word Order")
    #     if difficulties["word_order"]:
    #         for point in difficulties["word_order"]:
    #             st.markdown(f"- {point}")
    #     else:
    #         st.markdown("- Standard word order")
    
    # Additional tip
    st.markdown("")
    st.markdown("💡 **Tip**: Practice reading similar sentences at your current CEFR level to gradually improve!")

if __name__ == "__main__":
    main()
