import asyncio
import time
from collections import deque
import logging
from src.analityc.core.person_amazona_inference import PersonAmazonasInference
from src.app.logger import AnalyticsLogger
from src.analityc.core.analytics.demographics import DemographicsModule
from src.analityc.core.analytics.people_counter import PeopleCounter
from src.analityc.core.analytics.attendance_tracker import AttendanceTracker

logger = logging.getLogger("ClientWorker")

class ClientWorker:
    def __init__(self, max_frames=5):
        self.queue = deque(maxlen=max_frames)
        self.inference = PersonAmazonasInference()
        self.analytics = AnalyticsLogger()
        self.demographics = DemographicsModule()
        self.people_counter = PeopleCounter()
        self.attendance = AttendanceTracker()
        self.frame_counter = 0
        self.running = True

    async def add_frame(self, frame_data):
        self.queue.append(frame_data)

    async def run_inference(self):
        # ... existing logic ...
        pass
