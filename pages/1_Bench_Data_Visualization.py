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
    rawData = pd.read_excel(benchData, sheet_name="Bench_Activities")
    fixedData = pd.read_excel(benchData, sheet_name="Fixed_Data")
    empNames = rawData['employeeName']
    dCategory = rawData['activityCategory']
    dLevel = rawData['level']
    dDesgination = rawData['designation']
    regions = fixedData['regionName']
    regionTotal = list(fixedData['regionTotal'])
    conSummary = st.container(border=True)
    for i in list(rawData['benchRemovalDate']):
        if isinstance(i,str):
            removalDate+=i
    conSummary.write("**Total number of employees on Bench** - "+str(empNames.index.size))
    conSummary.write('**Total number of employees with Bench Removal Date** - '+str((empNames.index.size)-removalDate.count('tentative')-removalDate.count(expected)-removalDate.count(altExpected)))
    conSummary.write('**Total number of employees with Tentative Bench Removal Date** - '+ str(removalDate.count('tentative')))
    conSummary.write('**Total number of employees who needs a Bench Removal Date (TBD)** - '+ str(removalDate.count(expected)+ removalDate.count(altExpected)))
    with st.popover("**Employees who need a Bench Removal Date**"):
        for name in list(rawData.query('benchRemovalDate == @expected')['employeeName']):
            st.write(name)
        for name in list(rawData.query('benchRemovalDate == @altExpected')['employeeName']):
            st.write(name)
    for r in regions:
        regionBench.append(list(rawData['region']).count(r))
    for i in range(len(regionBench)):
        regionRate.append(round((regionBench[i]*100)/regionTotal[i],2))
    regionPie = px.pie(rawData['region'], values=regionBench, names=regions, title='Bench Report Summary based on Region - PLATO Level')
    st.plotly_chart(regionPie)
    regionBar = go.Figure(
        data=[go.Bar(x=regions, y=regionTotal, name="Total region count", text=regionTotal),
            go.Bar(x=regions, y=regionBench, name="Bench count per region", text=regionBench),
            go.Bar(x=regions, y=regionRate, name="Employee % on Bench", text=regionRate)])
    regionBar.update_layout(title_text="Region-wise Bench summary - Region Level", bargap=0.2, bargroupgap=0)
    st.plotly_chart(regionBar)
    designationPie = px.histogram(dDesgination, x = "designation", title='Bench Report Summary based on Designation', text_auto=True).update_xaxes(categoryorder='total descending')
    st.plotly_chart(designationPie)
    levelPie = px.histogram(dLevel, x = "level", title='Bench Report Summary based on experience level', text_auto=True).update_xaxes(categoryorder='total descending')
    st.plotly_chart(levelPie)
    categoryBar = px.histogram(dCategory, x = "activityCategory", title='Bench Report Summary based on Activity Category', text_auto=True).update_xaxes(categoryorder='total descending')
    st.plotly_chart(categoryBar)
    for n in list(rawData['benchTime']):
        timeCount=timeCount+1
        if (n < 45):
            benchEmployeeBlue.append(rawData['employeeName'][timeCount])
            benchTimeBlue.append(n)
        elif (45 <= n <= 90):
            benchEmployeeAmber.append(rawData['employeeName'][timeCount])
            benchTimeAmber.append(n)
        elif (n > 90):
            benchEmployeeRed.append(rawData['employeeName'][timeCount])
            benchTimeRed.append(n)
    benchTimeBar = go.Figure(
        data=[go.Bar(x=benchEmployeeRed, y=benchTimeRed, name="Tenure more than 90 days", text=benchTimeRed, marker_color='FireBrick'),
            go.Bar(x=benchEmployeeAmber, y=benchTimeAmber, name="Tenure between 45 to 90 days", text=benchTimeAmber, marker_color='DarkOrange'),
            go.Bar(x=benchEmployeeBlue, y=benchTimeBlue, name="Tenure less than 45 days", text=benchTimeBlue, marker_color='Blue')])
    benchTimeBar.update_layout(title_text="Bench Tenure Summary", bargap=0.2, bargroupgap=0)
    st.plotly_chart(benchTimeBar)