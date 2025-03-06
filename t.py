import matplotlib.pyplot as plt
import numpy as np


G = 6.67430e-11  
M_p = 5.972e26 
M_s = 1000  
r_p = 6.371e6


x_p, y_p = 0, 0
v_px, v_py = 0, 0.5e3
x_s, y_s = -4e8, 6e7
v_x, v_y = 7e4, 8e3
dt = 100
num_steps = 7850


initial_distance = np.sqrt((x_s - x_p)**2 + (y_s - y_p)**2)
def EulerMethod(x_s, y_s, x_p, y_p, v_x, v_y):
    x_trajectory, y_trajectory = [], []
    x_planet_trajectory, y_planet_trajectory = [], []
    speed, distance = [], []
    for _ in range(num_steps):
        r = np.sqrt((x_s - x_p)**2 + (y_s - y_p)**2)
        if r <= r_p:
            print("Crash! The spacecraft has collided with the planet.")
            break

        
        a_x = -G * M_p * (x_s - x_p) / r**3
        a_y = -G * M_p * (y_s - y_p) / r**3

        
        v_x += a_x * dt
        v_y += a_y * dt

        
        x_s += v_x * dt
        y_s += v_y * dt
        x_p += v_px * dt
        y_p += v_py * dt

        
        x_trajectory.append(x_s)
        y_trajectory.append(y_s)
        x_planet_trajectory.append(x_p)
        y_planet_trajectory.append(y_p)

        
        speed.append(np.sqrt(v_x**2 + v_y**2))
        distance.append(r)
    return x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory, speed, distance     

def RK4Method(x_s, y_s, x_p, y_p, v_x, v_y):
    x_trajectory, y_trajectory = [], []
    x_planet_trajectory, y_planet_trajectory = [], []
    speed, distance = [], []

    def acceleration(x_s, y_s, x_p, y_p):
        r = np.sqrt((x_s - x_p)**2 + (y_s - y_p)**2)
        if r <= r_p:
            print("Crash! The spacecraft has collided with the planet.")
            return None, None  # Остановка при столкновении
        
        a_x = -G * M_p * (x_s - x_p) / r**3
        a_y = -G * M_p * (y_s - y_p) / r**3
        return a_x, a_y

    for _ in range(num_steps):
        # Вычисляем ускорение в начальной точке
        a_x1, a_y1 = acceleration(x_s, y_s, x_p, y_p)
        if a_x1 is None: break  # Остановка при столкновении

        # K1
        k1_vx, k1_vy = a_x1 * dt, a_y1 * dt
        k1_x, k1_y = v_x * dt, v_y * dt

        # K2 (используем половину шага)
        a_x2, a_y2 = acceleration(x_s + 0.5 * k1_x, y_s + 0.5 * k1_y, x_p, y_p)
        k2_vx, k2_vy = a_x2 * dt, a_y2 * dt
        k2_x, k2_y = (v_x + 0.5 * k1_vx) * dt, (v_y + 0.5 * k1_vy) * dt

        # K3 (ещё одна половина шага)
        a_x3, a_y3 = acceleration(x_s + 0.5 * k2_x, y_s + 0.5 * k2_y, x_p, y_p)
        k3_vx, k3_vy = a_x3 * dt, a_y3 * dt
        k3_x, k3_y = (v_x + 0.5 * k2_vx) * dt, (v_y + 0.5 * k2_vy) * dt

        # K4 (полный шаг)
        a_x4, a_y4 = acceleration(x_s + k3_x, y_s + k3_y, x_p, y_p)
        k4_vx, k4_vy = a_x4 * dt, a_y4 * dt
        k4_x, k4_y = (v_x + k3_vx) * dt, (v_y + k3_vy) * dt

        # Обновляем скорость спутника
        v_x += (k1_vx + 2 * k2_vx + 2 * k3_vx + k4_vx) / 6
        v_y += (k1_vy + 2 * k2_vy + 2 * k3_vy + k4_vy) / 6

        # Обновляем координаты спутника
        x_s += (k1_x + 2 * k2_x + 2 * k3_x + k4_x) / 6
        y_s += (k1_y + 2 * k2_y + 2 * k3_y + k4_y) / 6

        # Обновляем координаты планеты (движется равномерно)
        x_p += v_px * dt
        y_p += v_py * dt

        # Сохраняем данные для визуализации
        x_trajectory.append(x_s)
        y_trajectory.append(y_s)
        x_planet_trajectory.append(x_p)
        y_planet_trajectory.append(y_p)
        speed.append(np.sqrt(v_x**2 + v_y**2))
        distance.append(np.sqrt((x_s - x_p)**2 + (y_s - y_p)**2))

    return x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory, speed, distance
def draw_nahui(x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory, speed, distance):
    plot_limit = 2 * initial_distance
    fig1, ax1 = plt.subplots(figsize=(10, 10))
    ax1.plot(x_trajectory, y_trajectory, label='Spacecraft Trajectory')
    ax1.plot(x_planet_trajectory, y_planet_trajectory, label='Planet Trajectory', linestyle='--')
    ax1.plot(x_p, y_p, 'ro', markersize=10, label='Planet')  
    ax1.plot(x_trajectory[0], y_trajectory[0], 'go', markersize=8, label='Start Point')  
    ax1.set_aspect('equal', adjustable='box')
    ax1.set_xlabel('X coordinate (m)')
    ax1.set_ylabel('Y coordinate (m)')
    ax1.set_title('Trajectory of the Spacecraft with Moving Planet (Hyperbolic)')
    ax1.set_xlim(-plot_limit, plot_limit)  
    ax1.set_ylim(-plot_limit, plot_limit)  
    ax1.grid(True)  
    ax1.legend()


    fig2, ax2 = plt.subplots(figsize=(10, 5))
    time = np.arange(0, len(speed) * dt, dt)
    ax2.plot(time, speed)
    ax2.axhline(speed[0], color='r', linestyle='--', label=f'Начальная скорость: {speed[0]:.2f} м/с')
    ax2.axhline(speed[-1], color='g', linestyle='--', label=f'Конечная скорость: {speed[-1]:.2f} м/с')
    ax2.set_xlabel('Время (c)')
    ax2.set_ylabel('Скорость (м/с)')
    ax2.set_title('Зависимость скорости космического аппарата от времени')
    plt.minorticks_on()
    plt.grid(True)
    plt.grid(which = 'minor' , color="grey", alpha=0.25)
    ax2.legend()  


    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.plot(time, distance)
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Distance (m)')
    ax3.set_title('Distance Between Spacecraft and Planet Over Time')
    ax3.grid(True)  

    plt.show()
        
  
x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory, speed, distance = EulerMethod(x_s, y_s, x_p, y_p, v_x, v_y)
draw_nahui(x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory, speed, distance)
x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory, speed, distance = RK4Method(x_s, y_s, x_p, y_p, v_x, v_y)
draw_nahui(x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory, speed, distance)