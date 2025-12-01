from music21 import chord
from harmony.midi_loader import extract_notes_from_file

def group_notes_by_time(notes, resolution=0.25):
    """
    Group notes that start at approximately the same time.
    `resolution` = time window size (in quarter notes).
    """

    # Sort notes by start time
    notes = sorted(notes, key=lambda n: n.offset)

    groups = []
    current_group = []
    current_start = None

    for n in notes:
        if current_start is None:
            # First note in first group
            current_start = n.offset
            current_group.append(n)
            continue

        # If note starts close enough to the current group time → same chord
        if abs(n.offset - current_start) < resolution:
            current_group.append(n)
        else:
            # New group starts
            groups.append(current_group)
            current_group = [n]
            current_start = n.offset

    # Add last group
    if current_group:
        groups.append(current_group)

    return groups

from music21 import note, chord

def extract_chords_from_file(path):
    # 1. Read notes from TXT file
    notes = []

    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            fields = line.split(", ")

            data = {}
            for field in fields:
                key, value = field.split(": ")
                data[key] = value

            n = note.Note(data['pitch_name'])
            n.pitch.midi = int(data['midi'])
            n.offset = float(data['start'])
            n.duration.quarterLength = float(data['duration'])
            notes.append(n)

    # 2. Group notes by offset (start time)
    chords_dict = {}
    for n in notes:
        offset = round(n.offset, 4)  # avoid precision errors

        if offset not in chords_dict:
            chords_dict[offset] = []

        chords_dict[offset].append(n)

    # 3. Convert groups to music21 Chords
    chord_objects = []
    for offset, note_group in sorted(chords_dict.items()):
        pitches = [n for n in note_group]
        c = chord.Chord(pitches)
        c.offset = offset
        chord_objects.append(c)

    return chord_objects
