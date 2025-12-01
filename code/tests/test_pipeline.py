import sys, os

# Add the project root (CBSP_project/code) to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from harmony.midi_loader import load_notes_midi
from harmony.chord_extractor import extract_chords_from_file
from harmony.key_detection import detect_key_from_chords
from harmony.harmony_analysis import analyze_harmony

def test_pipeline(midi_path):
    print("----- TESTING MIDI LOADER -----")
    notes = load_notes_midi(midi_path)
    print(f"Loaded {len(notes)} notes.")
    print()

    # Determine TXT file path from your loader
    txt_path = midi_path.replace("/raw/", "/txt/").replace(".mid", ".txt")

    print("----- TESTING TXT IMPORT -----")
    chords = extract_chords_from_file(txt_path)
    print(f"Extracted {len(chords)} chord events.")
    print()

    print("----- TESTING KEY DETECTION -----")
    key = detect_key_from_chords(chords)
    print(f"Detected key: {key}")
    print()

    print("----- TESTING HARMONY ANALYSIS -----")
    harmony_chords = analyze_harmony(chords, key)

    for hc in harmony_chords:
        print(
            f"Time: {hc.chord.offset:5.2f} | "
            f"Chord: {hc.chord.pitchNames} | "
            f"RN: {hc.roman:5} | "
            f"Func: {hc.function:12} | "
            f"Emotion: {hc.emotion}"
        )

    print("\n----- DONE -----")


if __name__ == "__main__":
    midi_path = "code/data/MIDI/raw/35393.mid"   # <-- change this
    test_pipeline(midi_path)