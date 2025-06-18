# Palmyra Financial Report Analyzer

This Streamlit web app allows you to upload a company's financial report (PDF or TXT), analyzes it using the Palmyra AI model, and provides a summary of the company's performance. You can also chat with the AI to ask follow-up questions about the report.

## Features
- **Upload Financial Reports:** Supports PDF and TXT files.
- **AI Analysis:** Automatically analyzes the uploaded report and summarizes the company's strengths, weaknesses, and trends.
- **Conversational Chat:** After analysis, chat with the AI for deeper insights or clarifications about the report.
- **Streaming Responses:** AI responses are streamed in real time for a smooth user experience.

## Setup

1. **Clone the repository** (if needed):
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your API key:**
   - Open `main.py` and set your NVIDIA API key in the `api_key` field:
     ```python
     client = OpenAI(
         base_url="https://integrate.api.nvidia.com/v1",
         api_key="<your-nvidia-api-key>"
     )
     ```

4. **Run the app:**
   ```bash
   streamlit run main.py
   ```

## Usage
1. Open the app in your browser (Streamlit will provide a local URL).
2. Upload a company's financial report in PDF or TXT format.
3. Click **Analyze Report** to get an AI-generated summary of the company's performance.
4. After analysis, use the chat interface to ask the AI further questions about the report.

## Requirements
- Python 3.7+
- Streamlit
- openai
- PyPDF2

Install all requirements with:
```bash
pip install -r requirements.txt
```

## Notes
- Make sure you have a valid NVIDIA API key for the Palmyra model.
- The app only processes the text content of the uploaded report.

---

Feel free to customize or extend the app for your specific needs! 