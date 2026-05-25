import pygame
pygame.init()

import sys
import random

pygame.font.init()
font = pygame.font.SysFont("arial", 28)


WIDTH=1000
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("The Console")
clock=pygame.time.Clock()
#clock is used to control the frame rate of the game, it will limit the game to run at 60 frames per second


music_tracks = {
    "character_select": "start.mp3",
    "sofa": "start.mp3",
    "outside": "flowerfight.mp3",
    "sidewalk": "start.mp3",
    "basement": "mazeboss.mp3",
    "parking": "mazeboss.mp3",
    "ending": "ending.mp3",
}


collect_sound = pygame.mixer.Sound("clover.mp3")
flowerhit_sound = pygame.mixer.Sound("fight1.mp3")
bosshit_sound = pygame.mixer.Sound("fight2.mp3")

current_music = None

def play_music(scene_name):
    global current_music

    if current_music != scene_name:
        pygame.mixer.music.load(music_tracks[scene_name])
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

        current_music = scene_name


def load_image(path, size=None):
    img= pygame.image.load(path).convert_alpha()
    if size:
        img=pygame.transform.scale(img, size)
    return img
#this function loads an image from the specified path and converts it to a formt that can be used in pygame

characters= {
    "Gumball": load_image("gumball.PNG", (120,120)),
    "Darwin": load_image("darwin.PNG", (120,120)),
    "Anais": load_image("anais.PNG", (120,120)),
}
#this is a dictionary that will store all the characters in the game,
#it will be used to keep track of their stats and inventory,
#while also allowing us to easily access it

backgrounds = {
    "sofa": load_image("sofa.jpg", (WIDTH, HEIGHT)),
    "outside": load_image("house.jpg", (WIDTH,HEIGHT)),
    "basement": load_image("basement.jpg", (WIDTH, HEIGHT)),
    "sidewalk": load_image("sidewalk.jpg", (WIDTH, HEIGHT)),
    "parking": load_image("parking.jpg", (WIDTH, HEIGHT)),
}
#same as characters - but for backgrounds,
#it will store all the backgrounds in the game ans allows us 
#to easily access them when needed

flower_img= load_image("flower.PNG", (120,120))
portal_img= load_image("portal.PNG", (120,120))
boss_img= load_image("boss.PNG", (200,200))
clover_img= load_image("clover.PNG",(50,50))
console_img= load_image("console.PNG", (100,100))


scene = "character_select"
#this variable will keep track of the current scene in the game
#which here is character select screen
selected_character=None
#variable used to track the selected character

flower_hp=100
boss_hp=200
clover_collected=0
maze_complete=False

player_x, player_y= 100, 450

clover_positions = []
for i in range (7):
    x=random.randint(50,900)
    y = random.randint(100,600)
    clover_positions.append((x,y))


def draw_text(text, x, y, color=(255,255,255), selected_font=font):
    text_surface = selected_font.render(text, True, color)
    screen.blit(text_surface, (x, y))

'''character select'''

def character_select(events):
    global selected_character, scene

#"In Python, the global keyword lets you declare that a variable used inside a function is global. 
# This allows you to modify the variable outside of the current function scope.
# The global keyword is essential when you need to work with variables
# that exist outside the local scope of a function." 

    screen.fill((30,30,50))
    draw_text("Choose your character", 320, 50)
    positions=[(150,250), (420,250), (690,250)]
    rects=[]

    for i, (name, img) in enumerate(characters.items()):
        rect = pygame.Rect(positions[i][0], positions[i][1], 120, 120)
        screen.blit(img, rect)
        draw_text(name, rect.x, rect.y + 130, (255,255,0), font)

        rects.append((rect,name))

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            for rect, name in rects:
                if rect.collidepoint(event.pos):
                    selected_character = name
                    scene = "sofa"

#checks whether the mouse click occurred inside the boundaries of an object’s rectangle.

'''SOFA (INSIDE THE HOUSE):'''

def sofa_scene(events):
    global scene

    screen.blit(backgrounds["sofa"], (0,0))

    console_rect = pygame.Rect(450, 300, 100, 100)
    screen.blit(console_img, console_rect)

    draw_text("Welcome into the games world!", 380, 200)

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if console_rect.collidepoint(event.pos):
                scene = "outside"



'''OUTSIDE(SIDEWALK)(FLOWER FIGHT)'''

flower_x, flower_y = 420, 250
flower_size = 120

def outside_scene(events):
    global flower_hp, scene, flower_x, flower_y

    screen.blit(backgrounds["outside"], (0,0))

    enemy_rect = pygame.Rect(flower_x, flower_y, flower_size, flower_size)

    if flower_hp > 0:
        screen.blit(flower_img, enemy_rect)
        draw_text(f"Flower HP: {flower_hp}", 400, 180)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if enemy_rect.collidepoint(event.pos):
                    flower_hp -= 20
                    flowerhit_sound.play()

                    # TELEPORT FLOWER AFTER HIT
                    flower_x = random.randint(50, WIDTH - flower_size - 50)
                    flower_y = random.randint(50, HEIGHT - flower_size - 50)

    else:
        screen.blit(portal_img, enemy_rect)
        draw_text("Click portal", 430, 180)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if enemy_rect.collidepoint(event.pos):
                    scene = "sidewalk"
  
'''SIDEWALK(COLLECTING CLOVERS)'''

def sidewalk_scene(events):
    global clover_collected, scene, clover_positions

    screen.blit(backgrounds["sidewalk"], (0,0))

    draw_text("Collect clovers for Penny", 330, 50)
    draw_text(f"Clovers: {clover_collected}/7", 50, 50)

    for pos in clover_positions[:]:
        rect = pygame.Rect(pos[0], pos[1], 50, 50)
        screen.blit(clover_img, rect)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect.collidepoint(event.pos):
                    clover_positions.remove(pos)
                    clover_collected += 1
                    collect_sound.play()

    if clover_collected == 7:
        draw_text("Thank you! Go to the basement! Good LUCK!", 250, 620)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    scene = "basement"



'''BASEMENT (MAZE)'''

maze_walls = [

    # Outer border

    pygame.Rect(50, 50, 900, 10),

    pygame.Rect(50, 50, 10, 600),

    pygame.Rect(50, 640, 850, 10),

    pygame.Rect(940, 50, 10, 550),

    # Maze inside walls

    pygame.Rect(150, 100, 10, 150),

    pygame.Rect(300, 50, 10, 200),

    pygame.Rect(450, 50, 10, 100),

    pygame.Rect(600, 100, 10, 150),

    pygame.Rect(750, 100, 10, 100),

    pygame.Rect(100, 150, 150, 10),

    pygame.Rect(300, 200, 120, 10),

    pygame.Rect(500, 250, 120, 10),

    pygame.Rect(700, 150, 120, 10),

    pygame.Rect(200, 250, 10, 120),

    pygame.Rect(400, 300, 10, 150),

    pygame.Rect(650, 250, 10, 180),

    pygame.Rect(100, 350, 180, 10),

    pygame.Rect(350, 450, 200, 10),

    pygame.Rect(650, 350, 220, 10),

    pygame.Rect(250, 500, 10, 140),

    pygame.Rect(550, 500, 10, 140),

    pygame.Rect(100, 550, 200, 10),

    pygame.Rect(400, 550, 200, 10),
]

  
def basement_scene(events):
    global player_x, player_y, scene

    screen.blit(backgrounds["basement"], (0,0))
    draw_text("Reach the portal!", 400, 20)

    speed = 4
    PLAYER_SIZE = 60

    old_x = player_x
    old_y = player_y

    keys = pygame.key.get_pressed()

    # movement
    if keys[pygame.K_LEFT]:
        player_x -= speed
    if keys[pygame.K_RIGHT]:
        player_x += speed
    if keys[pygame.K_UP]:
        player_y -= speed
    if keys[pygame.K_DOWN]:
        player_y += speed

    # player hitbox
    player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)

    # collision detection
    for wall in maze_walls:
        if player_rect.colliderect(wall):
            player_x = old_x
            player_y = old_y
            break

    # draw maze
    for wall in maze_walls:
        pygame.draw.rect(screen, (70,70,70), wall)

    # draw player
    player_img = pygame.transform.scale(
        characters[selected_character],
        (PLAYER_SIZE, PLAYER_SIZE)
    )
    screen.blit(player_img, (player_x, player_y))

    # portal (EXIT)
    exit_rect = pygame.Rect(900, 600, 70, 70)
    screen.blit(portal_img, exit_rect)

    # win condition
    if player_rect.colliderect(exit_rect):
        scene = "parking"


'''DRAGON BOSS FIGHT'''

boss_x, boss_y = 400, 200
boss_size = 200

def parking_scene(events):
    global boss_hp, scene, boss_x, boss_y

    screen.blit(backgrounds["parking"], (0,0))

    boss_rect = pygame.Rect(boss_x, boss_y, boss_size, boss_size)

    screen.blit(boss_img, boss_rect)
    draw_text(f"Dragon HP: {boss_hp}", 400, 150)

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if boss_rect.collidepoint(event.pos):
                boss_hp -= 25
                bosshit_sound.play()

                # TELEPORT BOSS AFTER HIT
                boss_x = random.randint(50, WIDTH - boss_size - 50)
                boss_y = random.randint(50, HEIGHT - boss_size - 50)

    if boss_hp <= 0:
        scene = "ending"


'''ENDING SCENE (FINISH)'''
def ending_scene():
    screen.fill((0,0,0))
    draw_text("Wake up?", 430, 320, (255,0,0))


while True:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    play_music(scene)

    if scene == "character_select":
        character_select(events)
    elif scene == "sofa":
        sofa_scene(events)
    elif scene == "outside":
        outside_scene(events)
    elif scene == "sidewalk":
        sidewalk_scene(events)
    elif scene == "basement":
        basement_scene(events)
    elif scene == "parking":
        parking_scene(events)
    elif scene == "ending":
        ending_scene()



    pygame.display.flip()
    clock.tick(60)


''' SOURCES:
--> https://stackoverflow.com/questions/51177475/python3-how-to-install-ttf-font-file
-->https://stackoverflow.com/questions/76221689/how-to-add-ttf-font-file-to-python-code-so-that-it-can-be-seen-on-any-computer
-->https://www.pygame.org/docs/ref/font.html
-->https://docs.python.org/3/library/sys.html
-->https://stackoverflow.com/questions/51177475/python3-how-to-install-ttf-font-file
-->https://stackoverflow.com/questions/76221689/how-to-add-ttf-font-file-to-python-code-so-that-it-can-be-seen-on-any-computer
-->https://pl.pinterest.com (characters)(later customised by me)
-->https://theamazingworldofgumball.fandom.com/wiki/Gumball_Watterson
-->https://realpython.com/ref/keywords/global/#:~:text=In%20Python%2C%20the%20global%20keyword,local%20scope%20of%20a%20function.
-->https://stackoverflow.com/questions/44998943/how-to-check-if-the-mouse-is-clicked-in-a-certain-area-pygame
'''