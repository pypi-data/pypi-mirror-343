from gtop.config import Config
from gtop.collector import CollectedMetricsBuffer
from typing import Any

PlotHandle = Any


def visualize(
    inputs: CollectedMetricsBuffer,
    plt: PlotHandle,
    cfg: Config,
) -> None:
    if cfg.text_mode:
        printout_metrics(inputs)
        return
    plt.clt()
    plt.cld()
    plt.subplots(1, 2)
    plt.theme(cfg.visualizer_plot_theme)
    plt.plotsize(cfg.visualizer_plot_size)
    # --------------
    plt.subplot(1, 2)
    timestamps = [input.timestamp for input in inputs]
    pci_tx_values = [input.pci_tx for input in inputs]
    pci_rx_values = [input.pci_rx for input in inputs]
    plt.plot(
        timestamps,
        pci_tx_values,
        label="TX",
        marker=cfg.visualizer_plot_marker,
    )
    plt.plot(
        timestamps,
        pci_rx_values,
        label="RX",
        marker=cfg.visualizer_plot_marker,
    )
    plt.title("GPU PCIe Throughput")
    plt.xlabel("Time (s)")
    plt.ylabel("Throughput (MB/s)")
    plt.ylim(0, max(1, max(pci_tx_values + pci_rx_values) * 1.2))

    # --------------
    plt.subplot(1, 1)
    process_values = [input.process for input in inputs]
    memory_values = [input.memory for input in inputs]
    plt.plot(
        timestamps,
        process_values,
        label="Process",
        marker=cfg.visualizer_plot_marker,
    )
    plt.plot(
        timestamps,
        memory_values,
        label="Memory",
        marker=cfg.visualizer_plot_marker,
    )
    plt.title("GPU Utilization")
    plt.xlabel("Time (s)")
    plt.ylabel("Utilization (%)")
    plt.ylim(0, 100)

    plt.show()


def printout_metrics(inputs: CollectedMetricsBuffer) -> None:
    print(inputs.last)
