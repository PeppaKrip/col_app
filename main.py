from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from PIL import Image as Pimage
from os import remove

__version__ = '0.0.1'

touch_s = []
a1 = 0
a2 = 0
a3 = 0


class ScrButton(Button):
    def __init__(self, screen, direction='right', goal='main', **kvargs):
        super().__init__(**kvargs)
        self.screen = screen
        self.direction = direction
        self.goal = goal

    def on_press(self):
        self.screen.manager.transition.direction = self.direction
        self.screen.manager.current = self.goal


class FirstScr(Screen):
    def __init__(self, **kvargs):
        super().__init__(**kvargs)
        main_layout = BoxLayout(orientation='vertical')
        btn_layout = BoxLayout(orientation='horizontal')
        btn_layout.size_hint = (1, .2)
        self.cameraObject = Camera()
        self.btn_cam = ScrButton(self, direction='up', goal='second', text="Take Photo", on_press=self.TakePhoto)
        btn_layout.add_widget(self.btn_cam)
        main_layout.add_widget(self.cameraObject)
        main_layout.add_widget(btn_layout)
        self.add_widget(main_layout)

    def TakePhoto(self, *args):
        try:
            remove('photo.png')
            self.cameraObject.export_to_png('./photo.png')
        except:
            self.cameraObject.export_to_png('./photo.png')


class SecondScr(Screen):
    global touch_s

    def __init__(self, **kvargs):
        super().__init__(**kvargs)
        self.m_layout = BoxLayout(orientation='vertical')
        self.anc_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        self.lab = Label(text='Click to activate screen')
        self.anc_layout.add_widget(self.lab)
        self.add_widget(self.anc_layout)
        self.add_widget(self.m_layout)

    def on_touch_down(self, touch):
        global a1
        self.anc_layout.remove_widget(self.lab)
        image_png = Image(source='photo.png')
        image_png.reload()
        if a1 == 0:
            self.m_layout.add_widget(image_png)
            a1 = 1
        print(touch.x, ' ', touch.y)
        print(Window.size)

    def on_touch_up(self, touch):
        global a2
        if a2 != 0:
            touch_s.append(touch.x)
            touch_s.append(touch.y)
            print('z')
            try:
                remove('screenshot0001.png')
                Window.screenshot('screenshot.png')
            except:
                Window.screenshot('screenshot.png')
            self.manager.current = 'third'
        else:
            a2 = 1


class ThirdScr(Screen):
    global rgb_value

    def __init__(self, **kvargs):
        super().__init__(**kvargs)
        self.vert_boxl1 = BoxLayout(orientation='vertical')
        self.vert_boxl2 = BoxLayout(orientation='vertical')
        self.vert_boxl3 = BoxLayout(orientation='vertical')
        self.horz_boxl1 = BoxLayout(orientation='horizontal')
        self.lab = Label(text='Click to activate screen')
        self.vert_boxl2.add_widget(self.lab)
        self.horz_boxl1.add_widget(self.vert_boxl1)
        self.horz_boxl1.add_widget(self.vert_boxl2)
        self.horz_boxl1.add_widget(self.vert_boxl3)
        self.add_widget(self.horz_boxl1)

    def restart(self):
        global a1, a2, a3, touch_s
        touch_s = []
        a1 = 0
        a2 = 0
        a3 = 0
        self.manager.current = 'first'

    def on_touch_down(self, touch):
        global a3
        if a3 == 0:
            self.vert_boxl2.remove_widget(self.lab)
            image_load = CoreImage.load('screenshot0001.png', keep_data=True)
            percent_rgba = image_load.read_pixel(touch_s[0], touch_s[1])
            rgb_value = [round(percent_rgba[0] * 255), round(percent_rgba[1] * 255), round(percent_rgba[2] * 255)]
            rgb_value_tup = tuple(rgb_value)
            prior_color = rgb_value.index(max(rgb_value))
            try:
                remove('left_square.png')
                remove('mid_square.png')
                remove('right_square.png')
            except:
                pass
            l_rgb_nums = []
            m_rgb_nums = []
            r_rgb_nums = []
            if prior_color == 0:
                left_square = Pimage.new('RGB', [round(Window.size[0] * 0.3), round(Window.size[0] * 0.3)],
                                         (rgb_value_tup[0], rgb_value_tup[1] - 30, rgb_value_tup[2] - 30))
                mid_square = Pimage.new('RGB', [round(Window.size[0] * 0.3), round(Window.size[0] * 0.3)],
                                        (rgb_value_tup[0], rgb_value_tup[1], rgb_value_tup[2]))
                right_square = Pimage.new('RGB', [round(Window.size[0] * 0.3), round(Window.size[0] * 0.3)],
                                          (rgb_value_tup[0], rgb_value_tup[1] + 30, rgb_value_tup[2] + 30))
                l_rgb_nums = [rgb_value_tup[0], rgb_value_tup[1] - 30, rgb_value_tup[2] - 30]
                m_rgb_nums = [rgb_value_tup[0], rgb_value_tup[1], rgb_value_tup[2]]
                r_rgb_nums = [rgb_value_tup[0], rgb_value_tup[1] + 30, rgb_value_tup[2] + 30]
            elif prior_color == 1:
                left_square = Pimage.new('RGB', [round(Window.size[0] * 0.3), round(Window.size[0] * 0.3)],
                                         (rgb_value_tup[0] - 30, rgb_value_tup[1], rgb_value_tup[2] - 30))
                mid_square = Pimage.new('RGB', [round(Window.size[0] * 0.3), round(Window.size[0] * 0.3)],
                                        (rgb_value_tup[0], rgb_value_tup[1], rgb_value_tup[2]))
                right_square = Pimage.new('RGB', [round(Window.size[0] * 0.3), round(Window.size[0] * 0.3)],
                                          (rgb_value_tup[0] + 30, rgb_value_tup[1], rgb_value_tup[2] + 30))
                l_rgb_nums = [rgb_value_tup[0] - 30, rgb_value_tup[1], rgb_value_tup[2] - 30]
                m_rgb_nums = [rgb_value_tup[0], rgb_value_tup[1], rgb_value_tup[2]]
                r_rgb_nums = [rgb_value_tup[0] + 30, rgb_value_tup[1], rgb_value_tup[2] + 30]
            elif prior_color == 2:
                left_square = Pimage.new('RGB', [round(Window.size[0] * 0.3), round(Window.size[0] * 0.3)],
                                         (rgb_value_tup[0] - 30, rgb_value_tup[1] - 30, rgb_value_tup[2]))
                mid_square = Pimage.new('RGB', [round(Window.size[0] * 0.3), round(Window.size[0] * 0.3)],
                                        (rgb_value_tup[0], rgb_value_tup[1], rgb_value_tup[2]))
                right_square = Pimage.new('RGB', [round(Window.size[0] * 0.3), round(Window.size[0] * 0.3)],
                                          (rgb_value_tup[0] + 30, rgb_value_tup[1] + 30, rgb_value_tup[2]))
                l_rgb_nums = [rgb_value_tup[0] - 30, rgb_value_tup[1] - 30, rgb_value_tup[2]]
                m_rgb_nums = [rgb_value_tup[0], rgb_value_tup[1], rgb_value_tup[2]]
                r_rgb_nums = [rgb_value_tup[0] + 30, rgb_value_tup[1] + 30, rgb_value_tup[2]]

            left_square.save('left_square.png')
            mid_square.save('mid_square.png')
            right_square.save('right_square.png')

            l_square_image = Image(source='left_square.png')
            m_square_image = Image(source='mid_square.png')
            r_square_image = Image(source='right_square.png')

            self.vert_boxl1.add_widget(l_square_image)
            self.vert_boxl2.add_widget(m_square_image)
            self.vert_boxl3.add_widget(r_square_image)

            str1 = ', '.join(str(e) for e in l_rgb_nums)
            str2 = ', '.join(str(e) for e in m_rgb_nums)
            str3 = ', '.join(str(e) for e in r_rgb_nums)

            l_rgb_lab = Label(text=str1)
            m_rgb_lab = Label(text=str2)
            r_rgb_lab = Label(text=str3)

            self.vert_boxl1.add_widget(l_rgb_lab)
            self.vert_boxl2.add_widget(m_rgb_lab)
            self.vert_boxl3.add_widget(r_rgb_lab)

            a3 = 1
        elif a3 == 1:
            self.restart()


class CamColorApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FirstScr(name='first'))
        sm.add_widget(SecondScr(name='second'))
        sm.add_widget(ThirdScr(name='third'))
        return sm


app = CamColorApp()
app.run()
