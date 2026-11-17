import cv2
import threading

class ThreadedVideoCapture:
    """Clase para leer el stream de red en un hilo separado y eliminar el retraso (lag)."""
    def __init__(self, src):
        self.cap = cv2.VideoCapture(src)
        self.ret, self.frame = self.cap.read()
        self.running = True
        self.lock = threading.Lock()
        
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()
        
    def _update(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.ret = ret
                    self.frame = frame
            else:
                break
                
    def read(self):
        with self.lock:
            if not self.ret or self.frame is None:
                return False, None
            return self.ret, self.frame.copy()
            
    def release(self):
        self.running = False
        self.thread.join()
        self.cap.release()

# Inicializar la cámara IP con el hilo optimizado
stream_url = "http://192.168.1.103:4747/video"
cap = ThreadedVideoCapture(stream_url)

ProtectorAClassif = cv2.CascadeClassifier('cascade.xml')

while True:
    ret, frame = cap.read()
    
    if not ret or frame is None:
        continue

    # Redimensionamos el fotograma para aligerar la carga de procesamiento (puedes ajustar a 640x480 o 480x360)
    frame_process = cv2.resize(frame, (640, 480))
    
    # Obtenemos las dimensiones para escalar las coordenadas del rectángulo después
    h_orig, w_orig = frame.shape[:2]
    h_proc, w_proc = frame_process.shape[:2]
    
    scale_x = w_orig / w_proc
    scale_y = h_orig / h_proc

    gray = cv2.cvtColor(frame_process, cv2.COLOR_BGR2GRAY)

    # Usamos tus valores originales que hicieron abrir la cámara rápido
    toy = ProtectorAClassif.detectMultiScale(
        gray,
        scaleFactor=5,
        minNeighbors=500,
        minSize=(70, 78)
    )

    for (x, y, w, h) in toy:
        # Escalamos las coordenadas detectadas de vuelta al tamaño original del video
        x = int(x * scale_x)
        y = int(y * scale_y)
        w = int(w * scale_x)
        h = int(h * scale_y)

        # Márgenes ajustados a 0 para que el recuadro sea exacto
        margen_x = int(w * 0.00)
        margen_y = int(h * 0.00)  # Modificado de 0.25 a 0.0 para eliminar el exceso inferior

        x1 = max(x - margen_x, 0)
        y1 = max(y - margen_y, 0)

        x2 = x + w + margen_x
        y2 = y + h + margen_y

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            'PROTECTOR AUDITIVO',
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
            cv2.LINE_AA
        )

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
5
