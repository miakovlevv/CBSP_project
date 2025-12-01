class HarmonyChord:
    def __init__(self, chord_obj, key):
        self.chord = chord_obj                   # music21 chord
        self.key = key

        # Roman numeral in context
        from music21 import roman
        self.roman = roman.romanNumeralFromChord(chord_obj, key).figure

        # Functional role
        self.function = self.compute_function()

        # Emotional attributes
        self.emotion = self.compute_emotion()

    def compute_function(self):
        rn = self.roman

        if rn.startswith(("I", "iii", "vi")):
            return "tonic"
        elif rn.startswith(("ii", "IV")):
            return "predominant"
        elif rn.startswith(("V", "vii")):
            return "dominant"
        else:
            return "other"

    def compute_emotion(self):
        # Simple examples — you can expand this
        if self.function == "tonic":
            return "stable"
        if self.function == "dominant":
            return "tense"
        if self.function == "predominant":
            return "moving"
        return "ambiguous"

    def __repr__(self):
        return f"{self.roman} ({self.function}, {self.emotion})"
