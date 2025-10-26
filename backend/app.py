'''from flask import Flask, render_template, Response
from utils.fruit_detector import FruitGame
import cv2

app = Flask(__name__)
game = FruitGame()

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    while True:
        frame = game.get_frame()
        if frame is None:
            continue
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, threaded=True, port=8000)
'''

'''from flask import Flask, render_template, Response, request, jsonify
from utils.fruit_detector import FruitGame
import cv2

app = Flask(__name__)
game = FruitGame()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    duration = int(request.form['duration'])
    game.start_game(duration)
    return jsonify({'status': 'started', 'duration': duration})

def generate_frames():
    while True:
        frame = game.get_frame()
        if frame is None:
            continue
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, port=5001)
'''







from flask import Flask, render_template, Response, request, jsonify
from utils.fruit_detector import FruitGame  # your fixed detector
import threading
import time

app = Flask(__name__)
game = FruitGame()  # background thread starts automatically

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game')
def start_game():
    seconds = int(request.args.get('time', 15))
    game.start(seconds)
    return '',204


@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            frame = game.get_frame()
            if frame is None:
                continue  # never block
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/end_game')
def end_game():
    return jsonify({'score': game.score})

if __name__ == "__main__":
    app.run(debug=True, threaded=True, port=5001)
