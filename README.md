[README.md](https://github.com/user-attachments/files/34998369/README.md)
# Detector de protector auditivo con Haar Cascade, OpenCV y DroidCam

**Avance de Proyecto Final 3 (AVPF-3)** · Universidad Tecnológica del Perú
**Autor:** Cristian Paul Chinguel Cruz
**Curso:** Inteligencia Artificial aplicada a la Ingeniería Civil
**Fecha:** noviembre de 2026

---

## Descripción

Este proyecto detecta en tiempo real un **protector auditivo tipo orejera** usando un clasificador Haar Cascade entrenado con un dataset propio. El video llega desde la cámara del celular mediante **DroidCam**, y el programa dibuja un rectángulo verde sobre el objeto con la etiqueta `PROTECTOR AUDITIVO`.

**Aplicación en Ingeniería Civil:** apoyar la verificación del uso de equipos de protección personal (EPP) en obras, por ejemplo en zonas con maquinaria de alto ruido como rotomartillos, sierras o compactadoras.

![Detección del protector auditivo](capturas/deteccion.png)

---

## Estructura del repositorio

```
.
├── APF3_CristianChinguel.py     # Detector en tiempo real (código final)
├── cascade.xml                  # Modelo entrenado
├── pos_samples.vec              # Muestras positivas (100, ventana 38x36)
├── pos.lst                      # Anotaciones de imágenes positivas
├── neg.lst                      # Lista de imágenes negativas
├── p/                           # Dataset positivo (100 imágenes)
├── n/                           # Dataset negativo (300 imágenes)
├── captura/
│   ├── Detector_Protector_Auditivo_p.py   # Captura de imágenes positivas
│   └── Detector_Protector_Auditivo_n.py   # Captura de imágenes negativas
├── versiones/                   # V1, V2 y V3 del detector
├── capturas/                    # Capturas de resultados
├── informe/                     # Informe técnico en PDF
└── README.md
```

> Ajusta los nombres de carpetas si tu repositorio está organizado distinto.

---

## Dataset

El dataset fue construido por mí, sin descargar imágenes de internet.

| | Positivas (`p/`) | Negativas (`n/`) |
|---|---|---|
| Cantidad | 100 | 300 |
| Archivos | `objeto_0` a `objeto_99` | `objeto_0` a `objeto_299` |
| Tamaño | 38 × 36 px | 38 px de ancho |

Las imágenes se capturaron con DroidCam usando un recuadro fijo de referencia. El programa recorta esa zona, la reduce a 38 px de ancho y la guarda al presionar la tecla **S**.

| Positiva | Negativa |
|---|---|
| ![Captura positiva](capturas/captura_positiva.png) | ![Captura negativa](capturas/captura_negativa.png) |

---

## Entrenamiento

Se usó **Cascade Trainer GUI** con las listas `pos.lst`, `neg.lst` y el archivo `pos_samples.vec`. Parámetros registrados en `cascade.xml`:

| Parámetro | Valor |
|---|---|
| Tipo de clasificador | BOOST |
| Característica | HAAR |
| Ventana (ancho × alto) | 38 × 36 px |
| Tipo de boosting | GAB |
| minHitRate | 0,995 |
| maxFalseAlarm | 0,5 |
| weightTrimRate | 0,95 |
| maxDepth | 1 |
| maxWeakCount | 100 |
| Etapas (stageNum) | 1 |

> **Nota:** el modelo obtenido tiene una sola etapa, por lo que filtra menos que una cascada de varias etapas. Por eso el detector necesita parámetros estrictos (ver limitaciones).

---

## Requisitos

- Python 3.x
- OpenCV
- imutils (solo para los programas de captura)
- DroidCam (celular y laptop en la misma red) o una webcam

```bash
pip install opencv-python imutils
```

---

## Uso

### 1. Capturar imágenes (opcional)

Edita la dirección IP en el script y ejecútalo. Presiona **S** para guardar y **ESC** para salir.

```bash
python captura/Detector_Protector_Auditivo_p.py   # guarda en p/
python captura/Detector_Protector_Auditivo_n.py   # guarda en n/
```

### 2. Ejecutar el detector

1. Abre DroidCam en el celular y copia la dirección IP que muestra.
2. En `APF3_CristianChinguel.py`, cambia la URL del video:

```python
stream_url = "http://192.168.1.103:4747/video"
```

   Para usar la webcam de la laptop, reemplázala por `cv2.VideoCapture(0, cv2.CAP_DSHOW)`.

3. Ejecuta:

```bash
python APF3_CristianChinguel.py
```

4. Presiona **ESC** para cerrar.

> `cascade.xml` debe estar en la misma carpeta que el script.

---

## Parámetros del detector

| Parámetro | Valor | Efecto |
|---|---|---|
| `scaleFactor` | 5 | Pocos niveles de escala, procesamiento rápido |
| `minNeighbors` | 500 | Exige muchas coincidencias para aceptar una detección |
| `minSize` | (70, 78) | Tamaño mínimo del objeto detectado |
| Resolución de proceso | 640 × 480 | Reduce la carga; las coordenadas se reescalan al video original |

El video se lee en un **hilo aparte** (`ThreadedVideoCapture`) para evitar retraso en el flujo de red.

### Versiones

| Versión | Cambio principal |
|---|---|
| V1 | Detección básica con `minNeighbors = 91` |
| V2 | Márgenes ampliados en el recuadro |
| V3 | `minNeighbors = 500`, lectura en hilo y reducción a 640 × 480 |
| Final | Recuadro exacto, sin márgenes |

---

## Resultados y limitaciones

- El detector identifica el protector cuando se ve completo y a una distancia parecida a la del dataset.
- Con valores bajos de `minNeighbors` aparecían detecciones erróneas, por eso se subió a 500.
- Puede fallar si el objeto está lejos, de lado, parcialmente tapado o con iluminación muy distinta.
- El dataset se tomó con un solo protector y en un ambiente cerrado.
- Las muestras de 38 px conservan poco detalle de la forma.
- No se calcularon métricas formales; la validación fue visual en tiempo real.

### Posibles mejoras

- Reentrenar con más etapas y más muestras, de mayor tamaño.
- Agregar imágenes del protector puesto en una persona y en fondos de obra.
- Evaluar con un conjunto de prueba separado y probar detectores como YOLO.

---

## Entregables

- 🎥 **Video demostrativo:** https://drive.google.com/file/d/1YQ-OaPRclJqTW1t1eQvpensyVTw5u5uv/view?usp=sharing
- 📄 **Informe técnico:** carpeta `informe/`
- 🧠 **Modelo entrenado:** `cascade.xml`
- 💻 **Código fuente:** `APF3_CristianChinguel.py`

---

## Referencias

- Viola, P., y Jones, M. (2001). *Rapid object detection using a boosted cascade of simple features.* CVPR.
- Lienhart, R., y Maydt, J. (2002). *An extended set of Haar-like features for rapid object detection.* ICIP.
- Bradski, G. (2000). *The OpenCV Library.* Dr. Dobb's Journal.
