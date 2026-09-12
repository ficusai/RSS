"""Background thread that runs pytest on each GUI test file."""

import subprocess
import re
import sys
from pathlib import Path
from PyQt6.QtCore import QThread, pyqtSignal


class TestRunnerWorker(QThread):
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(list)

    def __init__(self, test_dir: Path):
        super().__init__()
        self.test_dir = Path(test_dir)
        self._stop_requested = False

    def stop(self) -> None:
        self._stop_requested = True

    def _collect_test_files(self) -> list[Path]:
        test_files: list[Path] = []
        for item in sorted(self.test_dir.iterdir()):
            if item.name == "conftest.py":
                continue
            if item.is_dir():
                for py_file in sorted(item.glob("*.py")):
                    if py_file.name.startswith("test_"):
                        test_files.append(py_file)
            elif item.is_file() and item.name.startswith("test_") and item.name.endswith(".py"):
                test_files.append(item)
        return test_files

    def _run_pytest(self, test_file: Path) -> dict:
        cmd = [
            sys.executable,
            "-m", "pytest",
            str(test_file),
            "-v",
            "--tb=short",
        ]
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
                env={**__import__("os").environ, "QT_QPA_PLATFORM": "offscreen"},
            )
            output = result.stdout + result.stderr
            return {
                "file": str(test_file.relative_to(self.test_dir)),
                "returncode": result.returncode,
                "output": output,
                "timed_out": False,
            }
        except subprocess.TimeoutExpired:
            return {
                "file": str(test_file.relative_to(self.test_dir)),
                "returncode": -1,
                "output": "TIMEOUT (exceeded 120s)",
                "timed_out": True,
            }

    def _parse_result(self, info: dict) -> dict:
        output = info["output"]
        name = info["file"]

        passed_re = re.findall(r"PASSED\s+.*?(?=FAILED|$)", output, re.DOTALL)
        failed_re = re.findall(r"FAILED\s+.*?(?=PASSED|SKIPPED|$)", output, re.DOTALL)
        skipped_re = re.findall(r"SKIPPED\s+.*?(?=PASSED|FAILED|$)", output, re.DOTALL)

        if "FAILED" in output and ("ERROR" in output or info["returncode"] != 0):
            status = "fail"
            short_name = name.rsplit("/", 1)[-1].replace(".py", "")
            error_lines = [
                line for line in output.splitlines()
                if "FAIL" in line or "ERROR" in line
            ]
            error_msg = "; ".join(error_lines[:3]) if error_lines else output[-500:]
            return {"name": short_name, "status": status, "error": error_msg}

        if "passed" in output.lower() or info["returncode"] == 0:
            return {"name": name.rsplit("/", 1)[-1].replace(".py", ""), "status": "pass", "error": ""}

        if "skip" in output.lower() and info["returncode"] != 0:
            return {"name": name.rsplit("/", 1)[-1].replace(".py", ""), "status": "skip", "error": ""}

        return {"name": name, "status": "fail", "error": output[-500:]}

    def run(self) -> None:
        test_files = self._collect_test_files()
        total = len(test_files)
        results: list[dict] = []

        if total == 0:
            self.log_signal.emit("No test files found.")
            self.finished_signal.emit(results)
            return

        for idx, test_file in enumerate(test_files):
            if self._stop_requested:
                self.log_signal.emit(f"\nStopped at {idx}/{total}.")
                break

            rel = str(test_file.relative_to(self.test_dir))
            self.log_signal.emit(f"[{idx+1}/{total}] Running: {rel}")

            info = self._run_pytest(test_file)
            result = self._parse_result(info)
            results.append(result)

            if result["status"] == "pass":
                self.log_signal.emit(f"  PASS  {result['name']}")
            elif result["status"] == "fail":
                self.log_signal.emit(f"  FAIL  {result['name']}")
                if result["error"]:
                    self.log_signal.emit(f"        {result['error'][:200]}")
            else:
                self.log_signal.emit(f"  SKIP  {result['name']}")

            pct = int((idx + 1) / total * 100)
            self.progress_signal.emit(pct)

        self.finished_signal.emit(results)
