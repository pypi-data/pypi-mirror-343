import sys

import emzed
import emzed.gui
import tadamz
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QPainter, QPixmap
from PyQt5.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from tadamz_gui.inspect_calibration import InspectCalibrationWindow


class RunWorkflowWindow(QWidget):
    def __init__(
        self,
        peak_table,
        samples,
        config,
        sample_table,
        calibration_table,
        # project_folder="",
    ):
        super().__init__()

        self.peak_table = peak_table
        self.samples = samples
        self.config = config
        self.sample_table = sample_table
        self.calibration_table = calibration_table

        # self.project_folder = project_folder
        self.t = None
        self.t_cal = None

        # allow redirection of outputs to GUI
        self.redirector = OutputRedirector()
        self.redirector.outputWritten.connect(self.update_terminal_output)

        self.setWindowTitle("Run workflow")
        self.resize(800, 600)

        # GUI contents

        self.run_peak_extraction_button = QPushButton(
            "Run peak integration and analysis"
        )
        self.run_peak_extraction_button.clicked.connect(self.run_peak_extraction)

        self.postprocess_button = QPushButton(
            "Run postprocessing (classification, co-elution, normalization)"
        )
        self.postprocess_button.clicked.connect(self.run_postprocessing)
        self.postprocess_button.setEnabled(False)

        self.run_calibration_button = QPushButton("Run calibration")
        self.run_calibration_button.setEnabled(False)
        self.run_calibration_button.clicked.connect(self.run_calibration)

        self.inspect_calibration_button = QPushButton("Inspect calibration")
        self.inspect_calibration_button.setEnabled(False)
        self.inspect_calibration_button.clicked.connect(self.inspect_calibration)

        self.run_quantification_button = QPushButton("Run quantification")
        self.run_quantification_button.setEnabled(False)
        self.run_quantification_button.clicked.connect(self.run_quantification)

        self.inspect_table_button = QPushButton("Inspect current table")
        self.inspect_table_button.clicked.connect(self.inspect_table)
        self.inspect_table_button.setEnabled(False)

        self.save_results_button = QPushButton("Save current results")
        self.save_results_button.clicked.connect(self.save_results)
        self.save_results_button.setEnabled(False)

        self.export_table_button = QPushButton("Export current table as CSV")
        self.export_table_button.clicked.connect(self.export_table)
        self.export_table_button.setEnabled(False)

        self.terminal_output = QTextEdit()
        self.terminal_output.setReadOnly(True)

        # Create and add status bar
        self.status_bar = QStatusBar()
        self.busy_indicator_label = QLabel()
        self.update_busy_indicator(False)
        self.status_bar.addPermanentWidget(self.busy_indicator_label)

        layout_wf_steps = QVBoxLayout()
        layout_wf_steps.addWidget(self.run_peak_extraction_button)
        layout_wf_steps.addWidget(self.postprocess_button)
        layout_wf_steps.addWidget(self.run_calibration_button)
        layout_wf_steps.addWidget(self.inspect_calibration_button)
        layout_wf_steps.addWidget(self.run_quantification_button)

        layout_general_buttons = QHBoxLayout()
        layout_general_buttons.addWidget(self.inspect_table_button)
        layout_general_buttons.addWidget(self.save_results_button)
        layout_general_buttons.addWidget(self.export_table_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout_wf_steps)
        main_layout.addWidget(self.terminal_output)
        main_layout.addLayout(layout_general_buttons)
        main_layout.addWidget(self.status_bar)

        self.setLayout(main_layout)

    def update_busy_indicator(self, busy):
        if busy:
            color = "orange"
        else:
            color = "green"

        pixmap = QPixmap(20, 20)
        pixmap.fill(QColor("transparent"))

        painter = QPainter(pixmap)
        painter.setBrush(QColor(color))
        painter.setPen(QColor(color))
        painter.drawEllipse(0, 0, 20, 20)
        painter.end()

        self.busy_indicator_label.setPixmap(pixmap)

    def run_peak_extraction(self):
        self.worker_thread = WorkerThread(
            function_to_run=tadamz.run_workflow,
            redirector=self.redirector,
            parent=self,
            args=[
                self.peak_table,
                self.samples,
                self.config,
                None,  # t_cal
                self.sample_table,
            ],
        )

        def _on_workflow_finish():
            if not self.worker_thread.error:
                self.t = self.worker_thread.func_return

                message = (
                    "Finished peak extraction, classification, and co-elution analysis"
                )
                self.print_to_GUI_terminal(message)
                self.status_bar.showMessage(message)

            else:
                self.display_error(str(self.worker_thread.error))

            self.enable_usable_buttons()

        self.worker_thread.finished.connect(_on_workflow_finish)
        self.worker_thread.start()

    def run_postprocessing(self):
        self.worker_thread = WorkerThread(
            function_to_run=tadamz.postprocess_result_table,
            redirector=self.redirector,
            parent=self,
            args=[
                self.t,
                self.config,
            ],
        )

        def _on_postprocessing_finish():
            if not self.worker_thread.error:
                self.t = self.worker_thread.func_return

                message = "Finished post-processing"
                self.print_to_GUI_terminal(message)
                self.status_bar.showMessage(message)
            else:
                self.display_error(str(self.worker_thread.error))

            self.enable_usable_buttons()

        self.worker_thread.finished.connect(_on_postprocessing_finish)
        self.worker_thread.start()

    def run_calibration(self):
        self.worker_thread = WorkerThread(
            function_to_run=tadamz.run_calibration,
            redirector=self.redirector,
            parent=self,
            args=[
                self.t,
                self.calibration_table,
                self.sample_table,
                self.config,
            ],
        )

        def _on_calibration_finish():
            if not self.worker_thread.error:
                self.t_cal = self.worker_thread.func_return

                message = "Finished calibration"
                self.print_to_GUI_terminal(message)
                self.status_bar.showMessage(message)

            else:
                self.display_error(str(self.worker_thread.error))

            self.enable_usable_buttons()

        self.worker_thread.finished.connect(_on_calibration_finish)
        self.worker_thread.start()

    def inspect_calibration(self):
        self.inspect_calibration_window = InspectCalibrationWindow(self.t_cal)
        self.inspect_calibration_window.show()

    def run_quantification(self):
        self.worker_thread = WorkerThread(
            function_to_run=tadamz.postprocess_result_table,
            redirector=self.redirector,
            parent=self,
            args=[
                self.t,
                self.config,
                1,
                self.t_cal,
            ],
        )

        def _on_postprocessing_finish():
            if not self.worker_thread.error:
                self.t = self.worker_thread.func_return

                message = "Finished quantification"
                self.print_to_GUI_terminal(message)
                self.status_bar.showMessage(message)
            else:
                self.display_error(str(self.worker_thread.error))

            self.enable_usable_buttons()

        self.worker_thread.finished.connect(_on_postprocessing_finish)
        self.worker_thread.start()

    def display_error(self, error_message):
        QMessageBox.critical(self, "Error", f"An error occurred: {error_message}")

    def inspect_table(self):
        if self.t is not None:
            t_mod = emzed.gui.inspect(self.t)

            if t_mod is not None:
                self.t = t_mod
                self.status_bar.showMessage(
                    "Table has been modified. Consider re-running processing steps."
                )
        else:
            self.status_bar.showMessage("No table to inspect")

    def save_results(self):
        if self.t is not None:
            options = QFileDialog.Options()
            options |= QFileDialog.ShowDirsOnly
            folder = QFileDialog.getExistingDirectory(
                self,
                "Select folder",
                # self.project_folder,
                options=options,
            )

            if folder:
                self.t.save(f"{folder}/results.table", overwrite=True)

                if self.t_cal is not None:
                    self.t_cal.save(f"{folder}/calibration.table", overwrite=True)

                    self.status_bar.showMessage(
                        f"Results saved to {folder}/results.table and {folder}/calibration.table"
                    )
                else:
                    self.status_bar.showMessage(
                        f"Results saved to {folder}/results.table"
                    )
        else:
            self.status_bar.showMessage("No results to save")

    def export_table(self):
        if self.t is not None:
            options = QFileDialog.Options()
            file, _ = QFileDialog.getSaveFileName(
                self,
                "Export results as CSV",
                # self.project_folder,
                filter="CSV files (*.csv)",
                options=options,
            )

            if file:
                self.t.save_csv(file, overwrite=True)
                self.status_bar.showMessage(f"Table exported to {file}")
        else:
            self.status_bar.showMessage("No table to export")

    @pyqtSlot(str)
    def update_terminal_output(self, text):
        cursor = self.terminal_output.textCursor()
        cursor.movePosition(cursor.End)
        if "\r" in text:
            cursor.select(cursor.LineUnderCursor)
            cursor.removeSelectedText()
            cursor.deletePreviousChar()
        cursor.insertText(text)
        self.terminal_output.setTextCursor(cursor)
        self.terminal_output.ensureCursorVisible()

    def print_to_GUI_terminal(self, text):
        self.redirector.write(text + "\n")

    def enable_usable_buttons(self):
        if self.t is not None:
            self.postprocess_button.setEnabled(True)
            self.inspect_table_button.setEnabled(True)
            self.save_results_button.setEnabled(True)
            self.export_table_button.setEnabled(True)

            if "normalized_area_chromatogram" in self.t.col_names:
                self.run_calibration_button.setEnabled(True)
        else:
            self.run_peak_extraction_button.setEnabled(True)

        if self.t_cal is not None:
            self.inspect_calibration_button.setEnabled(True)
            self.run_quantification_button.setEnabled(True)

    def disable_all_buttons(self):
        self.run_peak_extraction_button.setEnabled(False)
        self.postprocess_button.setEnabled(False)
        self.run_calibration_button.setEnabled(False)
        self.inspect_calibration_button.setEnabled(False)
        self.run_quantification_button.setEnabled(False)
        self.inspect_table_button.setEnabled(False)
        self.save_results_button.setEnabled(False)
        self.export_table_button.setEnabled(False)


class OutputRedirector(QObject):
    outputWritten = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.buffer = ""

    def write(self, text):
        self.buffer += text
        if "\r" in text or "\n" in text:
            self.flush()

    def flush(self):
        self.outputWritten.emit(self.buffer)
        self.buffer = ""


class WorkerThread(QThread):
    def __init__(self, function_to_run, redirector, parent, args=None):
        super().__init__()
        self.function_to_run = function_to_run
        self.redirector = redirector
        self.args = args
        self.error = None
        self.func_return = None
        self.parent = parent

    def run(self):
        self.parent.update_busy_indicator(True)
        self.parent.disable_all_buttons()

        # Redirect output
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = self.redirector
        sys.stderr = self.redirector

        try:
            self.func_return = self.function_to_run(*self.args)
        except Exception as e:
            self.error = e
        finally:
            # Redirect output back
            sys.stdout = old_stdout
            sys.stderr = old_stderr

            self.parent.update_busy_indicator(False)
