"""
Interfaz Gráfica para el Visualizador de Números Primos Gemelos

Este módulo proporciona una interfaz gráfica de usuario (GUI) para
facilitar la visualización y análisis de los números primos gemelos.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import numpy as np
import time
import csv

# Importamos nuestros módulos
from gemelos import encontrar_primos_gemelos, visualizar_recta_numerica, visualizar_dispersion
from optimizado import encontrar_primos_gemelos_optimizado, comparar_rendimiento
from estadisticas import visualizar_analisis_completo

class PrimosGemelosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Números Primos Gemelos")
        self.root.geometry("900x600")
        
        # Variables de estado
        self.gemelos = []
        self.limite = tk.IntVar(value=100)
        self.method_var = tk.StringVar(value="optimizado")
        self.visualization_var = tk.StringVar(value="recta")
        
        # Configuración general
        self.root.configure(bg="#f0f0f0")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Crear el diseño principal
        self.create_widgets()
        
    def create_widgets(self):
        # Panel superior para controles
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(fill=tk.X)
        
        # Entrada para el límite
        ttk.Label(control_frame, text="Límite:").grid(row=0, column=0, padx=5, pady=5)
        limite_entry = ttk.Entry(control_frame, textvariable=self.limite, width=10)
        limite_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Selector de método
        ttk.Label(control_frame, text="Método:").grid(row=0, column=2, padx=5, pady=5)
        method_combo = ttk.Combobox(control_frame, textvariable=self.method_var, 
                               values=["básico", "optimizado"], width=10)
        method_combo.grid(row=0, column=3, padx=5, pady=5)
        
        # Selector de visualización
        ttk.Label(control_frame, text="Visualización:").grid(row=0, column=4, padx=5, pady=5)
        visual_combo = ttk.Combobox(control_frame, textvariable=self.visualization_var, 
                              values=["recta", "tendencia", "espiral", "histograma"], width=10)
        visual_combo.grid(row=0, column=5, padx=5, pady=5)
        
        # Botones de acción
        generate_btn = ttk.Button(control_frame, text="Generar", command=self.generar_primos)
        generate_btn.grid(row=0, column=6, padx=5, pady=5)
        
        visualize_btn = ttk.Button(control_frame, text="Visualizar", command=self.visualizar)
        visualize_btn.grid(row=0, column=7, padx=5, pady=5)
        
        stats_btn = ttk.Button(control_frame, text="Estadísticas", command=self.mostrar_estadisticas)
        stats_btn.grid(row=0, column=8, padx=5, pady=5)
        
        export_btn = ttk.Button(control_frame, text="Exportar CSV", command=self.exportar_csv)
        export_btn.grid(row=0, column=9, padx=5, pady=5)
        
        clear_btn = ttk.Button(control_frame, text="Limpiar", command=self.limpiar)
        clear_btn.grid(row=0, column=10, padx=5, pady=5)
        
        # Panel central dividido
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo para resultados de texto
        self.text_frame = ttk.LabelFrame(main_paned, text="Resultados")
        main_paned.add(self.text_frame, weight=1)
        
        self.result_text = scrolledtext.ScrolledText(self.text_frame, wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panel derecho para visualizaciones
        self.graph_frame = ttk.LabelFrame(main_paned, text="Visualización")
        main_paned.add(self.graph_frame, weight=2)
        
        # Inicialmente vacío, se llenará con gráficos
        
        # Barra de estado inferior
        self.status_var = tk.StringVar(value="Listo")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                         relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def generar_primos(self):
        """Genera los primos gemelos según el método seleccionado."""
        try:
            limite = self.limite.get()
            if limite <= 0:
                messagebox.showerror("Error", "El límite debe ser un número positivo.")
                return
                
            self.status_var.set("Generando primos gemelos...")
            self.root.update_idletasks()
            
            # Usar un hilo para no bloquear la interfaz
            def generate_thread():
                start_time = time.time()
                
                if self.method_var.get() == "básico":
                    self.gemelos = encontrar_primos_gemelos(limite)
                else:
                    self.gemelos = encontrar_primos_gemelos_optimizado(limite)
                    
                elapsed = time.time() - start_time
                
                # Actualizar resultados en el hilo principal
                self.root.after(0, lambda: self.mostrar_resultados(elapsed))
            
            thread = threading.Thread(target=generate_thread)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar primos gemelos: {str(e)}")
            self.status_var.set("Error en la generación")
    
    def mostrar_resultados(self, tiempo):
        """Muestra los resultados en el área de texto."""
        self.result_text.delete(1.0, tk.END)
        
        self.result_text.insert(tk.END, f"Primos gemelos hasta {self.limite.get()}\n")
        self.result_text.insert(tk.END, f"Método: {self.method_var.get()}\n")
        self.result_text.insert(tk.END, f"Tiempo de generación: {tiempo:.4f} segundos\n")
        self.result_text.insert(tk.END, f"Total de pares encontrados: {len(self.gemelos)}\n\n")
        
        if len(self.gemelos) > 0:
            self.result_text.insert(tk.END, "Pares de primos gemelos encontrados:\n")
            # Convertir los valores de NumPy a enteros normales para mostrarlos de forma más limpia
            for i, par in enumerate(self.gemelos):
                # Convertir los valores np.int64 a enteros normales
                par_limpio = (int(par[0]), int(par[1]))
                self.result_text.insert(tk.END, f"{i+1}. {par_limpio}\n")
        
        self.status_var.set(f"Generación completada: {len(self.gemelos)} pares encontrados")
    
    def visualizar(self):
        """Visualiza los primos gemelos según el método seleccionado."""
        if not self.gemelos:
            messagebox.showinfo("Información", "Primero debes generar los primos gemelos.")
            return
            
        self.status_var.set("Generando visualización...")
        self.root.update_idletasks()
        
        # Limpiar el frame de gráficos
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        # Crear una figura para matplotlib
        fig = plt.Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Diferentes visualizaciones
        tipo_visual = self.visualization_var.get()
        limite = self.limite.get()
        
        try:
            if tipo_visual == "recta":
                # Dibujar la recta numérica
                ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
                
                # Marcar las posiciones de cada 10 unidades
                for i in range(0, limite + 1, max(1, limite // 10)):
                    ax.axvline(x=i, color='gray', linestyle='--', alpha=0.2)
                    ax.text(i, -0.15, str(i), ha='center')
                
                # Dibujar los primos gemelos
                for par in self.gemelos:
                    # Dibujamos los puntos
                    ax.plot([par[0], par[1]], [0, 0], 'ro', markersize=6)
                    # Conectamos con una línea
                    ax.plot([par[0], par[1]], [0, 0], 'r-', linewidth=2)
                
                ax.set_title(f'Primos Gemelos hasta {limite} en la Recta Numérica')
                ax.set_ylim(-0.5, 0.5)
                ax.set_xlim(-1, limite + 1)
                ax.grid(False)
                ax.set_yticks([])
                
            elif tipo_visual == "tendencia":
                # Calculamos distancias entre pares consecutivos
                distancias = []
                indices = []
                
                for i in range(len(self.gemelos) - 1):
                    distancia = self.gemelos[i+1][0] - self.gemelos[i][0]
                    distancias.append(distancia)
                    indices.append(i)
                
                if not distancias:
                    messagebox.showinfo("Información", "No hay suficientes pares para calcular distancias.")
                    self.status_var.set("Listo")
                    return
                
                # Calcular estadísticas y línea de tendencia
                from scipy import stats
                pendiente, intercepto, r_valor, p_valor, error_std = stats.linregress(
                    indices, distancias)
                
                # Visualizar como scatter plot con línea de tendencia
                ax.scatter(indices, distancias, color='blue', s=35, alpha=0.7)
                
                # Línea de tendencia
                x = np.array(indices)
                y = intercepto + pendiente * x
                ax.plot(x, y, 'r-', linewidth=2, 
                       label=f'Tendencia: y = {pendiente:.4f}x + {intercepto:.2f}')
                
                ax.set_title(f'Tendencia en las Distancias entre Primos Gemelos hasta {limite}')
                ax.set_xlabel('Índice del Par')
                ax.set_ylabel('Distancia')
                ax.legend()
                ax.grid(True, alpha=0.3)
                
                # Añadir texto con coeficiente de correlación
                ax.text(0.05, 0.95, f'Correlación: {r_valor:.4f}', 
                       transform=ax.transAxes, fontsize=10,
                       verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
                
            elif tipo_visual == "espiral":
                # Extraer todos los primos que forman parte de pares gemelos
                primos_en_pares = []
                for par in self.gemelos:
                    primos_en_pares.extend(par)
                
                # Generar coordenadas para la espiral (espiral de Arquímedes)
                theta = np.sqrt(np.arange(1, limite + 1))
                x = theta * np.cos(theta)
                y = theta * np.sin(theta)
                
                # Dibujar todos los números en la espiral (puntos pequeños y grises)
                ax.scatter(x, y, color='lightgray', s=10, alpha=0.3)
                
                # Resaltar los primos gemelos
                for primo in primos_en_pares:
                    if primo <= limite:
                        ax.scatter(x[primo-1], y[primo-1], color='red', s=50, alpha=0.8)
                
                ax.set_title(f'Espiral de Primos Gemelos hasta {limite}')
                ax.axis('equal')
                ax.grid(False)
                ax.axis('off')
                
            elif tipo_visual == "histograma":
                # Calculamos distancias entre pares consecutivos
                distancias = []
                for i in range(len(self.gemelos) - 1):
                    distancia = self.gemelos[i+1][0] - self.gemelos[i][0]
                    distancias.append(distancia)
                
                if not distancias:
                    messagebox.showinfo("Información", "No hay suficientes pares para calcular distancias.")
                    self.status_var.set("Listo")
                    return
                
                # Calculamos estadísticas
                media = np.mean(distancias)
                mediana = np.median(distancias)
                
                bins = max(10, min(20, int(np.sqrt(len(distancias)))))
                ax.hist(distancias, bins=bins, color='orange', alpha=0.7, edgecolor='black')
                ax.axvline(x=media, color='red', linestyle='--', 
                          label=f'Media: {media:.2f}')
                ax.axvline(x=mediana, color='green', linestyle='-', 
                          label=f'Mediana: {mediana:.2f}')
                
                ax.set_title('Distribución de Distancias entre Pares Consecutivos')
                ax.set_xlabel('Distancia')
                ax.set_ylabel('Frecuencia')
                ax.legend()
                ax.grid(True, alpha=0.3)
            
            # Agregar el gráfico al frame
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            self.status_var.set(f"Visualización '{tipo_visual}' generada correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar visualización: {str(e)}")
            self.status_var.set("Error en la visualización")
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas sobre los primos gemelos."""
        if not self.gemelos:
            messagebox.showinfo("Información", "Primero debes generar los primos gemelos.")
            return
            
        # Analizar las distancias entre pares consecutivos
        distancias = []
        for i in range(len(self.gemelos) - 1):
            distancia = self.gemelos[i+1][0] - self.gemelos[i][0]
            distancias.append(distancia)
            
        if not distancias:
            messagebox.showinfo("Información", "No hay suficientes pares para calcular estadísticas.")
            return
            
        # Calcular estadísticas
        media = np.mean(distancias)
        mediana = np.median(distancias)
        desviacion = np.std(distancias)
        maximo = max(distancias)
        minimo = min(distancias)
        
        # Calcular cuartiles y percentiles relevantes
        q1 = np.percentile(distancias, 25)
        q3 = np.percentile(distancias, 75)
        rango_iqr = q3 - q1
        p90 = np.percentile(distancias, 90)
        p99 = np.percentile(distancias, 99)
        
        # Calcular la moda (valor más frecuente)
        from collections import Counter
        contador = Counter(distancias)
        moda = contador.most_common(1)[0][0]
        freq_moda = contador.most_common(1)[0][1]
        
        # Análisis de tendencia
        from scipy import stats
        pendiente, intercepto, r_valor, p_valor, error_std = stats.linregress(
            range(len(distancias)), distancias)
        
        # Calcular proporción respecto a primos
        if self.method_var.get() == "optimizado":
            from optimizado import criba_eratostenes
            todos_primos = criba_eratostenes(self.limite.get())
            proporcion = len(self.gemelos) * 2 / len(todos_primos)
            
            # Calcular densidad estimada según la teoría
            limite = self.limite.get()
            C = 0.66  # Constante de los primos gemelos
            densidad_teorica = C * limite / (np.log(limite) ** 2) / limite * 100
        else:
            # Si no usamos el método optimizado, no calculamos estos valores
            proporcion = 0
            densidad_teorica = 0
            todos_primos = []
        
        # Crear una ventana más grande para las estadísticas
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Análisis Estadístico de Primos Gemelos")
        stats_window.geometry("800x600")
        
        # Crear un notebook (pestañas) para organizar la información
        notebook = ttk.Notebook(stats_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña 1: Estadísticas básicas
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Estadísticas básicas")
        
        stats_text = scrolledtext.ScrolledText(tab1, wrap=tk.WORD)
        stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        stats_text.insert(tk.END, "ESTADÍSTICAS DE PRIMOS GEMELOS\n")
        stats_text.insert(tk.END, "=" * 40 + "\n\n")
        stats_text.insert(tk.END, f"Número total de pares: {len(self.gemelos)}\n")
        stats_text.insert(tk.END, f"Límite de búsqueda: {self.limite.get()}\n\n")
        
        stats_text.insert(tk.END, "DISTRIBUCIÓN\n")
        stats_text.insert(tk.END, "-" * 40 + "\n")
        stats_text.insert(tk.END, f"• Primer par: {(int(self.gemelos[0][0]), int(self.gemelos[0][1]))}\n")
        stats_text.insert(tk.END, f"• Último par: {(int(self.gemelos[-1][0]), int(self.gemelos[-1][1]))}\n\n")
        
        stats_text.insert(tk.END, "DISTANCIAS ENTRE PARES CONSECUTIVOS\n")
        stats_text.insert(tk.END, "-" * 40 + "\n")
        stats_text.insert(tk.END, f"• Media: {media:.2f}\n")
        stats_text.insert(tk.END, f"• Mediana: {mediana:.2f}\n")
        stats_text.insert(tk.END, f"• Moda: {moda} (aparece {freq_moda} veces)\n")
        stats_text.insert(tk.END, f"• Desviación estándar: {desviacion:.2f}\n")
        stats_text.insert(tk.END, f"• Coeficiente de variación: {(desviacion/media*100):.2f}%\n\n")
        
        stats_text.insert(tk.END, f"• Valor mínimo: {minimo}\n")
        stats_text.insert(tk.END, f"• Primer cuartil (Q1): {q1:.2f}\n")
        stats_text.insert(tk.END, f"• Tercer cuartil (Q3): {q3:.2f}\n")
        stats_text.insert(tk.END, f"• Rango intercuartílico: {rango_iqr:.2f}\n")
        stats_text.insert(tk.END, f"• Percentil 90: {p90:.2f}\n")
        stats_text.insert(tk.END, f"• Percentil 99: {p99:.2f}\n")
        stats_text.insert(tk.END, f"• Valor máximo: {maximo}\n\n")
        
        stats_text.insert(tk.END, "ANÁLISIS DE TENDENCIA\n")
        stats_text.insert(tk.END, "-" * 40 + "\n")
        stats_text.insert(tk.END, f"• Pendiente: {pendiente:.4f}\n")
        stats_text.insert(tk.END, f"• Coeficiente de correlación: {r_valor:.4f}\n")
        stats_text.insert(tk.END, f"• Interpretación: {'Tienden a separarse más' if pendiente > 0 else 'No hay tendencia clara'}\n\n")
        
        stats_text.insert(tk.END, "DENSIDAD Y PROPORCIÓN\n")
        stats_text.insert(tk.END, "-" * 40 + "\n")
        # Densidad global (pares por cada 100 números)
        densidad = len(self.gemelos) * 100 / self.limite.get()
        stats_text.insert(tk.END, f"• Densidad observada: {densidad:.4f} pares por cada 100 números\n")
        
        if self.method_var.get() == "optimizado":
            stats_text.insert(tk.END, f"• Densidad teórica estimada: {densidad_teorica:.4f} pares por cada 100 números\n")
            stats_text.insert(tk.END, f"• Diferencia con teoría: {((densidad-densidad_teorica)/densidad_teorica*100):.2f}%\n\n")
            stats_text.insert(tk.END, f"• Proporción de primos en pares gemelos: {proporcion:.4f}\n")
            stats_text.insert(tk.END, f"• Cantidad de primos: {len(todos_primos)}\n")
            stats_text.insert(tk.END, f"• Primos en pares gemelos: {len(self.gemelos)*2} ({(len(self.gemelos)*2/len(todos_primos)*100):.2f}%)\n")
        
        # Pestaña 2: Histograma de distancias
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Histograma")
        
        fig1 = plt.Figure(figsize=(7, 5), dpi=100)
        ax1 = fig1.add_subplot(111)
        
        bins = max(10, min(30, int(np.sqrt(len(distancias)))))
        ax1.hist(distancias, bins=bins, color='skyblue', alpha=0.7, edgecolor='black')
        ax1.axvline(x=media, color='red', linestyle='--', label=f'Media: {media:.2f}')
        ax1.axvline(x=mediana, color='green', linestyle='-', label=f'Mediana: {mediana:.2f}')
        ax1.axvline(x=moda, color='purple', linestyle=':', label=f'Moda: {moda}')
        
        ax1.set_title('Distribución de Distancias entre Pares Consecutivos')
        ax1.set_xlabel('Distancia')
        ax1.set_ylabel('Frecuencia')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        canvas1 = FigureCanvasTkAgg(fig1, master=tab2)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Pestaña 3: Box Plot
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="Box Plot")
        
        fig2 = plt.Figure(figsize=(7, 5), dpi=100)
        ax2 = fig2.add_subplot(111)
        
        ax2.boxplot(distancias, vert=False, patch_artist=True, 
                   boxprops=dict(facecolor='lightblue'))
        
        ax2.set_title('Box Plot de Distancias entre Pares de Primos Gemelos')
        ax2.set_xlabel('Distancia')
        ax2.grid(True, alpha=0.3, axis='x')
        
        # Añadir texto con estadísticas clave
        stats_text = (
            f"Mín: {minimo}, Q1: {q1:.2f}, Med: {mediana:.2f}, "
            f"Q3: {q3:.2f}, Máx: {maximo}\n"
            f"Media: {media:.2f}, Desv. Est.: {desviacion:.2f}"
        )
        ax2.text(0.5, 0.01, stats_text, horizontalalignment='center',
                verticalalignment='bottom', transform=ax2.transAxes)
        
        canvas2 = FigureCanvasTkAgg(fig2, master=tab3)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Pestaña 4: Tendencia
        tab4 = ttk.Frame(notebook)
        notebook.add(tab4, text="Tendencia")
        
        fig3 = plt.Figure(figsize=(7, 5), dpi=100)
        ax3 = fig3.add_subplot(111)
        
        # Scatter plot
        ax3.scatter(range(len(distancias)), distancias, alpha=0.5, color='blue')
        
        # Línea de tendencia
        x = np.array(range(len(distancias)))
        y = intercepto + pendiente * x
        ax3.plot(x, y, 'r-', label=f'Tendencia: y = {pendiente:.4f}x + {intercepto:.2f}')
        
        ax3.set_title('Tendencia en las Distancias de Primos Gemelos')
        ax3.set_xlabel('Índice del Par')
        ax3.set_ylabel('Distancia')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        canvas3 = FigureCanvasTkAgg(fig3, master=tab4)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Si hay un error por no tener scipy, mostramos solo las estadísticas básicas
        if 'pendiente' not in locals():
            notebook.hide(tab4)
    
    def limpiar(self):
        """Limpia los resultados y gráficos."""
        self.gemelos = []
        self.result_text.delete(1.0, tk.END)
        
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
            
        self.status_var.set("Listo")
    
    def on_close(self):
        """Maneja el cierre de la ventana."""
        if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
            # Cerrar todas las figuras pendientes de matplotlib
            plt.close('all')
            self.root.destroy()
            
    def exportar_csv(self):
        """Exporta los primos gemelos generados a un archivo CSV."""
        if not self.gemelos:
            messagebox.showinfo("Información", "No hay primos gemelos para exportar. Primero debes generarlos.")
            return
            
        # Solicitar al usuario la ubicación para guardar el archivo
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")],
            title="Guardar primos gemelos como CSV"
        )
        
        if not filename:  # Si el usuario cancela la operación
            return
            
        try:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                # Escribir encabezado
                writer.writerow(["Índice", "Primer Primo", "Segundo Primo", "Diferencia"])
                
                # Escribir datos
                for i, par in enumerate(self.gemelos):
                    writer.writerow([i+1, int(par[0]), int(par[1]), int(par[1])-int(par[0])])
                    
            self.status_var.set(f"Primos gemelos exportados a {filename}")
            messagebox.showinfo("Exportación Exitosa", f"Se han exportado {len(self.gemelos)} pares de primos gemelos a:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar archivo CSV: {str(e)}")
            self.status_var.set("Error en la exportación")

if __name__ == "__main__":
    root = tk.Tk()
    app = PrimosGemelosGUI(root)
    root.mainloop() 