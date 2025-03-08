from numpy import pi, sqrt

G = 6.67430e-11                             # Гравитационная постоянная
M_planet = 5.972e27                         # Масса планеты (кг)
M_star = 1.989e30                           # Масса Солнца (кг)
r_planet = 6.371e6                          # Радиус планеты (м)
r_star = 6.963e8                            # Радиус Солнца (м)
orbit_radius = 1.5e12                       # Радиус орбиты (м)

x_planet, y_planet = 0, 0                   # Начальная позиция планеты
x_star, y_star = x_planet + orbit_radius, 0 # Начальная позиция Cолнца
v_p = 0.5e3                                 # Начальная скорость планеты (м/с)

x_starship, y_starship = 3 * r_planet, 2 * r_planet       # Начальная позиция космического аппарата
v_x_starship, v_y_starship = -7e3, 3e3                    # Начальная скорость космического аппарата (м/с)

dt = 20                                     # Шаг времени (с)
day = 1440                                  # Минут в сутках
num_steps = day*10                          # Количество шагов
T = 360 * 24 * 3600                         # Период орбиты (с)

omega = 2 * pi / T                                                                # Угловая скорость (рад/сек)
initial_distance = sqrt((x_starship - x_planet)**2 + (y_starship - y_planet)**2)  # Начальное расстояние