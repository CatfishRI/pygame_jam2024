# Import the pygame module
# Import random for random numbers
import random
import sys
import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_DOWN,
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    K_UP,
    KEYDOWN,
    QUIT,
)

#initialize pygame

pygame.init()

# Define constants for the screen width and height
infoObject = pygame.display.Info()
SCREEN_WIDTH = infoObject.current_w
SCREEN_HEIGHT = infoObject.current_h

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# story

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# variable for mode
play_mode = 0
speed = 0
luck = 0

# Set up the font for rendering text
FONT_SIZE = 24
font = pygame.font.Font(None, FONT_SIZE)

# Define the game states
INTRO = "intro"
CHOOSE_PLANE = "choose_plane"
CHOOSE_MODE = "choose_mode"
GAME_OVER = "game_over"
ENDING = "ending"
PLAY = "play"

# gameplay

# Initialize game state
current_state = INTRO

# Initialize user input variables
user_input = ""

# Initialize feedback messages for each state
feedback = {
    CHOOSE_PLANE: "",
    CHOOSE_MODE: ""
}


def render_text(lines, start_y=50, line_spacing=30, feedback_message=""):
    """
    Renders a list of text lines on the screen starting from start_y with specified spacing.
    Optionally displays a feedback message.
    """
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, WHITE)
        screen.blit(text_surface, (50, start_y + i * line_spacing))

    if feedback_message:
        feedback_surface = font.render(
            feedback_message, True, (255, 0, 0))  # Red color for feedback
        screen.blit(feedback_surface, (50, start_y +
                    len(lines) * line_spacing + 10))

def introduction():
    """
    Displays the introduction scene.
    """
    global current_state
    lines = [
        "Welcome to Plane FI!",
        "You are part of the Earth Defence Force, and are fighting against aliens from space!",
        "But beware, the aliens are smart and are firing at you from above...",
        "It is up to you to reach them and protect our planet!"
        "",
        "Press ENTER to start your attack..."
    ]
    render_text(lines, start_y=50, line_spacing=30)

def plane():
    """
    Presents the first choice to the player.
    """
    global current_state
    lines = [
        "Choose your plane:",
        "1. Lucky Snail",
        "2. Speedy Seal",
        "",
        "Enter 1 or 2:"
    ]
    render_text(lines, start_y=50, line_spacing=30,
                feedback_message=feedback[CHOOSE_PLANE])

def playmode():
    """
    Presents the first choice to the player.
    """
    global current_state
    lines = [
        "Choose your battle:",
        "1. Normal",
        "2. Bullet Hell",
        "3. Uncertain Ultimatum",
        "4. Missile Maneuver",
        "5. Infinite Insanity"
        "",
        "Enter 1, 2, 3, 4 or 5:"
    ]
    render_text(lines, start_y=50, line_spacing=30,
                feedback_message=feedback[CHOOSE_MODE])

def ending():
    """
    Displays the game ending.
    """
    global current_state
    lines = [
        "Congratulations! You've defeated the evil aliens!",
        "They have been pushed back to their home world and will never be seen again.",
        "As a reward, you are named a general of the Defence Force",
        "However, there are more aliens out there waiting for their chance to strike...",
        "",
        "Press Enter to play again"
    ]
    render_text(lines, start_y=50, line_spacing=30)

def game_over():
    """
    Displays a game over message.
    """
    global current_state
    lines = [
        f"Game Over!",
        "",
        "Press ENTER to play again"
    ]
    render_text(lines, start_y=50, line_spacing=30)

def handle_input():
    global current_state, user_input, feedback, speed, luck, play_mode

    if current_state == INTRO:
        current_state = CHOOSE_MODE
        user_input = ""
        feedback[CHOOSE_MODE] = ""

    elif current_state == CHOOSE_MODE:
        if user_input in ["1", "2", "3", "4", "5"]:
            play_mode = int(user_input)
            current_state = CHOOSE_PLANE
            feedback[CHOOSE_PLANE] = ""
        else:
            feedback[CHOOSE_MODE] = "Invalid choice. Please enter 1, 2, 3, 4 or 5."
        user_input = ""

    elif current_state == CHOOSE_PLANE:
        if user_input == "1":
            speed = 18
            luck = 18
            current_state = PLAY
        elif user_input == "2":
            speed = 27
            luck = 9
            current_state = PLAY
        else:
            feedback[CHOOSE_PLANE] = "Not a choice. Please try again."
        user_input = ""

    elif current_state == GAME_OVER:
        current_state = INTRO
        user_input = ""
        feedback[INTRO] = ""

    elif current_state == ENDING :
        current_state = INTRO
        user_input = ""
        feedback[INTRO] = ""

def update_display():
    """
    Updates the entire display.
    """
    pygame.display.flip()

def clear_screen():
    """
    Clears the game window by filling it with black color.
    """
    screen.fill(BLACK)

def gameplay(play_mode, speed, luck) :
    # gameplay
    global current_state
    spawn_time = 250
    health = 3
    score = 0

    # Define the Player object extending pygame.sprite.Sprite
    # The surface we draw on the screen is now a property of 'player'

    class Player(pygame.sprite.Sprite):
        def __init__(self, speed):
            super(Player, self).__init__()
            self.surf = pygame.Surface((75, 25))
            self.surf.fill((255, 255, 255))
            self.rect = self.surf.get_rect(
                center=(
                    SCREEN_WIDTH / 5,
                    SCREEN_HEIGHT / 2
                )
            )
            self.speed = speed  # Use the passed speed value

        def change_color(self, new_color):
            self.surf.fill(new_color)  # Fill the surface with the new color

        # Move the sprite based on keypresses
        def update(self, pressed_keys):
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -self.speed)
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, self.speed)
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-self.speed, 0)
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(self.speed, 0)

            # Keep player on the screen
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
            if self.rect.top <= 0:
                self.rect.top = 0
            elif self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT


    # Define the enemy object extending pygame.sprite.Sprite
    # The surface we draw on the screen is now a property of 'enemy'


    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super(Enemy, self).__init__()
            self.surf = pygame.Surface((25, 5))
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT),
                )
            )
            self.speed = random.randint(-10, -5)
            self.move = random.randint(-5,5)
            if play_mode == 1 :
                self.type = random.randint(1,9)
            elif play_mode == 2 :
                self.type = random.randint(7,9)
            elif play_mode == 3 :
                self.type = random.randint(4,6)
            elif play_mode == 4 :
                self.type = random.randint(1,3)
            elif play_mode == 5 :
                self.type = random.randint(1,9)
            else :
                self.type = 1

            if self.type < 4 :
                self.surf.fill((255, random.randint(0,50), random.randint(0,50)))
            elif self.type > 6 :
                self.surf.fill((random.randint(0,50), 255, random.randint(0,50)))
            else :
                self.surf.fill((random.randint(0,50), random.randint(0,50), 255))

        # Move the sprite based on speed
        # Remove it when it passes the left edge of the screen
        def update(self):
            if self.type < 4 :
                self.rect.move_ip(self.speed, self.move)
            elif self.type > 6 :
                self.rect.move_ip(random.randint(-50,-10), 0)
            else :
                self.rect.move_ip(random.randint(-20,-5), random.randint(-20,20))
            if self.rect.right < 0:
                self.kill()

    # Define the power object extending pygame.sprite.Sprite
    # The surface we draw on the screen is now a property of 'power'

    class Clear(pygame.sprite.Sprite):
        def __init__(self):
            super(Clear, self).__init__()
            self.surf = pygame.Surface((30, 30))
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT),
                )
            )
            self.surf.fill((255,100,100))

        # Move the sprite based on speed
        # Remove it when it passes the left edge of the screen
        def update(self):
            self.rect.move_ip(-10, 0)

            if self.rect.right < 0:
                self.kill()
                

    class Shield(pygame.sprite.Sprite):
        def __init__(self):
            super(Shield, self).__init__()
            self.surf = pygame.Surface((30, 30))
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT),
                )
            )
            self.surf.fill((100,100,255))

        # Move the sprite based on speed
        # Remove it when it passes the left edge of the screen
        def update(self):
            self.rect.move_ip(-10, 0)

            if self.rect.right < 0:
                self.kill()

    # Create a custom event for adding a new enemy.
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, spawn_time)

    # Create a custom event for adding a new power.
    ADDPOWER = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDPOWER, 9000-luck*300)

    UNBLOCK = pygame.USEREVENT + 3

    MOREENEMY = pygame.USEREVENT + 4
    pygame.time.set_timer(MOREENEMY,1000)

    ADDSCORE = pygame.USEREVENT + 5
    pygame.time.set_timer(ADDSCORE,100)

    # Create our 'player'
    player = Player(speed)

    # Create groups to hold enemy sprites, power sprites, and every sprite
    # - enemies and powers is used for collision detection and position updates
    # - all_sprites is used for rendering
    players = pygame.sprite.Group()
    players.add(player)
    enemies = pygame.sprite.Group()
    powers = pygame.sprite.Group()
    shields = pygame.sprite.Group()
    clears = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Variable to keep our main loop running
    running = True
    is_blocking = False


    # Our main loop
    while running:
        if play_mode != 5 :
            if score >= 10000 :
                current_state = ENDING
                running = False
        
        if health <= 0 :
            current_state = GAME_OVER
            running = False

        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop
                if event.key == K_ESCAPE:
                    running = False

            # Did the user click the window close button? If so, stop the loop
            elif event.type == QUIT:
                running = False

            # Should we add a new enemy?
            elif event.type == ADDENEMY:
                # Create the new enemy, and add it to our sprite groups
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

            # Should we add a new enemy?
            elif event.type == ADDPOWER:
                # Create the new enemy, and add it to our sprite groups
                x = random.randint(0,2)
                if x<1 :
                    new_power = Shield()
                    shields.add(new_power)
                else :
                    new_power = Clear()
                    clears.add(new_power)
                powers.add(new_power)
                all_sprites.add(new_power)
            
            elif event.type == UNBLOCK:
                is_blocking = False
                player.change_color((255,255,255))

            elif event.type == MOREENEMY:
                spawn_time = spawn_time - 5

            elif event.type == ADDSCORE :
                score = score + 10

        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        # Update the position of our enemies and powers
        enemies.update()
        powers.update()

        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw all our sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        score_surface = font.render(f"Score: {score}", True, WHITE)
        health_surface = font.render(f"Health: {health}", True, WHITE)
        screen.blit(score_surface, (10, 10))  # Adjust position as needed
        screen.blit(health_surface, (10, 40))  # Adjust position as needed

        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(player, enemies):
            # If so, remove the player and stop the loop
            collided_enemy = pygame.sprite.spritecollideany(player, enemies)
            if not is_blocking :
                health -= 1
                collided_enemy.kill()
            else :
                collided_enemy.kill()
        
        # Check if any powers have collided with the player
        if pygame.sprite.spritecollideany(player, shields):
            # If so, determine power type and 
            collided_shield = pygame.sprite.spritecollideany(player, shields)
            is_blocking = True
            player.change_color((100,100,255))
            pygame.time.set_timer(UNBLOCK, 3000)
            collided_shield.kill()

        if pygame.sprite.spritecollideany(player, clears):
            collided_clear = pygame.sprite.spritecollideany(player, clears)
            for enemy in enemies:
                enemy.kill()
            collided_clear.kill()

        # Flip everything to the display
        pygame.display.flip()

        # Limit the frame rate to 30 frames per second
        clock.tick(30)

def main():
    global user_input

    # Start with the introduction
    introduction()

    while True:
        clear_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if current_state == PLAY:
                        continue  # Skip handling input during gameplay
                    handle_input()
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    if current_state in [CHOOSE_MODE, CHOOSE_PLANE]:
                        if event.unicode.isalnum() or event.unicode in [" ", "?", "."]:
                            user_input += event.unicode

        # Render current state
        if current_state == INTRO:
            introduction()
        elif current_state == CHOOSE_MODE:
            playmode()
        elif current_state == CHOOSE_PLANE:
            plane()
        elif current_state == ENDING:
            ending()
        elif current_state == GAME_OVER:
            game_over()
        elif current_state == PLAY:
            # Call the gameplay function here to keep it running
            gameplay(play_mode, speed, luck)

        # Display user input
        if current_state in [CHOOSE_MODE, CHOOSE_PLANE]:
            input_surface = font.render(
                f"Your input: {user_input}", True, WHITE)
            screen.blit(input_surface, (50, 500))

        update_display()
        clock.tick(30)  # Limit to 30 FPS

if __name__ == "__main__":
    main()