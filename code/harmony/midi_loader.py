from music21 import converter, note, chord
from pathlib import Path
import subprocess 
import os

def load_notes_midi(path):
    """
    Load a MIDI file and return a list of notes.
    Each note is returned as a dictionary:
    {
        'pitch_name': 'C4',
        'midi': 60,
        'start': 0.0,
        'duration': 1.0
    }
    """

    try:
        stream = converter.parse(path).flatten()
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        print(f"Explanation: We cannot load the {path} file")
    except TypeError as tp_error:
        print(tp_error)
        print(f"Explanation: The {path} file is not a MIDI file")

    notes_list = []

    for element in stream:
        # Case 1: Single note
        if isinstance(element, note.Note):
            notes_list.append({
                'pitch_name': element.nameWithOctave,
                'midi': element.pitch.midi,
                'start': float(element.offset),
                'duration': float(element.quarterLength)
            })

        # Case 2: A chord (convert to multiple notes)
        elif isinstance(element, chord.Chord):
            for n in element.notes:
                notes_list.append({
                    'pitch_name': n.nameWithOctave,
                    'midi': n.pitch.midi,
                    'start': float(element.offset),
                    'duration': float(element.quarterLength)
                })

    txt_path = get_txt_path(path)

    with open(txt_path, "a") as f:
        for n in notes_list:
            f.write(
            f"pitch_name: {n['pitch_name']}, "
            f"midi: {n['midi']}, "
            f"start: {n['start']}, "
            f"duration: {n['duration']}\n"
        )
            
    return notes_list




def get_txt_path(path):
    """
    Returns a path to create a txt file
    containing the notes of a song
    """
    p = Path(path)

    # data/MIDI/raw/"...".mid -> data/MIDI/txt/"...".txt
    txt_dir = p.parent.parent / "txt"
    txt_dir.mkdir(parents=True, exist_ok=True)

    return txt_dir / (p.stem + ".txt")



def extract_notes_from_file(path):
    """
    returns a list of notes from a file
    """
    notes = []

    with open(path, "r") as f:
        for line in f:
            # Remove newlines and extra spaces
            line = line.strip()

            # Split into fields
            fields = line.split(", ")

            # Convert each field into key/value
            data = {}
            for field in fields:
                key, value = field.split(": ")
                data[key] = value

            # Create the music21 note
            n = note.Note(data['pitch_name'])
            n.pitch.midi = int(data['midi'])
            n.offset = float(data['start'])
            n.duration.quarterLength = float(data['duration'])

            notes.append(n)

    return notes