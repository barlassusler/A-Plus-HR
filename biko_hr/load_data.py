import pandas as pd
from biko_hr.models import JobCategory, Position

# Load the Excel file
file_path = 'static/pozisyon_isimleri.xlsx'
data = pd.read_excel(file_path)

# Iterate through the rows and insert data into the database
for _, row in data.iterrows():
    category_name = row['Category']
    position_title = row['Position']

    # Get or create the category
    category, _ = JobCategory.objects.get_or_create(category_name=category_name)

    # Get or create the position
    Position.objects.get_or_create(position=position_title, category=category)

print("Data successfully imported.")
