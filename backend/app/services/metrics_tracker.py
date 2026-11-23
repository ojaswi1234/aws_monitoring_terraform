import time

class MetricsTracker:
    def __init__(self):
        self.start_time = time.time()
        self.total_requests = 0

    def record_request(self):
        self.total_requests += 1

    def get_uptime_seconds(self) -> float:
        return round(time.time() - self.start_time, 2)

    def get_metrics(self) -> dict:
        return {
            "uptime_seconds": self.get_uptime_seconds(),
            "total_requests": self.total_requests,
        }

tracker = MetricsTracker()
