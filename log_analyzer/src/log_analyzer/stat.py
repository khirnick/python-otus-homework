from collections import defaultdict
import statistics


class UrlStat:

    def __init__(self) -> None:
        self._requests_times = []
    
    def add(self, time: float) -> None:
        self._requests_times.append(time)
    
    def __iadd__(self, time) -> None:
        self.add(time)
        return self

    @property
    def entries(self) -> int:
        return len(self._requests_times)

    @property
    def average(self) -> float:
        return self.sum / self.entries
    
    @property
    def sum(self) -> float:
        return sum(self._requests_times)

    @property
    def max(self) -> float:
        return max(self._requests_times)
    
    @property
    def median(self) -> float:
        return statistics.median(self._requests_times)


class UrlsStat(defaultdict):

    def __init__(self) -> None:
        super().__init__(UrlStat)
    
    @property
    def entries(self) -> int:
        return len(self)
    
    @property
    def sum(self) -> float:
        return sum(url.sum for url in self.values())
