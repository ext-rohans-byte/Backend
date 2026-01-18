import uuid
import random
import time

class MockPaymentGateway:
    def charge(self, amount: float):
        time.sleep(0.3)  # simulate latency

        if random.random() < 0.9:
            return {
                "status": "success",
                "reference": str(uuid.uuid4()),
            }

        return {
            "status": "failed",
            "reference": None,
        }
