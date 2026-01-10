import random
import time

class RouletteService:

    @staticmethod
    def spin_stream():
        angle = 0.0
        angular_velocity = random.uniform(30.0, 40.0)
        decay = random.uniform(0.975, 0.98)

        while angular_velocity > 0.1:
            angle = (angle + angular_velocity) % 360
            yield round(angle, 2)

            angular_velocity *= decay
            time.sleep(0.02)

        # 停止後の結果確定
        adjusted_angle = (360 - angle + 15) % 360
        result = int(adjusted_angle / 30) + 1
        yield f"RESULT:{result}"
