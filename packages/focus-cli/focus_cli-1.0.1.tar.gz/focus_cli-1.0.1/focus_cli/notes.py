from utils import load_json, save_json

# Path to notes.json to track notes
notes_file = "data/notes.json"

def add_note(note_content):
    """Adds a new note."""
    notes = load_json(notes_file)
    
    note_id = len(notes) + 1  # Generate unique note ID
    note = {
        "id": note_id,
        "content": note_content,
    }
    
    notes[note_id] = note
    save_json(notes_file, notes)
    
    print(f"Note added! Note ID: {note_id}")

def list_notes():
    """Lists all notes."""
    notes = load_json(notes_file)
    
    if not notes:
        print("No notes available.")
        return
    
    print("Notes:")
    for note in notes.values():
        print(f"ID: {note['id']} - {note['content']}")

def delete_note(note_id):
    """Deletes a note by ID."""
    notes = load_json(notes_file)
    
    if note_id not in notes:
        print(f"Note with ID {note_id} not found.")
        return
    
    note = notes.pop(note_id)
    save_json(notes_file, notes)
    
    print(f"Note '{note['content']}' deleted.")
