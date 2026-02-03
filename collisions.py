import math 

# return true or flase for collisions between two objects
def isCollision(targetX,targetY,homeX,homeY, proximity,adjust):
    distance =  math.sqrt((math.pow((targetX+adjust) - homeX,2)) + (math.pow((targetY+adjust) - homeY,2)))
    if distance < proximity:
        return True
    else:
        return False 
    
   
            



