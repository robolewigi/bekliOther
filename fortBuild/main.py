import pygame
import random

class variables():
 def __init__(self):
  self.width= 700
  self.height= 500
  self.run= 0
  self.debug= [0, True]
v= variables()

class world():
 def __init__(self):
  self.gridX=10
  self.gridY=10
  self.resources=[] #(-1)-removed 0-None 1-wheat 2-wood 3-metal
  self.enemies=[]
  self.difficulty= 10
w= world()

class player():
 def __init__(self):
  self.wood= 5
  self.metal= 5
  self.wheat= 5
  self.improvements=[] #0-None 1-walls 2-tower 3-tradePost 4-station
  self.location=[0,0]
  self.ranges=[] #0-None 1-command 2-shot
  self.profits=[0,1,1,0] #NaWhWoMe
 
 def endTurn(self):
  self.wheat+= self.profits[1]
  self.wood+= self.profits[2]
  self.metal+= self.profits[3]
  activateBuild()
  moveEnemies()
  w.difficulty+= 1
p= player()

def createWorld():
 p.wood= 5
 p.metal= 5
 p.wheat= 5
 p.profits=[0,1,1,0]
 w.enemies= [0]* (w.gridX*w.gridY)
 p.improvements= [0]* (w.gridX*w.gridY)
 w.difficulty= 10
 p.ranges= [0]* (w.gridX*w.gridY)
 w.resources= [0]* (w.gridX*w.gridY)
 for y in range(w.gridY):
  for x in range(w.gridX):
   is_border = x==0 or y==0 or x== w.gridX-1 or y== w.gridY-1
   rand = random.random()
   if is_border:
    w.resources[y* w.gridX+ x]= -1
   elif rand>0.5:
    w.resources[y* w.gridX+ x]= 0
   elif rand>0.3:
    w.resources[y* w.gridX+ x]= 1
   elif rand>0.1:
    w.resources[y* w.gridX+ x]= 2
   elif rand>0.05:
    w.resources[y* w.gridX+ x]= 3
   else:
    w.resources[y* w.gridX+ x]= 4
 p.improvements[3* w.gridX+ 3]= 4
 searchRange()

def createSquare(pos= [88,44], col=[0,144,0], siz=44):
 pygame.draw.rect(screen, tuple(col), pygame.Rect(pos[0], pos[1],  siz, siz))

def drawMenuText():
 menu_items = [
  "1- walls",
  "2- tower",
  "3- tradePost",
  "4- station",
  f"wheat= {p.wheat}+ {p.profits[1]}",
  f"wood= {p.wood}+ {p.profits[2]}",
  f"metal= {p.metal}+ {p.profits[3]}",
  "costs:",
  "1- 0Wh 1Wo 0Me", 
  "2- 1Wh 1Wo 0Me",  
  "3- 2Wh 2Wo 1Me",  
  "4- 3Wh 3Wo 2Me",  
  "space to build",
  "enter to end turn",
  f"difficulty: {w.difficulty}",
 ]
 
 start_x = 480  
 start_y = 40  
 line_spacing = 30
 
 for index, text in enumerate(menu_items):
  # render(text, antialias, color)
  text_surface = font.render(text, True, (255, 255, 255)) 
  screen.blit(text_surface, (start_x, start_y + (index * line_spacing)))

def activateBuild():
 newArea=[[0,0]]* (w.gridX* w.gridY)
 for i in range(len(p.improvements)):
  if p.improvements[i]==2:
   newBreak= False
   for y in range(-1,2):
    for x in range(-1,2):
     if w.enemies[i+ y*w.gridX+ x]>0:
      w.enemies[i+ y*w.gridX+ x]= max(w.enemies[i+ y*w.gridX+ x]-1, 0)
      newBreak= True
      break
    if newBreak: break

def moveEnemies():
  # 1. Find where the station (improvement ) actually is
  station_index = -1
  for i in range(len(p.improvements)):
   if p.improvements[i] not in [0,1]:
    station_index = i
    break

  # 2. Only move enemies if a station exists on the map
  if station_index != -1:
   target_coords = [station_index % w.gridX, station_index // w.gridX]
   newEne = w.enemies.copy()
   
   for i in range(len(newEne)):
    if newEne[i] > 0:
     if p.improvements[i]!= 0:
      if p.improvements[i]==1 and w.enemies[i]==1: continue
      if p.improvements[i]==1: w.enemies[i]-=2
      else: w.enemies[i]-=1
      p.improvements[i]= 0
      searchRange()
     if w.enemies[i]==0: continue

     curr_coords = [i % w.gridX, i // w.gridX]
     newPath = pathFinding(curr_coords, target_coords)
     new_index = newPath[1] * w.gridX + newPath[0]
     
     if i != new_index:
      w.enemies[i] -= newEne[i]
      w.enemies[new_index] += newEne[i]

  # 3. Spawn a new enemy on a random border tile (-1 resource)
  for _ in range(w.difficulty//10):
   available = [i for i, x in enumerate(w.resources) if x == -1]
   if available: # Safety check to make sure border tiles exist
    random_index = random.choice(available)
    if len(w.enemies)<= random_index: return
    w.enemies[random_index] += 1

def pathFinding(current, target):
    curr_x, curr_y = current
    target_x, target_y = target

    if curr_x < target_x:
        return [curr_x + 1, curr_y]  # Move Right
    elif curr_x > target_x:
        return [curr_x - 1, curr_y]  # Move Left
        
    elif curr_y < target_y:
        return [curr_x, curr_y + 1]  # Move Up (or Down depending on grid setup)
    elif curr_y > target_y:
        return [curr_x, curr_y - 1]  # Move Down (or Up depending on grid setup)

    return current

def searchRange():
 anyFour= False
 p.ranges= [0]* (w.gridY* w.gridX)
 for i in range(len(p.improvements)):
  if p.improvements[i]==4: anyFour= True
  if p.improvements[i] in [2,4]:
   for y in range([0,0,-1,0,-2][p.improvements[i]], [0,0,2,0,3][p.improvements[i]]):
    for x in range([0,0,-1,0,-2][p.improvements[i]], [0,0,2,0,3][p.improvements[i]]):
     newNum= i% w.gridX+ x
     if newNum<0 or newNum>= w.gridX: continue
     newNum= y* w.gridX+ i+ x
     if len(p.ranges)> newNum and newNum>= 0:
      if p.ranges[newNum]== [0,0,1,0,2][p.improvements[i]]:
       p.ranges[newNum]= 3
      else:
       p.ranges[newNum]= max(p.ranges[newNum], [0,0,2,0,1][p.improvements[i]])
 if not anyFour:
  createWorld()
     
def keyEvents(event):
 if event.type == pygame.KEYDOWN:
  if event.key == pygame.K_a: # Move Left
   p.location[0]= max(0, p.location[0]-1)
  elif event.key == pygame.K_d: # Move Right
   p.location[0]= min(w.gridX-1, p.location[0]+1)
  elif event.key == pygame.K_w: # Move Up
   p.location[1]= max(0, p.location[1]-1)
  elif event.key == pygame.K_s: # Move Down
   p.location[1]= min(w.gridY-1, p.location[1]+1)
  elif event.key == pygame.K_RETURN:
   p.endTurn()
  elif event.key == pygame.K_SPACE:
   newLoc= p.location[1]* w.gridX+ p.location[0]
   if p.ranges[newLoc] in [1,3]:
    if w.enemies[newLoc]>0: return
    if p.improvements[newLoc]!=4:
     costs= [[0,1,0], [1,1,0], [2,2,1], [3,3,2]]
     newCost= costs[p.improvements[newLoc]]
     if p.wheat>= newCost[0] and p.wood>= newCost[1] and p.metal>= newCost[2]:
      if w.resources[newLoc]!= -1:
       if p.improvements[newLoc]!=4:
        p.wheat-= newCost[0]
        p.wood-= newCost[1]
        p.metal-= newCost[2]
        p.improvements[newLoc]+=1
        if p.improvements[newLoc]==3:
         p.profits[w.resources[newLoc]]+= 1
        if p.improvements[newLoc]==4:
         p.profits[w.resources[newLoc]]-= 1
      searchRange()

pygame.init() 
screen = pygame.display.set_mode((v.width, v.height))
pygame.display.set_caption('cityBuilder')
clock = pygame.time.Clock()

font = pygame.font.Font(None, 20)

createWorld()
while v.run!= 2:
 clock.tick(60)
 for event in pygame.event.get():
  if event.type == pygame.QUIT:
   v.run = 2
  keyEvents(event)

 screen.fill((0, 0, 0)) 

 for y in range(w.gridY):
  for x in range(w.gridX):
   newCol= [0,0,0]
   if p.location==[x,y]:
    newCol[2]+= 122
   if p.ranges[y* w.gridX+ x] in [2,3]:
    newCol[0]+= 111
   
   createSquare([37+ x*40, 37+ y*40], newCol, siz=40)
   col= [0,144,0]
   newNum= y* w.gridX+ x
   if w.resources[newNum]==-1:
    col= [0,0,0]
   elif w.resources[newNum]==1:
    col= [111,111,0]
   elif w.resources[newNum]==2:
    col= [111,44,0]
   elif w.resources[newNum]==3:
    col= [44,66,88]
   createSquare([x*40+40, y*40+40],col, siz=34)

   if w.resources[newNum] != -1 and p.ranges[newNum] in [1, 3]:
        newNum = y * w.gridX + x
        imp_value = str(p.improvements[newNum])
        
        text_surface = font.render(imp_value, True, (255, 255, 255))
        screen.blit(text_surface, (x * 40 + 46, y * 40 + 42))
        
   if w.enemies[newNum]!=0:
    second_value = f"{w.enemies[newNum]}" 
    text_surface2 = font.render(second_value, True, (255, 0, 0))
    screen.blit(text_surface2, (x * 40 + 60, y * 40 + 42))

 drawMenuText()

 pygame.display.flip()

pygame.quit()