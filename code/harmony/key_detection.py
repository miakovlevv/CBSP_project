from music21 import converter, key, stream as m21stream

def detect_key_from_stream(midi_stream):
    """
    Detect the key from a full music21 stream.
    Uses the Krumhansl-Schmuckler algorithm.
    """
    try:
        return midi_stream.analyze("Krumhansl")
    except Exception as e:
        print("Key detection failed:", e)
        return None


def detect_key_from_chords(chord_list):
    """
    Convert a list of music21 Chord objects into a temporary stream
    and detect the key from that stream.
    """
    if not chord_list:
        print("No chords provided for key detection.")
        return None
    
    s = m21stream.Stream()

    for c in chord_list:
        s.append(c)

    try:
        return s.analyze("Krumhansl")
    except Exception as e:
        print("Key detection failed:", e)
        return None


def detect_key_from_midi(path):
    """
    Load a MIDI file directly and detect its key.
    Useful for debugging or independent use.
    """
    try:
        midi_stream = converter.parse(path)
        return midi_stream.analyze("Krumhansl")
    except Exception as e:
        print("Could not detect key from MIDI file:", path, e)
        return None
