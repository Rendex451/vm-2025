import numpy as np

from config import *
from visualization import animate_trajectories, draw_nahui


def move_planet(t):
    x_p = -ORBIT_RADIUS * np.cos(OMEGA * t) + ORBIT_RADIUS
    y_p = ORBIT_RADIUS * np.sin(OMEGA * t)
    
    return x_p, y_p


def planet_acceleration(x_sc, y_sc, x_p, y_p):
    r = np.sqrt((x_sc - x_p)**2 + (y_sc - y_p)**2)
    if r <= R_PLANET:
        print("Crash! The spacecraft has collided with the planet.")
        return 0, 0, r
    
    a_x = -G * M_PLANET * (x_sc - x_p) / r**3
    a_y = -G * M_PLANET * (y_sc - y_p) / r**3

    return a_x, a_y, r


def star_acceleration(x_sc, y_sc):
    r = np.sqrt((x_sc-X_STAR)**2 + (y_sc - Y_STAR)**2)
    if r <= R_STAR:
        print("Crash! The spacecraft has collided with the star.")
        return 0, 0

    a_x = -G * M_STAR * (x_sc - X_STAR) / r**3
    a_y = -G * M_STAR * (y_sc - Y_STAR) / r**3

    return a_x, a_y


def euler_method(x_sc, y_sc, x_p, y_p, v_x, v_y):
    x_trajectory, y_trajectory = [], []
    x_planet_trajectory, y_planet_trajectory = [], []
    speed, distance = [], []
    t=0
    for _ in range(NUM_STEPS):
        a_x_p, a_y_p, r_p = planet_acceleration(x_sc, y_sc, x_p, y_p)
        a_x_s, a_y_s = star_acceleration(x_sc, y_sc)
        if a_x_s == 0 or a_x_p == 0:
            break
        a_x = a_x_s + a_x_p
        a_y = a_y_s + a_y_p
        
        v_x += a_x * DT
        v_y += a_y * DT
        
        x_sc += v_x * DT
        y_sc += v_y * DT
        x_p, y_p = move_planet(t)
        #x_p += v_px * dt
        #y_p += v_py * dt
        
        x_trajectory.append(x_sc)
        y_trajectory.append(y_sc)
        x_planet_trajectory.append(x_p)
        y_planet_trajectory.append(y_p)
        
        speed.append(np.sqrt(v_x**2 + v_y**2))
        distance.append(r_p)
        t+=DT

    return x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory, speed, distance     

def rk4_method(x_sc, y_sc, x_p, y_p, v_x, v_y):
    x_trajectory, y_trajectory = [], []
    x_planet_trajectory, y_planet_trajectory = [], []
    speed, distance = [], []
    t = 0
    
    for _ in range(NUM_STEPS):
        # Вычисляем ускорение в начальной точке (K1)
        a_x_p1, a_y_p1, r_p = planet_acceleration(x_sc, y_sc, x_p, y_p)
        a_x_s1, a_y_s1 = star_acceleration(x_sc, y_sc)
        if a_x_p1 == 0 or a_x_s1 == 0:
            break  # Остановка при столкновении
        a_x1 = a_x_p1 + a_x_s1
        a_y1 = a_y_p1 + a_y_s1
        
        k1_vx, k1_vy = a_x1 * DT, a_y1 * DT
        k1_x, k1_y = v_x * DT, v_y * DT

        # K2 (половина шага)
        a_x_p2, a_y_p2, _ = planet_acceleration(x_sc + 0.5 * k1_x, y_sc + 0.5 * k1_y, x_p, y_p)
        a_x_s2, a_y_s2 = star_acceleration(x_sc + 0.5 * k1_x, y_sc + 0.5 * k1_y)
        if a_x_p2 == 0 or a_x_s2 == 0:
            break  # Остановка при столкновении
        a_x2 = a_x_p2 + a_x_s2
        a_y2 = a_y_p2 + a_y_s2
        
        k2_vx, k2_vy = a_x2 * DT, a_y2 * DT
        k2_x, k2_y = (v_x + 0.5 * k1_vx) * DT, (v_y + 0.5 * k1_vy) * DT

        # K3 (ещё одна половина шага)
        a_x_p3, a_y_p3, _ = planet_acceleration(x_sc + 0.5 * k2_x, y_sc + 0.5 * k2_y, x_p, y_p)
        a_x_s3, a_y_s3 = star_acceleration(x_sc + 0.5 * k2_x, y_sc + 0.5 * k2_y)
        if a_x_p3 == 0 or a_x_s3 == 0:
            break  # Остановка при столкновении
        a_x3 = a_x_p3 + a_x_s3
        a_y3 = a_y_p3 + a_y_s3
        
        k3_vx, k3_vy = a_x3 * DT, a_y3 * DT
        k3_x, k3_y = (v_x + 0.5 * k2_vx) * DT, (v_y + 0.5 * k2_vy) * DT

        # K4 (полный шаг)
        a_x_p4, a_y_p4, _ = planet_acceleration(x_sc + k3_x, y_sc + k3_y, x_p, y_p)
        a_x_s4, a_y_s4 = star_acceleration(x_sc + k3_x, y_sc + k3_y)
        if a_x_p4 == 0 or a_x_s4 == 0:
            break  # Остановка при столкновении
        a_x4 = a_x_p4 + a_x_s4
        a_y4 = a_y_p4 + a_y_s4
        
        k4_vx, k4_vy = a_x4 * DT, a_y4 * DT
        k4_x, k4_y = (v_x + k3_vx) * DT, (v_y + k3_vy) * DT

        # Обновляем скорость спутника
        v_x += (k1_vx + 2 * k2_vx + 2 * k3_vx + k4_vx) / 6
        v_y += (k1_vy + 2 * k2_vy + 2 * k3_vy + k4_vy) / 6
        
        # Обновляем координаты спутника
        x_sc += (k1_x + 2 * k2_x + 2 * k3_x + k4_x) / 6
        y_sc += (k1_y + 2 * k2_y + 2 * k3_y + k4_y) / 6

        x_p, y_p = move_planet(t)

        # Сохраняем данные для визуализации
        x_trajectory.append(x_sc)
        y_trajectory.append(y_sc)
        x_planet_trajectory.append(x_p)
        y_planet_trajectory.append(y_p)
        speed.append(np.sqrt(v_x**2 + v_y**2))
        distance.append(np.sqrt((x_sc - x_p)**2 + (y_sc - y_p)**2))
        t += DT

    return x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory, speed, distance

def main():
    x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory, speed, distance \
        = euler_method(X_SPACECRAFT, Y_SPACECRAFT, X_PLANET, Y_PLANET, V_X_SPACECRAFT, V_Y_SPACECRAFT)
    # animate_trajectories(x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory)
    draw_nahui(x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory, speed, distance)

    x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory, speed, distance \
        = rk4_method(X_SPACECRAFT, Y_SPACECRAFT, X_PLANET, Y_PLANET, V_X_SPACECRAFT, V_Y_SPACECRAFT)
    # animate_trajectories(x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory)
    draw_nahui(x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory, speed, distance)
  
if __name__ == "__main__":
    main()
