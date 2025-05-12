plt.figure(figsize=(6, 6))
plt.plot(x, y, color='cyan', lw=2)
plt.axis('off')
plt.title("Hydrogen Wave Radiation Pattern")
plt.gca().set_facecolor('black')
img_path = os.path.join(output_dir, "hydrogen_wave_pattern.png")
plt.savefig(img_path, dpi=300, bbox_inches='tight')
print(f"[✓] Saved: {img_path}")
return img_path

for i in range(3):
    midi.addTempo(i, 0, bpm)

# Track 0: Hydrogen tone
for i in range(16):
    midi.addNote(0, 0, 97, i * 0.5, 0.5, 70)

# Track 1: African drums (snare)
for i in range(8):
    for offset in [0.0, 0.25, 0.5, 0.75]:
        midi.addNote(1, 9, 38, i + offset, 0.1, 100)

# Track 2: String arpeggios
string_notes = [60, 64, 67]
for i in range(4):
    for j, note in enumerate(string_notes):
        midi.addNote(2, 2, note, i * 2 + j * 0.25, 1, 80)

midi_path = os.path.join(output_dir, "hydrogen_string_composition.mid")
with open(midi_path, "wb") as f:
    midi.writeFile(f)
print(f"[✓] Saved: {midi_path}")
return midi_path