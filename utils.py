import pandas as pd

# Utility to safely extract text from a tag
def get_text_from_tag(tag):
    if tag:
        return tag.get_text().strip()
    return None

# Utility to safely extract a link from a tag
def get_link_from_tag(tag):
    if tag and tag.find('a'):
        return tag.find('a')['href']
    return None

def get_tag_from_field(row, field):
    return row.find('td', class_=field)

# Utility to safely extract the ID from a link in a field
# Assumes ID is the last part of the link (e.g., "/v4/node/83945" -> 83945)
def get_id_from_link(link):
    if link:
        return link.split('/')[-1]  # Assuming the ID is at the end of the URL
    return None

# Utility to extract the ID from a field if it contains a link
def get_id_from_field(row, field):
    tag = get_tag_from_field(row, field)
    link = get_link_from_tag(tag)
    return get_id_from_link(link)

# Utility to extract text from a field
def get_text_from_field(row, field):
    tag = get_tag_from_field(row, field)
    return get_text_from_tag(tag)

# Utility to extract a link from a field
def get_link_from_field(row, field):
    tag = get_tag_from_field(row, field)
    return get_link_from_tag(tag)

# Function to save data to CSV
def save_to_csv(filename, columns, data_list):
    if len(data_list) == 0:
        print(f"No data was retrieved...")
        return
    
    try:
        # Check if the number of columns matches the length of each row in data_list
        if all(len(row) == len(columns) for row in data_list):
            df = pd.DataFrame(data_list, columns=columns)
            df.to_csv(f'./scraped_data/{filename}', index=False)
            print(f"Data saved to scraped_data/{filename}.")
        else:
            raise ValueError("Number of columns does not match the number of items in data_list rows.")
    except (ValueError, IndexError) as e:
        print(f"Error while saving the data to scraped_data/: {e}")
