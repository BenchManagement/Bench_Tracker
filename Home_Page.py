import streamlit as st

st.set_page_config(page_title="Bench Tracker", page_icon="📒")
st.sidebar.header("Bench Tracker - Home Page")
st.markdown("# PLATO - Bench Activities Tracker")
st.write(
    """
   The bench activity tracker is a powerful tool designed to streamline and visualize essential
   data from the bench report Excel file. Through simplified and graphical representations, the tool
   offers a clear and insightful overview of bench utilization and activity distribution within PLATO.""")
st.subheader("Instructions.")
st.write('''
    * Bench Data Visualization - Please select the ‘Bench data Visualization’
    tab from left panel. Import the bench report file, and the data should flow 
    automatically. This section focuses mainly on bench count.
    * Bench Details – Please select ‘Bench Details’ tab from left panel. This
    section provides more granular details on bench activity assignment and Bench
    removal plans.
    * With the Email Trigger option, automatic emails can be send in below cases-
        * Activity End date is past due date.
        * Bench Removal date is a past date.''') 
st.subheader("More Information:")
st.write("Still have questions? Feel free to send your queries to bench.management@platotech.com")
st.write("Check out this [GitHub Repository](https://github.com/BenchManagement/Bench_Tracker) for the code source.")