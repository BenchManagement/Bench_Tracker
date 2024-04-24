import streamlit as st
import pandas as pd
from datetime import datetime

managerList=[]
employeeList=[]
employeeRemovalDateList=[]
count=-1
removalDateCount=-1
email=""
employee=""
employeeRemovalDate=""

st.set_page_config(page_title="Bench Details", page_icon="📖")
st.markdown("# Bench Details")
st.sidebar.header("Bench Details")

benchData = st.file_uploader("Choose the data file")
if(benchData):
    rawData = pd.read_excel(benchData, sheet_name="Bench_Activities")
    empNames = rawData['employeeName']
    activityCategories = rawData['activityCategory'].unique()
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
            #if conValidationDate.button('Send Emails to the respective Reporting Managers'):
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
        conEmployee.write(selectedRow['activityCategory'])
        conEmployee.write(selectedRow['activityDetails'])
        conEmployee.write(selectedRow['benchRemovalPlan'])
        conEmployee.write(selectedRow['benchRemovalDate'])