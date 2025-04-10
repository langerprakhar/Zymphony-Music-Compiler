from music21 import stream, note, instrument, metadata
import pretty_midi
import subprocess

def parse_midi_file(file_path):
    midi_data = pretty_midi.PrettyMIDI(file_path)
    tracks = []

    for instr in midi_data.instruments:
        notes = []
        for n in instr.notes:
            notes.append({
                'note': n.pitch,
                'start': n.start,
                'velocity': n.velocity,
                'instrument': instr.name if instr.name else 'Piano'
            })
        if notes:
            tracks.append(notes)

    return tracks

def midi_data_to_stream(parsed_data):
    score = stream.Score()

    for i, track in enumerate(parsed_data):
        part = stream.Part()
        instr_name = track[0].get('instrument', 'Piano')

        try:
            instr_obj = instrument.fromString(instr_name)
        except:
            print(f"[!] Unknown instrument '{instr_name}' — defaulting to Piano")
            instr_obj = instrument.Piano()

        part.insert(0, instr_obj)

        last_time = 0
        for note_data in track:
            pitch = note_data['note']
            start = note_data['start']
            duration = max(start - last_time, 0.5)

            # Snap duration to nearest readable sheet music values
            closest_durations = [0.25, 0.5, 1.0, 2.0]
            duration = min(closest_durations, key=lambda x: abs(x - duration))

            n = note.Note(pitch)
            n.quarterLength = duration
            part.append(n)

            last_time = start

        score.append(part)

    # Add metadata
    score.insert(0, metadata.Metadata())
    score.metadata.title = "Converted MIDI"
    score.metadata.composer = "Zymphony"

    return score

def convert_to_musicxml(input_midi_path, output_file_path):
    print(f"[+] Parsing MIDI: {input_midi_path}")
    parsed = parse_midi_file(input_midi_path)

    print("[+] Converting to MusicXML stream...")
    m21_score = midi_data_to_stream(parsed)

    print(f"[+] Writing MusicXML to: {output_file_path}")
    m21_score.write("musicxml", fp=output_file_path)

    # ✅ Auto-convert to PDF using MuseScore
    pdf_path = output_file_path.replace(".xml", ".pdf")
    try:
        subprocess.run(["mscore", output_file_path, "-o", pdf_path], check=True)
        print(f"[✔] PDF exported: {pdf_path}")
    except Exception as e:
        print(f"[!] MuseScore PDF export failed: {e}")

if __name__ == "__main__":
    convert_to_musicxml("Never-Gonna-Give-You-Up-2.mid", "output_musicxml.xml")
