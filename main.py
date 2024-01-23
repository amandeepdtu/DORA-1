import streamlit as st
import pandas as pd

# Load your Excel data


general_excel_file_path = r"C:\Users\Amandeep Singh\Downloads\GT_DORA_Control_Gap_Assessment_Template_v.02 (1).xlsx"
specific_excel_file_path = r"C:\Users\Amandeep Singh\Downloads\Copy of DORA_per_Organisation_Template_v0.4.xlsx"

specific_excel_data = pd.ExcelFile(specific_excel_file_path)

# Get the list of sheet names for dropdown options from the specific requirements
specific_requirements_sheet = "Organisation List"  # Replace with your sheet name
specific_requirements_df = pd.read_excel(specific_excel_file_path)
dropdown_values = specific_requirements_df["Organisation Type"].tolist()

# Create a dropdown to select a value
selected_value = st.sidebar.selectbox("Select Orgnisation Type", dropdown_values)

# Display a specific column from the "General_Requirements" sheet
general_requirements_df = pd.read_excel(general_excel_file_path, sheet_name="DORA Requirements")
st.sidebar.table(general_requirements_df["DORA Requirement"])

# Check if the selected value exists in the specific requirements sheet
if selected_value in specific_excel_data.sheet_names:
    # Display a specific column from the specific requirements sheet
    selected_sheet_df = pd.read_excel(specific_excel_file_path, sheet_name=selected_value)
    st.table(selected_sheet_df["Article Text (i.e requirement)"])

else:
    st.info("Additional requirements don't exist for the selected organization type.")