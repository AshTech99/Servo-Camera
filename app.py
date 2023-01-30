import cv2
from flask import Flask, render_template, Response
import RPi.GPIO as GPIO

app = Flask(__name__)

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pin for servo motor
servo_pin = 21

# Set up servo motor on GPIO pin
GPIO.setup(servo_pin, GPIO.OUT)
servo = GPIO.PWM(servo_pin, 50)
servo.start(7.5)

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    # Open USB camera
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Convert the frame to JPEG format
        ret, jpeg = cv2.imencode('.jpg', frame)

        # Return the current frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/<servo_pos>')
def move_servo(servo_pos):
    servo.ChangeDutyCycle(float(servo_pos))
    return "Servo position set to {}".format(servo_pos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True, debug=False)
