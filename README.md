# ICI-OpenSourceMonitoring

Script docente para la asignatura **Instrumentación Computacional Inteligente (ICI)** del **Máster en Investigación en Ingeniería de Sistemas y de la Computación** en la Universidad de Cádiz.

## Descripción
Este repositorio contiene scripts en Python desarrollados para la docencia de la asignatura **Instrumentación Computacional Inteligente (ICI)** durante el curso académico 2024-2025. Los scripts permiten la monitorización en tiempo real de datos energéticos (demanda y generación eléctrica) obtenidos de la API de Red Eléctrica de España (REE) y su publicación en un broker MQTT para análisis en sistemas inteligentes. Fueron utilizados en **prácticas de laboratorio** para enseñar a los estudiantes conceptos de instrumentación, adquisición de datos y comunicación en sistemas computacionales.

El script principal (`main.py`) realiza las siguientes funciones:  
- Recoge datos históricos de demanda y generación eléctrica desde la API de REE (`get_ree_demanda`, `get_ree_generacion`).  
- Procesa los datos usando pandas y los envía a un broker MQTT (`send_df_to_mqtt`) para su integración en sistemas de monitorización.  
- Simula (en código comentado) la generación de datos de sensores (temperatura, humedad, pH) para prácticas de instrumentación.

## Uso Docente
Los scripts se emplearon en **prácticas regladas** de ICI para:  
- Introducir a los estudiantes en el uso de APIs abiertas para la adquisición de datos reales.  
- Enseñar técnicas de procesamiento de datos con pandas y comunicación en tiempo real con MQTT.  
- Desarrollar habilidades en instrumentación computacional aplicada a sistemas energéticos inteligentes.  

Los estudiantes usaron estos scripts como base para analizar datos energéticos, implementar sistemas de monitorización y explorar protocolos de comunicación en el contexto de ingeniería de sistemas.

## Instalación y Ejecución
### Requisitos
- Python 3.8 o superior  
- Bibliotecas: `requests`, `pandas`, `paho-mqtt`, `statistics`  
  ```bash
  pip install requests pandas paho-mqtt
  ```

### Instrucciones
1. Clona el repositorio:  
   ```bash
   git clone https://github.com/manuelespinosa/ICI-OpenSourceMonitoring.git
   ```
2. Navega al directorio:  
   ```bash
   cd ICI-OpenSourceMonitoring
   ```
3. Ejecuta el script principal:  
   ```bash
   python main.py
   ```
4. El script se conectará a un broker MQTT público (`mqtt.eclipseprojects.io`) y publicará datos de REE en los tópicos `ICI/Energia/demanda` y `ICI/Energia/generacion`.

**Nota**: Modifica la URL del broker MQTT en `main.py` si usas un servidor local (p. ej., `imp3ddicei1.uca.es`).

## Estructura del Repositorio
- `main.py`: Script principal para adquisición, procesamiento y publicación de datos energéticos.  
- `README.md`: Documentación del proyecto.  
- (Opcional) Añade ejemplos de datos o capturas en `/ejemplos` si los tienes.

## Autoría
- **Manuel Jesús Espinosa Gavira**  
  Docente e investigador, Universidad de Cádiz  
  Correo: manuel.espinosa@uca.es  

## Licencia
Este proyecto está licenciado bajo la **Licencia MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## Citación
Si usas este software en un contexto académico, cita el repositorio:  
Espinosa Gavira, M. J. (2025). ICI-OpenSourceMonitoring. GitHub: https://github.com/manuelespinosa/ICI-OpenSourceMonitoring

## Agradecimientos
A los estudiantes del Máster en Investigación en Ingeniería de Sistemas y de la Computación por su feedback durante las prácticas.
