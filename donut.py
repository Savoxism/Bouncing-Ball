import math
import os
import time

# Constants for the animation
theta_spacing = 0.07
phi_spacing = 0.02
R1 = 1
R2 = 2
K2 = 5
screen_width = 80
screen_height = 40
K1 = screen_width * K2 * 3 / (8 * (R1 + R2))


def render_frame(A, B):
    # Precompute sines and cosines of A and B
    cosA = math.cos(A)
    sinA = math.sin(A)
    cosB = math.cos(B)
    sinB = math.sin(B)

    # Initialize the output and z-buffer
    output = [[' ' for _ in range(screen_width)] for _ in range(screen_height)]
    zbuffer = [[0] * screen_width for _ in range(screen_height)]

    # Theta loop
    theta = 0
    while theta < 2 * math.pi:
        costheta = math.cos(theta)
        sintheta = math.sin(theta)

        # Phi loop
        phi = 0
        while phi < 2 * math.pi:
            cosphi = math.cos(phi)
            sinphi = math.sin(phi)

            # Circle coordinates
            circlex = R2 + R1 * costheta
            circley = R1 * sintheta

            # 3D transformations
            x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
            y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
            z = K2 + cosA * circlex * sinphi + circley * sinA
            ooz = 1 / z

            # 2D projection
            xp = int(screen_width / 2 + K1 * ooz * x)
            yp = int(screen_height / 2 - K1 * ooz * y)

            # Luminance calculation
            L = cosphi * costheta * sinB - cosA * costheta * sinphi - sinA * sintheta + cosB * (cosA * sintheta - costheta * sinA * sinphi)

            if L > 0:  # Only render visible surfaces
                if 0 <= xp < screen_width and 0 <= yp < screen_height:  # Stay within bounds
                    if ooz > zbuffer[yp][xp]:  # Depth check
                        zbuffer[yp][xp] = ooz
                        luminance_index = int(L * 8)
                        luminance_chars = ".,-~:;=!*#$@"
                        output[yp][xp] = luminance_chars[luminance_index]

            phi += phi_spacing
        theta += theta_spacing

    # Render the frame
    os.system("cls" if os.name == "nt" else "clear")
    for row in output:
        print("".join(row))


# Animation loop
A = 0
B = 0
while True:
    render_frame(A, B)
    A += 0.04
    B += 0.02
    time.sleep(0.03)
