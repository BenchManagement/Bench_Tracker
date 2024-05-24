import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

timeCount=-1
employeeRemovalDateList=[]
regionBench = []
regionRate = []
removalDate = ""
expected = 'TBD'
altExpected = 'TDB'
benchTimeRed=[]
benchEmployeeRed=[]
benchTimeAmber=[]
benchEmployeeAmber=[]
benchTimeBlue=[]
benchEmployeeBlue=[]

st.set_page_config(page_title="Bench Data Visualization", page_icon="📈")
st.markdown("# Bench Data Visualization")
st.sidebar.header("Bench Data Visualization")

benchData = st.file_uploader("Choose the data file")
if(benchData):
    rawData = pd.read_excel(benchData, sheet_name="Bench")
    fixedData = pd.read_excel(benchData, sheet_name="Region_Count")
    empNames = rawData['Employee_LName_FName']
    dCategory = rawData['Activity_Category']
    dLevel = rawData['Level']
    dDesgination = rawData['Job_Title']
    regions = fixedData['Region']
    regionTotal = list(fixedData['Region_Total'])
    conSummary = st.container(border=True)
    for i in list(rawData['Bench_Removal_Start_Date']):
        if isinstance(i,str):
            removalDate+=i
    conSummary.write("**Total number of employees on Bench** - "+str(empNames.index.size))
    conSummary.write('**Total number of employees with Bench Removal Date** - '+str((empNames.index.size)-removalDate.count('tentative')-removalDate.count(expected)-removalDate.count(altExpected)))
    conSummary.write('**Total number of employees with Tentative Bench Removal Date** - '+ str(removalDate.count('tentative')))
    conSummary.write('**Total number of employees who needs a Bench Removal Date (TBD)** - '+ str(removalDate.count(expected)+ removalDate.count(altExpected)))
    for r in regions:
        regionBench.append(list(rawData['Region']).count(r))
    for i in range(len(regionBench)):
        regionRate.append(round((regionBench[i]*100)/regionTotal[i],2))
    regionPie = px.pie(rawData['Region'], values=regionBench, names=regions, title='Regional Bench Distribution: PLATO-Wide Percentage.')
    st.plotly_chart(regionPie)
    regionBar = go.Figure(
        data=[go.Bar(x=regions, y=regionTotal, name="Total region count", text=regionTotal),
            go.Bar(x=regions, y=regionBench, name="Bench count per region", text=regionBench),
            go.Bar(x=regions, y=regionRate, name="Employee % on Bench", text=regionRate)])
    regionBar.update_layout(title_text="Regional Bench Distribution: Region-Wide Percentage.", bargap=0.2, bargroupgap=0)
    st.plotly_chart(regionBar)
    designationPie = px.histogram(dDesgination, x = "Job_Title", title='Bench Count based on Designations.', text_auto=True).update_xaxes(categoryorder='total descending')
    st.plotly_chart(designationPie)
    levelPie = px.histogram(dLevel, x = "Level", title='Bench Count based on Experience Level.', text_auto=True).update_xaxes(categoryorder='total descending')
    st.plotly_chart(levelPie)
    categoryBar = px.histogram(dCategory, x = "Activity_Category", title='Bench Productivity Chart: Activity-Based Distribution.', text_auto=True).update_xaxes(categoryorder='total descending')
    st.plotly_chart(categoryBar)
    for n in list(rawData['Time_On_Bench']):
        timeCount=timeCount+1
        if (n < 45):
            benchEmployeeBlue.append(rawData['Employee_LName_FName'][timeCount])
            benchTimeBlue.append(n)
        elif (45 <= n <= 90):
            benchEmployeeAmber.append(rawData['Employee_LName_FName'][timeCount])
            benchTimeAmber.append(n)
        elif (n > 90):
            benchEmployeeRed.append(rawData['Employee_LName_FName'][timeCount])
            benchTimeRed.append(n)
    benchTimeBar = go.Figure(
        data=[go.Bar(x=benchEmployeeRed, y=benchTimeRed, name="Tenure more than 90 days", text=benchTimeRed, marker_color='FireBrick'),
            go.Bar(x=benchEmployeeAmber, y=benchTimeAmber, name="Tenure between 45 to 90 days", text=benchTimeAmber, marker_color='DarkOrange'),
            go.Bar(x=benchEmployeeBlue, y=benchTimeBlue, name="Tenure less than 45 days", text=benchTimeBlue, marker_color='Blue')])
    benchTimeBar.update_layout(title_text="Bench Tenure Summary.", bargap=0.2, bargroupgap=0)
    st.plotly_chart(benchTimeBar)