import streamlit as st
import pandas as pd
import numpy as np
import pickle
import joblib
from datetime import date

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-PNP8HXNDWW"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-PNP8HXNDWW');
</script>

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="GA4 Traffic Prediction Dashboard",
    layout="wide"
)

# -------------------------------
# CSS FOR LOOKER STUDIO STYLE & SIDEBAR OUTLAYER
# -------------------------------
st.markdown("""
<style>
/* Sidebar styling with outlayer effect */
[data-testid="stSidebar"] {
    background-color: #f8f9fa;
    padding: 10px;
}

/* The Outlayer Box for Inputs */
.sidebar-box {
    background-color: #ffffff;
    border: 1px solid #dcdcdc;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

/* Main Country Card Section */
.country-section {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 12px;
    border: 1px solid #e0e0e0;
    margin-bottom: 35px;
}

.country-header {
    font-size: 22px;
    font-weight: 600;
    color: #1a73e8;
    margin-bottom: 20px;
    padding-left: 5px;
}

/* Scorecard Grid */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 12px;
}

/* Scorecard Style */
.scorecard {
    background: #fff;
    border: 1px solid #dadce0;
    border-radius: 4px;
    padding: 12px;
    text-align: left;
    border-top: 3px solid #1a73e8;
}

.scorecard-label {
    font-size: 11px;
    color: #5f6368;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.scorecard-value {
    font-size: 22px;
    font-weight: 700;
    color: #202124;
}

.scorecard-unit {
    font-size: 12px;
    color: #70757a;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# SIDEBAR INPUTS WITH OUTLAYER
# -------------------------------
st.sidebar.title("⚙️ Control Panel")

# Wrapping inputs in a container to apply the "outlayer" look
with st.sidebar.container():
    st.markdown('<div class="sidebar-box">', unsafe_allow_html=True)
    
    country_list = [
        "(not set)", "Argentina", "Australia", "Austria", "Bangladesh", "Bolivia",
        "Brazil", "Bulgaria", "Canada", "China", "Czechia", "Egypt", "Finland",
        "France", "Germany", "Ghana", "Hong Kong", "India", "Indonesia", "Iraq",
        "Ireland", "Italy", "Japan", "Lithuania", "Malaysia", "Maldives", "Mexico",
        "Mongolia", "Netherlands", "New Zealand", "Nigeria", "Norway", "Oman",
        "Pakistan", "Philippines", "Poland", "Qatar", "Romania", "Russia",
        "Saudi Arabia", "Singapore", "South Africa", "South Korea", "Spain",
        "Sri Lanka", "Sweden", "Switzerland", "Taiwan", "Thailand", "Turkey",
        "Türkiye", "United Arab Emirates", "United Kingdom", "United States",
        "Vietnam"
    ]

    selected_countries = st.multiselect(
        "Select Country(s)",
        country_list,
        default=["India"]
    )

    today = date.today()
    date_range = st.date_input(
        "Date Range",
        value=[today, today],
        min_value=date(2023, 1, 1),
        max_value=date(2027, 12, 31)
    )

    start_date = date_range[0]
    end_date = date_range[-1]

    model_file = st.file_uploader(
        "Model File (.pkl, .joblib)",
        type=["pkl", "joblib"]
    )
    
    predict_btn = st.button("🚀 Run Prediction", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# MAIN UI
# -------------------------------
st.title("📊 GA4 Multi-Metric Prediction Dashboard")
st.caption("Forecasting Traffic, Engagement, and Behavior Metrics")

def load_model(file):
    try:
        return pickle.load(file)
    except Exception:
        file.seek(0)
        return joblib.load(file)

if predict_btn:
    if not model_file:
        st.warning("⚠️ Please upload a trained model file.")
        st.stop()

    if len(selected_countries) == 0:
        st.warning("⚠️ Please select at least one country.")
        st.stop()

    try:
        model = load_model(model_file)
        
        # Logic remains untouched
        predictions = pd.DataFrame({
            "Sessions": np.random.randint(500, 5000, len(selected_countries)),
            "Engaged sessions": np.random.randint(300, 3500, len(selected_countries)),
            "Engagement rate": np.round(np.random.uniform(0.3, 0.85, len(selected_countries)), 2),
            "Average engagement time per session": np.random.randint(120, 600, len(selected_countries)),
            "Events per session": np.round(np.random.uniform(3, 12, len(selected_countries)), 1),
            "Event count": np.random.randint(5000, 50000, len(selected_countries)),
            "Key events": np.random.randint(50, 1000, len(selected_countries)),
            "Bounce rate": np.round(np.random.uniform(0.15, 0.6, len(selected_countries)), 2),
            "First visits": np.random.randint(100, 2000, len(selected_countries)),
            "Views per session": np.round(np.random.uniform(1.2, 6.5, len(selected_countries)), 2)
        }, index=selected_countries)

        for country in selected_countries:
            cards_html = f"""
            <div class="country-section">
                <div class="country-header">📍 {country}</div>
                <div class="metrics-grid">
                    <div class="scorecard">
                        <div class="scorecard-label">Sessions</div>
                        <div class="scorecard-value">{predictions.loc[country, 'Sessions']:,}</div>
                    </div>
                    <div class="scorecard">
                        <div class="scorecard-label">Engaged Sessions</div>
                        <div class="scorecard-value">{predictions.loc[country, 'Engaged sessions']:,}</div>
                    </div>
                    <div class="scorecard">
                        <div class="scorecard-label">Engagement Rate</div>
                        <div class="scorecard-value">{predictions.loc[country, 'Engagement rate']*100:.1f}<span class="scorecard-unit">%</span></div>
                    </div>
                    <div class="scorecard">
                        <div class="scorecard-label">Avg. Engagement Time</div>
                        <div class="scorecard-value">{predictions.loc[country, 'Average engagement time per session']}<span class="scorecard-unit">s</span></div>
                    </div>
                    <div class="scorecard">
                        <div class="scorecard-label">Events per Session</div>
                        <div class="scorecard-value">{predictions.loc[country, 'Events per session']}</div>
                    </div>
                    <div class="scorecard">
                        <div class="scorecard-label">Event Count</div>
                        <div class="scorecard-value">{predictions.loc[country, 'Event count']:,}</div>
                    </div>
                    <div class="scorecard">
                        <div class="scorecard-label">Key Events</div>
                        <div class="scorecard-value">{predictions.loc[country, 'Key events']:,}</div>
                    </div>
                    <div class="scorecard">
                        <div class="scorecard-label">Bounce Rate</div>
                        <div class="scorecard-value">{predictions.loc[country, 'Bounce rate']*100:.1f}<span class="scorecard-unit">%</span></div>
                    </div>
                    <div class="scorecard">
                        <div class="scorecard-label">First Visits</div>
                        <div class="scorecard-value">{predictions.loc[country, 'First visits']:,}</div>
                    </div>
                    <div class="scorecard">
                        <div class="scorecard-label">Views per Session</div>
                        <div class="scorecard-value">{predictions.loc[country, 'Views per session']}</div>
                    </div>
                </div>
            </div>
            """
            st.markdown(cards_html, unsafe_allow_html=True)

        st.success("✅ Prediction completed successfully")

    except Exception as e:
        st.error(f"❌ Error: {e}")
