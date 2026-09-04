from typing import Self


class MeanStream:
    def __init__(self, mean_range: int) -> None:
        self._mean_range = mean_range
        
        self._stream: list[float] = []
        self._mean: list[float] = []

    def append(self, *values: float) -> None:
        for value in values:
            self._stream.append(value)
            
            if len(self._stream) <= self._mean_range:
                self._mean.append(sum(self._stream) / len(self._stream))
                continue
            
            prev_sum = self._mean[-1] * self._mean_range 
            prev_val = self._stream[-self._mean_range - 1]
            next_sum = prev_sum - prev_val + value
            
            self._mean.append(next_sum / self._mean_range)
            
    @property
    def stream(self) -> list[float]:
        return self._stream
    
    @property
    def mean(self) -> list[float]:
        return self._mean
    
    @classmethod
    def from_array(cls, array: list[float], mean_range: int) -> Self:
        arr = cls(mean_range)
        arr.append(*array)
        return arr


if __name__ == '__main__':
    stream = MeanStream(3)
    stream.append(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 11)
    print(stream.stream)
    print(stream.mean)
