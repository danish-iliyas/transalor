# Ampyr Document Translator

A document translation application powered by Azure AI Translator and Azure OpenAI.

![Ampyr Solar Europe](https://img.shields.io/badge/Ampyr-Solar%20Europe-1A988B)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0+-green)

## Features

- 📄 **Document Upload** - Translate PDF, DOCX, and TXT files
- ✍️ **Text Translation** - Direct text input translation
- 🤖 **AI Summarization** - Summarize documents before translating (using Azure OpenAI)
- 🌐 **Multiple Languages** - Support for Hindi, Spanish, French, German, Chinese, and more
- 🎨 **Modern UI** - Beautiful dark-themed web interface

## Tech Stack

- **Backend**: Python, Flask
- **AI Services**: Azure AI Translator, Azure OpenAI (GPT-4o-mini)
- **Document Processing**: pdfplumber, python-docx
- **Frontend**: HTML, CSS, JavaScript

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Umarkhan260/Ampyr-Document-Translator.git
cd Ampyr-Document-Translator
```

### 2. Create virtual environment

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file with your Azure credentials:

```env
AZURE_TRANSLATOR_KEY=your-translator-key
AZURE_TRANSLATOR_REGION=centralindia
AZURE_TRANSLATOR_ENDPOINT=https://api.cognitive.microsofttranslator.com/

AZURE_OPENAI_API_KEY=your-openai-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### 5. Run the application

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web UI |
| GET | `/health` | Health check |
| GET | `/languages` | List supported languages |
| POST | `/translate` | Translate text |
| POST | `/upload` | Upload & translate document |
| POST | `/analyze` | Analyze document with AI |

## Project Structure

```
├── app.py                 # Flask API
├── translator.py          # Azure Translator integration
├── openai_client.py       # Azure OpenAI integration
├── document_processor.py  # PDF/DOCX text extraction
├── main.py               # CLI demo
├── templates/
│   └── index.html        # Web UI
├── requirements.txt
└── .env                  # Credentials (not in repo)
```

## License

© Ampyr Solar Europe
