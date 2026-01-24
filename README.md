# 🌍 Language Learning Assistant

A Streamlit app that helps language learners by providing translations, CEFR level analysis, and difficulty breakdowns for sentences in multiple target languages.

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get a DeepL API Key (Free):**
   - Sign up at https://www.deepl.com/pro-api?cta=header-pro-api
   - Free tier: 500,000 characters/month
   - Copy your API key

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

4. **Configure API Key:**
   - Option 1: Enter it in the sidebar when running the app
   - Option 2: Set as environment variable: `export DEEPL_API_KEY="your-key-here"`
   - Option 3: Use Streamlit secrets (create `.streamlit/secrets.toml`)

## 📝 Features

- ✅ Translate sentences to multiple target languages simultaneously
- ✅ CEFR level distribution (A1-C2) with explanations
- ✅ Support for 20+ target languages

## 🔧 API Alternatives

If you want to replace DeepL with other translation APIs:

1. **Google Translate API (Free tier available):**
   - Replace `get_deepl_translation()` function
   - Use `googletrans` library: `pip install googletrans==4.0.0rc1`

2. **HuggingFace Translation Models:**
   - Use `transformers` library for local inference
   - No API key needed, but requires more setup

3. **OpenAI API (requires paid account):**
   - Can use GPT models for translation and analysis

## 📁 File Structure

```
.
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🎯 Usage

1. Enter your DeepL API key when prompted (required to start using the app)
2. Enter any sentence in the input field
3. Select one or more target languages from the dropdown
4. Click "Translate and Analyze"
5. View translations and CEFR levels for each language

## ⚠️ Note

The CEFR analysis uses heuristic-based approaches. For production use, consider integrating:
- NLP models for more accurate CEFR classification
- Grammar analysis tools
- Vocabulary difficulty databases
