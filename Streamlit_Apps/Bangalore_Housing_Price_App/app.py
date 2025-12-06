import streamlit as st

# ** Set up navigation menu for different pages

home = st.Page(
    page= "Views/home.py",
    title= "Home",
    icon= ":material/home:",
    default= True
)

analysis = st.Page(
    page="Views/analysis.py",
    title= "Analysis",
    icon= ":material/bar_chart:"
)

model = st.Page(
    page= "Views/model.py",
    title= "Model",
    icon= ":material/robot_2:"
)

conclusion = st.Page(
    page= "Views/conclusion.py",
    title= "Conclusion",
    icon= ":material/gavel:"
)

nav = st.navigation(pages=[home,analysis,model,conclusion])

# ** Logo for sidebar and whole page

st.logo(image="https://cdn-icons-png.flaticon.com/512/10058/10058840.png",size="large")

nav.run()
