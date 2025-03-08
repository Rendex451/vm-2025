import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from src.config import *

def draw_nahui(x_trajectory, y_trajectory, x_planet_trajectory, y_planet_trajectory, speed, distance):
    plot_limit = 2 * initial_distance
    fig1, ax1 = plt.subplots(figsize=(10, 10))
    ax1.plot(x_trajectory, y_trajectory, label='Spacecraft Trajectory')
    ax1.plot(x_planet_trajectory, y_planet_trajectory, label='Planet Trajectory', linestyle='--')
    ax1.plot(x_planet, y_planet, 'ro', markersize=10, label='Planet')  
    ax1.plot(x_trajectory[0], y_trajectory[0], 'go', markersize=8, label='Start Point')  
    ax1.plot(x_star, y_star, 'yo', markersize=15, label = "Sun")
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

def animate_trajectories(x_traj, y_traj, x_planet_traj, y_planet_traj):
    assert len(x_traj) == len(y_traj) == len(x_planet_traj) == len(y_planet_traj), \
        "Все траектории должны иметь одинаковую длину!"

    fig, ax = plt.subplots(figsize=(10, 10))
    plot_limit = 2 * initial_distance

    spacecraft_line, = ax.plot([], [], 'b-', label='Spacecraft Trajectory')
    planet_line, = ax.plot([], [], 'r--', label='Planet Trajectory')
    spacecraft_point, = ax.plot([], [], 'bo', markersize=8, label='Spacecraft')
    planet_point, = ax.plot([], [], 'ro', markersize=10, label='Planet')
    star_point, = ax.plot([x_star], [y_star], 'yo', markersize=15, label='Sun')

    ax.set_xlim(-plot_limit, plot_limit)
    ax.set_ylim(-plot_limit, plot_limit)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel('X coordinate (m)')
    ax.set_ylabel('Y coordinate (m)')
    ax.set_title('Animated Trajectories of Spacecraft and Planet')
    ax.grid(True)
    ax.legend()

    def init():
        spacecraft_line.set_data([], [])
        planet_line.set_data([], [])
        spacecraft_point.set_data([], [])
        planet_point.set_data([], [])
        return spacecraft_line, planet_line, spacecraft_point, planet_point

    def update(frame):
        spacecraft_line.set_data(x_traj[:frame], y_traj[:frame])
        planet_line.set_data(x_planet_traj[:frame], y_planet_traj[:frame])
        spacecraft_point.set_data([x_traj[frame]], [y_traj[frame]])
        planet_point.set_data([x_planet_traj[frame]], [y_planet_traj[frame]])
        return spacecraft_line, planet_line, spacecraft_point, planet_point

    ani = FuncAnimation(fig, update, init_func=init, frames=len(x_traj),
                        interval=50, blit=True, repeat=False)

    # ani.save(f'{method_name}.gif', writer='pillow', fps=10)

    plt.show()
