import time


class LatencyLogger:

    def __init__(self):

        self.timings = {}

    def start(self, stage):

        self.timings[stage] = {
            "start": time.time()
        }

    def stop(self, stage):

        if stage not in self.timings:
            return 0

        end_time = time.time()

        latency = (
            end_time -
            self.timings[stage]["start"]
        ) * 1000

        self.timings[stage]["latency_ms"] = latency

        print(f"{stage}: {latency:.2f} ms")

        return latency

    def summary(self):

        total = 0

        print("\n===== LATENCY REPORT =====")

        for stage, data in self.timings.items():

            latency = data.get("latency_ms", 0)

            total += latency

            print(f"{stage}: {latency:.2f} ms")

        print(f"TOTAL: {total:.2f} ms")

        print("==========================")
        