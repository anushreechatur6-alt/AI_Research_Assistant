# 🔍 Researchly

Researchly is an AI-powered research assistant that generates structured research reports from any topic within seconds.

Instead of manually searching through multiple websites, Researchly performs web research, gathers relevant information, and uses Google's Gemini model to generate a comprehensive report with key insights and cited sources.

---

## ✨ Features

* 🌐 Performs real-time web research using Tavily Search
* 🤖 Generates detailed reports using Google Gemini 2.5 Flash
* 📑 Produces well-structured reports containing:

  * Executive Summary
  * Key Takeaways
  * Detailed Findings
  * Cited Sources
* 🎨 Clean and modern Streamlit interface
* 📥 Export reports as Markdown (.md)

---

## 🛠️ Tech Stack

* Python
* Streamlit
* Google Gemini API
* Tavily Search API
* python-dotenv

---

## 🚀 How It Works

1. Enter a research topic.
2. Tavily searches the web for relevant sources.
3. The search results are provided to Gemini as context.
4. Gemini generates a structured research report.
5. Download the report as a Markdown file.

---

## 📂 Project Structure

```
Researchly/
│
├── research_assistant.py
├── .env
├── requirements.txt
├── README.md
└── screenshots/
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/researchly.git
cd researchly
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Run the application:

```bash
streamlit run research_assistant.py
```

---

## 💡 Future Improvements

* PDF export support
* Research history
* Follow-up questions on generated reports
* Report customization (academic, business, technical, etc.)

---

