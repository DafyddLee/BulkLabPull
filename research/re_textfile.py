import re
import pandas as pd
from datetime import datetime

def extract_lab_results_from_text(text):
    # Define patterns to extract relevant data for all tests
    date_pattern = r"Date collected\s+(\d{2}/\d{2}/\d{4})"
    episode_pattern = r"Episode\s+\S+\s+Date collected\s+(\d{2}/\d{2}/\d{4}).?Authorised by.?\n\n(.*?)\n\n"
    
    # Original tests patterns
    test_patterns = {
        'Creatinine': r"Creatinine\s+(\d+)\s+L\s+umol/L", ## Got to make sure that is the right Creatinine
        'eGFR (MDRD)': r"eGFR \(MDRD formula\)\s+([^ ]+)",
        'eGFR (CKD-EPI)': r"eGFR \(CKD-EPI formula\)\s+(\d+)"
        ## Need to add - Histopath as well as FBC, Hb , Urinalysis
    }

    # Use a dictionary to store results
    lab_results = {}

    # Find all dates and extract original tests results associated with them
    dates = re.findall(date_pattern, text)
    for date in dates:
        if date not in lab_results:
            lab_results[date] = {}
        for test, pattern in test_patterns.items():
            # Ensure only the first occurrence of a test result for a date is taken
            if test not in lab_results[date]:
                test_result = re.search(date + r".*?" + pattern, text, re.DOTALL)
                lab_results[date][test] = test_result.group(1) if test_result else "N/A"
                # print(f"Date: {date}, Test: {test}, Result: {lab_results[date][test]}")  # Print statement for debugging

    # Convert lab results to a DataFrame
    df = pd.DataFrame.from_dict(lab_results, orient='index')

    # Check for any empty rows (dates without any test results) and remove them
    df.dropna(how='all', inplace=True)

    # Transpose the DataFrame to have tests as rows and dates as columns
    df_transposed = df.transpose()

    return df_transposed

def process_text_file_to_excel(file_path,id):
    # Read the content of the text file
    with open(file_path, 'r', encoding='utf-8') as file:
        text_content = file.read()
    
    # Extract lab results
    transposed_df = extract_lab_results_from_text(text_content)
    
    # Generate a timestamped output file name
    output_file_name = "sheets\\" + id + '.xlsx'

    
    # Save the transposed DataFrame to an Excel file on the Desktop
    transposed_df.to_excel(output_file_name, index=True)
    print(f'Lab results have been saved to {output_file_name}')
