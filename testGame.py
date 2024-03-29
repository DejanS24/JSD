"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/

From:
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py

Explanation video: http://youtu.be/QplXBw_NK5Y

Part of a series:
http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py
http://programarcadegames.com/python_examples/f.php?file=maze_runner.py
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py
http://programarcadegames.com/python_examples/f.php?file=platform_moving.py
http://programarcadegames.com/python_examples/sprite_sheets/

"""

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

GAME_TITLE = "Side scrolling platformer"
FONT_NAME = "arial"
DEFAULT_COLOR = BLACK
FPS = 60


class Player(pygame.sprite.Sprite):
    """
    This class represents the bar at the bottom that the player controls.
    """

    movespeed = 6
    buff_timer = 5

    # -- Methods
    def __init__(self, game):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.width = 40
        self.height = 60

        # self.image = pygame.Surface([width, height])
        # self.image.fill(RED)

        self.default_image = pygame.image.load("C:/Users/Dejan/Pictures/spriteTest3.PNG")
        self.idle_image = pygame.image.load("C:/Users/Dejan/Pictures/spriteTest4.PNG")
        self.jumping_image = pygame.image.load("C:/Users/Dejan/Pictures/spriteTest5.PNG")
        self.image = pygame.transform.scale(self.default_image, (self.width, self.height))

        self.standing_frames = [self.default_image, self.idle_image]
        self.walking_frames = [self.default_image, self.idle_image]

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        # List of sprites we can bump against
        self.level = None

    def update(self):
        """ Move the player. """
        self.animate()
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
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.game.jump_sound.play()
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

    def animate(self):
        now = pygame.time.get_ticks()
        if self.change_x != 0:
            self.walking = True
        else:
            self.walking = False

        if self.change_y != 0:
            self.jumping = True
        else:
            self.jumping = False

        # show walk animation
        if self.walking or (not self.jumping and not self.walking):
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames)
                bottom = self.rect.bottom
                x_c = self.rect.x
                self.image = pygame.transform.scale(self.walking_frames[self.current_frame], (self.width, self.height))
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.rect.x = x_c
    #
        if self.jumping:
            bottom = self.rect.bottom
            x_c = self.rect.x
            self.image = pygame.transform.scale(self.jumping_image, (self.width, self.height))
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
            self.rect.x = x_c

        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                x_c = self.rect.x
                self.image = pygame.transform.scale(self.standing_frames[self.current_frame], (self.width, self.height))
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.rect.x = x_c
        # self.mask = pygame.mask.from_surface(self.image)
    #


class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height, image=None):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super().__init__()

        self.image = pygame.Surface([width, height])
        if image:
            img = pygame.image.load(image)
            self.image = pygame.transform.scale(img, (width, height))
        else:
            self.image.fill(GREEN)

        self.rect = self.image.get_rect()


class Level:
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.pickups = pygame.sprite.Group()
        self.player = player

        self.background = pygame.image.load("C:/Users/Dejan/Pictures/boujee3.PNG")

        # How far this world has been scrolled left/right
        self.world_shift = 0

        self.boost = SpeedBoost(player)

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


class Item(pygame.sprite.Sprite):

    def __init__(self, player, color=WHITE):
        super().__init__()

        self.player = player
        width = 30
        height = 30
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()

    def picked_up(self):
        self.kill()


class SpeedBoost(Item):
    def picked_up(self):
        super().picked_up()
        self.player.game.boost_sound.play()
        self.player.movespeed = 20


class Point(Item):
    def picked_up(self):
        super().picked_up()
        self.player.game.point_sound.play()
        self.player.game.score += 10


# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -1000

        self.boost.rect.x = 520
        self.boost.rect.y = 320
        self.pickups.add(self.boost)

        self.point1 = Point(self.player, BLUE)
        self.point1.rect.x = 600
        self.point1.rect.y = 200
        self.pickups.add(self.point1)

        # Array with width, height, x, and y of platform
        level = [[210, 70, 500, 500],
                 [210, 70, 800, 400],
                 [210, 70, 1000, 500],
                 [210, 70, 1120, 280],
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1], "C:/Users/Dejan/Pictures/Backgrounds/11louisenadeau-springrain.jpg")
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            self.platform_list.add(block)


# Create platforms for the level
class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -1000

        self.boost.rect.x = 500
        self.boost.rect.y = 300
        self.pickups.add(self.boost)

        # Array with type of platform, and x, y location of the platform.
        level = [[210, 30, 450, 570],
                 [210, 30, 850, 420],
                 [210, 30, 1000, 520],
                 [210, 30, 1120, 280],
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            self.platform_list.add(block)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.load_sounds()

    def load_sounds(self):
        self.jump_sound = pygame.mixer.Sound("C:/Users/Dejan/Music/Jump33.wav")
        self.boost_sound = pygame.mixer.Sound("C:/Users/Dejan/Music/Boost16.wav")
        self.point_sound = pygame.mixer.Sound("C:/Users/Dejan/Music/Jump40.wav")

    def new(self):
        self.score = 0
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.level_list = []
        self.level_list.append(Level_01(self.player))
        self.level_list.append(Level_02(self.player))

        self.current_level_no = 0
        self.current_level = self.level_list[self.current_level_no]
        self.player.level = self.current_level
        pygame.mixer.music.load("C:/Users/Dejan/Music/Happy Tune.ogg")
        self.run()

    def run(self):
        pygame.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(500)

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

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT or \
        #             (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        #         if self.playing:
        #             self.playing = False
        #         self.running = False
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_SPACE:
        #             self.player.jump()

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
        self.draw_text("Press SPACE to play again", 22, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)

        pygame.display.flip()
        pygame.mixer.music.load("C:/Users/Dejan/Music/Yippee.ogg")
        pygame.mixer.music.play(loops=-1)

        self.wait_for_key()
        pygame.mixer.music.fadeout(500)

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


def main():

    """ Main Program """
    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Side-scrolling Platformer")

    # Create the player
    player = Player()

    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)
    for l in level_list:
        active_sprite_list.add(l.boost)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
             (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                done = True

            if event.type == pygame.KEYDOWN:
                if player.pickup_boost(current_level.boost):
                    player.speed_boost()
                    current_level.boost.picked_up()
                    # current_level.boost.remove([active_sprite_list])
                    # active_sprite_list.remove(current_level.boost)

                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        # Update the player.
        active_sprite_list.update()

        # Update items in the level
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 20:
            diff = 20 - player.rect.left
            player.rect.left = 20
            current_level.shift_world(diff)

        # If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            player.rect.x = 120
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()


if __name__ == "__main__":
    # main()

    g = Game()
    # show start screen
    while g.running:
        g.new()
        g.show_end_screen()

    pygame.quit()
