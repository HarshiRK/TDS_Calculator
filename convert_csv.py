import pandas as pd
import os

def convert():
    csv_path = r"c:\Users\intel\Desktop\tds_data.csv"
    dest_dir = r"c:\Users\intel\Desktop\TDS Calculator\backend\data"
    dest_path = os.path.join(dest_dir, "tds_rates.xlsx")
    
    # Create target directory if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)
    
    print(f"Reading and parsing CSV from {csv_path}...")
    
    parsed_rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        header_line = f.readline().strip()
        headers = [col.strip() for col in header_line.split(',')[:13]]
        
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(',')]
            
            # Strip any empty trailing columns resulting from excess commas
            while len(parts) > 13 and parts[-1] == '':
                parts.pop()
                
            if len(parts) == 13:
                row_dict = dict(zip(headers, parts))
                parsed_rows.append(row_dict)
            elif len(parts) > 13:
                # Re-assemble Payer Category (index 3)
                N = len(parts) - 13
                payer_category = ', '.join(parts[3 : 3 + N + 1])
                reconstructed = parts[0:3] + [payer_category] + parts[3 + N + 1:]
                row_dict = dict(zip(headers, reconstructed))
                parsed_rows.append(row_dict)
            else:
                # Under-sized row
                padded = parts + [''] * (13 - len(parts))
                row_dict = dict(zip(headers, padded))
                parsed_rows.append(row_dict)
                
    # Create DataFrame
    df = pd.DataFrame(parsed_rows)
    
    # Clean cells
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({'nan': '', 'None': '', '<NA>': ''})
        
    print(f"Writing parsed Excel to {dest_path}...")
    df.to_excel(dest_path, index=False, engine='openpyxl')
    print("Conversion completed successfully!")

if __name__ == "__main__":
    convert()
