from harmony.HarmonyChord import HarmonyChord

def analyze_harmony(chord_list, key_obj):
    """
    Convert a list of music21 Chord objects into HarmonyChord objects.
    """

    analyzed = []

    for c in chord_list:
        try:
            hc = HarmonyChord(c, key_obj)
            analyzed.append(hc)
        except Exception as e:
            print("Error analyzing chord:", c, e)

    return analyzed