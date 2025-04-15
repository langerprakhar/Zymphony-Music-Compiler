import pretty_midi
def parse_midi(file_path):
    """
    Parses a MIDI file and extracts notes, instruments, and timing information.
    Returns a structured dictionary.
    """
    try:
        midi_data = pretty_midi.PrettyMIDI(file_path)
        structured_output = []

        for instrument in midi_data.instruments:
            notes_list = []
            for note in instrument.notes:
                notes_list.append({
                    "pitch": note.pitch,
                    "start": note.start,
                    "end": note.end,
                    "velocity": note.velocity
                })
            structured_output.append({
                "instrument": instrument.name,
                "is_drum": instrument.is_drum,
                "program": instrument.program,
                "notes": notes_list
            })

        return structured_output

    except Exception as e:
        print(f"[ERROR] Failed to parse MIDI: {e}")
        return None

# Example usage
if __name__ == "__main__":
    midi_file = "test.mid"  # Place a MIDI file in your project folder
    result = parse_midi(midi_file)

    if result:
        for instrument in result:
            print(f"\nInstrument: {instrument['instrument']}")
            for note in instrument['notes'][:5]:  # show first 5 notes only
                print(note)
