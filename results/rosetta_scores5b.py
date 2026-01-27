#!/usr/bin/env python3

import os
import math
import csv
import shutil


def safe_float(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return float('nan')


def load_scores():
    data = []
    header = []

    for filename in os.listdir('.'):
        if filename.endswith('.sc') and filename.startswith('score'):
            with open(filename, 'r') as f:
                for line in f:
                    if line.startswith('#') or not line.strip():
                        continue
                    tokens = line.strip().split()
                    if not header:
                        header = tokens
                        continue
                    if tokens[0] == header[0] or len(tokens) < len(header):
                        continue

                    row = {}
                    for i, col in enumerate(header):
                        if col == 'description':
                            row[col] = tokens[-1].strip()
                        else:
                            row[col] = safe_float(tokens[i])
                    data.append(row)
    return data, header


def main():
    CST_CUTOFF = 1.0
    TOP_N = 10
    OUTPUT_DIR = "logs_best_interfaces"

    data, header = load_scores()
    if not data:
        print("❌ No valid score data found.")
        return

    # Find interface energy key
    interf_E_key = next((k for k in header if k.startswith("SR_3_interf_E_1_2")), None)
    if interf_E_key is None:
        print("❌ Missing SR_3_interf_E_1_2 field.")
        return

    # Apply constraint filter
    filtered = [row for row in data if row.get('all_cst', float('inf')) < CST_CUTOFF]
    print(f"✅ Passed constraint filter (all_cst < {CST_CUTOFF}): {len(filtered)} entries")

    if not filtered:
        print("❌ No entries passed constraint filter.")
        return

    # Sort by interface energy and take top N
    filtered.sort(key=lambda r: r.get(interf_E_key, float('inf')))
    top_final = filtered[:TOP_N]
    print(f"✅ Selected top {TOP_N} by best {interf_E_key} (interface energy)")

    # Output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    csv_out = os.path.join(OUTPUT_DIR, "top_interfaces.csv")
    txt_out = os.path.join(OUTPUT_DIR, "top_interfaces.txt")

    # Write CSV
    with open(csv_out, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for row in top_final:
            writer.writerow({k: row.get(k, 'NA') for k in header})

    # Write plain text summary
    with open(txt_out, 'w') as f:
        summary_fields = ['description', 'total_score', 'all_cst', interf_E_key]
        header_line = '  '.join(f"{k:<20}" for k in summary_fields)
        f.write(header_line + "\n")

        for row in top_final:
            line = '  '.join(
                f"{row[k]:<20.2f}" if isinstance(row.get(k), float) and not math.isnan(row[k])
                else f"{row.get(k, 'NA'):<20}"
                for k in summary_fields
            )
            f.write(line + "\n")

    # Copy PDBs
    copied = []
    for row in top_final:
        pdb_name = row['description']
        if not pdb_name.endswith('.pdb'):
            pdb_name += '.pdb'
        if os.path.exists(pdb_name):
            shutil.copy2(pdb_name, os.path.join(OUTPUT_DIR, pdb_name))
            copied.append(pdb_name)
        else:
            print(f"⚠️ PDB not found: {pdb_name}")

    print("\n📝 Output written to:")
    print(f" - CSV: {csv_out}")
    print(f" - TXT summary: {txt_out}")
    if copied:
        print(f"📁 Copied {len(copied)} PDB files to {OUTPUT_DIR}/")
    else:
        print(f"⚠️ No PDBs copied.")

if __name__ == "__main__":
    main()
