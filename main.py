from kivymd.uix.backdrop.backdrop import MDBoxLayout
from kivy.uix.accordion import FloatLayout
from kivymd.uix.bottomsheet.bottomsheet import MDLabel
from kivy.animation import Animation
from kivy.uix.bubble import Image
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock

from kivymd.uix.screen import MDScreen
from kivy.uix.image import Image
from kivymd.uix.card import MDCard
from kivy.metrics import dp
import kivy
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from kivy.core.window import Window

Window.size = (360,660)

# import os
# os.environ["KIVY_TEXT"] = "sdl2"

# font_path = os.path.abspath("comici.ttf")
# LabelBase.register(name="ComicBD", fn_regular=font_path)



class GameScreen3(MDScreen):
    freebuttons = [1,2,3,4,5,6,7,8,9]
    playerno = 1
    playerx = []
    playero = []
    win = 0
    winsound = SoundLoader.load('winsound.mp3')

    
    def ButtonClick(self,root,buttonno):
        if(self.win==0):
            if buttonno in self.freebuttons:
                self.freebuttons.remove(buttonno)
                
                #1 = O  2 = X
                if self.playerno == 1:
                    self.playerno = 2

                    self.ids.playerturn.text = "Turn: Player X"
                    
                    self.playero.append(buttonno)
                    self.current = self.playero

                    root.md_bg_color = (255/256,87/256,87/256,1)
                    root.add_widget(Image(source="circle.png",size_hint=(0.97,0.97),pos_hint= {"center_x": .5, "center_y": .5}))

                elif self.playerno == 2:
                    self.playerno = 1

                    self.ids.playerturn.text = "Turn: Player O"
                    
                    self.playerx.append(buttonno)
                    self.current = self.playerx
                    
                    root.md_bg_color = (0/256,191/256,99/256,1)
                    root.add_widget(Image(source="cross.png",size_hint=(0.9,0.9),pos_hint={"center_x": .5, "center_y": .5}))

                

                if(buttonno==1):
                    if (2 in self.current and 3 in self.current) or (4 in self.current and 7 in self.current) or (5 in self.current and 9 in self.current):
                        self.win = self.playerno
                
                elif(buttonno==2):
                    if (1 in self.current and 3 in self.current) or (5 in self.current and 8 in self.current):
                        self.win = self.playerno

                elif(buttonno==3):
                    if (1 in self.current and 2 in self.current) or (6 in self.current and 9 in self.current) or (5 in self.current and 7 in self.current):
                        self.win = self.playerno
                
                elif(buttonno==4):
                    if (1 in self.current and 7 in self.current) or (5 in self.current and 6 in self.current):
                        self.win = self.playerno
                
                elif(buttonno==5):
                    if (2 in self.current and 8 in self.current) or (4 in self.current and 6 in self.current) or (1 in self.current and 9 in self.current) or (3 in self.current and 7 in self.current):
                        self.win = self.playerno
                
                elif(buttonno==6):
                    if (3 in self.current and 9 in self.current) or (4 in self.current and 5 in self.current):
                        self.win = self.playerno
                
                elif(buttonno==7):
                    if (1 in self.current and 4 in self.current) or (8 in self.current and 9 in self.current) or (3 in self.current and 5 in self.current):
                        self.win = self.playerno

                elif(buttonno==8):
                    if (2 in self.current and 5 in self.current) or (7 in self.current and 9 in self.current):
                        self.win = self.playerno

                elif(buttonno==9):
                    if (3 in self.current and 6 in self.current) or (7 in self.current and 8 in self.current) or (1 in self.current and 5 in self.current):
                        self.win = self.playerno

                if(self.win==1):
                    self.win=2
                
                elif(self.win==2):
                    self.win=1

                if(self.win==0 and self.freebuttons == []):
                    print("Tie")
                    
                    self.reset()

                elif(self.win!=0):
                    print("Win: ",self.win)
                    self.winanimation(root,buttonno)
                    #self.reset()

    def winanimation(self,root,button):
        x,y = root.to_window(*root.pos)
        width, height = root.size

        self.mainlayout = self.ids.floatlayout
        
        self.overlay_card = MDCard(
            id = "overlay",
            size_hint=(None, None),
            size=(width, height), 
            pos=(x, y),
            md_bg_color=(255/256,87/256,87/256,1) if self.playerno == 2 else (0/256,191/256,99/256,1)
        )


        self.image = Image(
                source = "circle.png" if self.playerno == 2 else "cross.png",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                size_hint = (1,1)
            )
        
        self.overlay_card.add_widget(self.image)
        #self.overlay_card.add_widget(self.wintext)


        self.wintext = Builder.load_file("wonthematch.kv")     

        self.restartbutton = Builder.load_file("RestartButton.kv")
        

        self.mainlayout.add_widget(self.overlay_card)
        self.mainlayout.add_widget(self.wintext)
        self.mainlayout.add_widget(self.restartbutton)
        
        print(self.ids.floatlayout.children[0])

        length = max(Window.size[0]*1.5,Window.size[1]*1.5)
                
        self.winsound.play()
        
        Animation(size=(length,length),
                  center_x=Window.size[0] / 2,
                  center_y=Window.size[1] / 2,
                  radius=[dp(700),dp(700),dp(700),dp(700)],
                  t = "in_out_circ",
                  duration = 1.6,#0.9
                  ).start(self.overlay_card)

        Animation(         
            size_hint = (0.2,0.2),
            pos_hint={"center_y":0.55},
            t = "in_out_sine",
            duration = 1.43#0.73
         ).start(self.image) #self.ids.floatlayout.children[1].children[0]

        Animation(
            font_size = 50,
            text_color=(1,1,1,1),
            t = "in_out_sine",
            duration = 1.5#0.8
        ).start(self.wintext)

        
        restartbuttonanimation = Animation(
            opacity = 0.8,
            t = "in_out_sine",
            duration = 1.5
        )

        Clock.schedule_once(lambda dt:restartbuttonanimation.start(self.restartbutton),1.7)

    def reset(self):
        self.freebuttons = [1,2,3,4,5,6,7,8,9]
        self.playero = []
        self.playerx = []
        self.win = 0
        
        for card in (list(self.ids.buttongrid.children)):
            if card.children:  
               card.remove_widget(card.children[0])
               card.md_bg_color = (215/256,215/256,215/256,1)
        
        self.mainlayout.remove_widget(self.overlay_card)
        self.mainlayout.remove_widget(self.wintext)
        self.mainlayout.remove_widget(self.restartbutton)
        

class TickTacToe(MDApp):
    def build(self):
        return Builder.load_file('main.kv') 


TickTacToe().run()