# 
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Parâmetros do circuito
C = 180e-6  # Capacitância (180 uF)
L = 11e-6   # Indutância (11 uH)
R = 85e-3   # Resistência (85 mΩ)
Vc0 = 900.0 # Tensão inicial do capacitor (900 V)
Il0 = 0.0   # Corrente inicial do indutor (0 A)

# Diodo desligado (C e L em série)
def serie(t, y):
    Vc, Il = y    #oq eu quero descobrir
    dVc_dt = -Il / C      # capacitor descarregando pela bobina
    dIl_dt = Vc / L       # tensão do capacitor acelera a corrente na bobina
    return [dVc_dt, dIl_dt]


# Diodo ligado (C, L e R em paralelo)
def paralelo(t, y):
    Vc, Il = y
    dIl_dt = (Vc - R * Il) / L      # corrente na bobina com resistor em paralelo LKT
    dVc_dt = -(Il + Vc / R) / C     # corrente que sai do capacitor vai para L e R
    return [dVc_dt, dIl_dt]

# Condições iniciais
y0 = [Vc0, Il0]
t_final = 400e-6  # 400 µs
t_span = (0.0, t_final)

# Quando Vc atingir 0 (diodo liga)
def diodo_liga(t, y):
    return y[0]           # Vc

diodo_liga.terminal = True   # parar a integração quando Vc = 0
diodo_liga.direction = -1    # controla a direção (só quando cruza de positivo para negativo)

# Fase 1: diodo desligado (C e L em série)
sol_rlc = solve_ivp(
    serie,                # modelo correto para a fase 1
    t_span,
    y0,
    events=diodo_liga,
    dense_output=True,
    method='RK45'
)

t1 = sol_rlc.t
y1_Vc = sol_rlc.y[0]
y1_Il = sol_rlc.y[1]

# Fase 2: diodo ligado (C, L e R em paralelo)
if sol_rlc.t_events[0].size > 0:
    t_event = sol_rlc.t_events[0][0]     # instante em que Vc = 0
    y0_rl = [0.0, sol_rlc.y[1, -1]]      # Vc = 0, corrente contínua
    t_span_rl = (t_event, t_final)

    sol_rl = solve_ivp(
        paralelo,         # modelo correto para a fase 2
        t_span_rl,
        y0_rl,
        dense_output=True,
        method='RK45'
    )

    t2 = sol_rl.t
    y2_Vc = sol_rl.y[0]
    y2_Il = sol_rl.y[1]

    # Combinação dos resultados das duas fases
    t_total = np.concatenate((t1, t2))
    Vc_total = np.concatenate((y1_Vc, y2_Vc))
    Il_total = np.concatenate((y1_Il, y2_Il))
else:
    # Se o evento não ocorrer, só existe a fase 1
    t_total = t1
    Vc_total = y1_Vc
    Il_total = y1_Il

# %%
# Plotagem
t_plot_us = t_total * 1e6  # converter tempo para µs

fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Tensão no capacitor
axes[0].plot(t_plot_us, Vc_total, color='tab:orange', label='Tensão no Capacitor ($V_C$)')
axes[0].set_ylabel('Tensão no Capacitor [V]')
axes[0].legend(loc='upper right')
axes[0].grid(linestyle=':', alpha=0.7)
axes[0].set_title('Tensão no Capacitor')

# Corrente na bobina
axes[1].plot(t_plot_us, Il_total, color='tab:blue', label='Corrente na Bobina ($i_L$)')
axes[1].set_ylabel('Corrente na Bobina [A]')
axes[1].set_xlabel('Tempo [µs]')
axes[1].legend(loc='upper right')
axes[1].grid(linestyle=':', alpha=0.7)
axes[1].set_title('Corrente na Bobina')

fig.suptitle('Resposta Temporal do Estimulador Magnético', fontsize=16)
fig.tight_layout(rect=[0, 0.03, 1, 0.95])

plt.savefig('resposta_circuito_separada.png')
plt.show()

print("Gráfico 'resposta_circuito_separada.png' gerado com sucesso.")
