from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Line, Color
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import random


class SimpleWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
           
        with self.canvas:
            self.rect = Rectangle(source="player.png", pos=(100, 100), size=(50, 50))
            self.score=0
            self.label_score = Label(text=str(self.score), pos=(50, 900),font_size='30sp')
            self.add_widget(self.label_score)
            self.rectenemy = []
            self.rectenemy1 = []
            self.finishline= Line(points=[10,10,10,1000])
            self.effect= None
            self.laser = None   
            self.enemylaser= None
            count = 300
            num = random.randint(2,5)
            for _ in range(8): # quantidade de naves inimigasw
                enemy = Rectangle(source="enemyship.png", pos=(2500+(count/2), (num+1)*100), size=(30, 50))
                self.rectenemy.append(enemy)  # Adiciona os retângulos inimigos à lista
                self.canvas.add(enemy)
                count += 300
                num = random.randint(1,5)
        
        Window.bind(on_key_down=self._on_keyboard_down)
        self.explosion_sound = SoundLoader.load("shipexplosion.wav")
        self.laser_sound = SoundLoader.load("lasersound.mp3")
        
        Clock.schedule_interval(self.enemy_movement, 1.0 / 120) 
        Clock.schedule_interval(self.enemy1_movement, 1.0 / 60.0) 

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        current_y = self.rect.pos[1]  # Obtém a posição atual em Y do quadrado

        if text == "w":  # Move para cima ao pressionar 'w'
            current_y += 100
        elif text == "s":  # Move para baixo ao pressionar 's'
            current_y -= 100
        
        # Limita a posição do quadrado para dentro da janela
        current_y = max(0, min(current_y, self.height - self.rect.size[1]))

        self.rect.pos = (self.rect.pos[0], current_y)  # Define a nova posição em Y do quadrado
        

        if text == " ":
            color = Color(0, 1, 0, 1)
            self.laser = Line(points=[150, current_y + 25, 2000, current_y + 25])
            self.effect = Line(points=[150, current_y + 25, 400, current_y + 25])
            self.canvas.add(color)  # Adiciona a cor ao canvas
            self.canvas.add(self.effect)  # Adiciona o laser ao canvas
            Clock.schedule_once(self.timer_laser, 0.05)
            if self.laser_sound:
                self.laser_sound.play()
            
    def timer_laser (self,dt):
        # Após 0.05 segundo, o laser é removido
        if self.effect is not None:
            remover= Color(0,0,0,1)
            self.canvas.add(remover)
            self.canvas.add(self.effect)

        # Remove o laser do canvas
    def enemy_movement(self, dt):
        # Movimento dos retângulos 'rectenemy' para a esquerda
        
        for enemy in self.rectenemy:
            enemy.pos = (enemy.pos[0] - 5, enemy.pos[1])  # Altera a posição X dos retângulos inimigos
            stop=0
            # Verifica se ho uve colisão entre o laser e um retângulo inimigo
            if self.laser is not None and self.laser_collision(enemy):
                respawn = random.randint(2,8)
                enemy.pos = (4500, respawn*100)
            # Verifica se houve colisão entre o enemy e a finishline
            if self.finishline_collision(enemy):
                App.get_running_app().stop()  # Fecha o aplicativo

    def enemy1_movement(self, dt):
        
        for enemy1 in self.rectenemy1:
            enemy1.pos = (enemy1.pos[0] - 5, enemy1.pos[1])  
            
            
    def laser_collision(self, enemy):
        if self.laser is not None:
            
            laser_x1, laser_y1, laser_x2, laser_y2 = self.laser.points
            
            
            enemy_x1, enemy_y1 = enemy.pos
            enemy_x2, enemy_y2 = enemy.pos[0] + enemy.size[0], enemy.pos[1] + enemy.size[1]
            
            
            if (laser_x1 < enemy_x2 and laser_x2 > enemy_x1 and
                laser_y1 < enemy_y2 and laser_y2 > enemy_y1):
                
                
                self.laser = None  # Define o laser como None para indicar que foi removido
                self.score+=10
                self.label_score.text = str(self.score)  # Atualiza o texto do Label do score
                if self.explosion_sound:
                    self.explosion_sound.play()

                return True
        return False
    
    def finishline_collision(self, enemy):
    # Verifica se houve colisão entre o enemy e a linha finishline
        enemy_x1, enemy_y1 = enemy.pos
        enemy_x2, enemy_y2 = enemy.pos[0] + enemy.size[0], enemy.pos[1] + enemy.size[1]

        finishline_x, finishline_y1, finishline_x, finishline_y2 = self.finishline.points

        if (finishline_x < enemy_x2 and finishline_x > enemy_x1 and
            finishline_y1 < enemy_y2 and finishline_y2 > enemy_y1):
            return True
        return False
class SimpleApp(App):
    def build(self):
        return SimpleWidget()


if __name__ == "__main__":
    SimpleApp().run()