import matplotlib.pyplot as plt
import numpy as np

n = 1 #which participant
angles = np.array([-10,-10,20,20,20,20,20,20]) #angles must be in degrees
distance = np.array([5,10,15,20])

def intersection(x1, y1, x2, y2, theta1_deg, theta2_deg):
    theta1 = np.deg2rad(theta1_deg)
    A1 = -np.sin(theta1)
    B1 =  np.cos(theta1)
    C1 = A1*x1 + B1*y1
    theta2 = np.deg2rad(theta2_deg)
    A2 = -np.sin(theta2)
    B2 =  np.cos(theta2)
    C2 = A2*x2 + B2*y2
    det = A1*B2 - A2*B1
    if abs(det) < 1e-10: 
        return None
    x = (C1*B2 - C2*B1) / det
    y = (A1*C2 - A2*C1) / det
    return (x, y)

def triangle(distance, Rangle, Langle):
    #triangle's vertices
    A = (0, distance)
    B = (-distance*np.sqrt(3)/2, -distance/2)
    C = (distance*np.sqrt(3)/2, -distance/2) 
    P_int = intersection(*B,*C,Rangle,180-Langle)
    # quadratic Bézier
    t = np.linspace(0, 1, 200)
    Bx = (1-t)**2 * B[0] + 2*(1-t)*t * P_int[0] + t**2 * C[0]
    By = (1-t)**2 * B[1] + 2*(1-t)*t * P_int[1] + t**2 * C[1]
    Bez = np.vstack((Bx, By))
    theta = 2*np.pi/3
    R = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta),  np.cos(theta)]])
    B_rot = R @ Bez
    B_rot2 = R @ B_rot
    return Bez, B_rot, B_rot2


plt.figure(figsize=(5,5))
for i in range(len(distance)):
    Bez, B_rot, B_rot2 = triangle(distance[i], angles[2*i], angles[2*i+1])
    plt.plot(Bez[0],Bez[1], 'k-')
    plt.plot(B_rot[0], B_rot[1], 'k-')
    plt.plot(B_rot2[0], B_rot2[1], 'k-')
    plt.scatter(*(0,0), color='black')
plt.axis('equal') 
plt.title("participant n."+str(n))
plt.show()