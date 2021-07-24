import asyncio


class Clock:
    def __init__(self):
        self.reset()

    def __call__(self):
        return float(self.time)

    def reset(self) -> None:
        self.time = 0.0

    def tick(self, delta: float) -> None:
        self.time += delta


# Workaround: Returns future if Python version less than 3.8, value otherwise.
# See https://stackoverflow.com/a/50031903
def _async_return(value):
    import sys
    if sys.version_info < (3, 8):
        f = asyncio.Future()
        f.set_result(value)
        return f
    else:
        return value
