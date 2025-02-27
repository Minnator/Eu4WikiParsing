from bs4 import BeautifulSoup
import csv

def parse_html_table(file_path, output_csv=None):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    tables = soup.find_all('table')
    if not tables:
        raise ValueError("No tables found in the HTML file.")

    all_headers = None
    all_rows = []

    for table in tables:
        headers = [th.get_text(strip=True) for th in table.find_all('th')]

        if all_headers is None:
            all_headers = headers
        elif all_headers != headers:
            continue  # Skip tables with different headers

        for tr in table.find_all('tr')[1:]:  # Skip header row
            cells = [td.get_text(strip=True) for td in tr.find_all('td')]
            if cells:
                all_rows.append(cells)

    # Optionally save to CSV
    if output_csv:
        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(all_headers)
            writer.writerows(all_rows)

    return all_headers, all_rows


def format_modifiers(data, modifier_index, type_index):
    modifier_dict = "public static readonly Dictionary<string, ModifierValueType> CountryModifiersDict = new()\n{\n"

    for row in data:
        modifier = row[modifier_index]
        effect_type = row[type_index]
        modifier_dict += f'   {{ "{modifier}", ModifierValueType.{effect_type} }},\n'

    modifier_dict += "};\n"

    return modifier_dict

def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)  # Read header row
        rows = list(reader)  # Read all data rows
    return headers, rows

def read_modifiers_from_csv(csv_file):
    headers, data = read_csv(csv_file)

    # Find the indexes for "Modifier" and "Effect Type"
    modifier_index = headers.index("Modifier")
    type_index = headers.index("Effect type")
    
    # Format the modifiers
    formatted_modifiers = format_modifiers(data, modifier_index, type_index)
    
    # save to file
    with open('modifiers.cs', 'w', encoding='utf-8') as f:
        f.write(formatted_modifiers)

# Example usage
parse_html_table('trigger_table.html', 'trigger_output.csv')
parse_html_table('effect_table.html', 'effect_output.csv')
parse_html_table('scope_table.html', 'scope_output.csv')
parse_html_table('modifier_table.html', 'modifier_output.csv')

read_modifiers_from_csv('modifier_output.csv')