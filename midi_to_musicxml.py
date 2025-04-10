from music21 import stream, note, chord, instrument, metadata
import mido

def parse_midi_file(file_path):
    midi = mido.MidiFile(file_path)
    tracks = []

    for i, track in enumerate(midi.tracks):
        notes = []
        current_time = 0

        for msg in track:
            current_time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                notes.append({
                    'note': msg.note,
                    'start': current_time,
                    'velocity': msg.velocity,
                    'instrument': track.name if track.name else 'Piano'
                })

        if notes:
            tracks.append(notes)

    return tracks

def midi_data_to_stream(parsed_data):
    score = stream.Score()

    for i, track in enumerate(parsed_data):
        part = stream.Part()
        instr_name = track[0].get('instrument', 'Piano')

        # Set instrument with fallback
        try:
            instr = instrument.fromString(instr_name)
        except:
            print(f"[!] Unknown instrument '{instr_name}' — defaulting to Piano")
            instr = instrument.Piano()

        part.insert(0, instr)

        last_time = 0
        for note_data in track:
            pitch = note_data['note']
            start = note_data['start']
            duration = start - last_time if start > last_time else 0.5

            n = note.Note(pitch)
            n.quarterLength = duration
            part.append(n)

            last_time = start

        score.append(part)

    # Add metadata
    score.insert(0, metadata.Metadata())
    score.metadata.title = "Converted MIDI"
    score.metadata.composer = "Zymphony"

    # ✅ Quantize to handle inexpressible durations
    score.quantize(quarterLengths=(0.25, 0.5, 1.0, 2.0))

    return score

def convert_to_musicxml(input_midi_path, output_file_path):
    print(f"[+] Parsing MIDI: {input_midi_path}")
    parsed = parse_midi_file(input_midi_path)

    print("[+] Converting to MusicXML stream...")
    m21_score = midi_data_to_stream(parsed)

    print(f"[+] Writing MusicXML to: {output_file_path}")
    m21_score.write("musicxml", fp=output_file_path)
    print("[✔] Conversion complete!")

if __name__ == "__main__":
    convert_to_musicxml("Never-Gonna-Give-You-Up-2.mid", "output_musicxml.xml")
