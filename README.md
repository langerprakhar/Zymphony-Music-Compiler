# 🎼 Zymphony Music Compiler

Zymphony is a Python-based music compiler that converts **MIDI files** into structured **MusicXML** and **sheet music (PDF)** formats using `pretty_midi`, `music21`, and `MuseScore`.

---

## ✨ Features

- 🎹 Parses standard `.mid` files
- 🎼 Converts to MusicXML (standard notation format)
- 🖨️ Automatically generates sheet music in PDF format via MuseScore
- 🎻 Detects instruments and notes with velocity & timing info
- 💡 Clean, readable code with expandable architecture (text/audio-to-MIDI in future)

---

## 🖥️ Demo

**Input MIDI File** →  
`Never-Gonna-Give-You-Up-2.mid`

**Output Sheet Music** →  
`output_musicxml.pdf`

<p align="center">
  <img src="docs/demo_sheet_music.png" width="600" alt="Generated Sheet Music Preview">
</p>

---

## ⚙️ How It Works

```bash
python midi_to_musicxml.py
