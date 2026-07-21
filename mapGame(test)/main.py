import pygame
import sys
import random, math

class Variables:
 def __init__(self):
  self.width = 700
  self.height = 500
  self.caption = "Simple Pygame Window"
  self.fps = 60
  self.mapFile = "pictures/map.png" 
  self.run= 0
  self.mapImage= None
  self.originalMap = None
  self.mapSize=[0,0]
  self.mapLoc=[[60.41, 31.48],[55.38, 32.95],[66.02, 32.77],[26.1, 56.21],[76.76, 27.94],[21.19, 39.08]]
  self.mapX=0
  self.mapY=0
  self.moveSpeed=5
  self.buttonIdx= -1
  self.buttons=[]
  self.showMap = True
  self.pictures= ["map", "egyptSmall", "egyptMedium", "egyptLarge"]
  self.loaded_images = {}
  self.river_points = []
  self.river_side_points = []
  self.manyPoints=[]
v = Variables()

class button():
 def __init__(self,px,py):
  self.px = (px / 100) * v.mapSize[0]
  self.py = (py / 100) * v.mapSize[1]
  self.hover= False
  self.pressed= False

 def check_hover(self, mouse_pos, index):
  screen_x, screen_y = self.px+ v.mapX, self.py+ v.mapY
  radius = 8
        
  distance = ((mouse_pos[0] - screen_x) ** 2 + (mouse_pos[1] - screen_y) ** 2) ** 0.5
  self.hover = distance <= radius
  if self.hover:
   v.buttonIdx = index
  else:
   # If the mouse hovers out, force release the press state
   self.pressed = False

 def draw(self, surface):
  screen_x, screen_y = self.px+ v.mapX, self.py+ v.mapY
  radius = 8

  if self.pressed and self.hover:
   color = (0, 0, 255)   # Blue while holding down the click
  elif self.pressed:
   color = (0, 255, 0)   # Green if toggled ON
  elif self.hover:
   color = (255, 255, 0) # Yellow if hovered
  else:
   color = (255, 0, 0)   # Default Red

  pygame.draw.circle(surface, color, (screen_x, screen_y), radius)

def generateRiver():
 v.river_points = []
 v.river_side_points = []
 
 # 1. Generate the River Path (Top to Bottom)
 num_segments = 50
 river_width = 40
 segment_height = v.height / num_segments
 
 # Randomize the curve dynamics
 frequency = random.uniform(0.02, 0.05)
 amplitude = random.uniform(80, 150)
 center_offset = random.uniform(v.width * 0.3, v.width * 0.7)

 for i in range(num_segments + 1):
  y = i * segment_height
  # Use sine wave + small noise for a natural winding look
  x = center_offset + math.sin(y * frequency) * amplitude + random.randint(-10, 10)
  v.river_points.append((x, y))

 # 2. Generate Surrounding Points (Not on top of the river)
 target_points = 30
 attempts = 0
 
 while len(v.river_side_points) < target_points and attempts < 500:
  attempts += 1
  px = random.randint(50, v.width - 50)
  py = random.randint(50, v.height - 50)
  
  # Find the closest point on the river to check distance
  min_distance = 9999
  for rx, ry in v.river_points:
   dist = math.hypot(px - rx, py - ry)
   if dist < min_distance:
    min_distance = dist
    
  if river_width < min_distance < 140:
   v.river_side_points.append((px, py))
   v.manyPoints.append(random.choices([0, 1, 2], weights=[70, 20, 5])[0])

def createMap():
 try:
  loaded_map = pygame.image.load("pictures/"+v.pictures[0]+ ".png").convert()
  orig_w = loaded_map.get_width()
  orig_h = loaded_map.get_height()
  aspect_ratio = orig_h / orig_w
  target_height = int(v.width * aspect_ratio)
  v.originalMap = pygame.transform.scale(loaded_map, (v.width, target_height))
  v.mapImage = v.originalMap.copy()
  v.mapSize = [v.mapImage.get_width(), v.mapImage.get_height()]

  for img_name in v.pictures[1:]:
   sizes= [(60,60), (111,111), (188,188)]
   names= ["Small", "Medium", "Large"]
   img_path = f"pictures/{img_name}.png"
   raw_img = pygame.image.load(img_path).convert_alpha()

   chosen_size = sizes[0] 
   for i, name in enumerate(names):
    if name in img_name:  
     chosen_size = sizes[i]
     break

   v.loaded_images[img_name] = pygame.transform.scale(raw_img, chosen_size)

 except FileNotFoundError as e:
  print(f"Error: Could not find image file. {e}")
  sys.exit()

def controls(event):
 if event.type == pygame.MOUSEMOTION:
        v.buttonIdx= -1
        for idx, btn in enumerate(v.buttons):
            btn.check_hover(event.pos, idx)

 if event.type == pygame.MOUSEBUTTONDOWN:
  if event.button == 1:  # Left Mouse Button
   if v.buttonIdx != -1:
    v.buttons[v.buttonIdx].pressed = True

 elif event.type == pygame.MOUSEBUTTONUP:
  if event.button == 1:  # Left Mouse Button
   if v.buttonIdx != -1:
    v.buttons[v.buttonIdx].pressed = False
    useButton(v.buttonIdx)

 elif event.type == pygame.KEYDOWN:
  if event.key == pygame.K_ESCAPE:
   v.showMap=True

def useButton(idx):
 if idx==1: 
  generateRiver()
  v.showMap = False

def handleMovement():
 keys = pygame.key.get_pressed()
 if keys[pygame.K_w]:
  v.mapY += v.moveSpeed  # Move map down = Camera looks up
 if keys[pygame.K_s]:
  v.mapY -= v.moveSpeed  # Move map up = Camera looks down
 if keys[pygame.K_a]:
  v.mapX += v.moveSpeed  # Move map right = Camera looks left
 if keys[pygame.K_d]:
  v.mapX -= v.moveSpeed

pygame.init()
screen = pygame.display.set_mode((v.width, v.height))
pygame.display.set_caption(v.caption)
clock = pygame.time.Clock()
createMap()
v.buttons = [button(loc[0], loc[1]) for loc in v.mapLoc]
print("wasd- move around\nescape- leave city\nleftButtonClick- select city")

while v.run!=2:
 for event in pygame.event.get():
  if event.type == pygame.QUIT:
   v.run = 2
  controls(event)
  
 screen.fill((34, 40, 49))
 if v.showMap:
  handleMovement()
  screen.blit(v.mapImage, (v.mapX, v.mapY))
  for btn in v.buttons:
   btn.draw(screen)
 else:
  if len(v.river_points) > 1:
    pygame.draw.lines(screen, (53, 162, 235), False, v.river_points, 30)
   
  for i in range(len(v.river_side_points)):
    screen.blit(v.loaded_images[["egyptSmall", "egyptMedium", "egyptLarge"][v.manyPoints[i]]], v.river_side_points[i])

 pygame.display.flip()
 clock.tick(v.fps)
 
pygame.quit()
sys.exit()