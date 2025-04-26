"""energy_monitor.py
Utility for measuring energy and latency of code blocks or functions.

Complies with 14_production_readiness: works with real sensors (via *pyRAPL* for
Intel/AMD RAPL counters and *pynvml* for NVIDIA GPUs).  Falls back gracefully if
these libraries or devices are not present so that production code never
crashes – instead, metrics are logged as `None`.

Example usage
-------------
>>> from quantum_finance.utils.energy_monitor import EnergyMonitor
>>> with EnergyMonitor("my_inference", output_csv="docs/benchmarking/baseline_2024Q2.csv"):
...     model.run(inputs)
>>> # A CSV row is appended containing timestamp, label, duration, cpu_energy_j,
... # gpu_energy_j.

The file purposefully lives in *src/quantum_finance/utils* to keep generic
utilities consolidated.
"""
from __future__ import annotations

import contextlib
import csv
import datetime as _dt
import logging
import os
import time
from typing import Any, Callable, Dict, Optional

# ---------------------------------------------------------------------------
# Optional imports – wrapped in try/except so production code never hard fails
# if the host lacks the specific hardware or library.
# ---------------------------------------------------------------------------
try:
    import pyRAPL  # type: ignore

    _HAS_PYRAPL = True
except ImportError:  # pragma: no cover
    _HAS_PYRAPL = False

try:
    import pynvml  # type: ignore

    _HAS_NVML = True
except ImportError:  # pragma: no cover
    _HAS_NVML = False

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
# Added: prevent log propagation to root and suppress non-warning logs by default
logger.propagate = False
logger.setLevel(logging.WARNING)

# ---------------------------------------------------------------------------
# Helper functions for each energy source
# ---------------------------------------------------------------------------

def _measure_cpu_energy_j() -> float | None:  # noqa: ANN001
    """Return energy (J) consumed since last call using pyRAPL.

    If *pyRAPL* is unavailable or sensors unreachable, returns ``None``.
    """
    if not _HAS_PYRAPL:
        return None

    try:
        if not pyRAPL.is_setup():  # type: ignore[attr-defined]
            pyRAPL.setup()  # type: ignore[attr-defined]
        m = pyRAPL.Measurement("energy_monitor")  # type: ignore[attr-defined]
        m.begin()
        # The caller should immediately call :func:`_measure_cpu_energy_j_end` to
        # finalise the measurement.  We stash the measurement object on the
        # module for retrieval.
        globals()["_CPU_MEAS"] = m
    except Exception as exc:  # pragma: no cover
        logger.debug("pyRAPL setup failed: %s", exc)
        return None
    return 0.0  # Dummy – real value captured on end.


def _measure_cpu_energy_j_end() -> float | None:  # noqa: ANN001
    if not _HAS_PYRAPL or "_CPU_MEAS" not in globals():
        return None
    m = globals().pop("_CPU_MEAS")
    try:
        m.end()
        return float(m.result.pkg[0].energy)  # type: ignore[attr-defined]
    except Exception as exc:  # pragma: no cover
        logger.debug("pyRAPL measurement end failed: %s", exc)
        return None


def _gpu_handle():
    """Return the first NVIDIA device handle or ``None`` if unavailable."""
    if not _HAS_NVML:
        return None
    try:
        pynvml.nvmlInit()
        return pynvml.nvmlDeviceGetHandleByIndex(0)
    except Exception as exc:  # pragma: no cover
        logger.debug("NVML init failed: %s", exc)
        return None


def _gpu_power_w(device) -> float | None:  # noqa: ANN001
    """Instantaneous GPU power in Watts, or ``None`` if unavailable."""
    if device is None:
        return None
    try:
        # Returns mW; convert to W
        return pynvml.nvmlDeviceGetPowerUsage(device) / 1000.0  # type: ignore[arg-type]
    except Exception as exc:  # pragma: no cover
        logger.debug("NVML power read failed: %s", exc)
        return None


# ---------------------------------------------------------------------------
# Main EnergyMonitor context manager
# ---------------------------------------------------------------------------

class EnergyMonitor(contextlib.AbstractContextManager):
    """Context manager and decorator for energy + latency measurement.

    Parameters
    ----------
    label : str
        Human‑readable identifier to log / write to CSV.
    output_csv : str | os.PathLike | None
        If provided, a row is *appended* to this CSV file with
        ``timestamp,label,duration_s,cpu_energy_j,gpu_energy_j``.
    enable_gpu : bool, default True
        Whether to attempt GPU measurement via *pynvml*.
    """

    def __init__(
        self,
        label: str,
        *,
        output_csv: str | os.PathLike | None = None,
        enable_gpu: bool = True,
    ) -> None:
        self.label = label
        self.output_csv = os.fspath(output_csv) if output_csv else None
        self.enable_gpu = enable_gpu and _HAS_NVML

        self._t0: float | None = None
        self._gpu_handle = _gpu_handle() if self.enable_gpu else None
        self._gpu_energy_acc: float | None = None

        self._cpu_energy_start: float | None = None
        self.metrics: Dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Context manager protocol
    # ------------------------------------------------------------------
    def __enter__(self) -> "EnergyMonitor":
        self._t0 = time.perf_counter()

        # CPU energy measurement start
        self._cpu_energy_start = _measure_cpu_energy_j()

        # GPU energy – integrate by sampling start/end power * duration
        if self._gpu_handle:
            self._gpu_power_start = _gpu_power_w(self._gpu_handle)
        else:
            self._gpu_power_start = None
        return self

    def __exit__(self, exc_type, exc, tb):  # noqa: ANN001
        t1 = time.perf_counter()
        duration_s = t1 - (self._t0 or t1)

        # CPU energy
        cpu_energy_j = _measure_cpu_energy_j_end()

        # GPU energy via trapezoidal approximation (2‑sample)
        gpu_energy_j: float | None
        if self._gpu_handle:
            power_end = _gpu_power_w(self._gpu_handle)
            if power_end is not None and self._gpu_power_start is not None:
                avg_p = 0.5 * (self._gpu_power_start + power_end)
                gpu_energy_j = avg_p * duration_s
            else:
                gpu_energy_j = None
        else:
            gpu_energy_j = None

        self.metrics = {
            "timestamp": _dt.datetime.utcnow().isoformat(sep=" ", timespec="seconds"),
            "label": self.label,
            "duration_s": round(duration_s, 6),
            "cpu_energy_j": None if cpu_energy_j is None else round(cpu_energy_j, 6),
            "gpu_energy_j": None if gpu_energy_j is None else round(gpu_energy_j, 6),
        }

        logger.info("[EnergyMonitor] %s – duration %.4fs, CPU J %s, GPU J %s", *self.metrics.values())

        if self.output_csv:
            self._append_csv_row(self.output_csv, self.metrics)

        # allow exceptions to propagate (returning False)
        return False

    # ------------------------------------------------------------------
    # Decorator helper – measure a function call easily
    # ------------------------------------------------------------------
    @classmethod
    def measure(
        cls,
        label: str,
        func: Callable[..., Any],
        *args: Any,
        output_csv: str | os.PathLike | None = None,
        enable_gpu: bool = True,
        **kwargs: Any,
    ) -> tuple[Any, Dict[str, Any]]:
        """Execute *func* under monitoring and return (result, metrics)."""
        with cls(label, output_csv=output_csv, enable_gpu=enable_gpu) as m:
            result = func(*args, **kwargs)
        return result, m.metrics

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _append_csv_row(path: str, row: Dict[str, Any]) -> None:
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        header = ["timestamp", "label", "duration_s", "cpu_energy_j", "gpu_energy_j"]
        exists = os.path.exists(path)
        try:
            with open(path, "a", newline="") as fh:
                writer = csv.DictWriter(fh, fieldnames=header)
                if not exists:
                    writer.writeheader()
                writer.writerow(row)
        except Exception as exc:  # pragma: no cover
            logger.warning("Failed to append energy metrics to %s: %s", path, exc) 