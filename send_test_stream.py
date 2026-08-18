import asyncio
import base64
import json
import websockets
import cv2


async def run_test():
  uri = "ws://localhost:9000/ws/PersonaldeAmazonas"
  video_path = "output/test_video.mp4"

  cap = cv2.VideoCapture(video_path)
  if not cap.isOpened():
    print(f"No se pudo abrir el video en {video_path}")
    return

  async with websockets.connect(uri) as websocket:
    print("Conectado al WebSocket. Enviando frames...")

    frame_count = 0
    while cap.isOpened():
      ret, frame = cap.read()
      if not ret:
        break

      # Redimensionar opcionalmente para aligerar la prueba
      # frame = cv2.resize(frame, (640, 480))

      # Codificar frame a JPEG y luego a Base64
      _, buffer = cv2.imencode(".jpg", frame)
      b64_image = base64.b64encode(buffer).decode("utf-8")

      payload = {
          "data": {
              "frame": b64_image,
              "roi_coordinates": [[500, 250], [900, 250], [1040, 560], [600, 560]],
              "roi_activate": True,
              "cosmetics_enabled": False,
              "camera_id": 1,
          }
      }

      # Enviar por WebSocket
      await websocket.send(json.dumps(payload))
      frame_count += 1
      print(f"Frame {frame_count} enviado...")

      # Esperar la respuesta del servidor con la analítica
      response = await websocket.recv()
      res_data = json.loads(response)
      print(
          "Respuesta recibida:",
          res_data.get("data", {}).get("metadata", {}),
      )

      # Controlar velocidad aproximada (ej. ~20 fps)
      await asyncio.sleep(0.05)

    cap.release()
    print("Prueba de streaming finalizada.")


if __name__ == "__main__":
  asyncio.run(run_test())