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
expected = 'TBD'
altExpected = 'TDB'

st.set_page_config(page_title="Bench Details", page_icon="📖")
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
st.markdown("# Bench Details")
st.sidebar.header("Bench Details")

benchData = st.file_uploader("Choose the data file")
if(benchData):
    rawData = pd.read_excel(benchData, sheet_name="Bench")
    empNames = rawData['Employee_LName_FName']
    activityCategories = rawData['Activity_Category'].unique()
    with st.popover("**Associates with no Bench Removal Date assigned.**"):
        for name in list(rawData.query('Bench_Removal_Start_Date == @expected')['Employee_LName_FName']):
            st.write(name)
        for name in list(rawData.query('Bench_Removal_Start_Date == @altExpected')['Employee_LName_FName']):
            st.write(name)
    conValidationDate = st.container(border=True)
    conValidationDate.write("**Associate's activity End date Status Check:**")
    validationDate = conValidationDate.date_input("This section will pull out the list of associates (along with Manager Email IDs) with 'Activity End Date' as past date from the bench report on the basis of the date entered below.", value=None)
    if(validationDate):
        for dateValue in rawData['Activity_End']:
            count=count+1
            if isinstance(dateValue, datetime):
                if(dateValue.date() > validationDate):
                    pass
                else:
                    managerList.append(rawData["Manager_ Email_Id"][count])  
                    employeeList.append(rawData['Employee_LName_FName'][count])
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
    validationRemovalDate = conValidationRemovalDate.date_input("**Associate's Bench Removal date Status Check:**", value=None, help="This section provides list of employees with 'Bench Removal Date' as past date on the basis of reference date entered.")
    if(validationRemovalDate):
        for dateValue in rawData['Bench_Removal_Start_Date']:
            removalDateCount=removalDateCount+1
            if isinstance(dateValue, datetime):
                if(dateValue.date() > validationRemovalDate):
                    pass
                else: 
                    employeeRemovalDateList.append(rawData['Employee_LName_FName'][removalDateCount])
        for name in employeeRemovalDateList:
            employeeRemovalDate= employeeRemovalDate+str(name)+"\n"
        if(len(employeeRemovalDateList)>0):
            conValidationRemovalDate.download_button('Download Employee list who has a Removal Bench date as a past value.', data=employeeRemovalDate, file_name='Bench Removal Date - Update Required - Employees.txt', help="Provides a text file that contains the list of employees whose Bench Removal Date needs an update.")
        else:
            conValidationRemovalDate.write("Bench Removal dates are up to date. No action is required.")     
    conCategory = st.container(border=True)
    selectedCat = conCategory.selectbox('**Activity Category Lookup:**', activityCategories, index=None, placeholder='Choose an activity category...', help="Select an activity to know the list of associates working in the particular area.")
    if(selectedCat):
        conCategory.write('Below employees are working on '+selectedCat)
        conCategory.table(rawData.query('Activity_Category == @selectedCat')[['Employee_LName_FName', 'Activity_Details']])     
    conEmployee = st.container(border=True)
    selectedEmp = conEmployee.selectbox('**Associate Task Overview:**',empNames, index=None, placeholder='Choose an associate...', help="This section provides details about the work and activities of a selected associate.")
    if(selectedEmp):
        selectedRow = rawData.query("Employee_LName_FName == @selectedEmp")
        conEmployee.write(selectedRow['Activity_Category'])
        conEmployee.write(selectedRow['Activity_Details'])
        conEmployee.write(selectedRow['Bench_Removal_Planned_Project'])
        conEmployee.write(selectedRow['Bench_Removal_Start_Date'])
