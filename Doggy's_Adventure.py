import pygame , random , os,string
pygame.init()
#screen
h,w = 1024,760
screen = pygame.display.set_mode((h,w))
screenrect = pygame.Rect(0, 0, 1024,760)
background_image=pygame.image.load("images/background1!.png").convert()
pygame.display.flip()
#preables
live = False
bonus = False
bmb = 0
numlvl = 0
menurunning = True
ending = False
hearth = 0
herotype = False
lvlrunning = False

kol = 10
rl = 10
lvlcode = 0
pygame.display.set_caption("Pet's Adventure")
codes = [['123',1],['456',2],['789',3],['444',4],['555',5]]
numberlvl = 0
#class of main things
def level(number):
    cod = 0
    font = pygame.font.Font(None, 50)
    for i in codes:
        if number == str(i[1]):
            cod = i[0]
    text3 = font.render('Code for level '+number+':  '+cod, 1, pygame.Color("grey"))
    text = font.render("Level " + number, 4, (255, 0, 0))
    text2 = font.render("(Press any key to continue)", 1, pygame.Color("grey"))
    text_x = h// 2 - text.get_width() // 2
    text_y = w // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    text_x2 = 300
    text_y2 = 500
    text_x3 = 100
    text_y3 = 100
    text_w2 = text2.get_width()
    text_h2 = text2.get_height()
    text_w3 = text2.get_width()
    text_h3 = text2.get_height()
    screen.blit(text3, (text_x3, text_y3))
    screen.blit(text, (text_x, text_y))
    screen.blit(text2, (text_x2, text_y2))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10, text_w + 20, text_h + 20), 1)
def counter(num,bombs,hr):
    font = pygame.font.Font(None, 50)
    text = font.render("Till the end: " + str( num * kol - bombs - 2)+'                                      '+'Your HP : '+ str(hr+1) , 4, (254,241,28))
    screen.blit(background_image, [0, 0])
    screen.blit(text, (50, 650))
    pygame.display.flip()
def end():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("Game over", 4, (255,0,0))
    text_x = h // 2 - text.get_width() // 2
    text_y = w // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10, text_w + 20, text_h + 20), 1)
class Player(pygame.sprite.Sprite):
    images = []
    def __init__(self):
        self.e = 1
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        if self.e != 0:
            self.rect.move_ip(472, 570)
        self.facing = -1
        self.rect = self.rect.clamp(screenrect)
    def move(self, direction):
        if direction:
            self.facing = direction
        self.rect.move_ip(direction*10, 0)
        self.rect = self.rect.clamp(screenrect)
        if direction < 0:
            self.image = self.images[0]
        elif direction > 0:
            self.image = self.images[1]
    def pp (self,pos):
        self.e = 0
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos,570)
class Bonus(pygame.sprite.Sprite):
    image = []
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos, 0)
    def update(self):
        global bonus
        global hero
        global player
        self.rect.move_ip(0, 8)
        if self.rect.bottom >= 626:
            self.kill()
        if self.rect.bottom >= player.rect.top and ((self.rect.left >= player.rect.left and self.rect.left <= player.rect.right) or (self.rect.right >= player.rect.left and self.rect.right <= player.rect.right)):
            pos = player.rect.left
            player.kill()
            if herotype:
                hero = pygame.image.load("images/hero2shield.png").convert_alpha()
            else:
                hero = pygame.image.load("images/hero1shield.png").convert_alpha()
            Player.images = [pygame.transform.flip(hero, 1, 0), hero]
            player = Player()
            player.pp(pos)
            self.kill()
            bonus = True
class Bomb(pygame.sprite.Sprite):
    image = []
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos, 0)
    def update(self):
        global live
        global bonus
        global hero
        global bmb
        global player
        global hearth
        move = random.randint(7, 11)
        self.rect.move_ip(0, move)
        if self.rect.bottom >= 626:
            self.kill()
            Explosion(self)
        if self.rect.bottom >= player.rect.top and ((self.rect.left >= player.rect.left and self.rect.left <= player.rect.right) or (self.rect.right >= player.rect.left and self.rect.right <= player.rect.right)) and not bonus:
            if hearth >0:
                bmb+=1
                hearth-=1
                counter(numlvl, bmb, hearth)
                self.kill()
            else:
                self.kill()
                live = False
                player.kill()
        if self.rect.bottom >= player.rect.top and ((self.rect.left >= player.rect.left and self.rect.left <= player.rect.right) or (self.rect.right >= player.rect.left and self.rect.right <= player.rect.right)) and bonus:
            self.kill()
            bmb += 1
            bonus = False
            pos = player.rect.left
            if herotype:
                hero = pygame.image.load("images/hero2.png").convert_alpha()
            else:
                hero = pygame.image.load("images/hero1.png").convert_alpha()
            player.kill()
            Player.images = [pygame.transform.flip(hero, 1, 0), hero]
            player = Player()
            player.pp(pos)
            self.kill()
            pygame.display.flip()
class Bone(pygame.sprite.Sprite):
    image = []
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.move_ip(screenrect.midtop[0]-8, 0)
    def update(self):
        global live
        if self.rect.bottom < 626:
            self.rect.move_ip(0, 4)
        if self.rect.bottom >= player.rect.top and ((self.rect.left >= player.rect.left and self.rect.left <= player.rect.right) or (self.rect.right >= player.rect.left and self.rect.right <= player.rect.right)):
            live = True
            self.kill()
            player.kill()
class Explosion(pygame.sprite.Sprite):
    image = []
    def __init__(self, bomb):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect(midbottom=bomb.rect.center)
        self.rect.move_ip(0, 8)
        self.time = 8
    def update(self):
        global live
        global bonus
        global hero
        global bmb
        global player
        global hearth
        global bmb
        if (self.rect.left + 7 >= player.rect.left and self.rect.left + 7 <= player.rect.right) or (self.rect.right - 7 >= player.rect.left and self.rect.right - 7 <= player.rect.right)and not bonus:
            if hearth>0:
                hearth -=1
                self.kill()
                counter(numlvl, bmb, hearth)
            else:
                live = False
                player.kill()
                self.kill()
        if (self.rect.left + 7 >= player.rect.left and self.rect.left + 7 <= player.rect.right) or (self.rect.right - 7 >= player.rect.left and self.rect.right - 7 <= player.rect.right)and bonus:
            self.kill()
            bonus = False
            pos = player.rect.left
            if herotype:
                hero = pygame.image.load("images/hero2.png").convert_alpha()
            else:
                hero = pygame.image.load("images/hero1.png").convert_alpha()
            player.kill()
            Player.images = [pygame.transform.flip(hero, 1, 0), hero]
            player = Player()
            player.pp(pos)
            self.kill()
            pygame.display.flip()
        self.time = self.time - 1
        if self.time <= 0:
            self.kill()
            bmb+=1
            counter(numlvl, bmb, hearth)
class Hearth(pygame.sprite.Sprite):
    image = []
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos, 0)
    def update(self):
        global hearth
        self.rect.move_ip(0, 10)
        if self.rect.bottom >= 626:
            self.kill()
        if self.rect.bottom >= player.rect.top and ((self.rect.left >= player.rect.left and self.rect.left <= player.rect.right) or (self.rect.right >= player.rect.left and self.rect.right <= player.rect.right)) and hearth < 5:
            hearth +=1
            counter(numlvl, bmb, hearth)
            print('adsfasdgasdgasdgasdfasdg', hearth)
            self.kill()
def mainmenue():
    global lvlrunning
    global ending
    class Label:
        def __init__(self, rect, text, text_color="black", background_color="green"):
            self.rect = pygame.Rect(rect)
            if background_color == -1:
                background_color = "black"
            self.text = text
            self.bgcolor = pygame.Color(background_color)
            self.font_color = pygame.Color(text_color)
            # Рассчитываем размер шрифта в зависимости от высоты
            self.font = pygame.font.Font(None, self.rect.height - 4)
            self.rendered_text = None
            self.rendered_rect = None
        def render(self, surface):
            surface.fill(self.bgcolor, self.rect)
            self.rendered_text = self.font.render(self.text, 1, self.font_color)
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
            # выводим текст
            surface.blit(self.rendered_text, self.rendered_rect)
    class GUI:
        def __init__(self):
            self.elements = []
        def add_element(self, element):
            self.elements.append(element)
        def render(self, surface):
            for element in self.elements:
                render = getattr(element, "render", None)
                if callable(render):
                    element.render(surface)
        def update(self):
            for element in self.elements:
                update = getattr(element, "update", None)
                if callable(update):
                    element.update()
        def get_event(self, event):
            for element in self.elements:
                get_event = getattr(element, "get_event", None)
                if callable(get_event):
                    element.get_event(event)
    class Button(Label):
        def __init__(self, rect, text):
            super().__init__(rect, text)
            self.bgcolor = pygame.Color("green")
            self.pressed = False
        def render(self, surface):
            surface.fill(self.bgcolor, self.rect)
            self.rendered_text = self.font.render(self.text, 1, self.font_color)
            if not self.pressed:
                color1 = pygame.Color("white")
                color2 = pygame.Color("white")
                self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 5, centery=self.rect.centery)
            else:
                color1 = pygame.Color("black")
                color2 = pygame.Color("black")
                self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 7, centery=self.rect.centery + 2)
            pygame.draw.rect(surface, color1, self.rect, 4)
            pygame.draw.line(surface, color2, (self.rect.right - 1, self.rect.top), (self.rect.right - 1, self.rect.bottom), 2)
            pygame.draw.line(surface, color2, (self. rect.left, self.rect.bottom - 1),
                             (self.rect.right, self.rect.bottom - 1), 2)
            surface.blit(self.rendered_text, self.rendered_rect)
        def get_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.pressed = self.rect.collidepoint(event.pos)
                menurunning = False
                lvlrunning = True
    class TextBox(object):
        def __init__(self, rect, **kwargs):
            self.rect = pygame.Rect(rect)
            self.buffer = []
            self.final = None
            self.rendered = None
            self.render_rect = None
            self.render_area = None
            self.blink = True
            self.blink_timer = 0.0
            self.delete_timer = 0.0
            self.accepted = string.ascii_letters + string.digits + string.punctuation + " "
            self.process_kwargs(kwargs)
        def process_kwargs(self, kwargs):
            defaults = {"id": None,
                        "command": None,
                        "active": True,
                        "color": pygame.Color("white"),
                        "font_color": pygame.Color("black"),
                        "outline_color": pygame.Color("black"),
                        "outline_width": 2,
                        "active_color": pygame.Color("blue"),
                        "font": pygame.font.Font(None, self.rect.height + 4),
                        "clear_on_enter": False,
                        "inactive_on_enter": True,
                        "blink_speed": 500,
                        "delete_speed": 75}
            for kwarg in kwargs:
                if kwarg in defaults:
                    defaults[kwarg] = kwargs[kwarg]
                else:
                    raise KeyError("TextBox accepts no keyword {}.".format(kwarg))
            self.__dict__.update(defaults)
        def get_event(self, event, mouse_pos=None):
            if event.type == pygame.KEYDOWN and self.active:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self.execute()
                elif event.key == pygame.K_BACKSPACE:
                    if self.buffer:
                        self.buffer.pop()
                elif event.unicode in self.accepted:
                    self.buffer.append(event.unicode)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not mouse_pos:
                    mouse_pos = pygame.mouse.get_pos()
                self.active = self.rect.collidepoint(mouse_pos)
        def execute(self):
            if self.command:
                self.command(self.id, self.final)
            self.active = not self.inactive_on_enter
            if self.clear_on_enter:
                self.buffer = []
        def switch_blink(self):
            if pygame.time.get_ticks() - self.blink_timer > self.blink_speed:
                self.blink = not self.blink
                self.blink_timer = pygame.time.get_ticks()
        def update(self):
            new = "".join(self.buffer)
            if new != self.final:
                self.final = new
                self.rendered = self.font.render(self.final, True, self.font_color)
                self.render_rect = self.rendered.get_rect(x=self.rect.x + 2,
                                                          centery=self.rect.centery)
                if self.render_rect.width > self.rect.width - 6:
                    offset = self.render_rect.width - (self.rect.width - 6)
                    self.render_area = pygame.Rect(offset, 0, self.rect.width - 6,
                                                   self.render_rect.height)
                else:
                    self.render_area = self.rendered.get_rect(topleft=(0, 0))
            self.switch_blink()
            self.handle_held_backspace()
        def handle_held_backspace(self):
            if pygame.time.get_ticks() - self.delete_timer > self.delete_speed:
                self.delete_timer = pygame.time.get_ticks()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_BACKSPACE]:
                    if self.buffer:
                        self.buffer.pop()
        def draw(self, surface):
            outline_color = self.active_color if self.active else self.outline_color
            outline = self.rect.inflate(self.outline_width * 2, self.outline_width * 2)
            surface.fill(outline_color, outline)
            surface.fill(self.color, self.rect)
            if self.rendered:
                surface.blit(self.rendered, self.render_rect, self.render_area)
            if self.blink and self.active:
                curse = self.render_area.copy()
                curse.topleft = self.render_rect.topleft
                surface.fill(self.font_color, (curse.right + 1, curse.y, 2, curse.h))
    gui = GUI()
    lvlrunning = False
    optionsrunning = False
    background_image=pygame.image.load("images/background1!.png").convert()
    screen.blit(background_image, [0, 0])
    def menu():
        global ending
        global lvlrunning
        global menurunning
        global ruls
        if menurunning:
            background_image = pygame.image.load("images/background1!.png").convert()
            screen.blit(background_image, [0, 0])
            pygame.display.flip()
            gui = GUI()
            b1 = Button((327, 200, 360, 62), "START THE GAME")
            b2 = Button((327, 300, 360, 62), "       OPTIONS")
            b3 = Button((327, 400, 360, 62), "  CHOOSE LEVEL")
            b4 = Button((327, 500, 360, 62), "           EXIT")
            b5 = Button((970, 20, 50, 50), " ?")
            gui.add_element(b1)
            gui.add_element(b2)
            gui.add_element(b3)
            gui.add_element(b4)
            gui.add_element(b5)
            optionsrunning = False
            buttonum = 1
            e = eval('b' + str(buttonum))
            print(buttonum)
            buttonPress = False
            e = eval('b' + str(buttonum))
            e.pressed = True
        while menurunning:
            background_image = pygame.image.load("images/background1!.png").convert()
            screen.blit(background_image, [0, 0])
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    ending = True
                    menurunning = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and buttonum < 4:
                    buttonum += 1
                    e = eval('b' + str(buttonum))
                    e.pressed = True
                    d = eval('b' + str(buttonum -1))
                    d.pressed = False
                    print(buttonum)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and buttonum > 1:
                    buttonum -=1
                    e = eval('b' + str(buttonum))
                    d = eval('b' + str(buttonum + 1))
                    d.pressed = False
                    print( buttonum)
                    e.pressed = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    e.pressed = True
                    buttonPress = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if b1.rect.collidepoint(event.pos):
                        menurunning = False
                        lvlrunning = True
                    elif b3.rect.collidepoint(event.pos):
                        menurunning = False
                        lvlch()
                    elif b2.rect.collidepoint(event.pos):
                        menurunning = False
                        settings()
                    elif b4.rect.collidepoint(event.pos):
                        menurunning = False
                        ending = True
                    elif b5.rect.collidepoint(event.pos):
                        menurunning = False
                        rules()
                gui.get_event(event)
            gui.render(screen)
            gui.update()
            if menurunning:
                if b4.pressed == True and buttonPress:
                    menurunning = False
                    ending = True
                if b1.pressed == True and buttonPress:
                    menurunning = False
                    lvlrunning = True
                if b2.pressed == True and buttonPress:
                    menurunning = False
                    settings()
                if b3.pressed == True and buttonPress:
                    menurunning = False
                    buttonPress = False
                    lvlch()
                pygame.display.flip()
    def settings():
        global herotype
        global menurunning
        background_image = pygame.image.load("images/background1!.png").convert()
        screen.blit(background_image, [0, 0])
        pygame.display.flip()
        kitty = pygame.image.load('images/cat.png')
        doggy = pygame.image.load('images/dog.png')
        screen.blit(doggy, [150, 200])
        screen.blit(kitty, [650, 200])
        pygame.display.flip()
        optionsrunning = True
        b1 = Button((327,100, 360, 52), "       START GAME")
        b2 = Button((100,400, 360, 62), "  Choose Dogge")
        b3 = Button((600,400, 360, 62), "    Choose Catty")
        b4 = Button((327,500, 360, 52), "              EXIT")
        gui.add_element(b1)
        gui.add_element(b2)
        gui.add_element(b3)
        gui.add_element(b4)
        global lvlrunning
        global ending
        buttonum = 1
        e = eval('b' + str(buttonum))
        print(buttonum)
        buttonPress = False
        e = eval('b' + str(buttonum))
        e.pressed = True
        while optionsrunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    ending = True
                    optionsrunning = False
                    menurunning = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and buttonum < 4:
                    buttonum += 1
                    e = eval('b' + str(buttonum))
                    e.pressed = True
                    d = eval('b' + str(buttonum -1))
                    d.pressed = False
                    print(buttonum)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and buttonum > 1:
                    buttonum -= 1
                    e = eval('b' + str(buttonum))
                    d = eval('b' + str(buttonum + 1))
                    d.pressed = False
                    print(buttonum)
                    e.pressed = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    e.pressed = True
                    buttonPress = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if b1.rect.collidepoint(event.pos):
                        optionsrunning = False
                        lvlrunning = True
                    elif b2.rect.collidepoint(event.pos):
                        optionsrunning = False
                        lvlrunning = True
                    elif b3.rect.collidepoint(event.pos):
                        optionsrunning = False
                        lvlrunning = True
                        herotype = True
                    elif b4.rect.collidepoint(event.pos):
                        optionsrunning = False
                        ending = True
                gui.get_event(event);
            gui.render(screen)
            gui.update()
            if b3.pressed == True and buttonPress:
                optionsrunning = False
                lvlrunning = True
                herotype = True
            if b1.pressed == True and buttonPress:
                optionsrunning = False
                lvlrunning = True
            if b2.pressed == True and buttonPress:
                optionsrunning = False
                lvlrunning = True
            if b4.pressed == True and buttonPress:
                optionsrunning = False
                menurunning = False
            pygame.display.flip()
    def lvlch():
        global ending
        global lvlrunning
        global menurunning
        global numberlvl
        global lvlc
        background_image = pygame.image.load("images/background1!.png").convert()
        screen.blit(background_image, [0, 0])
        pygame.display.flip()
        lvlc=True
        if lvlc:
            gui = GUI()
            b1 = Label((327, 200, 360, 62), "     ENTER CODE")
            gui.add_element(b1)
            b2 = Button((327, 400, 360, 62), "           BACK")
            gui.add_element(b2)
            def print_on_enter(id, final):
                global lvlcode
                lvlcode = format(final)
            settings = {
                "command": print_on_enter,
                "inactive_on_enter": False,
            }
            entry = TextBox(rect=(327, 300, 360, 62), **settings)
        while lvlc:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    ending = True
                    lvlc = False
                    menurunning = False
                entry.get_event(event)
                gui.get_event(event)
            gui.render(screen)
            gui.update()
            for i in codes:
                if lvlcode == i[0]:
                    lvlc = False
                    lvlrunning = True
                    numberlvl = i[1]-1
            if b2.pressed:
                lvlc = False
                menurunning = True
            entry.update()
            entry.draw(screen)
            pygame.display.update()
    def rules():
        global ending
        global lvlrunning
        global menurunning
        global numberlvl
        global ruls
        background_image = pygame.image.load("images/background1!.png").convert()
        screen.blit(background_image, [0, 0])
        pygame.display.flip()
        ruls=True
        if ruls:
            gui = GUI()
            b2 = Button((327, 685, 360, 62), "           BACK")
            font = pygame.font.Font(None, 50)
            text = font.render("Main characters", 4, (0, 0, 0))
            text2 = font.render("You must run away from this things!!!", 4, (0, 0, 0))
            text3 = font.render("Take it if you want to stay alive!", 4, (0, 0, 0))
            text4 = font.render("Catch this         or this         to end the level!", 4, (0, 0, 0))
            text5 = font.render("Good luck! Have fun! :3 ", 4, (0, 0, 0))
            kitty = pygame.image.load('images/hero1.png')
            doggy = pygame.image.load('images/hero2.png')
            screen.blit(doggy, [215, 20])
            screen.blit(kitty, [700, 20])
            d1 = pygame.image.load('images/bomb1!.png')
            d2 = pygame.image.load('images/bomb2!.png')
            d3 = pygame.image.load('images/bomb3!.png')
            d4 = pygame.image.load('images/bomb4!.png')
            d5 = pygame.image.load('images/bomb5!.png')
            take1 = pygame.image.load('images/heart.png')
            take2 = pygame.image.load('images/bonus.png')
            life = pygame.image.load('images/bone.png')
            life2 = pygame.image.load('images/fish.png')
            screen.blit(d1, [320, 170])
            screen.blit(d2, [420, 170])
            screen.blit(d3, [510, 170])
            screen.blit(d4, [600, 170])
            screen.blit(d5, [690, 170])
            screen.blit(take1, [320,295])
            screen.blit(take2, [690, 295])
            screen.blit(life, [340, 375])
            screen.blit(life2, [529, 375])
            text_x = h // 2 - text.get_width() // 2
            text_x2 = h // 2 - text2.get_width() // 2
            text_x3 = h // 2 - text3.get_width() // 2
            text_x4 = h // 2 - text4.get_width() // 2
            text_x5 = h // 2 - text5.get_width() // 2
            screen.blit(text, (text_x, 30))
            screen.blit(text2, (text_x2,125))
            screen.blit(text3, (text_x3, 250))
            screen.blit(text4, (text_x4, 375))
            screen.blit(text5, (text_x5, 500))
            pygame.display.flip()
            gui.add_element(b2)
        while ruls:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    ending = True
                    ruls = False
                    menurunning = False
                gui.get_event(event)
            gui.render(screen)
            gui.update()
            if b2.pressed:
                ruls = False
                menurunning = True
            pygame.display.update()
    menu()
mainmenue()
#realization of textures
if herotype:
    hero = pygame.image.load("images/hero2.png").convert_alpha()
    bone = pygame.image.load("images/fish.png")
else:
    hero = pygame.image.load("images/hero1.png").convert_alpha()
    bone = pygame.image.load("images/bone.png")
Player.images = [pygame.transform.flip(hero, 1, 0), hero]
bomba = pygame.image.load("images/bomb1!.png")
bonus = pygame.image.load("images/bonus.png")
hp = pygame.image.load("images/heart.png")
exp = pygame.image.load("images/Explosion1!.png")
Explosion.image=exp
Hearth.image = hp
Bomb.image = bomba
Bone.image = bone
Bonus.image = bonus
bombs = pygame.sprite.Group()
bone = pygame.sprite.Group()
bonus = pygame.sprite.Group()
hp = pygame.sprite.Group()
all = pygame.sprite.RenderUpdates()
Player.containers = all
Bomb.containers = bombs, all
Explosion.containers = all
Bone.containers = all, bone
Bonus.containers = all
Hearth.containers = all
player = Player()
pygame.mouse.set_visible(0)
#function of level
def lvl(num):
    global bmb
    global numlvl
    global ending
    global live
    global hearth
    bmb = 0
    reload = 0
    bombs = 0
    running1 = True
    num = num+1
    numlvl = num
    f = str(num)
    running = True
    while running:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and (event.type == pygame.KEYDOWN and event.key != pygame.K_ESCAPE ) :
                running = False
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                running1 = False
                ending = True
                live = False
                player.kill()
                break
        level(f)
        pygame.display.flip()
    chanse = random.randint(0, 10)
    hearthq = random.randint(0, num * kol)
    hearthch = False
    if chanse < 4:
         hearthch = True
    if player.alive():
        screen.blit(background_image, (0, 0))
        pygame.display.flip()
        numla = 1
        if numla == 1:
            font = pygame.font.Font(None, 50)
            text = font.render("Till the end: " + str(
                num * kol - bombs - 2) + '                                      ' + 'Your HP : ' + str(hearth+1), 4,
                               (254,241,28))
            text_x = h // 2 - text.get_width() // 2
            text_y = w // 2 - text.get_height() // 2
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(background_image, [0, 0])
            screen.blit(text, (50, 650))
            pygame.display.flip()
            numla = 0
    while running1 and player.alive():
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running1 = False
                ending = True
                player.kill()
        keystate = pygame.key.get_pressed()
        all.clear(screen, background_image)
        all.update()
        direction = keystate[pygame.K_RIGHT] - keystate[pygame.K_LEFT]
        player.move(direction)
        if bombs < num * kol and reload == 0:
            bombs += 1
            Bomb(random.randint(0, h))
            reload = rl
        if bombs == num * kol/2 :
            bombs += 1
            if not bonus:
                Bonus(random.randint(0, h))
                pygame.display.flip()
        elif bombs == hearthq:
            bombs+=1
            if hearthch:
                Hearth(random.randint(0,h))
        elif num * kol - 1 < bombs < num * kol + (kol/2):
            bombs += 1
        elif bombs == num * kol + (kol/2):
            bombs += 1
            Bone()
        elif reload > 0:
            reload -= 1
        scene = all.draw(screen)
        pygame.display.update(scene)
        pygame.time.Clock().tick(40)
#main loop
if lvlrunning:
    for i in range(numberlvl,5):
        if i == 1:
            background_image = pygame.image.load("images/background2!.png").convert()
            screen.blit(background_image, [0, 0])
            bomba = pygame.image.load("images/bomb2!.png")
            exp = pygame.image.load("images/Explosion2!.png")
            Explosion.image = exp
            Bomb.image = bomba
            pygame.display.flip()
        if i == 2:
            background_image = pygame.image.load("images/background3!.png").convert()
            screen.blit(background_image, [0, 0])
            bomba = pygame.image.load("images/bomb3!.png")
            exp = pygame.image.load("images/Explosion3!.png")
            Explosion.image = exp
            Bomb.image = bomba
            pygame.display.flip()
        if i == 3:
            background_image = pygame.image.load("images/background4!.png").convert()
            screen.blit(background_image, [0, 0])
            bomba = pygame.image.load("images/bomb4!.png")
            exp = pygame.image.load("images/Explosion4!.png")
            Explosion.image = exp
            Bomb.image = bomba
            pygame.display.flip()
        if i == 4:
            background_image = pygame.image.load("images/background5!.png").convert()
            screen.blit(background_image, [0, 0])
            bomba = pygame.image.load("images/bomb5!.png")
            exp = pygame.image.load("images/Explosion5!.png")
            Explosion.image = exp
            Bomb.image = bomba
            pygame.display.flip()
        if player.alive():
            lvl(i)
            if live:
                player = Player()
        else:
            break
#end of the game
if player.alive() == False and not ending:
    for q in range(600):
        end()
        pygame.display.flip()
if player.alive() == False and ending:
    background_image = pygame.image.load("images/background1!.png").convert()
    screen.blit(background_image, [0, 0])
    pygame.display.flip()
    pygame.quit()
pygame.quit()