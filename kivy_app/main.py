from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
import paho.mqtt.client as mqtt
import time


class Grid(Widget):
    fps_label = ObjectProperty(None)
    fps_hist = ObjectProperty(None)

    def update_fps(self, fps):
        self.fps_label.text = fps
        self.fps_hist.text += fps + '\n'


class ChronoApp(App):
    client = mqtt.Client('chronoapp' + str(time.time_ns()))

    def fps_cb(self, client, usr_data, msg):
        fps = msg.payload.decode()
        self.root.update_fps(fps)

    def build(self):
        grid = Grid()
        self.connect_mqtt()
        return grid

    def connect_mqtt(self):
        self.client.connect('192.168.0.60')
        self.client.message_callback_add('chrono', self.fps_cb)
        self.client.subscribe('chrono/#')
        self.client.loop_start()

    def on_pause(self):
        self.client.disconnect()

    def on_resume(self):
        self.connect_mqtt()


if __name__ == "__main__":
    ChronoApp().run()
