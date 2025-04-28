import pygame
import sys
import os
import time

# Initialize pygame for graphical components
pygame.init()

# Set up window dimensions for graphical display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Farewell Message")

# Load the image for the background
img_path = os.path.join(os.path.dirname(__file__), 'farewell.png')  # Path to the image
background_image = pygame.image.load(img_path)
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Load the music for playing
music_path = os.path.join(os.path.dirname(__file__), 'farewell.mp3')  # Path to the music
pygame.mixer.music.load(music_path)

# Define the farewell message to display in the console
farewell_lines = [
    "**************************************************",
    "*                                                *",
    "*         THANK YOU FOR EVERYTHING               *",
    "*         Farewell from Rohit Ghadi               *",
    "*    Wishing you all love, success, and light     *",
    "*     Keep shining bright forever! 🌟             *",
    "*                                                *",
    "**************************************************"
]

# Set up fonts for displaying the lyrics
font = pygame.font.SysFont("Arial", 28)

def display_text(text, y_position):
    """Helper function to display text at a given Y position."""
    text_surface = font.render(text, True, (255, 255, 255))  # White text color
    window.blit(text_surface, (40, y_position))  # Display the text with some margin from the left

def play_music():
    """Play the farewell music."""
    pygame.mixer.music.play(-1, 0.0)  # Loop the music indefinitely

def display_console_message():
    """Display the farewell message in the console."""
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')

    for line in farewell_lines:
        print(line.center(80))
        time.sleep(0.7)

    # Final personal message
    time.sleep(1)
    print("\n" + "Always in my heart ❤️ - Rohit Ghadi".center(80))
    time.sleep(2)

    # Thank you message
    print("\nThank you for being part of my journey 🙏 - Rohit Ghadi".center(80))
    time.sleep(2)

def main():
    # Display the console farewell message
    display_console_message()

    # Set up the graphical window and display the image
    window.blit(background_image, (0, 0))

    # Display the lyrics at the top
    y_position = 40  # Starting Y position for the first line of lyrics
    for line in farewell_lines:
        display_text(line, y_position)
        y_position += 40  # Increase Y position for next line

    pygame.display.update()

    # Start the music
    play_music()

    # Keep the window open for a while (10 seconds)
    time.sleep(10)  # Show for 10 seconds before closing

    # Quit pygame and close the program
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
