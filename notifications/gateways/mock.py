import random
import time

class MockNotificationGateway:
    def send(self, *, user, message: str):
        time.sleep(0.3)  # simulate latency

        if random.random() < 0.85:
            return True

        raise Exception("External notification service failed")
