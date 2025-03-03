import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

timeCount = -1
removal_date_count = 0
employeeRemovalDateList = []
regionBench = []
regionRate = []
removalDate = ""
expected = 'TBD'
altExpected = 'TDB'
benchTimeRed = []
benchEmployeeRed = []
benchTimeAmber = []
benchEmployeeAmber = []
benchTimeBlue = []
benchEmployeeBlue = []
tenure_options = ['All']

st.set_page_config(page_title="Bench Data Visualization", page_icon="📈")
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
st.markdown("# Bench Data Visualization")
st.sidebar.header("Bench Data Visualization")

bench_data = st.file_uploader("Choose the data file")
if bench_data:
    rawData = pd.read_excel(bench_data, sheet_name="Bench")
    fixedData = pd.read_excel(bench_data, sheet_name="Region_Count")
    empNames = rawData['Employee_LName_FName']
    dCategory = rawData['Activity_Category']
    dLevel = rawData['Level']
    dDesignation = rawData['Job_Title']
    pool_data = rawData['Pool']
    regions = fixedData['Region']
    regionTotal = list(fixedData['Region_Total'])
    conSummary = st.container(border=True)
    for i in list(rawData['Bench_Removal_Start_Date']):
        if isinstance(i, str):
            removalDate += i
        elif isinstance(i, datetime):
            removal_date_count = removal_date_count + 1
    conSummary.write("**Total number of employees on Bench** - " + str(empNames.index.size))
    conSummary.write('**Total number of employees with Bench Removal Date** - ' + str(removal_date_count))
    conSummary.write(
        '**Total number of employees with Tentative Bench Removal Date** - ' + str(removalDate.count('tentative')))
    conSummary.write('**Total number of employees who needs a Bench Removal Date (TBD)** - ' + str(
        removalDate.count(expected) + removalDate.count(altExpected)))
    for r in regions:
        regionBench.append(list(rawData['Region']).count(r))
    for i in range(len(regionBench)):
        regionRate.append(round((regionBench[i] * 100) / regionTotal[i], 2))
    regionPie = px.pie(rawData['Region'], values=regionBench, names=regions, title='Regional Bench Distribution: PLATO-Wide Percentage.')
    st.plotly_chart(regionPie)
    st.divider()
    region_plot = go.Figure(
        data=[go.Bar(x=regions, y=regionTotal, name="Total region count", text=regionTotal),
              go.Bar(x=regions, y=regionBench, name="Bench count per region", text=regionBench),
              go.Bar(x=regions, y=regionRate, name="Employee % on Bench", text=regionRate)])
    region_plot.update_layout(title_text="Regional Bench Distribution: Region-Wide Percentage.", bargap=0.2,
                              bargroupgap=0)
    st.plotly_chart(region_plot)
    st.divider()
    designation_plot = px.histogram(dDesignation.str.strip(), x="Job_Title", title='Bench Count based on Designations.',
                                    text_auto=True).update_xaxes(categoryorder='total descending')
    st.plotly_chart(designation_plot)
    st.divider()
    pool_plot = px.histogram(pool_data.str.strip(), x="Pool", title='Bench Count based on Pool.',
                                    text_auto=True).update_xaxes(categoryorder='total descending')
    st.plotly_chart(pool_plot)
    st.divider()
    level_plot = px.histogram(dLevel.str.strip(), x="Level", title='Bench Count based on Experience Level.',
                              text_auto=True).update_xaxes(categoryorder='total descending')
    st.plotly_chart(level_plot)
    st.divider()
    category_plot = px.histogram(dCategory.str.strip(), x="Activity_Category", title='Bench Productivity Chart: '
                                                                                     'Activity-Based '
                                                                                     'Distribution.',
                                 text_auto=True).update_xaxes(categoryorder='total descending')
    st.plotly_chart(category_plot)
    st.divider()
    for pool in pool_data.dropna().unique():
        tenure_options.append(pool)
    tenure_selection = st.selectbox("**Enter your selection for Bench Tenure visualization.**", options=tenure_options)
    if tenure_selection == 'All':
        pool_employee = list(rawData['Employee_LName_FName'])
        pool_tenure = list(rawData['Time_On_Bench'])
    else:
        graph_data = rawData.query('Pool == @tenure_selection')
        pool_employee = list(graph_data['Employee_LName_FName'])
        pool_tenure = list(graph_data['Time_On_Bench'])
    for n in pool_tenure:
        timeCount = timeCount + 1
        if n < 45:
            benchEmployeeBlue.append(pool_employee[timeCount])
            benchTimeBlue.append(n)
        elif 45 <= n <= 90:
            benchEmployeeAmber.append(pool_employee[timeCount])
            benchTimeAmber.append(n)
        elif n > 90:
            benchEmployeeRed.append(pool_employee[timeCount])
            benchTimeRed.append(n)  
    benchTimeBar = go.Figure(
        data=[go.Bar(x=benchEmployeeRed, y=benchTimeRed, name="Tenure more than 90 days", text=benchTimeRed,
                     marker_color='FireBrick'),
              go.Bar(x=benchEmployeeAmber, y=benchTimeAmber, name="Tenure between 45 to 90 days", text=benchTimeAmber,
                     marker_color='DarkOrange'),
              go.Bar(x=benchEmployeeBlue, y=benchTimeBlue, name="Tenure less than 45 days", text=benchTimeBlue,
                     marker_color='Blue')])
    benchTimeBar.update_layout(title_text="Bench Tenure Summary - "+tenure_selection, bargap=0.2, bargroupgap=0, xaxis={'categoryorder':'total descending'})
    st.plotly_chart(benchTimeBar)