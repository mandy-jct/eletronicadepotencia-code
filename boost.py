import numpy as np
import matplotlib.pyplot as plt

#Parâmetros
Vin = 180.0      #tensão de entrada (V)
Vout_ref = 380.0      #tensão de saída desejada (V)
Fs = 40e3       #frequência de chaveamento (Hz)
Ts = 1 / Fs     #período de chaveamento (s)
VIl = 0.20             #20% de ripple na corrente do indutor
VVl = 0.01             #1% de ripple na tensão de saída

#Valores nominais
D = 0.5263          #razão cíclica
Iout = 3.42            #corrente de saída (A)
Iin = 7.2222          #corrente de entrada (A)
R = 111.08          #resistência de carga (ohms)

#Calculo L e C
L = (Vin * D) / (Fs * VIl * Iin)         # Indutância (H)
C = (Iout * D) / (Fs * VVl * Vout_ref)   # Capacitância (F)

#Tempo de simulação
t_end = 20e-3           
dt = Ts / 200       
t = np.arange(0, t_end, dt)

# Vetores de estado
iL = np.zeros_like(t)   # Corrente no indutor
vO = np.zeros_like(t)   # Tensão de saída

# Condições iniciais
iL[0] = 0.0
vO[0] = 0.0

#LOOP DE SIMULAÇÃO 
for k in range(len(t) - 1):
    t_cycle = t[k] % Ts

    #Chave ON ou OFF
    if t_cycle < D * Ts:
        vL = Vin              # ON
    else:
        vL = Vin - vO[k]      # OFF

    #Atualiza iL
    iL[k+1] = iL[k] + (vL / L) * dt

    #Atualiza vO
    i_load = vO[k] / R
    vO[k+1] = vO[k] + (iL[k] - i_load) / C * dt

#GRÁFICO 
plt.figure(figsize=(9,4))
plt.plot(t * 1e3, vO, label='vO(t)')
plt.axhline(Vout_ref, linestyle='--', label=f'Referência = {Vout_ref:.1f} V')
plt.xlabel('Tempo (ms)')
plt.ylabel('Tensão (V)')
plt.title('Tensão de saída - Conversor Boost (180 V → 380 V)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
