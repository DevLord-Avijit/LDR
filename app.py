from flask import Flask, render_template, jsonify, Response
from camera_thread import CameraThread  # import the class

app = Flask(__name__)

# create and start the camera thread
camera = CameraThread()
camera.start()

# ------------------- Routes -------------------

@app.route('/')
def index():
    return render_template('index.html')  # your templates/index.html

@app.route('/status')
def status():
    """Old status route, can be used by existing frontend"""
    return jsonify({
        'laser_status': camera.status,
        'position': camera.position
    })

@app.route('/api/laser_status')
def api_laser_status():
    """New API for more sensitive frontend polling"""
    return jsonify({
        'laser_status': camera.status,
        'position': camera.position
    })

@app.route('/video_feed')
def video_feed():
    """Streaming video frames as MJPEG"""
    def generate():
        while True:
            frame = camera.get_frame()
            if frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Flask serves static files automatically from 'static/' folder
# e.g., your alarm.mp3 should be placed in project/static/alarm.mp3

# ------------------- Run App -------------------
if __name__ == '__main__':
    try:
        # run on all interfaces, accessible via LAN IP
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        camera.stop()
