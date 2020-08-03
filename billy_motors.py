"""
Billy Bass motors controlled by the Adafruit Motor HAT
"""

from adafruit_motorkit import MotorKit
import time
from threading import Timer

class BillyMotors:
    def __init__(self):
        self._kit = MotorKit()
        self._mouth_opened = False
        self._tail_active = False
        self._tail_timer = None
        self._mouth_timer = None
        self._tail_moves = 0

    def _move_mouth(self):
        if self._mouth_opened:
            self._kit.motor2.throttle = -1.0
            self._mouth_opened = False
        else:
            self._kit.motor2.throttle = 1.0
            self._mouth_opened = True
        self._mouth_timer = Timer(0.3, self._move_mouth)
        self._mouth_timer.start()

    def _move_tail(self):
        if self._tail_active:
            self._kit.motor3.throttle = 0
            self._tail_active = False
            self._tail_moves -= 1
        else:
            self._kit.motor3.throttle = 1.0
            self._tail_active = True
        if self._tail_moves > 0:
            self._tail_timer = Timer(0.4, self._move_tail)
            self._tail_timer.start()

    def listen(self):
        self._tail_moves = 2
        self._move_tail()
        pass

    def think(self):
        self._kit.motor1.throttle = 1.0
        pass

    def speak(self):
        self._move_mouth()

    def finish(self):
        if self._mouth_timer is not None:
            self._mouth_timer.cancel()
        if self._tail_timer is not None:
            self._tail_timer.cancel()

        self._kit.motor1.throttle = 0
        self._kit.motor2.throttle = 0
        self._kit.motor3.throttle = 0
        time.sleep(0.5)
        self._kit.motor1.throttle = None
        self._kit.motor2.throttle = None
        self._kit.motor3.throttle = None

    def test_motor(self, id):
        throttle = 1.0
        delay = 5.0
        if id == 1:
            self._kit.motor1.throttle = throttle
            time.sleep(delay)
            self._kit.motor1.throttle = 0

        elif id == 2:
            self._kit.motor2.throttle = -throttle
            time.sleep(delay/2)
            self._kit.motor2.throttle = throttle
            time.sleep(delay/2)
            self._kit.motor2.throttle = 0
        elif id == 3:
            self._kit.motor3.throttle = throttle
            time.sleep(delay)
            self._kit.motor3.throttle = 0
        else:
            print("Wrong ID")


billy = BillyMotors()

if __name__ == "__main__":

    # print("Listening", end="... ")
    # billy.listen()
    # time.sleep(5.0)
    # print("done")

    print("Thinking", end="... ")
    billy.think()
    time.sleep(5.0)
    print("done")

    print("Speaking", end="... ")
    billy.speak()
    time.sleep(5.0)
    print("done")

    billy.finish()
    print("Bye!")