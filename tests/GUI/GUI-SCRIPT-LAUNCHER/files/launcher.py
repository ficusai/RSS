"""PyQt6 launcher for running all GUI test scripts in RSS/tests/GUI/."""

import sys
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QProgressBar,
    QMessageBox,
)
from PyQt6.QtCore import Qt

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from run_tests_worker import TestRunnerWorker


class LauncherWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RSS GUI Test Launcher")
        self.setMinimumSize(800, 600)

        self.test_dir = Path(__file__).resolve().parents[1]
        self.results: list[dict] = []

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        btn_row = QHBoxLayout()
        self.run_btn = QPushButton("Run")
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setEnabled(False)
        self.run_btn.clicked.connect(self._on_run)
        self.stop_btn.clicked.connect(self._on_stop)
        btn_row.addWidget(self.run_btn)
        btn_row.addWidget(self.stop_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setText("Ready. Click Run to start tests.\n")
        layout.addWidget(self.output)

        self.worker: TestRunnerWorker | None = None

    def _log(self, text: str) -> None:
        self.output.append(text)
        cursor = self.output.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.output.setTextCursor(cursor)
        self.output.ensureCursorVisible()

    def _on_run(self) -> None:
        self.run_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress.setValue(0)
        self.output.clear()
        self.output.setText("Starting tests...\n")
        self.results.clear()

        self.worker = TestRunnerWorker(self.test_dir)
        self.worker.log_signal.connect(self._log)
        self.worker.progress_signal.connect(self.progress.setValue)
        self.worker.finished_signal.connect(self._on_finished)
        self.worker.start()

    def _on_stop(self) -> None:
        if self.worker is not None:
            self.worker.stop()
            self._log("Stopping...")

    def _on_finished(self, results: list[dict]) -> None:
        self.worker = None
        self.run_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress.setValue(100)
        self.results = results

        passed = sum(1 for r in results if r["status"] == "pass")
        failed = sum(1 for r in results if r["status"] == "fail")
        skipped = sum(1 for r in results if r["status"] == "skip")
        total = len(results)

        self._log(f"\n{'='*40}")
        self._log(f"SUMMARY: {total} tests — PASS: {passed}  FAIL: {failed}  SKIP: {skipped}")
        self._log(f"{'='*40}")

        summary_text = (
            f"Tests completed!\n\n"
            f"Total: {total}\n"
            f"Passed: {passed}\n"
            f"Failed: {failed}\n"
            f"Skipped: {skipped}"
        )
        QMessageBox.information(self, "Test Summary", summary_text)


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = LauncherWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
