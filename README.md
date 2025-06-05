# Fashion Recommender Bot

**Fashion Recommender Bot** is a smart Streamlit application that helps you discover outfits tailored to your body type, personal style, and fashion goals. Powered by [Agno](https://github.com/agno-agi/agno), OpenAI's GPT-4o, and SerpAPI, this bot analyzes a full-body photo and preferences to deliver a personalized, well-structured fashion report with curated outfit inspirations and styling advice.

## Folder Structure

```
Fashion-Recommender-Bot/
├── fashion-recommender-bot.py
├── README.md
└── requirements.txt
```

* **fashion-recommender-bot.py**: The main Streamlit application.
* **requirements.txt**: Required Python packages.
* **README.md**: This documentation file.

## Features

* **Style Questionnaire**
  Upload your full-body image and answer simple questions about your favorite styles, color palette, and outfit goals.

* **AI-Powered Visual Analysis**
  A computer vision agent evaluates your photo to determine your body shape and silhouette for ideal styling suggestions.

* **Smart Outfit Search**
  A second AI agent uses SerpAPI to fetch links to trending outfit inspirations, Pinterest boards, and blog lookbooks tailored to your selected aesthetic.

* **Personalized Fashion Report**
  A markdown-style report is generated that includes:

  * Body shape & styling strategies
  * Focus area tactics
  * Outfit and silhouette recommendations
  * Color palette tips
  * Fabric and layering ideas
  * Accessories to consider
  * Hyperlinked outfit inspirations

* **Clean Streamlit UI**
  User-friendly layout and sidebar key input ensure a smooth, responsive experience.

* **Download Option**
  Download your fashion report as a `.md` file to keep your style insights handy.

## Prerequisites

* Python 3.11 or higher
* An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))
* A SerpAPI key ([Get one here](https://serpapi.com/manage-api-key))

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/akash301191/Fashion-Recommender-Bot.git
   cd Fashion-Recommender-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:

   ```bash
   streamlit run fashion-recommender-bot.py
   ```

2. **In your browser**:

   * Add your OpenAI and SerpAPI keys in the sidebar.
   * Upload a full-body image.
   * Select your preferred styles, color palettes, and fashion goals.
   * Click **👗 Generate Fashion Report**.
   * View and download your personalized markdown-style fashion report.

3. **Download Option**
   Use the **📥 Download Fashion Report** button to save your personalized insights and outfit suggestions.

## Code Overview

* **`render_sidebar()`**: Collects and manages API keys.
* **`render_style_preferences()`**: Renders UI components for user image and fashion input collection.
* **`generate_fashion_report()`**:

  * Calls a `Fashion Visual Analyzer` agent to infer body shape.
  * Uses a `Fashion Search Assistant` agent to pull curated outfit inspiration via SerpAPI.
  * Generates a descriptive Markdown report with the `Fashion Report Generator`.
* **`main()`**: Handles page layout, UI flow, and report download functionality.

## Contributions

Contributions are welcome! Feel free to fork this repo, suggest features, report bugs, or submit a pull request. Make sure your changes are clean, tested, and aligned with the project’s goals.