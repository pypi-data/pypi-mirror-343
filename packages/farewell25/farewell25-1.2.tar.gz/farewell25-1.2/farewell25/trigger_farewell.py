import pygame
import sys
import os

# Initialize pygame for graphical components
pygame.init()

# Set up the screen in fullscreen mode
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # (0, 0) will make the window take up the full screen
pygame.display.set_caption("Farewell Message")

# Get screen resolution (width and height) for full screen
WINDOW_WIDTH, WINDOW_HEIGHT = window.get_size()

# Path to the resources
resource_dir = os.path.dirname(__file__)  # Get the directory of the current script

# Load the image for the background
img_path = os.path.join(resource_dir, 'farewell.png')  # Path to the image
background_image = pygame.image.load(img_path)
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Load the music for playing
music_path = os.path.join(resource_dir, 'farewell.mp3')  # Path to the music
pygame.mixer.music.load(music_path)

# Define the farewell message to display in the console
farewell_lines = [
    "*                                                *",
    "*         THANK YOU FOR EVERYTHING               *",
    "*         Farewell from Rohit Ghadi               *",
    "*    Wishing you all love, success, and light     *",
    "*     Keep shining bright forever! 🌟             *",
    "*                                                *",
    ]

# Set up fonts for displaying the lyrics (larger and more elegant)
font = pygame.font.SysFont("Arial", 50)  # Larger font for better impact

def display_text(text, y_position):
    """Helper function to display text at a given Y position with an outline."""
    text_surface = font.render(text, True, (255, 255, 255))  # White text color
    text_width = text_surface.get_width()  # Get the width of the text
    x_position = (WINDOW_WIDTH - text_width) // 2  # Center the text horizontally
    window.blit(text_surface, (x_position, y_position))  # Display the text with centered position

def play_music():
    """Play the farewell music."""
    pygame.mixer.music.play(-1, 0.0)  # Loop the music indefinitely

def main():
    # Immediately start the graphical farewell message and music
    window.blit(background_image, (0, 0))  # Display the background image

    # Set the starting Y position for the text to appear at the top center
    y_position = 50  # Starting Y position near the top of the screen

    for line in farewell_lines:
        display_text(line, y_position)
        y_position += 60  # Increase Y position for next line, larger spacing for better readability

    pygame.display.update()

    # Start the music right away
    play_music()

    # Keep the window open until the user closes it
    running = True
    while running:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
