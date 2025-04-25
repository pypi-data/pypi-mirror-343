class Segment(object):
    def __init__(self, text: str, start_time: float, end_time: float) -> None:
        self.text = text
        self.start_time = start_time
        self.end_time = end_time
