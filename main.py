import pygame
import sys
import random

pygame.init()
pygame.display.set_caption("My first PyGame program")
screen = pygame.display.set_mode((1280, 768))  # Sets resolution.

screenWidth = 1280
screenHeight = 768

clock = pygame.time.Clock()  # Built-in function that enables frame-rate control.
cloudImage = pygame.image.load("cloud.png")  # Loading an image from a file. Put the file inside the project folder.
humanImage = pygame.image.load("human_umbrella.png")


class Human:

    def __init__(self):
        self.xPosition = 0
        self.yPosition = 768 - 192
        self.hitBox = pygame.Rect(self.xPosition, self.yPosition, 170, 20)

    def draw(self):
        screen.blit(humanImage, (self.xPosition, self.yPosition))
        self.hitBox = pygame.Rect(self.xPosition, self.yPosition, 170, 20)

    def move(self):
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.xPosition -= 10

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.xPosition += 10


class Raindrop:

    def __init__(self, x, y, colour):  # On initiation, give the raindrops these values. These are randomised ONE TIME per instance of raindrop.
        self.xPosition = x
        self.yPosition = y
        self.size = random.randint(1, 5)
        self.startSpeed = random.randint(5, 20)
        self.speed = self.startSpeed
        self.colour = colour
        self.hitBox = pygame.Rect(self.xPosition, self.yPosition, self.size, self.size)

    def draw(self):  # Called every frame, takes the values from initialisation. Different for each instance of raindrop.
        pygame.draw.circle(screen, self.colour, (self.xPosition, self.yPosition), self.size)
        self.hitBox = pygame.Rect(self.xPosition, self.yPosition, self.size, self.size)

    def move(self):  # Called every frame, takes the values from initialisation. Different for each instance of raindrop.
        self.yPosition += self.speed


class Cloud:

    def __init__(self):
        self.xCloudPos = random.randint(-500, 600)  # Create cloud position here, use directly in raindrop creation to avoid global variables.
        self.yCloudPos = -200  # Create cloud position here, use directly in raindrop creation to avoid global variables.
        self.size = random.randint(1, 2)

    def draw(self):  # Called every frame, takes the values from initialisation. Different for each instance of raindrop.
        screen.blit(cloudImage, (self.xCloudPos, self.yCloudPos))  # Put the cloud on the screen.

    def move(self):  # Called every frame, takes the values from initialisation. Different for each instance of raindrop.
        self.xCloudPos += 2

    def spawn_rain(self):
        raindropsList.append(Raindrop((random.randint(self.xCloudPos + 150, self.xCloudPos + 900)), self.yCloudPos + 400, (255, 255, 255)))  # Add the raindrop instance to a list.



raindropsList = []  # MUST be defined outside the while loop, otherwise list is erased every frame (duh).

cloudInstance = Cloud()

humanInstance = Human()

while True:

    clock.tick(60)  # Setting the frame-rate.
    for event in pygame.event.get():  # See the pygame user guide for various events (e.g. get button down).
        if event.type == pygame.QUIT:
            sys.exit()

    # Rendering section (order matters).
    screen.fill((150, 150, 150))  # Filling the screen with a colour.

    if humanInstance.xPosition >= (screenWidth - 119):  # Check the position of each droplet.
        humanInstance.xPosition = (screenWidth - 119)  # Delete the droplets if they cross the bottom border.
    elif humanInstance.xPosition <= -30:
        humanInstance.xPosition = -30
    humanInstance.move()
    humanInstance.draw()

    for i in range(1, 5):
        raindrop = Raindrop(random.randint(0, screenWidth), 0, (100, 100, 100))
        raindropsList.append(raindrop)

    for droplet in raindropsList:  # Iterate through the list.

        if humanInstance.hitBox.colliderect(droplet.hitBox):
            droplet.speed = 0
        elif droplet.speed < droplet.startSpeed:
            droplet.speed += 1

        if droplet.yPosition >= screenHeight:
            raindropsList.remove(droplet)  # Delete the droplets if they cross the bottom border.
        else:
            droplet.move()  # Also move its position.
            droplet.draw()  # If the droplet isn't below the bottom border, draw it on screen.

        if cloudInstance.xCloudPos >= screenWidth:  # Check the position of each droplet.
            cloudInstance.xCloudPos = -1000  # Delete the droplets if they cross the bottom border.
    cloudInstance.move()
    cloudInstance.draw()
    cloudInstance.spawn_rain()

    pygame.display.flip()  # 2 buffers: stuff that's going to draw, stuff that's already drawn. Flip turns the two.