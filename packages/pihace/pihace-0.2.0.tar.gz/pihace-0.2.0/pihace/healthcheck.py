import json
from typing import Callable, Dict, Union

from .utils import get_utc_timestamp, calculate_status, format_rate
from .system_info import get_system_info

class HealthCheck:
    def __init__(self, with_system: bool = False, name: str = None, version: str = None):
        self.with_system = with_system
        self.component_name = name
        self.component_version = version
        self.checkers: Dict[str, Callable[[], Union[bool, tuple]]] = {}

    def register(self, name: str, checker: Callable):
        self.checkers[name] = checker

    def check(self, output: str = "dict", pretty: bool = True) -> Union[dict, str]:
        failures = {}
        success_count = 0
        total_count = len(self.checkers)

        for name, checker in self.checkers.items():
            try:
                result = checker() if callable(checker) else False
                if result is True:
                    success_count += 1
                elif isinstance(result, tuple) and not result[0]:
                    failures[name] = result[1]
                else:
                    failures[name] = "pihace: log are unavailable"
            except Exception as e:
                failures[name] = str(e)

        status = calculate_status(success_count, total_count)
        response = {
            "status": status,
            "timestamp": get_utc_timestamp(),
            "failure": failures if failures else None,
            "rate": format_rate(success_count, total_count),
            "system": get_system_info() if self.with_system else None,
            "component": {
                "name": self.component_name,
                "version": self.component_version
            } if self.component_name and self.component_version else None
        }

        if output == "json":
            return json.dumps(response, indent=4 if pretty else None)
        elif output == "str":
            lines = [
                f"Status: {response['status']} ({response['rate']} healthy)",
                f"Timestamp: {response['timestamp']}"
            ]
            if failures:
                lines.append("Failures:")
                for k, v in failures.items():
                    lines.append(f" - {k}: {v}")
            if response.get("component"):
                lines.append(f"Component: {response['component']['name']} {response['component']['version']}")
            if self.with_system:
                sysinfo = response.get("system", {})
                lines.append("System: " + ", ".join([
                    f"CPU {sysinfo.get('cpu_usage')}",
                    f"Mem {sysinfo.get('memory_usage')}",
                    f"Disk {sysinfo.get('disk_usage')}",
                    f"Free Mem: {sysinfo.get('memory_available')}",
                    f"Python {sysinfo.get('python_version')}",
                    f"OS: {sysinfo.get('os')}"
                ]))
            return "\n".join(lines)

        return response
