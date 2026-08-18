# SERVER-IA Backend

Servidor backend para procesamiento de IA y análisis de video.

## Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone <URL-del-repo>
    cd "SERVER-IA"
    ```

2.  **Crear y activar un entorno virtual:**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # Linux / macOS
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar el servidor:**
    Asegúrate de que el backend esté ejecutándose antes de iniciar el cliente frontend:
    ```bash
    uvicorn src.app.server:app --reload --port 9000
    ```
