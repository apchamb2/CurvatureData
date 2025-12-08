import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# n = 1 #which participant
# angles = np.array([
#     6.04783333333333,
#     0.0144166666666666,
#    -2.22983333333333,
#    -0.6362,
#    -0.4575,
#    -0.627833333333333,
#    -1.36008333333333,
#    -1.15433333333333,
#    -0.608583333333333,
#    -1.1475
#  ]) #angles must be in degrees
# distance = np.array([2, 4, 6, 8, 10, 12, 14, 16, 18, 20])

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

###
# plt.figure(figsize=(5,5))
# for i in range(len(distance)):
#     angle = angles[i]          # one angle per distance?
#     Bez, B_rot, B_rot2 = triangle(distance[i], angle, angle)  # confused about  "angles[2*i], angles[2*i+1])"
#     plt.plot(Bez[0],Bez[1], 'k-')
#     plt.plot(B_rot[0], B_rot[1], 'k-')
#     plt.plot(B_rot2[0], B_rot2[1], 'k-')
#     plt.scatter(*(0,0), color='black')
# plt.axis('equal') 
# plt.title("Group Mean Error")
# plt.show()
###

# read .csv to make plots for all participants

df = pd.read_csv("subject_distance_means.csv")


#df["ParticipantNumber"] = df["ParticipantNumber"].astype(str)   
#df["Distance"]          = df["Distance"].astype(float)
#df["mean_Error"]        = df["mean_Error"].astype(float)

from matplotlib.lines import Line2D

for pid, df_p in df.groupby("ParticipantNumber"):
    plt.figure(figsize=(5, 5))

    for _, row in df_p.iterrows():
        dist  = row["Distance"]
        angle = row["mean_Error"] 
        angle = -angle  # invert sign to match visual representation    
        Rangle = angle
        Langle = angle

        Bez, B_rot, B_rot2 = triangle(dist, Rangle, Langle)
        if Bez is None:
            continue

        if angle > 0:
            col = 'red'
        elif angle < 0:
            col = 'blue'
        else:
            col = 'gray'

        plt.plot(Bez[0],    Bez[1],    color=col)
        plt.plot(B_rot[0],  B_rot[1],  color=col)
        plt.plot(B_rot2[0], B_rot2[1], color=col)

    plt.scatter(0, 0, color='black')
    plt.axis('equal')
    plt.title(f"participant n.{pid}")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    legend_lines = [
    Line2D([0], [0], color='blue', lw=2, label='Positive error'),
    Line2D([0], [0], color='red',  lw=2, label='Negative error')
    ]

    plt.legend(handles=legend_lines)

    plt.savefig(f"participant_{pid}_color.png", dpi=300, bbox_inches="tight")
    plt.show()

plt.close('all')

# now plot using group mean error
# for _, row in df.iterrows():
#     dist  = row["Distance"]
#     angle = row["group_mean_Error"]

#     Rangle = angle
#     Langle = angle

#     Bez, B_rot, B_rot2 = triangle(dist, Rangle, Langle)
#     if Bez is None:
#         continue

#     plt.plot(Bez[0],    Bez[1],    'k-', alpha=0.7)
#     plt.plot(B_rot[0],  B_rot[1],  'k-', alpha=0.7)
#     plt.plot(B_rot2[0], B_rot2[1], 'k-', alpha=0.7)


# plt.scatter(0, 0, color='black')
# plt.axis('equal')
# plt.title("Group Mean")
# plt.xlabel("x (m)")
# plt.ylabel("y (m)")

# plt.savefig("group_mean_arcplot.png", dpi=300, bbox_inches="tight")
# plt.close()
