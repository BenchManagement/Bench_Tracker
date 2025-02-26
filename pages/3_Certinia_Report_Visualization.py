import streamlit as st
import pandas as pd
import plotly.express as px

new_headers = ['pool','','employee_name', 'total_hours', 'start_date', 'end_date', 
               'region', 'role', 'automation', 'data', 'functional', 'performance',
               'manager_name', 'last_activity']
cell_buffer_value = None
table_pointer = None
st.set_page_config(page_title="Certinia Report Visualization", page_icon="📊")
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
st.markdown("# Certinia Report Visualization")
st.sidebar.header("Certinia Report Visualization")

certinia_raw_file = st.file_uploader("Upload the Certinia report")
if certinia_raw_file:
    raw_data = pd.read_excel(certinia_raw_file)
    clean = st.button("Clean the Certinia Report", icon="🧹")
    if clean:
        raw_data = raw_data.drop(raw_data.columns[0], axis=1)
        for index, row in raw_data.iterrows():
            if row.astype(str).str.contains("Project  ↑", case=False).any():
                table_pointer = index
        raw_data = raw_data.iloc[table_pointer+1:].reset_index(drop=True)
        raw_data.columns = new_headers
        st.toast('Updated column headers!', icon="☑️")
        raw_data = raw_data[~raw_data.apply(lambda row: row.astype(str).str.contains('|'.join(['Subtotal', 'Sum', 'Count', 'Confidential', 'Copyright','Total']), case=False).any(), axis=1)]
        raw_data = raw_data.loc[:, raw_data.columns.notna() & (raw_data.columns != '')]
        raw_data = raw_data.dropna(how='all')
        raw_data = raw_data[~raw_data['employee_name'].apply(lambda x: isinstance(x, int))]
        st.toast('Removed unnecessary rows and columns!', icon="🧹")
        for row_number in range(0, len(raw_data)):
            if pd.isna(raw_data.iloc[row_number, 0]):
                raw_data.iloc[row_number, 0] = cell_buffer_value
            else:
                cell_buffer_value = raw_data.iloc[row_number, 0]
        st.toast('Successfully made the data structured!', icon="☑️")
        st.divider()
        pool_data = raw_data['pool']
        pool_plot = px.histogram(pool_data.str.strip(), x="pool", title='Bench Count based on Pool.',
                                        text_auto=True).update_xaxes(categoryorder='total descending')
        st.plotly_chart(pool_plot)
        st.write("Note: One resource may belong to two or more pools.")
        st.divider()
        region_data = raw_data.drop_duplicates(subset=['employee_name', 'region'])
        region_plot = px.histogram(region_data, x="region", title='Bench Count based on Region.',
                                        text_auto=True).update_xaxes(categoryorder='total descending')
        st.plotly_chart(region_plot)
        st.divider()
        role_data = region_data = raw_data.drop_duplicates(subset=['employee_name', 'role'])
        designation_plot = px.histogram(role_data, x="role", title='Bench Count based on Designations.',
                                    text_auto=True).update_xaxes(categoryorder='total descending')
        st.plotly_chart(designation_plot)
        st.divider()