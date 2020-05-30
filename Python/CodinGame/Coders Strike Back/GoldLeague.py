import sys
import math
# To debug: print("Debug messages...", file=sys.stderr)

# Permet de définir si on utilise le boost ou pas
def UseBoost(distNextCheck, angle, boost, thrust):
    if distNextCheck > 5500 and angle < 40:
        if boost == 0:
            boost = 1
            thrust = "BOOST"
    return boost, thrust

def distance2(x1,y1,x2,y2):
    return (x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2);

def distance(x1,y1,x2,y2):
    return math.sqrt(distance2(x1,y1,x2,y2))


def getAngle(check_x, check_y, x_pod, y_pod, distNewCheck):
    d = distance(check_x, check_y, x_pod, y_pod)
    dx = (x_pod - check_x) / d
    dy = (x_pod - check_y) / d
    # Trigonométrie simple. On multiplie par 180.0 / PI pour convertir en degré.
    a = math.acos(dx) * 180.0 / math.pi
    # Si le point qu'on veut est en dessus de nous, il faut décaler l'angle pour qu'il soit correct.
    if (dy < 0):
        a = 360.0 - a

    return a

def diffAngle(check_x, check_y, x_pod, y_pod, distNewCheck, angle):
    a = getAngle(check_x, check_y, x_pod, y_pod, distNewCheck)

    # Pour connaitre le sens le plus proche, il suffit de regarder dans les 2 sens et on garde le plus petit
    if angle <= a:
        right = a - angle
        left = angle + 360.0 - a
    else:
        right = 360.0 - angle + a
        left = angle - a

    if right < left:
        return right
    else:
        return left * -1

def rotate(check_x, check_y, x_pod, y_pod, distNewCheck, angle):
    a = diffAngle(check_x, check_y, x_pod, y_pod, distNewCheck, angle)

    # On ne peut pas tourner de plus de 18° en un seul tour
    if a > 18.0:
        a = 18.0
    else:
        if a < -18.0:
            a = -18.0
    angle += a

    if angle >= 360.0:
        angle = angle - 360.0
    else:
        if angle < 0.0:
            angle += 360.0
    
    return angle

def boost(check_x, check_y, x_pod, y_pod, distNewCheck, angle, thrust, vx_pod, vy_pod):
    angle = rotate(check_x, check_y, x_pod, y_pod, distNewCheck, angle)
    # Conversion de l'angle en radian
    ra = angle * math.pi / 180.0
    
    vx_pod += math.cos(ra) * thrust
    vy_pod += math.sin(ra) * thrust

    return vx_pod, vy_pod

def move(check_x, check_y, x_pod, y_pod, distNewCheck, angle, thrust, vx_pod, vy_pod, CheckpointRadius):
    vx_pod, vy_pod = boost(check_x, check_y, x_pod, y_pod, distNewCheck, angle, thrust, vx_pod, vy_pod)
    x_pod = int(check_x) + CheckpointRadius - 2 * (vx_pod * 0.85)
    y_pod = int(check_y) + CheckpointRadius - 2 * (vy_pod * 0.85)
    return x_pod, y_pod

# Permet d'obtenir la nouvelle position du pod
def NewPosition(x_pod, y_pod, vx_pod, vy_pod, x_check, y_check, CheckpointRadius):

    xm_pod = int(x_check) - 4 * vx_pod
    ym_pod = int(y_check) - 4 * vy_pod
    return xm_pod, ym_pod

# Quelques variables
boost_pod1 = 0
boost_pod2 = 0
CheckpointRadius = 0
# Lectures des données de début
laps  = int(input())
checkpointCount = int(input())
print(checkpointCount, file=sys.stderr)
coordCheck = []
checkpointX = []
checkpointY = []
for i in range(checkpointCount):
    coordCheck.append(input().split(" "))
    checkpointX.append(coordCheck[i][0])
    checkpointY.append(coordCheck[i][1])

while True:

    x_pod1, y_pod1, vx_pod1, vy_pod1, angle_pod1, nextCheckPointId_pod1 = [int(i) for i in input().split()]
    x_pod2, y_pod2, vx_pod2, vy_pod2, angle_pod2, nextCheckPointId_pod2 = [int(i) for i in input().split()]
    x_opponent1, y_opponent1, vx_opponent1, vy_opponent1, angle_opponent1, nextCheckPointId_opponent1 = [int(i) for i in input().split()]
    x_opponent2, y_opponent2, vx_opponent2, vy_opponent2, angle_opponent2, nextCheckPointId_opponent2 = [int(i) for i in input().split()]

    distNextCheck_pod1 = distance(x_pod1, y_pod1, int(checkpointX[nextCheckPointId_pod1]), int(checkpointY[nextCheckPointId_pod1]))
    distNextCheck_pod2 = distance(x_pod2, y_pod2, int(checkpointX[nextCheckPointId_pod2]), int(checkpointY[nextCheckPointId_pod2]))
    
    distOppo1To2 = distance(x_pod2, y_pod2, x_opponent1, y_opponent1) 
    distOppo2To2 = distance(x_pod2, y_pod2, x_opponent2, y_opponent2) 
    
    thrust_pod1 = 100
    thrust_pod2 = 100
        
    xm_pod1, ym_pod1 = move(int(checkpointX[nextCheckPointId_pod1]), int(checkpointY[nextCheckPointId_pod1]), x_pod1, y_pod1, distNextCheck_pod1, angle_pod1, thrust_pod1, vx_pod1, vy_pod1, CheckpointRadius)
    #xm_pod2, ym_pod2 = move(int(checkpointX[nextCheckPointId_pod2]), int(checkpointY[nextCheckPointId_pod2]), x_pod2, y_pod2, distNextCheck_pod2, angle_pod2, thrust_pod2, vx_pod2, vy_pod2, CheckpointRadius)
    if distOppo1To2 < distOppo2To2:
        xm_pod2, ym_pod2 = NewPosition(x_pod2, y_pod2, vx_pod2, vy_pod2, x_opponent1, y_opponent1, CheckpointRadius)
    else:
        xm_pod2, ym_pod2 = NewPosition(x_pod2, y_pod2, vx_pod2, vy_pod2, x_opponent1, y_opponent1, CheckpointRadius)
    
    if distNextCheck_pod1 < 900:
        if nextCheckPointId_pod1+1 > checkpointCount-1:
            xm_pod1, ym_pod1 = move(int(checkpointX[0]), int(checkpointY[0]), x_pod1, y_pod1, distNextCheck_pod1, angle_pod1, thrust_pod1, vx_pod1, vy_pod1, CheckpointRadius)
        else:
            xm_pod1, ym_pod1 = move(int(checkpointX[nextCheckPointId_pod1+1]), int(checkpointY[nextCheckPointId_pod1+1]), x_pod1, y_pod1, distNextCheck_pod1, angle_pod1, thrust_pod1, vx_pod1, vy_pod1, CheckpointRadius)
    '''
    if distNextCheck_pod2 < 1000:
        if nextCheckPointId_pod2+1 > checkpointCount-1:
            xm_pod2, ym_pod2 = move(int(checkpointX[0]), int(checkpointY[0]), x_pod2, y_pod2, distNextCheck_pod2, angle_pod2, thrust_pod2, vx_pod2, vy_pod2, CheckpointRadius)
        else:
            xm_pod2, ym_pod2 = move(int(checkpointX[nextCheckPointId_pod2+1]), int(checkpointY[nextCheckPointId_pod2+1]), x_pod2, y_pod2, distNextCheck_pod2, angle_pod2, thrust_pod2, vx_pod2, vy_pod2, CheckpointRadius)
    '''      
    boost_pod1, thrust_pod1 = UseBoost(distNextCheck_pod1, angle_pod1, boost_pod1, thrust_pod1)
    boost_pod2, thrust_pod2 = UseBoost(distNextCheck_pod2, angle_pod2, boost_pod2, thrust_pod2)
    
    print(int(xm_pod1), int(ym_pod1), thrust_pod1)
    print(int(xm_pod2), int(ym_pod2), thrust_pod2)

