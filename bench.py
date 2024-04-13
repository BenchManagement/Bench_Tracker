import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go
count=-1
removalDateCount=-1
timeCount=-1
managerList=[]
employeeList=[]
employeeRemovalDateList=[]
regionBench = []
regionRate = []
email=""
employee=""
employeeRemovalDate=""
removalDate = ""
expected = 'TBD'
benchTimeRed=[]
benchEmployeeRed=[]
benchTimeAmber=[]
benchEmployeeAmber=[]
benchTimeGreen=[]
benchEmployeeGreen=[]
st.title("PLATO - Bench Activity Summary")
benchData = st.file_uploader("Choose the data file")
if(benchData):
    rawData = pd.read_excel(benchData, sheet_name="Bench_Activities")
    fixedData = pd.read_excel(benchData, sheet_name="Fixed_Data")
    empNames = rawData['employeeName']
    activityCategories = rawData['activityCategory'].unique()
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
    conSummary.write('**Total number of employees with Bench Removal Date** - '+str((empNames.index.size)-removalDate.count('tentative')-removalDate.count(expected)))
    conSummary.write('**Total number of employees with Tentative Bench Removal Date** - '+ str(removalDate.count('tentative')))
    conSummary.write('**Total number of employees who needs a Bench Removal Date (TBD)** - '+ str(removalDate.count(expected)))
    with st.popover("**Employees who need a Bench Removal Date**"):
        for name in list(rawData.query('benchRemovalDate == @expected')['employeeName']):
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
            benchEmployeeGreen.append(rawData['employeeName'][timeCount])
            benchTimeGreen.append(n)
        elif (45 <= n <= 90):
            benchEmployeeAmber.append(rawData['employeeName'][timeCount])
            benchTimeAmber.append(n)
        elif (n > 90):
            benchEmployeeRed.append(rawData['employeeName'][timeCount])
            benchTimeRed.append(n)
    benchTimeBar = go.Figure(
        data=[go.Bar(x=benchEmployeeRed, y=benchTimeRed, name="Tenure more than 90 days", text=benchTimeRed, marker_color='FireBrick'),
            go.Bar(x=benchEmployeeAmber, y=benchTimeAmber, name="Tenure between 45 to 90 days", text=benchTimeAmber, marker_color='DarkOrange'),
            go.Bar(x=benchEmployeeGreen, y=benchTimeGreen, name="Tenure less than 45 days", text=benchTimeGreen, marker_color='Lime')])
    benchTimeBar.update_layout(title_text="Bench Tenure Summary", bargap=0.2, bargroupgap=0)
    st.plotly_chart(benchTimeBar)
    conValidationDate = st.container(border=True)
    validationDate = conValidationDate.date_input("**Activity End Date - Enter the validation date:**", value=None, help="This feature helps to validate the Bench Report's End Date values. To set a reference date please input this field.")
    if(validationDate):
        for dateValue in rawData['endDate']:
            count=count+1
            if(dateValue.date() > validationDate):
                pass
            else:
                managerList.append(rawData["managerID"][count])  
                employeeList.append(rawData['employeeName'][count])
        for id in list(set(managerList)):
            email= email+str(id)+";"+" "
        for name in list(set(employeeList)):
            employee= employee+str(name)+"\n"
        if(len(list(set(managerList)))>0):
            conValidationDate.write("Detected "+str(len(list(set(managerList))))+" Managers. Download the below file to get their contact details.")
            conValidationDate.download_button('Download Email IDs of Reporting Managers', data=email, file_name='Bench Report Update Required - Managers.txt', help="Provides a text file that contains Email IDs of Managers who needs to update their Associate's Bench Activity details.")
            conValidationDate.download_button('Download Employee list', data=employee, file_name='Bench Report Update Required - Employees.txt', help="Provides a text file that contains the list of employees whose End Date needs an update.")
        else:
            conValidationDate.write("Bench Report is updated. No action is required.")
    conValidationRemovalDate = st.container(border=True)
    validationRemovalDate = conValidationRemovalDate.date_input("**Bench Removal - Enter the validation date:**", value=None, help="This feature helps to validate the Bench Removal Date values. To set a reference date please input this field.")
    if(validationRemovalDate):
        for dateValue in rawData['benchRemovalDate']:
            removalDateCount=removalDateCount+1
            if isinstance(dateValue, datetime):
                if(dateValue.date() > validationRemovalDate):
                    pass
                else: 
                    employeeRemovalDateList.append(rawData['employeeName'][removalDateCount])
        for name in employeeRemovalDateList:
            employeeRemovalDate= employeeRemovalDate+str(name)+"\n"
        if(len(employeeRemovalDateList)>0):
            conValidationRemovalDate.download_button('Download Employee list who has a Removal Bench date as a past value.', data=employeeRemovalDate, file_name='Bench Removal Date - Update Required - Employees.txt', help="Provides a text file that contains the list of employees whose Bench Removal Date needs an update.")
        else:
            conValidationRemovalDate.write("Bench Removal dates are up to date. No action is required.")     
    conCategory = st.container(border=True)
    selectedCat = conCategory.selectbox('**Select an activity.**', activityCategories, index=None, placeholder='Choose an option...', help="Provides a list of employees who are performing similar activity.")
    if(selectedCat):
        conCategory.write('Below employees are working on '+selectedCat)
        conCategory.table(rawData.query('activityCategory == @selectedCat')[['employeeName', 'activityDetails']])     
    conEmployee = st.container(border=True)
    selectedEmp = conEmployee.selectbox('**Select an employee.**',empNames, index=None, placeholder='Choose an employee...', help="Provides the details of an employee that is available on the Bench Report.")
    if(selectedEmp):
        selectedRow = rawData.query('employeeName == @selectedEmp')
        conEmployee.write(selectedEmp+"'s present activity is found to be - "+ selectedRow['activityCategory'])
        conEmployee.write("To be specific it is - "+ selectedRow['activityDetails'])
        conEmployee.write("Bench Removal plan: "+selectedRow['benchRemovalPlan'])
        conEmployee.write(selectedRow['benchRemovalDate'])