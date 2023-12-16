import openpyxl
from tamil_transliteration import transliteration

# Open the Excel file
wb = openpyxl.load_workbook("/Users/asampathkuma/Downloads/Project4000/tamilwords.xlsx")
sheet = wb["Sheet1"]  # Replace "Sheet1" with your actual sheet name

# Define the transliteration system
system = "tamilnet"  # Choose from "tamilnet", "itrans", "harvard-kyoto"

# Loop through each row in column A1
for row in sheet["A"]:
    # Get the Tamil word
    tamil_word = row.value

    # Transliterate the word
    english_word = transliterate(tamil_word, system=system)

    # Print the transliterated text
    print(english_word)

# Close the Excel file
wb.close()
