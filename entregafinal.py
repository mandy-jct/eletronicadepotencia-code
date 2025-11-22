import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Parâmetros do circuito
C = 180e-6   # Capacitor (180 uF)
L = 11e-6    # Indutor (11 uH)
R = 85e-3   # Resistor (85 mΩ)
Vc0 = 900 # Tensão inicial do capacitor (900 V)
Il0 = 0   # Corrente inicial no indutor (0 A)

# Diodo desligado (C e L em série)
def serie(t, y):
    Vc, Il = y # oq quero descobrir
    dVc_dt = -Il / C            # da formula da corrente do capacitor
    dIl_dt = Vc / L             # da formula da tensão do indutor
    return [dVc_dt, dIl_dt]

# Diodo ligado (C, L e R em paralelo)
def paralelo(t, y):
    Vc, Il = y # oq quero descobrir
    dIl_dt = (Vc - R * Il) / L  # corrente na bobina com resistor
    dVc_dt = -(Il + Vc / R) / C # corrente do capacitor se divide em Il e Vc/R
    return [dVc_dt, dIl_dt]

# Verifica a tensão para definir se o diodo liga ou não
def circuito(t, y):
    Vc, Il = y

    if Vc > 0:                  # enquanto Vc > 0 - diodo desligado
        return serie(t, y)
    else:                       # quando Vc <= 0 - diodo liga
        return paralelo(t, y)

# Condições iniciais
y0 = [Vc0, Il0]

# Tempo de simulação
tinicial = 0.0
tfinal = 400e-6
t_intervalo = np.linspace(tinicial, tfinal, 4000)

# Resolver o sistema
sol = solve_ivp(circuito, [tinicial, tfinal], y0, t_eval=t_intervalo)
t = sol.t
Vc = sol.y[0]
Il = sol.y[1]

# Converter tempo para microssegundos
t_us = t * 1e6

# Gráfico
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(t_us, Vc, color='red')
plt.ylabel("Tensão (Vc)")
plt.title("Tensão capacitor")
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(t_us, Il, color='red')
plt.xlabel("Tempo (µs)")
plt.ylabel("Corrente (Il)")
plt.title("Corrente indutor")
plt.grid()

plt.tight_layout()
plt.show()