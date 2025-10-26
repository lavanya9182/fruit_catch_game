

```markdown
# 🍎 Fruit Catch Game 🍌

![Fruit Catch Game](https://img.shields.io/badge/Game-Version-1.0-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8-yellow)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-orange)
![pygame](https://img.shields.io/badge/Pygame-2.4-red)

---

## 🎮 About
**Fruit Catch Game** is an interactive **computer vision-based game** built with Python, OpenCV, MediaPipe, and Pygame.  
Players catch falling fruits using **hand gestures**, tracked by the webcam. The game features **real-time scoring**, **pop sounds** for caught fruits, and a **success sound** when the game ends.

---

## 🛠 Features
- Real-time hand tracking with **MediaPipe**
- Fruits spawn **randomly** and fall continuously
- **Score increases** when fruit is caught
- **Pop sound** on catching a fruit
- **Success sound** at the end of the game
- Responsive basket movement following your hand
- Adjustable **game duration** (15s, 30s, 60s)

---

## 📂 Folder Structure

```

fruit_catch_game/
│
├─ fruits/                  # Fruit images (apple.jpg, banana.jpeg)
├─ sounds/                  # Pop and success mp3 files
├─ fruit_detector.py        # Main game logic
├─ app.py                   # Flask app for frontend (optional)
├─ static/                  # Frontend CSS & JS (if using web)
└─ README.md                # Project documentation

````

---

## 💻 Requirements
- Python 3.9+
- OpenCV
- MediaPipe
- Numpy
- Pygame

**Install dependencies:**

```bash
pip install opencv-python mediapipe numpy pygame
````

---

## 🚀 How to Run

1. Clone the repository:

```bash
git clone https://github.com/yourusername/fruit_catch_game.git
cd fruit_catch_game
```

2. Run the game:

```
python backend/app.py
python fruit_detector.py
```

3. Move your hand in front of the webcam to control the basket.
4. Catch the falling fruits and enjoy the **pop sounds**!
5. Game ends after the selected duration and plays a **success sound**.

---

## 🎨 Frontend (Optional)

If integrated with Flask:

* `app.py` serves the video feed and game controls.
* HTML buttons allow starting the game for 15s, 30s, or 60s.
* Scores and winner are displayed in real-time.

---

## 🔊 Sounds

* **Pop Sound:** Played when a fruit is caught
  `pop-423717.mp3`
* **Success Sound:** Played when the game ends
  `success-1-6297.mp3`

---


## ❤️ Acknowledgements

* [OpenCV](https://opencv.org/)
* [MediaPipe](https://mediapipe.dev/)
* [Pygame](https://www.pygame.org/)
* Inspiration from fun interactive games for learning CV & Python.



