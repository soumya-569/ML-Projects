import streamlit as st
from analytics import location,average_price,avg_price_sqft,total_properties,location_summary
from chart_clean import most_properties,area_type_ratio,price_distribution,price_per_sqft_distribution,bhk_distribution,avg_price_bhk,pps_bhk,sqft_vs_price,bhk_sqft,ten_exp_loc,ten_least_loc,heatmap,metric_selection

st.set_page_config(layout="wide")

css_path = "Streamlit_Apps/Bangalore_Housing_Price_App/CSS/analysis.css"

with open(css_path) as load_css:
    st.markdown(f"<style>{load_css.read()}</style>",unsafe_allow_html=True)

@st.cache_data
def call_kpi4():
    return avg_price_sqft()

@st.cache_data
def call_chart5():
    return bhk_distribution()

kpi1,kpi2,kpi3,kpi4 = st.columns(4,gap='small')

with kpi1:
    st.metric("Total Properties",total_properties())

with kpi2:
    st.metric("Most Property In a Location",location())

with kpi3:
    st.metric("Average House Price",average_price())

with kpi4:
    st.metric("Average Price/sqft",call_kpi4())

st.header("General Insights")
st.divider()

gen1,gen2,gen3 = st.columns(3,gap="small")

with gen1:
    st.plotly_chart(price_per_sqft_distribution())
    st.info("Price per Sqft helps compare properties of different sizes. Extreme outliers are removed for clarity.")

with gen2:
    st.plotly_chart(area_type_ratio())

with gen3:
    user_opt = st.radio("Select a feature to display violin plot against it",options=["Bath","Balcony"])
    st.plotly_chart(metric_selection(user_opt))

st.header("Size vs Price Relation")
st.divider()

chart1,chart2,chart3 = st.columns(3,gap="small")

with chart1:
    st.plotly_chart(price_distribution())

with chart2:
    st.plotly_chart(sqft_vs_price())

with chart3:
    st.plotly_chart(pps_bhk())

st.header("BHK Analysis")
st.divider()

bhk1,bhk2,bhk3 = st.columns(3,gap="small")

with bhk1:
    st.plotly_chart(call_chart5())

with bhk2:
    st.plotly_chart(avg_price_bhk())

with bhk3:
    st.plotly_chart(bhk_sqft())

st.header("Location Price Insights")
st.divider()

loc1,loc2,loc3 = st.columns(3,gap="small")

with loc1:
    st.plotly_chart(most_properties())

with loc2:
    st.plotly_chart(ten_exp_loc())

with loc3:
    st.plotly_chart(ten_least_loc())


st.header("Correlation Heatmap")
st.divider()

st.plotly_chart(heatmap())
st.info("""
A correlation heatmap reveals relationships between features.
High correlation with price indicates strong predictive power.
""")

st.header("Location-Wise Statistical Table")
st.divider()

st.dataframe(location_summary())

analysis_insights = """
# 📊 Bangalore Real Estate – Analysis Insights

---

## 🧮 1. Summary Metrics — What the Overall Market Tells Us

- **12,198+ properties** highlight the scale and diversity of Bangalore’s housing market.
- **Whitefield** leads in total listings — confirming its position as one of the fastest-growing IT corridors.
- The **average house price (~₹99 Lakhs)** reflects a strong metropolitan market.
- **Average price per sqft (~₹6,000)** signals steady demand and long-term appreciation.

These metrics paint a picture of a **dynamic and expanding real-estate landscape** driven by IT growth, migration, and urban development.

---

## 📉 2. Price per Sqft Distribution — Understanding Market Spread

- Most properties fall between **₹4,000–₹8,000 per sqft**, the city’s mid-range pricing zone.
- A long upper tail (>₹15,000 per sqft) captures premium areas like *Indiranagar, Koramangala, HSR, MG Road*.
- After data cleaning, the shape is smoother and more realistic.

This tells us that **Bangalore is a mix of affordable and ultra-premium micro-markets**, each with unique price behavior.

---

## 🏘️ 3. Area Type Distribution — How Homes are Classified

- **Super built-up areas** dominate (~70%), common in Bengaluru apartment projects.
- **Built-up** and **Plot areas** have smaller shares, representing villas and independent houses.
- **Carpet area listings are rare**, mostly due to older pre-RERA documentation.

This distribution reinforces how **sqft-based features strongly influence price predictions**.

---

## 🚿 4. Bathroom Count vs Price — A Strong Luxury Indicator

- Prices increase steadily with more bathrooms.
- **3+ bathrooms** strongly correlate with high-end homes.
- This trend confirms bathrooms as a **top predictor** of price after sqft.

More bathrooms typically signal **bigger, premium, or higher-segment homes**.

---

## 💸 5. Price Range Distribution — The City’s Affordability Curve

- A right-skewed shape: majority of homes lie below **₹50–80 Lakhs**.
- Fewer properties exist in high-value brackets (>₹2 Cr).
- Ultra-premium listings create the long tail.

This is typical of a metro where **mid-segment demand is highest**.

---

## 📈 6. Total Sqft vs Price — The Strongest Direct Relationship

- Clear positive correlation: more space = higher price.
- The trendline shows strong consistency after outlier removal.
- Some above-line points represent premium areas; below-line represent budget locations.

This reaffirms **total_sqft as the single most important pricing factor**.

---

## 📦 7. Price per Sqft by BHK — How Size Relates to Value

- PPSF remains stable from **2 to 4 BHK** categories.
- Higher BHKs (5–8 BHK) show large price variability due to luxury villas.
- Clean boxplots indicate well-handled outlier removal.

This shows that **BHK alone is not a strong predictor — segments matter more**.

---

## 🛏️ 8. BHK Distribution — How the Market is Structured

- **2 BHK and 3 BHK dominate**, forming nearly 85% of total listings.
- 4+ BHK properties are niche segments (luxury projects).
- This makes the dataset ideal for ML modeling due to strong representation.

The market is **heavily mid-segment focused**, aligning with urban working populations.

---

## 💰 9. Average Price by BHK — Understanding Value Growth

- Prices rise with BHK count but **not in a simple linear fashion**.
- Big jumps occur only in luxury segments (7+ BHK).
- Helps confirm the pricing clusters in Bangalore’s segment-based housing market.

---

## 🧭 10. Location Insights — Where Buyers Pay the Most or Least

### 📍 Top 10 Locations with Most Properties
- Whitefield, Sarjapur, Electronic City dominate supply.
- These areas have high developer activity due to IT parks.

### 💎 Top 10 Most Expensive Locations
- Indiranagar, D’Souza Layout, Sadhashivnagar show **₹20K+ per sqft** prices.
- These are legacy and luxury micro-markets.

### 🏡 Top 10 Most Affordable Locations
- Koppa, Bagur, BDS Layout offer **₹2,000–₹3,000 per sqft** homes.
- Ideal for first-time buyers and investment-focused buyers.

---

## 🔥 11. Correlation Heatmap — Feature Importance at a Glance

- **Total Sqft (0.79)** and **Bath Count (0.62)** have the strongest correlation with price.
- **BHK (0.56)** also correlates but is weaker compared to bathrooms.
- **Balcony** has very low influence on price.

This aligns with your preprocessing logic and improves confidence in model selection.

---

## 📑 12. Location-Wise Statistical Table — A Complete Area Breakdown

This table helps users compare neighborhoods by:

- **Average Price**
- **Average Price per Sqft**
- **Total Property Count**

It acts as a **data-driven real-estate guide** for smart property decisions.

---

## ⭐ Final Insight

The combination of cleaned visuals, structured insights, and strong transformations gives a **complete, realistic, and business-ready overview** of Bangalore’s property market — exactly what real estate analysts present to stakeholders and leadership.

"""

with st.expander("Key Findings After Analysis"):
    st.markdown(analysis_insights, unsafe_allow_html=True)