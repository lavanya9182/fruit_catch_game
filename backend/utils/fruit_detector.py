import cv2
import mediapipe as mp
import numpy as np
import os
import random
import threading
import time
from playsound import playsound
import pygame
pygame.mixer.init()


class FruitGame:
    def __init__(self):
        # Webcam
        self.pop_sound = pygame.mixer.Sound('/Users/lavanya/Library/Mobile Documents/com~apple~CloudDocs/Desktop/fruit_catch_game/pop-423717.mp3')
        self.game_over_sound = pygame.mixer.Sound('/Users/lavanya/Library/Mobile Documents/com~apple~CloudDocs/Desktop/fruit_catch_game/success-1-6297.mp3')


        self.cap = cv2.VideoCapture(0)
        self.frame = np.zeros((480, 640, 3), dtype=np.uint8)

        # Basket
        self.basket_x, self.basket_y = 320, 400
        self.score = 0

        # Game timer
        self.running = False
        self.start_time = None
        self.duration = 0

        # Hand detection
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1)

        # Fruits
        fruit_dir = '/Users/lavanya/Library/Mobile Documents/com~apple~CloudDocs/Desktop/fruit_catch_game/fruits'
        self.fruits_imgs = []
        for fname in ['apple.jpg', 'banana.jpeg']:
            path = os.path.join(fruit_dir, fname)
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if img is not None:
                self.fruits_imgs.append(cv2.resize(img, (80, 80)))

        if not self.fruits_imgs:
            raise ValueError("No fruit images found!")

        # Active fruits
        self.active_fruits = []

        # Start background capture loop
        threading.Thread(target=self._capture_loop, daemon=True).start()

    # Background capture + update loop
    def _capture_loop(self):
        while True:
            try:
                ret, frame = self.cap.read()
                if not ret or frame is None:
                    continue

                frame = cv2.flip(frame, 1)
                
                # Hand detection (update basket position)
                try:
                    frame = self._detect_hand(frame)
                except Exception as e:
                    print("Hand detection error:", e)

                if self.running:
                    # Randomly spawn fruits continuously
                    if random.random() < 0.05:  # Adjust spawn rate here
                        self._spawn_fruit(frame)

                    # Update fruits (movement + collision)
                    try:
                        self._update_fruits(frame)
                    except Exception as e:
                        print("Fruit update error:", e)

                    # Stop game if duration is over
                    if time.time() - self.start_time >= self.duration:
                        self.running = False
                        self.game_over_sound.play()


                # Draw basket and score
                try:
                    frame = self._draw_basket(frame)
                except Exception as e:
                    print("Draw basket error:", e)

                # Always update self.frame — this keeps video feed continuous
                self.frame = frame

            except Exception as e:
                print("Capture loop error:", e)
                # Keep last frame instead of resetting to black
                continue


    # Return current frame as JPEG
    def get_frame(self):
        try:
            ret, jpeg = cv2.imencode('.jpg', self.frame)
            if not ret:
                return cv2.imencode('.jpg', np.zeros((480,640,3), dtype=np.uint8))[1].tobytes()
            return jpeg.tobytes()
        except Exception as e:
            print("get_frame error:", e)
            return cv2.imencode('.jpg', np.zeros((480,640,3), dtype=np.uint8))[1].tobytes()

    # Start game
    def start(self, duration):
        self.running = True
        self.start_time = time.time()
        self.duration = duration
        self.score = 0
        self.active_fruits.clear()
        print(f"✅ Game started for {duration} seconds")

    # Hand detection
    def _detect_hand(self, frame):
        try:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb)
            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]
                self.basket_x = int(hand.landmark[9].x * frame.shape[1])
        except Exception as e:
            print("Hand detection error:", e)
        return frame

    # Draw basket and score
    def _draw_basket(self, frame):
        try:
            cv2.rectangle(frame, (self.basket_x-50, self.basket_y-20),
                          (self.basket_x+50, self.basket_y+20), (0,255,0), -1)
            cv2.putText(frame, f"Score: {self.score}", (10,30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        except Exception as e:
            print("Draw basket error:", e)
        return frame

    # Spawn new fruit
    def _spawn_fruit(self, frame):
        fruit_img = random.choice(self.fruits_imgs)
        x = random.randint(50, frame.shape[1]-50)
        speed = random.randint(5, 10)
        self.active_fruits.append({'img': fruit_img, 'x': int(x), 'y': 0, 'speed': int(speed),'caught': False })

    # Update fruits safely
    def _update_fruits(self, frame):
        new_active_fruits = []

        for fruit in self.active_fruits:
            fruit['y'] += fruit['speed']
            self._overlay(frame, fruit['img'], fruit['x'], fruit['y'])

            center_x = int(fruit['x'] + fruit['img'].shape[1] // 2)
            center_y = int(fruit['y'] + fruit['img'].shape[0] // 2)

            # Check collision
            if not fruit.get('caught', False):
                if (self.basket_x-50 < center_x < self.basket_x+50 and
                    self.basket_y-20 < center_y < self.basket_y+20):
                    self.score += 1
                    fruit['caught'] = True  # Mark as caught
                    self.pop_sound.play()


                    continue  # Skip adding to new_active_fruits, effectively removing it

            # Remove if out of screen
            if fruit['y'] > frame.shape[0]:
                continue  # Skip adding, so it disappears

            # Otherwise, keep the fruit in active list
            new_active_fruits.append(fruit)

        self.active_fruits = new_active_fruits


        
    # Overlay fruit with alpha
    def _overlay(self, bg, ov, x, y):
        try:
            h, w = ov.shape[:2]
            if x < 0: x = 0
            if y < 0: y = 0
            if x + w > bg.shape[1]: w = bg.shape[1] - x
            if y + h > bg.shape[0]: h = bg.shape[0] - y
            if w <= 0 or h <= 0: return
            ov = ov[:h, :w]

            if ov.shape[2] == 4:
                alpha_s = ov[:,:,3]/255.0
                alpha_l = 1-alpha_s
                for c in range(3):
                    bg[y:y+h, x:x+w, c] = alpha_s*ov[:,:,c] + alpha_l*bg[y:y+h, x:x+w, c]
            else:
                bg[y:y+h, x:x+w] = ov
        except Exception as e:
            print("Overlay error:", e)
