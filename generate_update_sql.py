#!/usr/bin/env python3
"""
Generate SQL to update existing entries with Interactive and Plenary passes
based on the seminar attendees CSV file.
"""

import csv

csv_file = "seminar attendees.csv"

# Read CSV and generate UPDATE statements
updates = []

with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row['Name']
        id_number = row['ID_Number']
        ex1 = row['Exhibition_Day_1'].lower() == 'yes'
        ex2 = row['Exhibition_Day_2'].lower() == 'yes'
        interactive = row['Interactive_Sessions'].lower() == 'yes'
        plenary = row['Plenary'].lower() == 'yes'

        # Generate UPDATE statement
        sql = f"""UPDATE entries
SET exhibition_day1 = {str(ex1).lower()},
    exhibition_day2 = {str(ex2).lower()},
    interactive_sessions = {str(interactive).lower()},
    plenary = {str(plenary).lower()},
    updated_at = NOW()
WHERE id_number = '{id_number}';
"""
        updates.append(sql)

# Write all SQL statements to a file
with open('update_seminar_passes.sql', 'w') as f:
    f.write("-- SQL to update seminar attendee passes\n")
    f.write("-- Generated from: seminar attendees.csv\n")
    f.write("-- Total updates: {}\n\n".format(len(updates)))
    f.write("\n".join(updates))

print(f"✅ Generated SQL file: update_seminar_passes.sql")
print(f"📊 Total UPDATE statements: {len(updates)}")
print("\nNext step: Run this SQL in Supabase SQL Editor")
