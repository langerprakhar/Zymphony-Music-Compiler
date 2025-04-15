import librosa
import numpy as np
import pretty_midi
import os

def mp3_to_midi(mp3_path, midi_path):
    print(f"Processing '{mp3_path}'...")

    # Load audio
    y, sr = librosa.load(mp3_path)

    # Extract pitches and magnitudes
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

    # Create MIDI object
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano

    threshold = 0.1  # Magnitude threshold
    frame_duration = librosa.frames_to_time(1, sr=sr)

    prev_note = None
    start_time = 0

    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        mag = magnitudes[index, t]

        if mag < threshold:
            if prev_note is not None:
                end_time = t * frame_duration
                note = pretty_midi.Note(velocity=100, pitch=prev_note, start=start_time, end=end_time)
                instrument.notes.append(note)
                prev_note = None
        else:
            current_note = librosa.hz_to_midi(pitch)
            current_note = int(np.round(current_note))

            if prev_note is None:
                start_time = t * frame_duration
                prev_note = current_note
            elif current_note != prev_note:
                end_time = t * frame_duration
                note = pretty_midi.Note(velocity=100, pitch=prev_note, start=start_time, end=end_time)
                instrument.notes.append(note)
                start_time = t * frame_duration
                prev_note = current_note

    # Add final note
    if prev_note is not None:
        end_time = len(y) / sr
        note = pretty_midi.Note(velocity=100, pitch=prev_note, start=start_time, end=end_time)
        instrument.notes.append(note)

    midi.instruments.append(instrument)
    midi.write(midi_path)
    print(f"✅ MIDI saved to: {midi_path}")

# Run interactively
if __name__ == "__main__":
    print("🎵 MP3 to MIDI Converter")

    mp3_path = input("Enter the path to your MP3 file: ").strip()
    while not os.path.isfile(mp3_path):
        print("❌ File not found. Please try again.")
        mp3_path = input("Enter the path to your MP3 file: ").strip()

    midi_path = input("Enter output MIDI filename (e.g., output.mid): ").strip()
    if not midi_path.endswith(".mid"):
        midi_path += ".mid"

    mp3_to_midi(mp3_path, midi_path)
