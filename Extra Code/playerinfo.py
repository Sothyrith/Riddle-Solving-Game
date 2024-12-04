import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('riddledb.db')
c = conn.cursor()
conn = sqlite3.connect('riddledb.db')
c = conn.cursor()

import sqlite3

# Connect to the SQLite database
c.execute("SELECT id, username, classic_completion, best_score FROM playerinfo")

# Fetch all rows
rows = c.fetchall()

# Check if the table has any data
if rows:
    # Print a header row for better readability
    print(f"{'ID':<5} {'Username':<20} {'Completion':<15} {'Best Score':<10}")
    print('-' * 60)

    # Loop through each row and print the data
    for row in rows:
        # Assuming your table has columns: id, username, classic_completion, best_score
        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<15} {row[3]:<10}")
else:
    print("No data found in the playerinfo table.")

# Close the connection
conn.close()
