🎮 2048 Game (Advanced Pygame Edition)

A visually enhanced and feature-rich implementation of the classic 2048 game built using Python & Pygame.
This version goes beyond the basic game by including smooth animations, particle effects, sound design, and modern UI elements.

🚀 Features

✨ Core Gameplay

Classic 4×4 grid-based 2048 mechanics
Tile merging and score tracking
Win condition at 2048 tile
Game over detection

🎨 Advanced UI/UX

Smooth tile movement animations
Dynamic scaling and pulse effects
Gradient backgrounds and glowing UI panels
Interactive buttons with hover & press effects

🔊 Sound Effects System

Procedurally generated sounds (no external files needed)
Move, merge, spawn, win, and lose sounds
Button interaction audio feedback

💥 Visual Effects

Particle explosion on tile merge
Floating score popups
Background motion effects
Win celebration animation

📊 Score System

Real-time score tracking
Persistent Best Score (saved locally)

🖥️ Responsive Window

Resizable screen
Adaptive board scaling

🛠️ Tech Stack

Language: Python
Library: Pygame
Concepts Used:
Object-Oriented Programming (OOP)
Game loop architecture
Animation interpolation
Procedural audio generation
Event-driven programming

📂 Project Structure

📦 2048-Game
 ┣ 📜 main.py (your code file)
 ┣ 📜 best_score.txt (auto-generated)
 ┗ 📜 README.md
 
▶️ How to Run

1. Install Dependencies
pip install pygame
2. Run the Game
python main.py

🎮 Controls

Key	Action
⬅️ Left Arrow	Move Left
➡️ Right Arrow	Move Right
⬆️ Up Arrow	Move Up
⬇️ Down Arrow	Move Down
R	Restart Game
Mouse Click	Button interactions

🧠 Game Logic Overview

The board is represented as a 2D grid (4×4).
Tiles slide in the chosen direction.
Matching tiles merge into one with double value.
After each move:
A new tile (2 or 4) spawns randomly.
Game ends when:
No empty cells AND
No possible merges.

🔊 Audio System

Instead of using external audio files, this project:

Generates sounds using mathematical wave functions
Uses:
Sine waves
Frequency modulation
Decay envelopes

This makes the project:
✔ Lightweight
✔ Fully self-contained
✔ Technically impressive

🎨 UI Highlights

Gradient background rendering
Glass-like tiles with lighting effects
Glow effects for best score
Animated overlays for:
🏆 Win screen
❌ Game Over screen
📸 Screenshots

1. High-performance 2048 game featuring glassmorphism UI, particle effects, and procedural animations built entirely with Python & Pygame.
<img width="648" height="940" alt="image" src="https://github.com/user-attachments/assets/a6de582b-b11d-4eaa-8a8f-c37f50b709de" />

2.Dynamic Game Over overlay featuring smooth transitions, layered UI effects, and persistent best score tracking.
<img width="650" height="932" alt="image" src="https://github.com/user-attachments/assets/2fd67373-a7b7-4d01-b8d5-1a7b958296e6" />



📈 Future Improvements

Add different grid sizes (5×5, 6×6)
Add undo feature
Add leaderboard system
Mobile/touch support
AI auto-play mode

📜 License

This project is open-source and available under the MIT License.

🙌 Author

Himagiri Siddesh M

⭐ Show Your Support

If you like this project:

👉 Star the repo
👉 Share with others
👉 Fork and build your own version
