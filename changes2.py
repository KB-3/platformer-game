
# Imports
import pygame
import random
import json

# Window settings
GRID_SIZE = 116
WIDTH = 16 * GRID_SIZE
HEIGHT = 9 * GRID_SIZE
TITLE = "Platformer"
FPS = 60


# Create window
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (0, 150, 255)
GRAY = (175, 175, 175)

# Load fonts
font_xs = pygame.font.Font(None, 14)
font_md = pygame.font.Font('assets/fonts/Dinomouse-Regular.otf', 32)
font_sm = pygame.font.Font('assets/fonts/Dinomouse-Regular.otf', 24)
font_xl = pygame.font.Font('assets/fonts/Dinomouse-Regular.otf', 96)
font_lg = pygame.font.Font('assets/fonts/Dinomouse-Regular.otf', 64)

# Stages
START = 0
PLAYING = 1
LOSE = 2
LEVEL_COMPLETE = 3
WIN = 7

# Load images
hero_h_imgs = [pygame.image.load('assets/images/characters/gum.png').convert_alpha(),
               pygame.image.load('assets/images/characters/gum1.png').convert_alpha()]   
          

grass_dirt_img = pygame.image.load('assets/images/tiles/ngrass.jpg').convert_alpha()
block_img = pygame.image.load('assets/images/tiles/nbb.jpg').convert_alpha()
gem_img = pygame.image.load('assets/images/items/gemm.png').convert_alpha()
heart_img = pygame.image.load('assets/images/items/heart1.png').convert_alpha()
pear_img = pygame.image.load('assets/images/items/pear.png').convert_alpha()
strawberry_img = pygame.image.load('assets/images/items/straw.png').convert_alpha()
background_img = pygame.image.load('assets/images/characters/background.jpg').convert_alpha()
heartpickup_imgs = [pygame.image.load('assets/images/items/heartpick.png').convert_alpha()]

coins_imgs = [pygame.image.load('assets/images/items/c1.png').convert_alpha(),
              pygame.image.load('assets/images/items/c2.png').convert_alpha(),
              pygame.image.load('assets/images/items/c3.png').convert_alpha(),
              pygame.image.load('assets/images/items/c4.png').convert_alpha(),
              pygame.image.load('assets/images/items/c5.png').convert_alpha()]

 
greenblob_imgs = [pygame.image.load('assets/images/characters/greenblob.png').convert_alpha()]

purpleblob_imgs = [pygame.image.load('assets/images/characters/purp.png').convert_alpha()]

redzombie_imgs = [pygame.image.load('assets/images/characters/redzom.png').convert_alpha(),
                  pygame.image.load('assets/images/characters/redzomhit.png').convert_alpha()]

flag_img = pygame.image.load('assets/images/tiles/nflag.png').convert_alpha()
pole_img = pygame.image.load('assets/images/tiles/nflagpole.png').convert_alpha()


# Load music
start_music = ('assets/music/intro.ogg')
main_music = ('assets/music/main.ogg')

# Load sounds
gem_snd = pygame.mixer.Sound('assets/sounds/gem.ogg')
heart_snd = pygame.mixer.Sound('assets/sounds/heart.ogg')
coin_snd = pygame.mixer.Sound('assets/sounds/coin.ogg')

# Levels
levels = ['assets/levels/world-1.json',
          'assets/levels/world-2.json',
          'assets/levels/world-3.json',
          'assets/levels/world-4.json',
          'assets/levels/world-5.json',
          'assets/levels/world-6.json',
          'assets/levels/world-7.json']

# Game classes
class Entity(pygame.sprite.Sprite):

     def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x * GRID_SIZE 
        self.rect.y = y * GRID_SIZE
         
          
        self.vx = 0
        self.vy = 0

     def apply_gravity(self):
         self.vy += gravity

         if self.vy > terminal_velocity:
              self.vy = terminal_velocity

     
                      
class AnimatedEntity(Entity):

    def __init__(self, x, y, images):
        super().__init__(x, y, images[0])

        self.images = images
        self.image_index = 0
        self.ticks = 0
        self.animation_speed = 1

    def animate(self):
        self.ticks += 1

        if self.ticks % self.animation_speed == 0:
            self.image_index += 1

            if self.image_index >= len(self.images):
                self.image_index = 0
                
            self.image = self.images[self.image_index]

    
class Platform(Entity):

     def __init__(self, x, y, image):
        super().__init__(x, y, image)


class Flag(Entity):

     def __init__(self, x, y, image):
        super().__init__(x, y, image)
       

class Enemy(AnimatedEntity):

     def __init__(self, x, y, images):
        super().__init__(x, y, images)

     
        self.vx = -2
        self.vy = 0

     def reverse(self):
          self.vx *= -1


     def move_and_check_platforms(self):
        
        self.rect.x += self.vx

        hits = pygame.sprite.spritecollide(self, platforms, False)

        for hit in hits:
            if self.vx > 0:
                self.rect.right = hit.rect.left
                self.reverse()
            elif self.vx < 0:
                self.rect.left = hit.rect.right
                self.reverse()

        self.rect.y += self.vy

        hits = pygame.sprite.spritecollide(self, platforms, False)

        for hit in hits:
             if self.vy > 0:
                  self.rect.bottom = hit.rect.top
             if self.vy < 0:
                  self.rect.top = hit.rect.bottom


             self.vy = 0

   
     def check_world_edges(self):
          if self.rect.left < 0:
              self.rect.left = 0
              self.reverse()
          elif self.rect.right > world_width:
              self.rect.right = world_width
              self.reverse()

    
     def check_platform_edges(self):
          self.rect.y += 2
          hits = pygame.sprite.spritecollide(self, platforms, False)
          self.rect.y -= 2

          must_reverse = True

          for platform in hits:
               if self.vx < 0 and platform.rect.left <= self.rect.left:
                    must_reverse = False
               elif self.vx > 0 and platform.rect.right >= self.rect.right:
                    must_reverse = False

               if must_reverse:
                    self.reverse()

class greenblob(Enemy):
      def __init__(self, x, y, images):
        super().__init__(x, y, images)


      def update(self):
        self.apply_gravity()
        self.move_and_check_platforms()
        self.check_world_edges()
        self.animate()

class purpleblob(Enemy):
      def __init__(self, x, y, images):
        super().__init__(x, y, images)


      def update(self):
        self.apply_gravity()
        self.move_and_check_platforms()
        self.check_world_edges()
        self.check_platform_edges()
        self.animate()

class redzombie(Enemy):
      def __init__(self, x, y, images):
        super().__init__(x, y, images)

      def update(self):
        self.move_and_check_platforms()
        self.check_world_edges()
        


class Hero(AnimatedEntity):
    
    def __init__(self, x, y, images):
        super().__init__(x, y, images)


        self.speed = 5
        self.jump_power = 18
        self.vx = 0
        self.vy = 0

        self.hearts = 3
        self.gems = 0
        self.score = 0
        self.coins = 0

        
        self.hurt_timer = 0
        self.animate_timer = 0

    def move_to(self, x, y):
         self.rect.centerx = x * GRID_SIZE + GRID_SIZE // 2
         self.rect.centery = y * GRID_SIZE + GRID_SIZE // 2
         
    def move_right(self):
    	self.vx = +self.speed
    	
    def move_left(self):
    	self.vx = -self.speed

    def stop(self):
        self.vx = 0
    
    def jump(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 2

        if len(hits) > 0:
             self.vy = -1 * self.jump_power


    def check_enemies(self):
         hits = pygame.sprite.spritecollide(self, enemies, False)

         for enemy in hits:
              enemy.animate()
              if self.hurt_timer == 0:
                   self.hearts -= 1
                   print(self.hearts)
                   print("Oof!")
                   self.hurt_timer = 1.0 * FPS
              else:
                   self.hurt_timer -= 1

              if self.hurt_timer < 0:
                   self.hurt_timer = 0
                   hero.kill()

              if self.rect.x < enemy.rect.x:
                   self.vx = -15
              elif self.rect.x > enemy.rect.x:
                   self.vx = 15

              if self.rect.y < enemy.rect.y:
                   self.vy = -5
              elif self.rect.y > enemy.rect.y:
                   self.vy = 5
               
                    




    def move_and_check_platforms(self):
         self.rect.x += self.vx

         hits = pygame.sprite.spritecollide(self, platforms, False)

         for hit in hits:
             if self.vx > 0:
                 self.rect.right = hit.rect.left
             elif self.vx < 0:
                 self.rect.left = hit.rect.right

         self.rect.y += self.vy

         hits = pygame.sprite.spritecollide(self, platforms, False)

         for hit in hits:
              if self.vy > 0:
                   self.rect.bottom = hit.rect.top
              if self.vy < 0:
                   self.rect.top = hit.rect.bottom
              self.vy = 0
       

    def check_world_edges(self):
     if self.rect.left < 0:
         self.rect.left = 0
     elif self.rect.right > world_width:
         self.rect.right = world_width

    def check_items(self):
           hits = pygame.sprite.spritecollide(self, items, True)

           for item in hits:
                item.apply(self)

    
    def check_powers(self):
           hits = pygame.sprite.spritecollide(self, powers, True)

           for power in hits:
               power.apply(self)

    def reached_goal(self):
         return pygame.sprite.spritecollideany(self, goal)

    def set_image_list(self):
        if powerup:
            self.animate()
        else:
            self.images = hero_h_imgs

    def update(self):
          self.apply_gravity()
          self.check_enemies()
          self.move_and_check_platforms()   
          self.check_world_edges()
          self.check_items()
          self.check_powers()
          
         

class Gem(Entity):
     def __init__(self, x, y, image):
          super().__init__(x, y, image)

     def apply(self, character):
          gem_snd.play()  
          character.gems += 1
          character.score += 36 
          print(character.gems)

class Powerup(AnimatedEntity):

     def __init__(self, x, y, images):
        super().__init__(x, y, images)

class Coin(Powerup):
     def __init__(self, x, y, images):
          super().__init__(x, y, images)

     

     def apply(self, character):
         coin_snd.play()
         if character.hearts < 3:
             character.animate()
             character.coins += 1
             character.score += 300

         else:
             character.coins += 1
             character.score += 120

class Life(Powerup):
     def __init__(self, x, y, images):
          super().__init__(x, y, images)

     

     def apply(self, character):

             heart_snd.play()  
             character.animate()
             character.hearts += 1
             character.score += 500
             



#Helper Functions
def show_start_screen():
     text = font_xl.render(TITLE, True, WHITE)
     rect = text.get_rect()
     rect.midbottom = WIDTH // 2, HEIGHT // 2
     screen.blit(text, rect)

     text = font_sm.render('press any key to start', True, WHITE)
     rect = text.get_rect()
     rect.midtop = WIDTH // 2, HEIGHT // 2
     screen.blit(text, rect)

def show_lose_screen():
     text = font_lg.render('Game Over', True, WHITE)
     rect = text.get_rect()
     rect.midbottom = WIDTH // 2, HEIGHT // 2
     screen.blit(text, rect)

     text = font_sm.render('press \'r\' to play again', True, WHITE)
     rect = text.get_rect()
     rect.midtop = WIDTH // 2, HEIGHT // 2
     screen.blit(text, rect) 

def show_win_screen():
     text = font_lg.render('You Win!', True, WHITE)
     rect = text.get_rect()
     rect.midbottom = WIDTH // 2, HEIGHT // 2
     screen.blit(text, rect)

     text = font_sm.render('press \'r\' to play again', True, WHITE)
     rect = text.get_rect()
     rect.midtop = WIDTH // 2, HEIGHT // 2
     screen.blit(text, rect)
     
def show_level_complete_screen():
     text = font_lg.render('Level Complete!', True, WHITE)
     rect = text.get_rect()
     rect.midbottom = WIDTH // 2, HEIGHT // 2
     screen.blit(text, rect)


def show_hud():
     text = font_md.render('Score:'+ str(hero.score), True, WHITE)
     rect = text.get_rect()
     rect.midtop = WIDTH // 2, 16
     screen.blit(text, rect)

     screen.blit(gem_img, [WIDTH - 116, 16])
     text = font_sm.render('x' + str(hero.gems), True, WHITE)
     rect = text.get_rect()
     rect.topleft = WIDTH - 60, 24
     screen.blit(text, rect)

     text = font_md.render("Level: " + str(current_level + 1), True, WHITE)
     rect = text.get_rect()
     rect.midtop = WIDTH - 1000, 900
     rect.right = WIDTH - 20
     screen.blit(text, rect)

     for i in range(hero.hearts):
          x = -i * 30 + 16 
          y = 16
          screen.blit(heart_img, [x, y])





                 
def draw_grid(offset_x=0, offset_y=0):
    for x in range(0, WIDTH + GRID_SIZE, GRID_SIZE):
        adj_x = x - offset_x % GRID_SIZE
        pygame.draw.line(screen, GRAY, [adj_x, 0], [adj_x, HEIGHT], 1)

    for y in range(0, HEIGHT + GRID_SIZE, GRID_SIZE):
        adj_y = y - offset_y % GRID_SIZE
        pygame.draw.line(screen, GRAY, [0, adj_y], [WIDTH, adj_y], 1)

    for x in range(0, WIDTH + GRID_SIZE, GRID_SIZE):
        for y in range(0, HEIGHT + GRID_SIZE, GRID_SIZE):
            adj_x = x - offset_x % GRID_SIZE + 4
            adj_y = y - offset_y % GRID_SIZE + 4
            disp_x = x // GRID_SIZE + offset_x // GRID_SIZE
            disp_y = y // GRID_SIZE + offset_y // GRID_SIZE
            
            point = '(' + str(disp_x) + ',' + str(disp_y) + ')'
            text = font_xs.render(point, True, GRAY)
            screen.blit(text, [adj_x, adj_y])



     
# Setup
def start_game():
     global hero, stage, current_level
     
     hero = Hero(0, 0, hero_h_imgs)
     stage = START
     current_level = 0

     pygame.mixer.music.load(start_music)
     pygame.mixer.music.play(-1)   
def start_level():
     global player, platforms, items, powers, enemies, goal, all_sprites
     global gravity, terminal_velocity
     global world_width, world_height
     
     player = pygame.sprite.GroupSingle()
     platforms = pygame.sprite.Group()
     items = pygame.sprite.Group()
     powers = pygame.sprite.Group()
     enemies = pygame.sprite.Group()
     goal = pygame.sprite.Group()
     all_sprites = pygame.sprite.Group()

     with open(levels[current_level]) as f:
          data = json.load(f)
     

     world_width = data['width'] * GRID_SIZE
     world_height = data['height'] * GRID_SIZE


     hero.move_to(data['start'][0], data['start'][1])
     player.add(hero)
     
     
     for i, loc in enumerate(data['flag_locs']):
          if i == 0:
               goal.add( Flag(loc[0], loc[1], flag_img) )
          else:
                goal.add( Flag(loc[0], loc[1], pole_img) )

     for loc in data['grass_locs']:
          platforms.add( Platform (loc[0], loc[1], grass_dirt_img) )
         

     for loc in data ['block_locs']:
          platforms.add( Platform (loc[0], loc[1], block_img) )





     for loc in data ['gem1_locs']:
          items.add( Gem (loc[0], loc[1], gem_img) )





     for loc in data ['gem2_locs']:
          items.add( Gem (loc[0], loc[1], pear_img) )



     for loc in data ['gem3_locs']:
          items.add( Gem (loc[0], loc[1], strawberry_img) )


     for loc in data ['coin_loc']:
          powers.add( Coin (loc[0], loc[1], coins_imgs) )

     
     for loc in data ['life_loc']:
          powers.add( Life (loc[0], loc[-1], heartpickup_imgs) )

     for loc in data ['greenblob_locs']:
          enemies.add( greenblob (loc[0], loc[1], greenblob_imgs) )




     for loc in data ['purpleblob_locs']:
          enemies.add( purpleblob (loc[0], loc[1], purpleblob_imgs) )


     for loc in data ['redzombie_locs']:
          enemies.add( redzombie (loc[0], loc[1], redzombie_imgs) )

     start_x = 3
     start_y = 7
     

     gravity = data['gravity']
     terminal_velocity = data['terminal_velocity']

     all_sprites.add(player, platforms, items, powers, enemies, goal)

# Game loop

grid_on = False
running = True

start_game()
start_level()

while running:
    # Input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
             if stage == START:
                  stage = PLAYING
                  pygame.mixer.music.load(main_music)
                  pygame.mixer.music.play(-1)

             elif stage == PLAYING:
                  if event.key == pygame.K_SPACE:
                       hero.jump()


             elif stage == LOSE or stage == WIN:
                  if event.key == pygame.K_r:
                       start_game()
                       start_level()

                  
      

             if event.key == pygame.K_g:
                  grid_on = not grid_on



    pressed = pygame.key.get_pressed()

    if stage == PLAYING:
         if pressed[pygame.K_LEFT]:
             hero.move_left()
         elif pressed[pygame.K_RIGHT]:
             hero.move_right()
         else:
             hero.stop()

    # Game logic
    if stage == PLAYING:
         all_sprites.update()

         if hero.hearts == 0:
              stage = LOSE

         elif hero.reached_goal():
              stage = LEVEL_COMPLETE
              countdown = 2 * FPS
    elif stage == LEVEL_COMPLETE:
         countdown -= 1
         if countdown <= 0:
              current_level += 1

              if current_level < len(levels):
                   start_level()
                   stage = PLAYING
              else:
                   stage = WIN

    if hero.rect.centerx < WIDTH // 2:
         offset_x = 0
    elif hero.rect.centerx > world_width - WIDTH // 2:
         offset_x = world_width - WIDTH
    else:
         offset_x = hero.rect.centerx - WIDTH // 2
               
    
 
    
    # Drawing code
    screen.fill(WHITE)
    screen.blit(background_img, [0,0])
    for sprite in all_sprites:
         screen.blit(sprite.image, [sprite.rect.x - offset_x, sprite.rect.y])
    
    show_hud()

    if grid_on:
         draw_grid(offset_x)

    if stage == START:
         show_start_screen()
    elif stage == LOSE:
         show_lose_screen()
    elif stage == WIN:
         show_win_screen()
    elif stage == LEVEL_COMPLETE:
         show_level_complete_screen()
    
    # Update screen
    pygame.display.update()


    # Limit refresh rate of game loop 
    clock.tick(FPS)


# Close window and quit
pygame.quit()

