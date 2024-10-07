
import os
import pdfplumber # type: ignore
import re
import pandas as pd
import shutil

#Extract text from a PDF
def extractContentPdf(pdfPath):
    allText = "" 
    with pdfplumber.open(pdfPath) as pdf:
        for pageNum in range(len(pdf.pages)):
            page = pdf.pages[pageNum]
            text = page.extract_text()
            if text:
                allText += text  
            else:
                print(f"No text extracted from page {pageNum + 1} in {pdfPath}")
    if allText:
        #print(f"Extracted content: {allText}")
        print("Extracted content: ")
    else:
        print(f"No text extracted from: {pdfPath}") 
    return allText

#Find app type 
def extractText(content, pattern):
    match = re.search(pattern, content)
    if match:
        firstLine = match.group(1)  
        secondLine = match.group(2)
        return firstLine + " " + secondLine
    return None

#Rename file
def renameFile(oldPath, newName):
    new_path = os.path.join(os.path.dirname(oldPath), f"{newName}.pdf")
    os.rename(oldPath, new_path)
    print(f"Renamed '{oldPath}' to '{new_path}'")

def append_to_csv(existing_csv_path, new_string):
    # Check if the file exists
    if not os.path.isfile(existing_csv_path):
        print(f"File '{existing_csv_path}' does not exist.")
        return
    # Convert the new string to a DataFrame
    new_data = pd.DataFrame([[new_string]], columns=['extracted_text'])  # You can modify the column name if needed
    # Append the new data to the existing CSV file
    new_data.to_csv(existing_csv_path, mode='a', header=False, index=False)  # Append without writing the header
    print(f"Appended '{new_string}' to '{existing_csv_path}'.")


#Extract content and rename
def extractRename(directory, pattern):
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdfPath = os.path.join(directory, filename)
            print(f"Pdf path '{pdfPath}'")
            content = extractContentPdf(pdfPath)
            extractedText = extractText(content, pattern)
            if extractedText:
                print(f"Text extracted: {extractedText}")
                append_to_csv(existing_csv_path, extractedText)
                cleanedName = re.sub(r'[^\w\s-]', '', extractedText).strip().replace(' ', '_')
                renameFile(pdfPath, cleanedName)
                print(f"cleanedName '{pdfPath}'")
                cenas = f"/Users/soniadias/Library/CloudStorage/OneDrive-Checkmarx/Clients/BP/automations/getDataFromPDF/TM copy/{cleanedName}.pdf"
                shutil.move(cenas, destination)
            else:
                print(f"Pattern not found in '{filename}'")
                os.remove(pdfPath)


directoryPath = os.path.join(os.getcwd(),"TM copy")
pattern = r'Executable etc\s*((?:[\w-]+\s*)*?)(?:\n)((?:[\w-]+\s*)*?)'
existing_csv_path  = '/Users/soniadias/Library/CloudStorage/OneDrive-Checkmarx/Clients/BP/automations/getDataFromPDF/output.csv'
destination = '/Users/soniadias/Library/CloudStorage/OneDrive-Checkmarx/Clients/BP/automations/getDataFromPDF/processed'
extractRename(directoryPath, pattern)

