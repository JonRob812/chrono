from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty

import paho.mqtt.client as mqtt
import time

# TODO change settings


class BackDrop(Widget):
    pass


def flash(back_drop, count, on, off):
    for i in range(count):
        back_drop.color = 1, 1, 1, 1
        time.sleep(on)
        back_drop.color = 0, 0, 0, 0
        time.sleep(off)


class Grid(Widget):
    fps_label = ObjectProperty(None)
    fps_hist = ObjectProperty(None)
    backdrop = ObjectProperty(None)
    average_label = ObjectProperty(None)

    all_shots = []

    def update_fps(self, fps):
        self.all_shots.append(float(fps))
        self.fps_label.text = fps
        self.show_shot_hist()
        self.avg_shots()
        flash(self.backdrop, 1, .1, .01)

    def show_shot_hist(self):
        self.fps_hist.text = "\n".join([str(shot) for shot in self.all_shots])

    def reset(self):
        self.all_shots = []
        self.show_shot_hist()
        self.avg_shots()

    def undo(self):
        if len(self.all_shots) > 0:
            self.all_shots.pop(-1)
            self.show_shot_hist()
            self.avg_shots()

    def avg_shots(self):
        if len(self.all_shots) > 1:
            self.average_label.text = f'avg: {round(sum(self.all_shots) / len(self.all_shots),2)}'
        else:
            self.average_label.text = f'avg: {round(sum(self.all_shots))}'



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
        return True

    def on_resume(self):
        self.connect_mqtt()


if __name__ == "__main__":
    ChronoApp().run()
