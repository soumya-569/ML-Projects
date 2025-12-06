import streamlit as st

css_path = "Streamlit_Apps/Bangalore_Housing_Price_App/CSS/conclusion.css"

with open(css_path) as load_css:
    st.markdown(f"<style>{load_css.read()}</style>",unsafe_allow_html=True)

conclusion_text = """
# 🎉 **Bangalore House Price Prediction – Final Conclusions**  
<hr style="border: 1px solid #444; margin-top: 10px; margin-bottom: 20px;" />

## 🏙️ **1. The Raw Housing Dataset Reveals a Highly Diverse Market**
The charts in the Analysis page show insights from **raw, unprocessed housing data**, reflecting real-world irregularities such as:

- Large variation in **price per sqft**  
- Unbalanced **BHK distribution**  
- Unrealistic or inconsistent **square-foot values**  
- Duplicates, missing values, and structural noise  

These raw visualizations help illustrate the **true complexity of Bangalore’s real-estate landscape**, where data inconsistency is common.

<hr style="border: 1px solid #333; margin-top: 15px; margin-bottom: 15px;" />

## 🧹 **2. Data Cleaning Brings Structure and Reliability**
In the research notebook, extensive data cleaning steps were applied:

- Normalizing `total_sqft` and handling ranges  
- Removing unrealistic BHK–SQFT combinations  
- Eliminating extreme outliers  
- Categorizing and standardizing locations  
- Engineering **price per sqft**, a key pricing indicator  

This transformed dataset allowed us to shift from *raw noise* to **market-responsible insights**, forming the basis of a reliable ML model.

<hr style="border: 1px solid #333; margin-top: 15px; margin-bottom: 15px;" />

## 📈 **3. Key Drivers of Housing Prices in Bangalore**
Across exploratory and processed data, several factors consistently show high predictive power:

- 📍 **Location** – The strongest determinant of price  
- 📐 **Total Square Foot Area** – Direct, non-linear impact on value  
- 🛁 **Number of Bathrooms** – Strong indicator of property class  
- 🛏️ **BHK Count** – Influential when supported by adequate area  

These align well with real-world real-estate economics in metropolitan cities.

<hr style="border: 1px solid #333; margin-top: 15px; margin-bottom: 15px;" />

## 🤖 **4. The Machine Learning Model Turns Data into a Decision Tool**
Using cleaned and structured features, the model:

- Provides **accurate price predictions**  
- Helps users avoid overpaying  
- Supports sellers in pricing competitively  
- Identifies under-valued localities  
- Makes market comparisons transparent and data-driven  

The model brings **precision and clarity** to a market filled with variability.

<hr style="border: 1px solid #333; margin-top: 15px; margin-bottom: 15px;" />

## 🌇 **5. Bangalore’s Real-Estate Market Continues to Grow**
Based on pricing patterns and locality dynamics:

- Tech-driven areas (Whitefield, ORR, Sarjapur) show strong appreciation  
- Premium neighborhoods (HSR, Indira Nagar, JP Nagar, Koramangala) retain high value  
- Metro expansion and road connectivity continue to push demand upward  

Bangalore remains one of India’s most resilient and opportunity-rich housing markets.

<hr style="border: 1px solid #333; margin-top: 15px; margin-bottom: 15px;" />

## 🧠 **6. Final Summary**
This project demonstrates the **end-to-end lifecycle of a real-estate analytics engine**, covering:

✔ Raw data understanding  
✔ Data cleaning and transformation  
✔ Exploratory visualizations  
✔ Machine learning modeling  
✔ Deployment as an interactive web application  

The **Bangalore House Price Prediction App** bridges the gap between complex real-estate patterns and **easy-to-understand pricing insights**, empowering buyers, sellers, and analysts to make **smarter, data-driven decisions.**

<hr style="border: 1px solid #333; margin-top: 20px; margin-bottom: 20px;" />

# ⭐ **Thank You for Using the App**  
Your feedback helps improve this platform and expand its capabilities!
"""

st.markdown(conclusion_text, unsafe_allow_html=True)