with open('/home/sidzcool/GeminiSolutions/01_Proyectos_Activos/Proyecto_Crypto/sniper_scanner.py', 'r') as f:
    lines = f.readlines()

for i in range(96, 305):
    if len(lines[i].strip()) > 0:
        lines[i] = "    " + lines[i]

with open('/home/sidzcool/GeminiSolutions/01_Proyectos_Activos/Proyecto_Crypto/sniper_scanner.py', 'w') as f:
    f.writelines(lines)
