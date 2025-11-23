"""
Sensors module for IoT simulator.
Contains TemperatureSensor, HumiditySensor, GPSSensor classes.
"""
from __future__ import annotations
import random
import time
from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime, timezone
import math


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class TemperatureSensor:
    name: str = "temperature"
    center_c: float = 22.0
    noise_sigma: float = 0.5
    unit: str = "C"

    def read(self) -> Dict[str, Any]:
        value = random.gauss(self.center_c, self.noise_sigma)
        return {
            "timestamp": utc_now_iso(),
            "sensor": self.name,
            "value": round(value, 2),
            "unit": self.unit
        }


@dataclass
class HumiditySensor:
    name: str = "humidity"
    min_pct: float = 20.0
    max_pct: float = 80.0
    drift: float = 0.5  # slow variation per read
    current: float = 50.0
    unit: str = "%"

    def __post_init__(self):
        # initialize within bounds
        if not (self.min_pct <= self.current <= self.max_pct):
            self.current = (self.min_pct + self.max_pct) / 2

    def read(self) -> Dict[str, Any]:
        # apply a slow random drift
        delta = random.uniform(-self.drift, self.drift)
        self.current = max(self.min_pct, min(self.max_pct, self.current + delta))
        # small measurement noise
        noisy = self.current + random.uniform(-0.2, 0.2)
        return {
            "timestamp": utc_now_iso(),
            "sensor": self.name,
            "value": round(noisy, 2),
            "unit": self.unit
        }


@dataclass
class GPSSensor:
    name: str = "gps"
    lat: float = 36.8065  # Tunis by default
    lon: float = 10.1815
    step_meters_min: float = 2.0
    step_meters_max: float = 6.0

    def _meters_to_degrees(self, meters: float) -> (float, float):
        # Approx conversion: 1 degree lat ~ 111_320 m; lon depends on latitude
        deg_lat = meters / 111_320.0
        deg_lon = meters / (111_320.0 * math.cos(math.radians(self.lat)))
        return deg_lat, deg_lon

    def read(self) -> Dict[str, Any]:
        # random heading and step
        heading = random.uniform(0, 2*math.pi)
        step_m = random.uniform(self.step_meters_min, self.step_meters_max)
        dx_m = math.cos(heading) * step_m
        dy_m = math.sin(heading) * step_m
        dlat_deg, dlon_deg = self._meters_to_degrees(abs(dy_m))[0], self._meters_to_degrees(abs(dx_m))[1]
        # preserve sign of movement
        self.lat += dlat_deg if dy_m >= 0 else -dlat_deg
        self.lon += dlon_deg if dx_m >= 0 else -dlon_deg
        return {
            "timestamp": utc_now_iso(),
            "sensor": self.name,
            "lat": round(self.lat, 6),
            "lon": round(self.lon, 6)
        }
