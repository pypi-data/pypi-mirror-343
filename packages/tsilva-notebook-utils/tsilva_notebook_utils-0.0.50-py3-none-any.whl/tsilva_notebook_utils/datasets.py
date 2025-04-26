from datasets import IterableDataset
from itertools import tee, islice

class ShiftedDataset(IterableDataset):
    def __init__(self, hf_dataset, shift=1):
        if shift < 1:
            raise ValueError("Shift must be >= 1")
        self.dataset = hf_dataset
        self.shift = shift

    def __iter__(self):
        it1, it2 = tee(self.dataset.__iter__(), 2)
        it2 = islice(it2, self.shift, None)

        for x, y in zip(it1, it2):
            yield {
                "x": x.get("x"),
                "y": y.get("y"),
            }

    def __len__(self):
        try:
            return len(self.dataset) - self.shift
        except TypeError:
            raise TypeError("Length is not defined for streaming datasets.")

    def __getitem__(self, idx):
        if idx < 0 or idx >= len(self):
            raise IndexError("Index out of range")
        x = self.dataset[idx]
        y = self.dataset[idx + self.shift]
        return {"x": x.get("x"), "y": y.get("y")}

