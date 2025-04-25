import argparse
import time
import plotext as plt
from gtop.collector import collect
from gtop.config import Config
from gtop.device import free_device, get_device
from gtop.visualizer import visualize
from gtop.metrics import Metrics
from gtop.collector import CollectedMetricsBuffer


def parse_arguments():
    parser = argparse.ArgumentParser(description="A basic CLI tool to Monitor GPU.")
    parser.add_argument(
        "--device-gpu-index",
        "-g",
        type=int,
        default=0,
        help="GPU index to monitor (default: 0)",
    )
    parser.add_argument(
        "--update-interval",
        "-u",
        type=float,
        default=1.0,
        help="Time interval between updates in seconds (default: 1.0)",
    )
    parser.add_argument(
        "--text-mode",
        "-t",
        action='store_true',
        help="Enable text mode (default: False)",
    )
    return parser.parse_args()


def main():
    cfg = Config.from_parser(args=parse_arguments())
    handle = get_device(cfg)
    metrics = Metrics.for_device(handle)
    buffer = CollectedMetricsBuffer(size=cfg.collector_buffer_size)
    start_time = time.time()
    try:
        while True:
            collected_metrics = collect(metrics, handle, start_time, cfg)
            buffer.append(collected_metrics)
            visualize(buffer, plt, cfg)
            time.sleep(cfg.update_interval)
    except KeyboardInterrupt:
        pass
    finally:
        free_device()


if __name__ == "__main__":
    main()
