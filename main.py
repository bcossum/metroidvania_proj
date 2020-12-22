import pygame as pg
import random
from settings import *
from sprites import *
from os import path


from pygame.locals import (
  RLEACCEL,
  K_UP,
  K_DOWN,
  K_LEFT,
  K_RIGHT,
  K_ESCAPE,
  KEYDOWN,
  KEYUP,
  QUIT,
  K_w,
  K_a,
  K_s,
  K_d,
)

class Game:
  def __init__(self):
    # Initialize Game
    pg.mixer.init()
    pg.init()
    pg.display.set_caption(TITLE)
    self.screen = pg.display.set_mode((WIDTH, HEIGHT))
    self.clock = pg.time.Clock()
    self.running = True
    self.font_name = pg.font.match_font(FONT_NAME)
    self.load_data()
    
  def load_data(self):
    self.dir = path.dirname(__file__)
    img_dir = path.join(self.dir, 'imgs')
    with open(path.join(self.dir, HS_FILE), 'w') as f:
      try:
        self.highscore = int(f.read())
      except:
        self.highscore = 0
    self.spritesheet = Spirtesheet(path.join(img_dir, SPRITESHEET))

  def new(self):
    # start a new game
    self.score = 0
    self.all_sprites = pg.sprite.Group()
    self.platforms = pg.sprite.Group()
    self.bullets = pg.sprite.Group()
    self.door = pg.sprite.Group()
    self.key = pg.sprite.Group()
    self.player = Player(self)
    self.all_sprites.add(self.player)
    # k = self.screen.blit(self.door, 395, 130)
    # d = self.screen.blit(self.key, 695, 430)
    for plat in MAP1_PLATFORM_LIST:
      p = Platform(self, *plat)
      self.all_sprites.add(p)
      self.platforms.add(p)
    #   self.key.add(k)
    #   self.door.add(d)
    # for plat in MAP2_PLATFORM_LIST:
    #   p = Platform(self, *plat)
    #   self.all_sprites.add(p)
    #   self.platforms.add(p)
    # if plat == MAP1_PLATFORM_LIST:
    #     # door_rect = self.screen.blit(self.door, (395, 130))
    #     # # if key_found == False:
    #     # key_rect = self.screen.blit(self.key, (680, 450))
    # if plat == MAP2_PLATFORM_LIST:
    #     door_rect = self.screen.blit(self.door, (695, 430))
    # if self.player.spritecollide(key_rect):
    #     key_found = True
    # if self.player.spritecollide(door_rect):
    #     if key_found == True:
    #         plat = MAP2_PLATFORM_LIST
    self.run()
    

  def run(self):
    # Game loop
    self.playing = True
    while self.playing:
      self.clock.tick(FPS)
      self.events()
      self.update()
      self.draw()

  def update(self):
    # Game Loop - Update
    self.all_sprites.update()
    # platform detection if falling
    if self.player.vel.y > 0:
      hits = pg.sprite.spritecollide(self.player, self.platforms, False)
      if hits:
        self.player.pos.y = hits[0].rect.top
        self.player.vel.y = 0
    # if self.player.rect.left >= HEIGHT - 200:
    #         self.player.pos.x -= abs(self.player.vel.x)
    #         for plat in self.platforms:
    #             plat.rect.x -= abs(self.player.vel.x)
    if self.player.rect.right <= WIDTH / 2:
            self.player.pos.x += abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x += abs(self.player.vel.x)
                # if plat.rect.right >= WIDTH:
                  # plat.kill()
                self.score += 1

    if self.player.rect.bottom > HEIGHT:
      for sprite in self.all_sprites:
        sprite.rect.y -= max(self.player.vel.y, 10)
        if sprite.rect.bottom <0:
          sprite.kill()
        if len(self.platforms) ==0:
          self.playing= False

    while len(self.platforms) < 6:
      width = random.randrange(50, 100)
      p = Platform(self, random.randrange(0, WIDTH-width),
                random.randrange(-75, -30))
      self.platforms.add(p)
      self.all_sprites.add(p)

  def events(self):
    # Game Loop - events
      keys = pg.key.get_pressed()
      for event in pg.event.get():
      # check for closing window
        if event.type == pg.QUIT:
          self.running = False
          if self.playing:
            self.playing = False
          
        
        if event.type == pg.KEYDOWN:
          if event.key == pg.K_UP:
            self.player.jump()

          if event.key == pg.K_SPACE:
            if keys[pg.K_d] and keys[pg.K_w]:
              facing = 3
            elif keys[pg.K_a] and keys[pg.K_w]:
              facing = -3
            elif keys[pg.K_w]:
              facing = 2
            elif keys[pg.K_d]:
              facing = 1
            elif self.player.left or keys[pg.K_a]:
              facing = -1        
            else:
              facing = 1
            b = Bullet(self.player.pos.x, self.player.pos.y, facing)
            self.all_sprites.add(b)
            self.bullets.add(b)

  def draw(self):
    #Game Loop - draw 
    self.screen.fill(BLACK)
    self.all_sprites.draw(self.screen)
    self.screen.blit(self.player.image, self.player.rect)
    self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15) 
    pg.display.flip()


  def show_start_screen(self):
    # game splash/start screen
    self.screen.fill(BLACK)
    self.draw_text("Welcome to Metroidvania... Enter if you dare!", 48, BLUE, WIDTH /2, HEIGHT / 4)
    self.draw_text("Controls: Right and Left Arrow to move, Up Arrow to jump", 22, WHITE, WIDTH / 2, HEIGHT /2)
    self.draw_text("You ready? Press a key to play", 22, WHITE, WIDTH /2, HEIGHT * 3/4)
    self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH /2, 15)
    pg.display.flip()
    self.wait_for_key()

  def show_go_screen(self):
    #game over/continue
    self.screen.fill(BLACK)
    if self.score < 4000:
      self.draw_text("You are pretty bad at this! GAME OVER!!!", 48, RED, WIDTH /2, HEIGHT / 4)
    else:
      self.draw_text("I've seen better! GAME OVER!", 48, RED, WIDTH /2, HEIGHT / 4)
    self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT /2)
    self.draw_text("Press key to play again", 22, WHITE, WIDTH /2, HEIGHT * 3/4)
    if self.score > self.highscore:
      self.highscore = self.score
      self.draw_text("New High Score: " + str(self.highscore), 22, WHITE, WIDTH /2, HEIGHT/2 + 40)
      with open(path.join(self.dir, HS_FILE), 'w') as f:
        f.write(str(self.score))
    else: 
      self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH /2, HEIGHT/2 + 40)
    pg.display.flip()
    self.wait_for_key()


  def wait_for_key(self):
    waiting = True
    while waiting:
      self.clock.tick(FPS)
      for event in pg.event.get():
        if event.type == pg.QUIT:
          waiting = False
          self.running = False
        if event.type == pg.KEYUP:
          waiting = False


  def draw_text(self, text, size, color, x, y):
    font = pg.font.Font(self.font_name, size)
    text_surface = font.render(text, True, color)
    text_rect= text_surface.get_rect()
    text_rect.midtop = (x,y)
    self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.run:
  g.new()
  g.show_go_screen()

pg.quit()