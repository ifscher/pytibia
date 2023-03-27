from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from KivyOnTop import register_topmost, unregister_topmost


class Gerenciador(ScreenManager):
    pass


class Menu(Screen):
    def on_pre_enter(self):
        Window.bind(on_request_close=self.confirmacao)

    def confirmacao(self, *args, **kwargs):
        # global popSound
        # popSound.play()
        self.export_to_png('Menu.png')
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        botoes = BoxLayout(padding=10, spacing=10)

        pop = Popup(title='Deseja mesmo sair?', content=box, size_hint=(None, None),
                    size=(150, 150))

        sim = Botao(text='Sim', on_release=App.get_running_app().stop)
        nao = Botao(text='Não', on_release=pop.dismiss)

        botoes.add_widget(sim)
        botoes.add_widget(nao)

        atencao = Image(source='atencao.png')

        box.add_widget(atencao)
        box.add_widget(botoes)

        animText = Animation(color=(0, 0, 0, 1)) + \
            Animation(color=(1, 1, 1, 1))
        animText.repeat = True
        animText.start(sim)
        anim = Animation(size=(300, 180), duration=0.2, t='out_back')
        anim.start(pop)
        pop.open()
        return True


class Botao(ButtonBehavior, Label):
    def on_press(self):
        pass

    def on_release(self):
        pass


class Tarefas(Screen):
    def __init__(self, tarefas=[], **kwargs):
        super().__init__(**kwargs)
        for tarefa in tarefas:
            self.ids.box.add_widget(Tarefa(text=tarefa))

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar)

    def voltar(self, window, key, *args):
        if key == 27:
            App.get_running_app().root.current = 'menu'
        return True

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)

    def addWidget(self):
        texto = self.ids.texto.text
        self.ids.box.add_widget(Tarefa(text=texto))
        self.ids.texto.text = ''


class Tarefa(BoxLayout):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.ids.label.text = text


class pyTibia(App):
    def on_start(self, *args):
        # Window.set_title(TITLE)

        # Register top-most
        register_topmost(Window, self.__class__.__name__)

        # Unregister top-most (not necessary, only an example)
        self.bind(on_stop=lambda *args, w=Window,
                  t=self.__class__.__name__: unregister_topmost(w, t))

        Window.size = (300, 500)

    def build(self):
        global popSound, poppapSound
        popSound = SoundLoader.load('pop.wav')
        poppapSound = SoundLoader.load('poppap.wav')
        return Gerenciador()


pyTibia().run()
