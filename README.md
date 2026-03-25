🎮 2048 Game (Advanced Pygame Edition)

A visually enhanced and feature-rich implementation of the classic **2048 game** built using **Python & Pygame**.

This version goes beyond the basic game by integrating:
- 🎨 Modern UI design  
- 💥 Particle effects  
- 🔊 Procedural audio system  
- ⚡ Smooth animations  


🚀 Features

 ✨ Core Gameplay
- Classic **4×4 grid-based mechanics**
- Tile merging & score tracking
- Win condition at **2048 tile**
- Game over detection system


🎨 Advanced UI/UX
- Smooth tile movement animations  
- Dynamic scaling & pulse effects  
- Gradient backgrounds with glowing panels  
- Interactive buttons (hover + press effects)  


🔊 Sound Effects System
- Fully **procedural audio generation** (no external files)  
- Sound feedback for:
  - Move  
  - Merge  
  - Spawn  
  - Win / Lose  
  - Button clicks  



### 💥 Visual Effects
- Particle explosion on tile merge  
- Floating score popups  
- Animated background motion  
- Win celebration effects  


📊 Score System
- Real-time score tracking  
- Persistent **Best Score** (stored locally)  


🖥️ Responsive Design
- Resizable game window  
- Adaptive board scaling  


🛠️ Tech Stack

| Category | Technology |
|--------|------------|
| Language | Python |
| Library | Pygame |
| Architecture | OOP + Game Loop |
| Audio | Procedural Synthesis |

📂 Project Structure

bash
📦 2048-Game
 ┣ 📜 main.py
 ┣ 📜 best_score.txt
 ┗ 📜 README.md

▶️ How to Run

1️⃣ Install Dependencies
pip install pygame

2️⃣ Run the Game
python main.py

🎮 Controls

Key	Action
⬅️	Move Left
➡️	Move Right
⬆️	Move Up
⬇️	Move Down
R	Restart Game
Mouse	UI interactions

🧠 Game Logic Overview

The board is represented as a 2D grid (4×4)
Tiles slide in the selected direction
Matching tiles merge into double value

After each move:

A new tile (2 or 4) spawns randomly

Game ends when:

No empty cells
No possible merges

🔊 Audio System

This project uses a procedural sound engine instead of external audio files.

It generates sound using:

Sine waves
Frequency modulation
Exponential decay

✅ Benefits

Lightweight
Fully self-contained
Technically advanced

🎨 UI Highlights

Gradient background rendering
Glass-like tile design
Glow effects for best score
Animated overlays:
🏆 Win screen
❌ Game Over screen

📸 Screenshots

🎮 Gameplay UI

High-performance 2048 game featuring glassmorphism UI, particle effects, and procedural animations.

<img src="https://github.com/user-attachments/assets/a6de582b-b11d-4eaa-8a8f-c37f50b709de" width="400"/>

❌ Game Over Screen

Dynamic overlay with smooth transitions, layered UI effects, and persistent best score tracking.

<img src="https://github.com/user-attachments/assets/2fd67373-a7b7-4d01-b8d5-1a7b958296e6" width="400"/>

📈 Future Improvements

🔢 Larger grid sizes (5×5, 6×6)
↩️ Undo functionality
🌐 Leaderboard system
📱 Mobile/touch support
🤖 AI auto-play mode
📜 License

This project is licensed under the MIT License.

🙌 Author

Himagiri Siddesh M

⭐ Show Your Support

If you like this project:

⭐ Star the repo
🍴 Fork it
📢 Share it
