import streamlit as st
import pandas as pd
import paramiko
from io import BytesIO

# Replace these variables with your actual EC2 details
ec2_host = "13.51.195.131"
ec2_user = "ubuntu"
ec2_private_key_path = "/home/ubuntu/DORA-1/DORA.pem"

# Define the remote file paths on your EC2 instance
remote_general_excel_file_path = "/home/ubuntu/DORA-1/GT_DORA_Control_Gap_Assessment_Template_v.02 (1).xlsx"
remote_specific_excel_file_path = "/home/ubuntu/DORA-1/Copy of DORA_per_Organisation_Template_v0.4.xlsx"

# Establish an SFTP connection to your EC2 instance
transport = paramiko.Transport((ec2_host, 22))
transport.connect(username=ec2_user, pkey=paramiko.RSAKey(filename=ec2_private_key_path))
sftp = paramiko.SFTPClient.from_transport(transport)

# Read Excel files into memory
general_excel_content = BytesIO(sftp.open(remote_general_excel_file_path).read())
specific_excel_content = BytesIO(sftp.open(remote_specific_excel_file_path).read())

# Load your Excel data
specific_excel_data = pd.ExcelFile(specific_excel_content)

# Get the list of sheet names for dropdown options from the specific requirements
specific_requirements_sheet = "Organisation List"  # Replace with your sheet name
specific_requirements_df = pd.read_excel(specific_excel_content, sheet_name=specific_requirements_sheet)
dropdown_values = specific_requirements_df["Organisation Type"].tolist()

# Create a dropdown to select a value
selected_value = st.sidebar.selectbox("Select Organization Type", dropdown_values)

# Display a specific column from the "General_Requirements" sheet
general_requirements_df = pd.read_excel(general_excel_content, sheet_name="DORA Requirements")
st.sidebar.table(general_requirements_df["DORA Requirement"])

# Check if the selected value exists in the specific requirements sheet
if selected_value in specific_excel_data.sheet_names:
    # Display a specific column from the specific requirements sheet
    selected_sheet_df = pd.read_excel(specific_excel_content, sheet_name=selected_value)
    st.table(selected_sheet_df["Article Text (i.e requirement)"])

else:
    st.info("Additional requirements don't exist for the selected organization type.")

# Close the SFTP connection
sftp.close()
transport.close()
