import sqlite3
import tkinter as tk

# Connect to the database (creates a new database if it doesn't exist)
conn = sqlite3.connect("bookmarks.db")

# Create a bookmarks table
conn.execute("""
    CREATE TABLE IF NOT EXISTS bookmarks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        url TEXT NOT NULL,
        tags TEXT
    )
""")

conn.commit()
conn.close()


def add_bookmark():
    title = entry_title.get()
    url = entry_url.get()
    tags = entry_tags.get().split(",")  # Split the input into a list of tags

    conn = sqlite3.connect("bookmarks.db")
    # Convert the list of tags to a comma-separated string for database storage
    tags_str = ",".join(tags)
    conn.execute("INSERT INTO bookmarks (title, url, tags) VALUES (?, ?, ?)", (title, url, tags_str))
    conn.commit()
    conn.close()

    # Clear the entry fields after adding a bookmark
    entry_title.delete(0, tk.END)
    entry_url.delete(0, tk.END)
    entry_tags.delete(0, tk.END)

def search_bookmarks():
    tags = entry_search_tags.get()

    conn = sqlite3.connect("bookmarks.db")
    cursor = conn.execute("SELECT title, url, tags, id FROM bookmarks WHERE tags LIKE ?", ('%' + tags + '%',))

    result_text.delete(1.0, tk.END)
    row_num = 0  # Initialize the row number

    for row in cursor:
        result_text.insert(tk.END, f"Title: {row[0]}\n\nURL: {row[1]}\n\nTags: {row[2]}\n")

        # Add an Edit button for each bookmark
        edit_button = tk.Button(app, text="Edit", command=lambda bookmark_id=row[3], title=row[0], url=row[1], tags=row[2]: edit_bookmark(bookmark_id, title, url, tags))
        edit_button.grid(row=row_num, column=3, padx=5, pady=5)

        row_num += 1  # Increment the row number for the next bookmark

    conn.close()


def edit_bookmark(bookmark_id, title, url, tags):
    # Open a new window for editing
    edit_window = tk.Toplevel(app)
    edit_window.title("Edit Bookmark")

    # Labels and Entry fields for editing
    tk.Label(edit_window, text="Title").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(edit_window, text="URL").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(edit_window, text="Tags").grid(row=2, column=0, padx=5, pady=5)

    entry_title = tk.Entry(edit_window)
    entry_url = tk.Entry(edit_window)
    entry_tags = tk.Entry(edit_window)

    entry_title.grid(row=0, column=1, padx=5, pady=5)
    entry_url.grid(row=1, column=1, padx=5, pady=5)
    entry_tags.grid(row=2, column=1, padx=5, pady=5)

    # Set the current values for editing
    entry_title.insert(0, title)
    entry_url.insert(0, url)
    entry_tags.insert(0, tags)

    # Save changes button
    def save_changes():
        new_title = entry_title.get()
        new_url = entry_url.get()
        new_tags = entry_tags.get()

        conn = sqlite3.connect("bookmarks.db")
        conn.execute("UPDATE bookmarks SET title=?, url=?, tags=? WHERE id=?", (new_title, new_url, new_tags, bookmark_id))
        conn.commit()
        conn.close()

        # Close the edit window after saving changes
        edit_window.destroy()

        # Optionally, you can refresh the search results or bookmarks list in the main window
        # based on the changes made.

    tk.Button(edit_window, text="Save Changes", command=save_changes).grid(row=3, column=0, columnspan=2, padx=5, pady=5)



# Create the main application window
app = tk.Tk()
app.title("Bookmark Manager")

# Labels
tk.Label(app, text="Title:").grid(row=0, column=0, padx=2, pady=2)
tk.Label(app, text="URL:").grid(row=1, column=0, padx=2, pady=2)
tk.Label(app, text="Tags:").grid(row=2, column=0, padx=2, pady=2)
tk.Label(app, text="Search by Tags:").grid(row=3, column=0, padx=5, pady=5)

# Entry fields
entry_title = tk.Entry(app)
entry_url = tk.Entry(app)
entry_tags = tk.Entry(app)
entry_search_tags = tk.Entry(app)

entry_title.grid(row=0, column=1, padx=2, pady=2)
entry_url.grid(row=1, column=1, padx=2, pady=2)
entry_tags.grid(row=2, column=1, padx=2, pady=2)
entry_search_tags.grid(row=3, column=1, padx=2, pady=2)

# Buttons
tk.Button(app, text="Add Bookmark", command=add_bookmark).grid(row=1, column=2, columnspan=1, padx=2, pady=2)
tk.Button(app, text="Search", command=search_bookmarks).grid(row=3, column=2, padx=2, pady=2)

# Result Text
result_text = tk.Text(app, width=60, height=10)
result_text.grid(row=5, column=0, columnspan=3, padx=2, pady=2)

app.mainloop()
