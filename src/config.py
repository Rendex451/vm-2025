from numpy import pi, sqrt

# G = 6.67430e-11                             # Гравитационная постоянная
# M_PLANET = 5.972e27                         # Масса планеты (кг)
# M_STAR = 1.989e30                           # Масса Солнца (кг)
# M_SPACECRAFT = 721                          # Масса космического аппарата (кг)
# R_PLANET = 6.371e6                          # Радиус планеты (м)
# R_STAR = 6.963e8                            # Радиус Солнца (м)
# ORBIT_RADIUS = 1.5e11                       # Радиус орбиты (м)

# X_SPACECRAFT, Y_SPACECRAFT = 3 * R_PLANET, -4 * R_PLANET        # Начальная позиция космического аппарата
# V_X_SPACECRAFT, V_Y_SPACECRAFT = -18e3, -3e3                    # Начальная скорость космического аппарата (м/с)


# Пример полезности Гравитационного маневра
G = 6.67430e-11                             # Гравитационная постоянная
M_PLANET = 1.9e27                         # Масса Юпитера (кг)
M_STAR = 1.989e30                           # Масса Солнца (кг)
M_SPACECRAFT = 721                          # Масса космического аппарата (кг)
R_PLANET = 7e7                          # Радиус Юпитера (м)
R_STAR = 6.963e8                            # Радиус Солнца (м)
ORBIT_RADIUS = 7.2e11                       # Радиус орбиты Юпитера (м)
X_SPACECRAFT, Y_SPACECRAFT = 3 * R_PLANET, 3 * R_PLANET
V_X_SPACECRAFT, V_Y_SPACECRAFT = -13e3, -2e3

X_PLANET, Y_PLANET = 0, 0                   # Начальная позиция планеты
X_STAR, Y_STAR = X_PLANET + ORBIT_RADIUS, 0 # Начальная позиция Cолнца
V_PLANET = 0.5e3                            # Начальная скорость планеты (м/с)

# Крушение:
# X_SPACECRAFT, Y_SPACECRAFT = 3 * R_PLANET, -4 * R_PLANET
# V_X_SPACECRAFT, V_Y_SPACECRAFT = -7e3, -3.5e3

# Зонд делает оборот вокруг звезды
# X_SPACECRAFT, Y_SPACECRAFT = 30 * R_PLANET, -40 * R_PLANET
# V_X_SPACECRAFT, V_Y_SPACECRAFT = -37e3, -3e3

# Зонд делает оборот вокруг планеты
# X_SPACECRAFT, Y_SPACECRAFT = 3 * R_PLANET, -4 * R_PLANET
# V_X_SPACECRAFT, V_Y_SPACECRAFT = -7e3, -3e3

# Манёвр по параболе
# X_SPACECRAFT, Y_SPACECRAFT = 3 * R_PLANET, -4 * R_PLANET
# V_X_SPACECRAFT, V_Y_SPACECRAFT = -18e3, -3e3

DT = 60                                     # Шаг времени (с)
DAY = 1440                                  # Минут в сутках
NUM_STEPS = DAY * 1000                      # Количество шагов
T = 360 * 24 * 3600                         # Период орбиты (с)

OMEGA = 2 * pi / T                                                                      # Угловая скорость (рад/сек)
INITIAL_DISTANCE = sqrt((X_SPACECRAFT - X_PLANET)**2 + (Y_SPACECRAFT - Y_PLANET)**2)    # Начальное расстояние
