"""
Hands-free Voice Assistant with Snowboy and Alexa Voice Service. The wake-up keyword is "alexa"

Requirement:
    pip install avs
    pip install voice-engine
"""


import time
import logging
from voice_engine.source import Source
from voice_engine.kws import KWS
from voice_engine.doa_respeaker_2mic_hat import DOA
from avs.alexa import Alexa
from billy_motors import billy
import RPi.GPIO as GPIO

def main():
    logging.basicConfig(level=logging.INFO)

    src = Source(rate=16000, frames_size=320)
    doa = DOA()
    kws = KWS(model='./Billy_Bass.pmdl', sensitivity=0.5)
    alexa = Alexa()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN)

    alexa.state_listener.on_listening = billy.listen
    alexa.state_listener.on_thinking = billy.think
    alexa.state_listener.on_speaking = billy.speak
    alexa.state_listener.on_finished = billy.finish

    src.link(doa)
    src.link(kws)
    kws.link(alexa)

    def on_detected(keyword):
        logging.info('detected {} from direction {}'.format(keyword, doa.get_direction()))
        alexa.listen()

    def on_button(button):
        logging.info("Button {} pressed".format(button))
        alexa.listen()

    kws.set_callback(on_detected)
    GPIO.add_event_detect(17, GPIO.RISING, callback=on_button)

    src.recursive_start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    src.recursive_stop()


if __name__ == '__main__':
    main()
