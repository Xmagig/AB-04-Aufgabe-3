import os
import random
import pygame
class Settings:
    Window = pygame.rect.Rect(0,0,600,400)
    FPS = 60 #limits The FPS to The number
    Timer = 0 # Der start des Fps Countgzers

    FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    IMAGE_PATH = os.path.join(FILE_PATH, "images")

class Drop(pygame.sprite.Sprite):
    def __init__(self, x = 10, y=10, width= 30, height=30):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, "drop1.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speedx = random.randint(-5,5)
        self.speedy = random.randint(-5,5)

    def update(self):
        self.rect = self.rect.move(self.speedx, self.speedy)
        if self.rect.left < 0 or self.rect.right > Settings.Window.width:
            self.speedx *= -1
        if self.rect.top < 0 or self.rect.bottom > Settings.Window.height:
            self.speedy *= -1

class Umbrella(pygame.sprite.Sprite):
    def __init__(self,x, y,):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, "Umbrella.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

def main():
    os.environ["SDL_VIDEO_WINDOW_POS"] = "10, 50"  
    pygame.init()


    screen = pygame.display.set_mode(Settings.Window.size)  #Gibt die Groesse die oben in settings angegeben ist ab.
    pygame.display.set_caption("Drops From Above")          # Setzt den tietel der window 
    clock = pygame.time.Clock()

    drops = pygame.sprite.Group()
    umbrellas = pygame.sprite.Group()
    drop = Drop()

    background_image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, "background04.png")).convert()
    background_image = pygame.transform.scale(background_image,Settings.Window.size)                        # Setzt den hintergrund auf die window size
    
    umbrella_position = [(150,75),
                         (250,150),
                         (500,300),
                         (300,250),
                         (350,75)]
    for pos in umbrella_position:
        umbrella =  Umbrella(*pos)
        umbrellas.add(umbrella)
    running = True
    drop_timer = 0 
    while running:
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen.blit(background_image,(0,0))    
        
        
        drop_timer+=1
        if drop_timer == 100:
            drop = Drop()
            drops.add(drop) 
            drop_timer = 0

        drops.update()


        for einzel_drop in drops:
            if pygame.sprite.spritecollideany(einzel_drop, umbrellas):
                einzel_drop.kill()              
                
        for drop in drops:# drops  werden nacheinander ausgegeben
            screen.blit(drop.image, drop.rect)


        for umbrella in umbrellas:  # Umbrellas werden nacheinander ausgegeben 
            screen.blit(umbrella.image, umbrella.rect)
        pygame.display.flip() # ueber traegt die aenderungen 
        
        #Fps Abfrage 
        Settings.Timer+=1   
        if Settings.Timer == 30:
            Settings.Timer=0
        clock.tick(Settings.FPS)

    pygame.quit()

if __name__ == "__main__":
    main()