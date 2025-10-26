import cv2, os

fruit_dir = '/Users/lavanya/Library/Mobile Documents/com~apple~CloudDocs/Desktop/fruit_catch_game/fruits'
apple = cv2.imread(os.path.join(fruit_dir, 'apple.jpg'))
banana = cv2.imread(os.path.join(fruit_dir, 'banana.jpeg'))

print("Apple loaded:", apple is not None)
print("Banana loaded:", banana is not None)
