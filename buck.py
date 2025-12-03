#IMPORTANDO AS BIBLIOTECAS
import numpy as np
import matplotlib.pyplot as plt

#Parâmetros
Vin = 55     #tensão de entrada (V)
Vout = 32     #tensão desejada na saída
L = 2.1411e-3     #indutância do indutor (H)
R = 10.24       #resistência de carga (Ω)
C = 6.1035e-6  #capacitância do capacitor de saída (F)
Fs = 20e3      #frequência de chaveamento (Hz) 
Ts = 1 / Fs    #período de chaveamento (s)

#DUTY CYCLE
D = Vout / Vin         #D = 0.58

# Tempo de simulação: 5 ms para ver o amortecimento
t_end = 5e-3           # 5 ms
dt = Ts / 200          # subdividindo cada período em 200 passos
t = np.arange(0, t_end, dt)

# Vetores de simulação
iL = np.zeros_like(t)     # Corrente do indutor
vout = np.zeros_like(t)   # Tensão do capacitor/saída

# Condições iniciais
iL[0] = 0.0
vout[0] = 0.0

# Loop de integração 
for k in range(len(t) - 1):
    t_cycle = t[k] % Ts
    # Determinar ON ou OFF
    if t_cycle < D * Ts:
        vL = Vin - vout[k]   #ON
    else:
        vL = -vout[k]        #OFF

    # Atualizar corrente do indutor
    iL[k + 1] = iL[k] + (vL / L) * dt

    # Atualizar tensão do capacitor
    i_load = vout[k] / R
    vout[k + 1] = vout[k] + (iL[k] - i_load) / C * dt

# Plot dos resultados
plt.figure(figsize=(10, 4))
plt.plot(t * 1e3, vout, label='Tensão de Saída (vout)')
plt.axhline(Vout, color='red', linestyle='--', label=f'Média Teórica = {Vout:.1f} V')
plt.title('Resposta Transitória e Estabilização da Tensão de Saída (55 V ==> 32 V)')
plt.xlabel('Tempo (ms)')
plt.ylabel('Tensão (V)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
