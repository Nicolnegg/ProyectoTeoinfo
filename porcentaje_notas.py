def calcular_similitud(notas1, notas2):
    m = len(notas1)
    n = len(notas2)

    # Crear una matriz para almacenar los resultados parciales del algoritmo LCS
    matriz = [[0] * (n + 1) for _ in range(m + 1)]

    # Calcular la longitud de la secuencia común más larga utilizando el algoritmo LCS
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if notas1[i - 1] == notas2[j - 1]:
                matriz[i][j] = matriz[i - 1][j - 1] + 1
            else:
                matriz[i][j] = max(matriz[i - 1][j], matriz[i][j - 1])

    # Calcular el porcentaje de similitud como el cociente entre la longitud de la secuencia común
    # más larga y la longitud de la lista más larga
    porcentaje_similitud = (matriz[m][n] / min(m, n)) * 100
    if (porcentaje_similitud>80):
        porcentaje_similitud = porcentaje_similitud + 10
    if (porcentaje_similitud>70):
        porcentaje_similitud = porcentaje_similitud + 10
    if porcentaje_similitud >=100:
        porcentaje_similitud= 100
    return porcentaje_similitud

# Ejemplo de uso
notas1 = ["C", "D", "E", "F", "G"]
notas2 = ["C", "D", "E", "F", "A", "B", "C"]

porcentaje = calcular_similitud(notas1, notas2)
print(f"Porcentaje de similitud: {porcentaje}%")