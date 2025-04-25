import time
from dataclasses import dataclass, field
from typing import List
from gtop.config import Config
from gtop.device import DeviceHandle
from gtop.metrics import Metrics


@dataclass
class CollectedMetrics:
    timestamp: float
    pci_tx: float
    pci_rx: float
    process: float
    memory: float

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"Time={self.timestamp:0.2f}(s)"
            f", PCI-TX={self.pci_tx:0.2f}(MB/s)"
            f", PCI-RX={self.pci_rx:0.2f}(MB/s)"
            f", Process={self.process:0.2f}(%)"
            f", Memory={self.memory:0.2f}(%)"
            ")"
        )


@dataclass
class CollectedMetricsBuffer:
    size: int
    buffer: List[CollectedMetrics] = field(default_factory=list)

    def append(self, item: CollectedMetrics) -> None:
        self.buffer.append(item)
        if len(self.buffer) > self.size:
            self.buffer = self.buffer[-self.size :]

    def __iter__(self):
        for item in self.buffer:
            yield item

    @property
    def last(self) -> CollectedMetrics:
        return self.buffer[-1]

    @property
    def first(self) -> CollectedMetrics:
        return self.buffer[0]


def collect(
    metrics: Metrics,
    handle: DeviceHandle,
    start_time: float,
    cfg: Config,
) -> CollectedMetrics:
    now = time.time() - start_time
    tx, rx = metrics.pci_throughput.measure()
    process = metrics.gpu_processs.measure()
    mem_used, mem_total = metrics.gpu_memory.measure()
    return CollectedMetrics(
        timestamp=max(now, cfg.collector_min_time_interval),
        pci_tx=tx,
        pci_rx=rx,
        process=process,
        memory=mem_used / mem_total * 100,
    )
