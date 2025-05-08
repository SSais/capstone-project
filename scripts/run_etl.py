from etl.extract.extract import extract_data

print("Starting data extraction...")
extracted_data = extract_data()
print("Data extraction complete.")

print("Starting data transformation...")
# transformed_data = transformed_data(extracted_data)
print("Data transformation complete.")

print("Loading data into Pagilla database...")
# Load data into database
print("Data loading complete.")


print("Streamlit can be run with updated data")