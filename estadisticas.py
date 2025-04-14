"""
Análisis Estadístico de Números Primos Gemelos

Este módulo analiza estadísticamente la distribución de los números
primos gemelos y genera visualizaciones basadas en distintas propiedades.
"""

import numpy as np
import matplotlib.pyplot as plt
from optimizado import encontrar_primos_gemelos_optimizado
from matplotlib.ticker import ScalarFormatter
import math

def calcular_densidad(gemelos, limite, tam_ventana=100):
    """
    Calcula la densidad de primos gemelos a lo largo del rango numérico.
    
    Args:
        gemelos (list): Lista de tuplas con pares de primos gemelos
        limite (int): Límite superior usado para generar los primos
        tam_ventana (int): Tamaño de la ventana deslizante para calcular la densidad
        
    Returns:
        tuple: (centros_ventanas, densidades)
    """
    # Extraemos los primeros primos de cada par para simplificar
    primeros_primos = [par[0] for par in gemelos]
    
    # Creamos ventanas deslizantes para calcular la densidad
    ventanas = np.arange(0, limite, tam_ventana)
    densidades = []
    centros_ventanas = []
    
    for i in range(len(ventanas) - 1):
        inicio = ventanas[i]
        fin = ventanas[i + 1]
        centro = (inicio + fin) / 2
        
        # Contamos cuántos primos gemelos comienzan en esta ventana
        count = sum(1 for p in primeros_primos if inicio <= p < fin)
        
        # Calculamos la densidad (primos por unidad)
        densidad = count / tam_ventana
        
        densidades.append(densidad)
        centros_ventanas.append(centro)
    
    return centros_ventanas, densidades

def analizar_distancias_entre_gemelos(gemelos):
    """
    Analiza la distribución de distancias entre pares consecutivos de primos gemelos.
    
    Args:
        gemelos (list): Lista de tuplas con pares de primos gemelos
        
    Returns:
        tuple: (distancias, media, mediana, desviacion_estandar)
    """
    # Si hay menos de 2 pares, no podemos calcular distancias
    if len(gemelos) < 2:
        return [], 0, 0, 0
    
    # Calculamos distancias entre pares consecutivos
    distancias = []
    for i in range(len(gemelos) - 1):
        distancia = gemelos[i+1][0] - gemelos[i][0]
        distancias.append(distancia)
    
    # Calculamos estadísticas
    media = np.mean(distancias)
    mediana = np.median(distancias)
    desviacion = np.std(distancias)
    
    return distancias, media, mediana, desviacion

def comparar_con_pi(limite):
    """
    Compara la cantidad de primos gemelos hasta un límite con
    las estimaciones teóricas basadas en el número π.
    
    La conjetura de los primos gemelos sugiere que la cantidad de 
    pares de primos gemelos hasta n es aproximadamente:
    cantidad ≈ C · n / (log n)²
    donde C es la constante de los primos gemelos (~0.66).
    
    Args:
        limite (int): Límite superior para buscar primos gemelos
        
    Returns:
        tuple: (limites, cantidades_reales, cantidades_estimadas)
    """
    # Constante de los primos gemelos
    C = 0.66
    
    # Generamos datos para distintos límites
    limites_escala = np.logspace(2, np.log10(limite), 20).astype(int)
    cantidades_reales = []
    cantidades_estimadas = []
    
    for lim in limites_escala:
        # Calculamos la cantidad real
        gemelos = encontrar_primos_gemelos_optimizado(lim)
        cantidades_reales.append(len(gemelos))
        
        # Estimamos según la fórmula teórica
        estimado = C * lim / (np.log(lim) ** 2)
        cantidades_estimadas.append(estimado)
    
    return limites_escala, cantidades_reales, cantidades_estimadas

def visualizar_analisis_completo(limite):
    """
    Realiza un análisis completo de los primos gemelos hasta el límite
    y genera visualizaciones de los resultados.
    
    Args:
        limite (int): Límite superior para buscar primos gemelos
    """
    print(f"Generando primos gemelos hasta {limite}...")
    gemelos = encontrar_primos_gemelos_optimizado(limite)
    print(f"Se encontraron {len(gemelos)} pares de primos gemelos.")
    
    # Configuración para gráficos
    plt.style.use('seaborn')
    
    # 1. Gráfico de densidad
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 2, 1)
    
    tam_ventana = max(limite // 100, 10)  # Ajustar tamaño de ventana según el límite
    centros, densidades = calcular_densidad(gemelos, limite, tam_ventana)
    
    plt.plot(centros, densidades, 'b-', alpha=0.7)
    plt.title('Densidad de Primos Gemelos')
    plt.xlabel('Número')
    plt.ylabel('Densidad')
    plt.grid(True, alpha=0.3)
    
    # 2. Histograma de distancias
    plt.subplot(2, 2, 2)
    
    distancias, media, mediana, desviacion = analizar_distancias_entre_gemelos(gemelos)
    
    bins = max(20, int(np.sqrt(len(distancias))))
    plt.hist(distancias, bins=bins, color='orange', alpha=0.7, edgecolor='black')
    plt.axvline(x=media, color='red', linestyle='--', 
                label=f'Media: {media:.2f}')
    plt.axvline(x=mediana, color='green', linestyle='-', 
                label=f'Mediana: {mediana:.2f}')
    
    plt.title('Distribución de Distancias entre Pares Consecutivos')
    plt.xlabel('Distancia')
    plt.ylabel('Frecuencia')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 3. Comparación con estimación teórica
    plt.subplot(2, 2, 3)
    
    limites_escala, cantidades_reales, cantidades_estimadas = comparar_con_pi(limite)
    
    plt.loglog(limites_escala, cantidades_reales, 'b-', marker='o', 
              markersize=4, label='Cantidad real')
    plt.loglog(limites_escala, cantidades_estimadas, 'r--', 
              label='Estimación teórica')
    
    plt.title('Comparación con la Estimación Teórica')
    plt.xlabel('Límite (escala logarítmica)')
    plt.ylabel('Cantidad de pares gemelos (escala logarítmica)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 4. Proporción de primos gemelos respecto a todos los primos
    plt.subplot(2, 2, 4)
    
    # Necesitamos contar todos los primos hasta el límite
    from optimizado import criba_eratostenes
    todos_primos = criba_eratostenes(limite)
    
    # Calcular proporción en ventanas
    ventanas = np.linspace(0, limite, min(100, limite//10))
    proporciones = []
    centros_ventanas = []
    
    for i in range(len(ventanas) - 1):
        inicio = ventanas[i]
        fin = ventanas[i + 1]
        centro = (inicio + fin) / 2
        
        # Contamos primos y pares gemelos en esta ventana
        primos_en_ventana = sum(1 for p in todos_primos if inicio <= p < fin)
        gemelos_en_ventana = sum(1 for g in gemelos if inicio <= g[0] < fin)
        
        # Calculamos proporción (si hay primos en la ventana)
        if primos_en_ventana > 0:
            proporcion = (gemelos_en_ventana * 2) / primos_en_ventana
            proporciones.append(proporcion)
            centros_ventanas.append(centro)
    
    plt.plot(centros_ventanas, proporciones, 'g-', alpha=0.7)
    plt.title('Proporción de Primos en Pares Gemelos')
    plt.xlabel('Número')
    plt.ylabel('Proporción')
    plt.grid(True, alpha=0.3)
    
    # Ajustes finales y guardar
    plt.tight_layout()
    plt.savefig('analisis_estadistico.png', dpi=300)
    plt.show()
    
    # Imprimimos algunas estadísticas adicionales
    print("\nESTADÍSTICAS:")
    print(f"- Media de distancia entre pares: {media:.2f}")
    print(f"- Mediana de distancia: {mediana:.2f}")
    print(f"- Desviación estándar: {desviacion:.2f}")
    print(f"- Distancia máxima observada: {max(distancias) if distancias else 0}")
    
    # Estimación de la constante de los primos gemelos
    ultimo_limite = limites_escala[-1]
    ultimo_real = cantidades_reales[-1]
    C_estimada = ultimo_real * (np.log(ultimo_limite) ** 2) / ultimo_limite
    print(f"- Constante de los primos gemelos estimada: {C_estimada:.4f} (valor teórico ≈ 0.66)")

if __name__ == "__main__":
    print("=" * 50)
    print("ANÁLISIS ESTADÍSTICO DE NÚMEROS PRIMOS GEMELOS")
    print("=" * 50)
    print("\nEste programa analiza la distribución estadística de")
    print("los números primos gemelos y sus propiedades.")
    
    while True:
        try:
            limite = int(input("\nIntroduce el límite para el análisis: "))
            if limite <= 0:
                print("Por favor, introduce un número positivo.")
                continue
            break
        except ValueError:
            print("Por favor, introduce un número entero válido.")
    
    visualizar_analisis_completo(limite) 