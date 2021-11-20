import pygame,sys,random
pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
laser_active = False
font = pygame.font.Font("goodfont.ttf",60)
score = 0
class Spaceship(pygame.sprite.Sprite):
    def __init__(self,path,xpos,ypos) :
        super().__init__()
        self.charge = pygame.image.load('spaceship_charged.png')
        self.uncharge = pygame.image.load(path)
        self.image = self.uncharge
        self.rect = self.image.get_rect(center = (xpos,ypos))
        self.shield_surface = pygame.image.load("shield.png")
        self.health = 5
    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.screen_constraint()
        self.shield()
        self.charged()
        self.discharged()
    def screen_constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= 1280:
            self.rect.right = 1280
    def shield(self):
            for index,health in enumerate(range(self.health)):
                screen.blit(self.shield_surface,(index * 40,0))
    def charged(self):
        self.image = self.charge
    def discharged(self):
        self.image = self.uncharge
class Meteor(pygame.sprite.Sprite):
    def __init__(self,path,xpos,ypos,xs,ys):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (xpos,ypos))
        self.xs = xs
        self.ys = ys
    def update(self):
        self.rect.centery += self.ys
        self.rect.centerx += self.xs
        if self.rect.centery >= 800:
            self.kill()
class Laser(pygame.sprite.Sprite):
    def __init__(self,path,pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = pos)
    
    def update(self):
        self.rect.centery -= 10
        if self.rect.centery <= -50:
            self.kill()
meteor_grp = pygame.sprite.Group()
METEOR_EVENT = pygame.USEREVENT
pygame.time.set_timer(METEOR_EVENT,100)
spaceship = Spaceship('spaceship.png',640,360)
spaceship_grp = pygame.sprite.GroupSingle()
spaceship_grp.add(spaceship)
laser_grp = pygame.sprite.Group()
laser_time = 0
def main_game():
    global laser_active
    laser_grp.draw(screen)
    laser_grp.update()
    spaceship_grp.draw(screen)
    spaceship_grp.update()
    meteor_grp.draw(screen)
    meteor_grp.update()
    if pygame.time.get_ticks() - laser_time >= 500:
        laser_active = True
        spaceship_grp.sprite.charged()

def end_game():
    text = font.render("Game over",True,(255,255,255))
    text_rect = text.get_rect(center = (640,300))
    screen.blit(text,text_rect)
    stext = font.render(f'Score : {score}',True,(255,255,255))
    stext_rect = stext.get_rect(center = (640,400))
    screen.blit(stext,stext_rect)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == METEOR_EVENT:
            path = random.choice(("Meteor1.png","Meteor2.png","Meteor3.png"))
            xpos = random.randrange(0,1280)
            ypos = random.randrange(-500,-50)
            xspeed = random.randrange(-1,1)
            yspeed = random.randrange(4,10)
            meteor = Meteor(path,xpos,ypos,xspeed,yspeed)
            meteor_grp.add(meteor)
        if event.type == pygame.MOUSEBUTTONDOWN and laser_active:
            path = "laser.png"
            pos = event.pos
            laser = Laser(path,pos)
            laser_grp.add(laser)
            laser_active = False
            laser_time = pygame.time.get_ticks()
            spaceship_grp.sprite.discharged()
        if event.type == pygame.MOUSEBUTTONDOWN and spaceship_grp.sprite.health <= 0:
            spaceship_grp.sprite.health = 5
            meteor_grp.empty()
            score = 0
    screen.fill((40,45,51))
    if spaceship_grp.sprite.health > 0:
        main_game()
        score += 1
    else:
        end_game()
    pygame.display.update()
    if pygame.sprite.spritecollide(spaceship_grp.sprite,meteor_grp,True):
        spaceship_grp.sprite.health -= 1
    for laser in laser_grp:
        pygame.sprite.spritecollide(laser,meteor_grp,True)
    clock.tick(120)
