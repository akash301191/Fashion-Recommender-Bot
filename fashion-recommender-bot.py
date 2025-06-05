import tempfile
import streamlit as st

from agno.agent import Agent
from agno.media import Image
from agno.models.openai import OpenAIChat
from agno.tools.serpapi import SerpApiTools

from textwrap import dedent

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    # SerpAPI Key input
    serp_api_key = st.sidebar.text_input(
        "Serp API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://serpapi.com/manage-api-key)."
    )
    if serp_api_key:
        st.session_state.serp_api_key = serp_api_key
        st.sidebar.success("✅ Serp API key updated!")

    st.sidebar.markdown("---")

def render_style_preferences():
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    # Column 1: Image Upload
    with col1:
        st.subheader("📸 Upload Your Full-Body Photo")
        uploaded_image = st.file_uploader(
            "Upload a front-facing full-body image",
            type=["jpg", "jpeg", "png"]
        )

    # Column 2: Style Preferences
    with col2:
        st.subheader("👗 Style Preferences")
        preferred_styles = st.multiselect(
            "Which fashion aesthetics do you like?",
            [
                "Casual", "Streetwear", "Minimalist", "Chic", "Glam", 
                "Boho", "Classic", "Vintage", "Ethnic", "Trend-forward"
            ]
        )

        color_palette = st.multiselect(
            "What colors do you prefer wearing?",
            [
                "Neutrals (black, white, beige)", "Pastels (mint, blush)", "Brights (red, yellow)", 
                "Earth tones (olive, rust)", "Jewel tones (emerald, sapphire)", "Metallics (gold, silver)"
            ]
        )

    # Column 3: Outfit Goals
    with col3:
        st.subheader("🎯 Outfit Goals")
        fashion_goal = st.selectbox(
            "What are you looking for?",
            [
                "Everyday wear", "Office/professional outfits", "Party or event looks", 
                "Vacation styling", "Seasonal wardrobe ideas", "Try a new aesthetic"
            ]
        )

        focus_area = st.selectbox(
            "Do you want to highlight or balance any features?",
            [
                "Highlight waist", "Accentuate legs", "Slim the hips", 
                "Add height", "Balance upper/lower body", "No preference"
            ]
        )

    return {
        "uploaded_image": uploaded_image,
        "preferred_styles": preferred_styles,
        "color_palette": color_palette,
        "fashion_goal": fashion_goal,
        "focus_area": focus_area
    }

def generate_fashion_report(style_input):
    uploaded_image = style_input["uploaded_image"]
    preferred_styles = style_input["preferred_styles"]
    color_palette = style_input["color_palette"]
    fashion_goal = style_input["fashion_goal"]
    focus_area = style_input["focus_area"]

    # Save uploaded image temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(uploaded_image.getvalue())
        image_path = tmp.name

    # Step 1: Fashion Visual Analyzer
    fashion_analyzer = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        name="Fashion Visual Analyzer",
        role="Analyzes a user's full-body image to infer body shape and styling considerations.",
        description=dedent("""
            You are a fashion stylist assistant. Analyze the uploaded photo to infer body shape, posture, and proportions.
            Based on this visual assessment, provide recommendations on ideal silhouettes, fit types, and outfit balance techniques.
        """),
        instructions=[
            "Carefully assess the user's full-body image.",
            "Determine the likely body shape (e.g., hourglass, rectangle, pear, etc.).",
            "List styling strategies for enhancing balance or proportions.",
            "Do not suggest specific clothing pieces yet—focus on visual characteristics."
        ],
        markdown=True
    )

    visual_insights = fashion_analyzer.run(
        "Analyze the user's fashion-relevant visual features.",
        images=[Image(filepath=image_path)]
    ).content

    # Step 2: Fashion Research Agent (with user preferences)
    fashion_search_agent = Agent(
        name="Fashion Search Assistant",
        role="Finds high-quality outfit ideas and fashion inspiration based on personal style preferences.",
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        description="Given style traits and visual analysis, generate a focused Google search to find relevant outfit inspirations.",
        instructions=[
            "Use the user's selected style preferences, color palette, fashion goals, and target features.",
            "Generate a smart Google search query (e.g., 'boho outfits for petite rectangle body in pastels').",
            "Use SerpAPI to find high-quality outfit ideas, Pinterest boards, and fashion blogs.",
            "Return 5–7 links in markdown format with meaningful titles.",
        ],
        tools=[SerpApiTools(api_key=st.session_state.serp_api_key)],
        markdown=True
    )

    search_prompt = f"""
    Preferred Styles: {', '.join(preferred_styles) if preferred_styles else 'Not specified'}
    Color Palette: {', '.join(color_palette) if color_palette else 'Not specified'}
    Fashion Goal: {fashion_goal}
    Focus Area: {focus_area}

    Generate a relevant Google search and return curated outfit links for this profile.
    """

    research_links = fashion_search_agent.run(search_prompt).content

    # Step 3: Report Generator Agent
    report_generator = Agent(
        name="Fashion Report Generator",
        model=OpenAIChat(id="o3-mini", api_key=st.session_state.openai_api_key),
        role="Generates a descriptive, structured fashion recommendation report using visual insights and curated research links.",
        description=dedent("""
            You are a fashion stylist report generator. You are given:
            1. A visual analysis of the user’s body type and proportions from an uploaded image.
            2. A list of curated fashion inspiration links based on user style preferences and goals.

            Your task is to write a rich, well-structured Markdown report with descriptive recommendations tailored to the user's appearance and preferences.
        """),
        instructions=[
            "Start the report with: ## 👗 Fashion Recommendation Report",
            "",
            "### 👤 Body Type & Styling Insights",
            "- Describe the user’s inferred body shape and proportions.",
            "- Explain styling choices with reasoning (e.g., why wrap dresses or pencil skirts work).",
            "- Embed hyperlinks where useful (e.g., [wrap dresses](https://...) or [tailored fits](https://...)).",
            "",
            "### 🎯 Focus Area Strategy",
            "- Suggest ways to visually emphasize the selected focus area using styling techniques.",
            "- Mention concepts like vertical lines, high-rise trousers, cropped jackets, etc.",
            "- Add links to helpful examples or guides (e.g., [vertical stripe styling](https://...), [high-waisted pants guide](https://...)).",
            "",
            "### 💡 Outfit & Silhouette Recommendations",
            "- For each outfit suggestion, explain the ‘why’ and link to relevant inspiration pages, lookbooks, or guides.",
            "- Embed links in outfit terms (e.g., [tailored suits](https://...), [fit-and-flare skirts](https://...)).",
            "",
            "### 🎨 Color Palette Styling Tips",
            "- Explain how the user’s chosen colors can be styled and paired.",
            "- Include links to visual inspiration or color theory resources (e.g., [monochrome layering tips](https://...)).",
            "",
            "### 🧥 Fabrics & Layering Ideas",
            "- Recommend specific fabrics and explain their benefits.",
            "- Embed links to fabric examples or guides (e.g., [chiffon styling](https://...), [structured cotton blazers](https://...)).",
            "",
            "### 👜 Accessories to Consider",
            "- Suggest accessories like belts, shoes, bags, and jewelry.",
            "- Use embedded links where possible (e.g., [pointed-toe shoes](https://...), [minimalist jewelry](https://...)).",
            "",
            "### 🔗 Curated Outfit Inspirations",
            "- Use clear, titled markdown hyperlinks for each link (e.g., [The Minimalist Wardrobe](https://...)).",
            "- Group similar links if applicable.",
            "",
            "**Important:** Embed helpful, relevant hyperlinks throughout the report—not just in the final section. Aim for at least 1–2 embedded links per section.",
            "",
            "Write in a confident, professional, and friendly tone.",
            "Use markdown headings, bullet points, and short paragraphs for clarity.",
            "Output only the final Markdown-formatted report—do not explain your reasoning or actions."
        ],
        markdown=True,
        add_datetime_to_instructions=True
    )

    final_prompt = f"""
    Visual Insights from Uploaded Photo:
    {visual_insights}

    Web-Sourced Fashion Inspirations: 
    {research_links}

    Generate a markdown-formatted fashion recommendation report.
    """

    final_report = report_generator.run(final_prompt).content

    return final_report

def main() -> None:
    # Page config
    st.set_page_config(page_title="Fashion Recommender Bot", page_icon="👗", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"], div[data-testid="stFileUploader"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>👗 Fashion Recommender Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Discover what suits you best. Fashion Recommender Bot analyzes your features and fashion vibe to deliver curated lookbooks tailored to your unique style.",
        unsafe_allow_html=True
    )

    render_sidebar()
    user_style_preferences = render_style_preferences()

    st.markdown("---")

    # Call the report generation method when the user clicks the button
    if st.button("👗 Generate Fashion Report"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not hasattr(st.session_state, "serp_api_key"):
            st.error("Please provide your SerpAPI key in the sidebar.")
        elif "uploaded_image" not in user_style_preferences or not user_style_preferences["uploaded_image"]:
            st.error("Please upload a full-body image before generating the report.")
        else:
            with st.spinner("Analyzing your style and crafting a personalized fashion report..."):
                report = generate_fashion_report(user_style_preferences)

                st.session_state.fashion_report = report
                st.session_state.fashion_image = user_style_preferences["uploaded_image"]

    # Display and download
    if "fashion_report" in st.session_state:
        st.markdown("## 📸 Uploaded Photo")
        st.image(st.session_state.fashion_image, use_container_width=False)

        st.markdown(st.session_state.fashion_report, unsafe_allow_html=True)

        st.download_button(
            label="📥 Download Fashion Report",
            data=st.session_state.fashion_report,
            file_name="fashion_recommendation_report.md",
            mime="text/markdown"
        )

if __name__ == "__main__":
    main()
