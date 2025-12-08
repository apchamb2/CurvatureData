import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

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
    # triangle's vertices
    A = (0, distance)
    B = (-distance*np.sqrt(3)/2, -distance/2)
    C = (distance*np.sqrt(3)/2, -distance/2) 

    P_int = intersection(*B, *C, Rangle, 180 - Langle)
    if P_int is None:
        return None, None, None

    # quadratic Bézier
    t = np.linspace(0, 1, 200)
    Bx = (1-t)**2 * B[0] + 2*(1-t)*t * P_int[0] + t**2 * C[0]
    By = (1-t)**2 * B[1] + 2*(1-t)*t * P_int[1] + t**2 * C[1]
    Bez = np.vstack((Bx, By))

    theta = 2*np.pi/3
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta),  np.cos(theta)]])
    B_rot  = R @ Bez
    B_rot2 = R @ B_rot
    return Bez, B_rot, B_rot2


# Load group mean data
df_group = pd.read_csv("distance_summary.csv")
df_group["Distance"] = df_group["Distance"].astype(float)
df_group["group_mean_Error"] = df_group["group_mean_Error"].astype(float)



# Only show these distances
allowed_distances = {2, 4, 6, 10, 14, 20}

plt.figure(figsize=(6, 6))

for _, row in df_group.iterrows():
    dist  = float(row["Distance"])
    if dist not in allowed_distances:
        continue

    angle = row["group_mean_Error"]
    angle = -angle  # invert sign to match your visual style

    Rangle = angle
    Langle = angle

    Bez, B_rot, B_rot2 = triangle(dist, Rangle, Langle)
    if Bez is None:
        continue

    # Color by sign: red = positive, blue = negative
    if angle > 0:
        col = 'red'
    elif angle < 0:
        col = 'blue'
    else:
        col = 'gray'

    plt.plot(Bez[0],    Bez[1], color=col)
    plt.plot(B_rot[0],  B_rot[1], color=col)
    plt.plot(B_rot2[0], B_rot2[1], color=col)

# origin
plt.scatter(0, 0, color='black')

# formatting
plt.axis('equal')
plt.xlim(-20, 20)   # force consistent x-axis range
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title("Group Mean Error (Selected Distances)")

# legend
legend_lines = [
    Line2D([0], [0], color='red',  lw=2, label='Positive error'),
    Line2D([0], [0], color='blue', lw=2, label='Negative error')
]
plt.legend(handles=legend_lines)

plt.savefig("group_mean_color.png", dpi=300, bbox_inches="tight")
plt.show()

plt.close()
