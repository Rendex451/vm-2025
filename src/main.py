import numpy as np

from src.config import *
from src.visualization import animate_trajectories, draw_nahui


def move_planet(t):
    x_p = -orbit_radius * np.cos(omega * t) + orbit_radius
    y_p = orbit_radius * np.sin(omega * t)
    
    return x_p, y_p


# TODO: Пофиксить визуализацию для случая столкновения
def acceleration(x_s, y_s, x_p, y_p):
    r = np.sqrt((x_s - x_p)**2 + (y_s - y_p)**2)
    if r <= r_planet:
        print("Crash! The spacecraft has collided with the planet.")
        return None, None, None
    
    a_x = -G * M_planet * (x_s - x_p) / r**3
    a_y = -G * M_planet * (y_s - y_p) / r**3

    return a_x, a_y, r


def star_acceleration(x_s, y_s):
    r = np.sqrt((x_s-x_star)**2 + (y_s - y_star)**2)
    if r <= r_star:
        print("Crash! The spacecraft has collided with the star.")
        return None, None

    a_x = -G * M_star * (x_s - x_star) / r**3
    a_y = -G * M_star * (y_s - y_star) / r**3

    return a_x, a_y


def EulerMethod(x_s, y_s, x_p, y_p, v_x, v_y):
    x_trajectory, y_trajectory = [], []
    x_planet_trajectory, y_planet_trajectory = [], []
    speed, distance = [], []
    t=0
    for i in range(num_steps):
        a_x_p, a_y_p, r_p = acceleration(x_s, y_s, x_p, y_p)
        a_x_s, a_y_s = star_acceleration(x_s, y_s)
        if a_x_s is None or a_x_p is None:
            break
        a_x = a_x_s + a_x_p
        a_y = a_y_s + a_y_p
        
        v_x += a_x * dt
        v_y += a_y * dt
        
        x_s += v_x * dt
        y_s += v_y * dt
        x_p, y_p = move_planet(t)
        #x_p += v_px * dt
        #y_p += v_py * dt
        
        x_trajectory.append(x_s)
        y_trajectory.append(y_s)
        x_planet_trajectory.append(x_p)
        y_planet_trajectory.append(y_p)
        
        speed.append(np.sqrt(v_x**2 + v_y**2))
        distance.append(r_p)
        t+=dt

    return x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory, speed, distance     

def RK4Method(x_s, y_s, x_p, y_p, v_x, v_y):
    x_trajectory, y_trajectory = [], []
    x_planet_trajectory, y_planet_trajectory = [], []
    speed, distance = [], []
    t = 0
    
    for i in range(num_steps):
        # Вычисляем ускорение в начальной точке
        a_x1, a_y1, _ = acceleration(x_s, y_s, x_p, y_p)
        if a_x1 is None: break  # Остановка при столкновении

        # K1
        k1_vx, k1_vy = a_x1 * dt, a_y1 * dt
        k1_x, k1_y = v_x * dt, v_y * dt

        # K2 (используем половину шага)
        a_x2, a_y2, _ = acceleration(x_s + 0.5 * k1_x, y_s + 0.5 * k1_y, x_p, y_p)
        if a_x2 is None: break  # Остановка при столкновении
        k2_vx, k2_vy = a_x2 * dt, a_y2 * dt
        k2_x, k2_y = (v_x + 0.5 * k1_vx) * dt, (v_y + 0.5 * k1_vy) * dt

        # K3 (ещё одна половина шага)
        a_x3, a_y3, _ = acceleration(x_s + 0.5 * k2_x, y_s + 0.5 * k2_y, x_p, y_p)
        if a_x3 is None: break  # Остановка при столкновении
        k3_vx, k3_vy = a_x3 * dt, a_y3 * dt
        k3_x, k3_y = (v_x + 0.5 * k2_vx) * dt, (v_y + 0.5 * k2_vy) * dt

        # K4 (полный шаг)
        
        a_x4, a_y4, _ = acceleration(x_s + k3_x, y_s + k3_y, x_p, y_p)
        if a_x4 is None: break  # Остановка при столкновении
        k4_vx, k4_vy = a_x4 * dt, a_y4 * dt
        k4_x, k4_y = (v_x + k3_vx) * dt, (v_y + k3_vy) * dt

        # Обновляем скорость спутника
        v_x += (k1_vx + 2 * k2_vx + 2 * k3_vx + k4_vx) / 6
        v_y += (k1_vy + 2 * k2_vy + 2 * k3_vy + k4_vy) / 6
        
        # Обновляем координаты спутника
        x_s += (k1_x + 2 * k2_x + 2 * k3_x + k4_x) / 6
        y_s += (k1_y + 2 * k2_y + 2 * k3_y + k4_y) / 6

        x_p, y_p = move_planet(t)

        # Сохраняем данные для визуализации
        x_trajectory.append(x_s)
        y_trajectory.append(y_s)
        x_planet_trajectory.append(x_p)
        y_planet_trajectory.append(y_p)
        speed.append(np.sqrt(v_x**2 + v_y**2))
        distance.append(np.sqrt((x_s - x_p)**2 + (y_s - y_p)**2))
        t += dt

    return x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory, speed, distance

def main():
    x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory, speed, distance \
        = EulerMethod(x_starship, y_starship, x_planet, y_planet, v_x_starship, v_y_starship)
    animate_trajectories(x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory)
    draw_nahui(x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory, speed, distance)

    x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory, speed, distance \
        = RK4Method(x_starship, y_starship, x_planet, y_planet, v_x_starship, v_y_starship)
    animate_trajectories(x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory)
    draw_nahui(x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory, speed, distance)
  
if __name__ == "__main__":
    main()
