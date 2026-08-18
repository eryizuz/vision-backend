from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import logging
import asyncio
import time
import cv2
import numpy as np
import base64
from src.app.app import ClientWorker
from src.analityc.core.utils.overlay import Overlay
from src.analityc.config import config
from src.analityc.core.analytics.attendance_tracker import AttendanceTracker
from src.analityc.core.analytics.seller_efficiency import SellerEfficiency
from src.analityc.core.analytics.stock_monitor import StockMonitor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SERVER-IA")

app = FastAPI(title="Amazonas AI Server")
worker = ClientWorker()
overlay = Overlay()
attendance_tracker = AttendanceTracker()
seller_efficiency = SellerEfficiency()
stock_monitor = StockMonitor()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(worker.run_inference())

@app.get("/")
async def root():
    return {"message": "Amazonas AI Server is running"}

@app.websocket("/ws/PersonaldeAmazonas")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            payload = data.get("data", {})
            frame_b64 = payload.get('frame')
            
            if not frame_b64: continue
            
            # Decodificar imagen
            if ',' in frame_b64:
                img_data = base64.b64decode(frame_b64.split(',')[1])
            else:
                img_data = base64.b64decode(frame_b64)
            
            nparr = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            start_time = time.perf_counter()
            worker.frame_counter += 1
            
            # Procesamiento
            detections = worker.inference.process_frame(frame)
            demographics = worker.demographics.analyze(frame)
            attendance = attendance_tracker.check_interaction(detections)
            seller_eff = seller_efficiency.calculate(attendance)
            stock_info = stock_monitor.monitor(detections)
            unique_people = worker.people_counter.update(detections)
            
            # Dibujar overlay
            annotated_frame = overlay.draw(frame, detections)
            
            # Codificar frame anotado
            _, buffer = cv2.imencode(".jpg", annotated_frame)
            annotated_b64 = "data:image/jpeg;base64," + base64.b64encode(buffer).decode("utf-8")
            
            processing_time = time.perf_counter() - start_time
            
            # Formato de respuesta dinámico
            response = {
                "data": {
                    "camera_id": payload.get("camera_id", 1),
                    "status": "success",
                    "processing_time": round(processing_time, 4),
                    "processed_image": annotated_b64,
                    "metadata": {
                        "frame_number": worker.frame_counter,
                        "persons_inside": len(detections),
                        "active_tracks": len(detections),
                        "people_counter": {"unique_total": unique_people},
                        "demographics": demographics,
                        "attendance": attendance,
                        "seller_efficiency": seller_eff,
                        "stock": stock_info
                    }
                }
            }
            try:
                await websocket.send_json(response)
            except (RuntimeError, WebSocketDisconnect):
                logger.info("El cliente cerró la conexión, deteniendo el envío.")
                break
    except WebSocketDisconnect:
        logger.info("Cliente desconectado")
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
