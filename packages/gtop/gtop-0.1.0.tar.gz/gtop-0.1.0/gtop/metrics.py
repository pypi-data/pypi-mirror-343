from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol
import pynvml

from gtop.device import DeviceHandle
from typing import Any, Tuple


class MetricInterface(Protocol):
    def measure() -> Any:
        ...


@dataclass
class PciThroughputMetric(MetricInterface):
    handle: DeviceHandle

    def measure(self) -> Tuple[float, float]:
        tx = (
            pynvml.nvmlDeviceGetPcieThroughput(
                self.handle,
                pynvml.NVML_PCIE_UTIL_TX_BYTES,
            )
            / 1024
        )
        rx = (
            pynvml.nvmlDeviceGetPcieThroughput(
                self.handle,
                pynvml.NVML_PCIE_UTIL_RX_BYTES,
            )
            / 1024
        )
        return tx, rx  # MB


@dataclass
class GpuProcessMetric(MetricInterface):
    handle: DeviceHandle

    def measure(self) -> float:
        util = pynvml.nvmlDeviceGetUtilizationRates(self.handle)
        return util.gpu


@dataclass
class GpuMemoryMetric(MetricInterface):
    handle: DeviceHandle

    def measure(self) -> Tuple[float, float]:
        mem_info = pynvml.nvmlDeviceGetMemoryInfo(self.handle)
        mem_used = int(mem_info.used / 1024**2)
        mem_total = int(mem_info.total / 1024**2)
        return mem_used, mem_total  # MB


@dataclass
class Metrics:
    pci_throughput: PciThroughputMetric
    gpu_processs: GpuProcessMetric
    gpu_memory: GpuMemoryMetric

    @classmethod
    def for_device(cls, handle: DeviceHandle):
        return cls(
            PciThroughputMetric(handle),
            GpuProcessMetric(handle),
            GpuMemoryMetric(handle),
        )
