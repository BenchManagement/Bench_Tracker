import streamlit as st

st.set_page_config(page_title="Bench Tracker", page_icon="📒")
st.sidebar.header("Bench Tracker - Home Page")
st.markdown("# PLATO - Bench Activities Tracker")
st.markdown(
    """
   The bench activity tracker is a powerful tool designed to streamline and visualize essential
   data from the bench report Excel file. Through simplified and graphical representations, the tool
   offers a clear and insightful overview of bench utilization and activity distribution within PLATO.
    ### Instructions.
        1. Bench Data Visualization - Please select the ‘Bench data Visualization’ tab from left panel. 
        Import the bench report file, and the data should flow automatically. This section focuses mainly 
        on bench count.
        2. Bench Details – Please select ‘Bench Details’ tab from left panel. This section provides more
        granular details on bench activity assignment and Bench removal plans.
        3. With the Email Trigger option, automatic emails can be send in below cases-
                a. Activity End date is past due date.
                b. Bench Removal date is a past date.
    ### More Info
"""
)
st.write("Still have questions? Feel free to send your queries to bench.management@platotech.com")
st.write("Check out this [GitHub Repository](https://github.com/BenchManagement/Bench_Tracker) for the code source.")