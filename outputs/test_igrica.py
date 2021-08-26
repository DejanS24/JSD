import pygame

# Global constants

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GAME_TITLE = 'Test igrica'
FONT_NAME = 'arial'
DEFAULT_COLOR = BLACK
FPS = 60

# Test igrica
class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """

    # -- Methods
    def __init__(self, game):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        self.game = game
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.width = 40
        self.height = 80
        self.last_update = 0
        self.current_frame = 0

        self.default_image = pygame.image.load("C:/Users/Dejan/Pictures/spriteTest3.PNG")
        self.image = pygame.transform.scale(self.default_image, (self.width, self.height))

        self.movespeed = 6

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        # List of sprites we can bump against
        self.level = None

    def update(self):
        """ Move the player. """
    
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

        pickups_hit_list = pygame.sprite.spritecollide(self, self.level.pickups, False)
        for pickup in pickups_hit_list:
            pickup.picked_up()

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = - self.movespeed

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = self.movespeed

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0


class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height, image=None):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()

        self.image = pygame.Surface([width, height])
        if image:
            img = pygame.image.load(image)
            self.image = pygame.transform.scale(img, (width, height))
        else:
            self.image.fill(GREEN)

        self.rect = self.image.get_rect()



class Item(pygame.sprite.Sprite):

    def __init__(self, player, color=WHITE):
        super().__init__()

        self.player = player
        self.width = 20
        self.height = 40
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color)

        self.rect = self.image.get_rect()

    def set_img(self, path):
        img = pygame.image.load(path)
        self.image = pygame.transform.scale(img, (self.width, self.height))

    def picked_up(self):
        self.kill()


class SpeedBoost(Item):
    def picked_up(self):
        super().picked_up()
        self.player.movespeed = 20


class Point(Item):
    def picked_up(self):
        super().picked_up()
        self.player.game.score += 10



class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.pickups = pygame.sprite.Group()
        self.player = player

        # Background image
        self.background = None

        # How far this world has been scrolled left/right
        self.world_shift = 0

        # self.boost = SpeedBoost()
        # self.boost.rect.x = 400
        # self.boost.rect.y = 200


    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
        self.pickups.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        if self.background:
          screen.blit(self.background, (0, 0))
        else:
          screen.f(BLUE)

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.pickups.draw(screen)

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll
        everything: """

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        for pickup in self.pickups:
            pickup.rect.x += shift_x



class Level1(Level):
    """ Definition for level Level1. """

    def __init__(self, player):
        """ Create level. """

        # Call the parent constructor
        Level.__init__(self, player)
        self.background = pygame.image.load("C:/Users/Dejan/Pictures/game_background12.jpg")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.item1 = SpeedBoost(self.player, GREEN)
        self.item1.rect.x = 120
        self.item1.rect.y = 150
        self.pickups.add(self.item1)
    

        self.level_limit = -1000
        platform1 = Platform(370, 100, 'C:/Users/Dejan/Pictures/Backgrounds/11louisenadeau-springrain.jpg')
        platform1.rect.x = 420
        platform1.rect.y = 210
        self.platform_list.add(platform1)
    

class Level2(Level):
    """ Definition for level Level2. """

    def __init__(self, player):
        """ Create level. """

        # Call the parent constructor
        Level.__init__(self, player)
        self.background = pygame.image.load("C:/Users/Dejan/Pictures/game_background13.jpg")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.level_limit = -1000
        platform1 = Platform(370, 100)
        platform1.rect.x = 420
        platform1.rect.y = 415
        self.platform_list.add(platform1)
    

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False
        self.font_name = pygame.font.match_font(FONT_NAME)

    def new(self):
        self.score = 0
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.level_list = []
    
        self.level_list.append(Level1(self.player))
        self.level_list.append(Level2(self.player))

        self.current_level_no = 0
        self.current_level = self.level_list[self.current_level_no]
        self.player.level = self.current_level
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False

                if event.key == pygame.K_LEFT:
                    self.player.go_left()
                if event.key == pygame.K_RIGHT:
                    self.player.go_right()
                if event.key == pygame.K_UP:
                    self.player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.change_x < 0:
                    self.player.stop()
                if event.key == pygame.K_RIGHT and self.player.change_x > 0:
                    self.player.stop()

    def update(self):
        self.all_sprites.update()

        self.current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if self.player.rect.right >= 500:
            diff = self.player.rect.right - 500
            self.player.rect.right = 500
            self.current_level.shift_world(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if self.player.rect.left <= 20 and self.current_level.world_shift > 20:
            self.player.rect.left = 20
        elif self.player.rect.left <= 20 and self.current_level.world_shift < 25:
            diff = 20 - self.player.rect.left
            self.player.rect.left = 20
            self.current_level.shift_world(diff)

        # If the player gets to the end of the level, go to the next level
        current_position = self.player.rect.x + self.current_level.world_shift
        if current_position < self.current_level.level_limit:
            self.player.rect.x = 120
            self.score += 30
            if self.current_level_no < len(self.level_list)-1:
                self.current_level_no += 1
                self.current_level = self.level_list[self.current_level_no]
                self.player.level = self.current_level
            else:
                self.playing = False

    def draw(self):
        self.current_level.draw(self.screen)
        self.all_sprites.draw(self.screen)

        #draw score
        self.draw_text(str(self.score), 22, WHITE, SCREEN_WIDTH / 2, 15)

        pygame.display.flip()

    def show_end_screen(self):
        if not self.running:
            return
        self.screen.fill(DEFAULT_COLOR)
        self.draw_text("GAME OVER", 48, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)

        pygame.display.flip()

        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                   (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


if __name__ == "__main__":
    g = Game()
    # show start screen
    while g.running:
        g.new()
        g.show_end_screen()

    pygame.quit()