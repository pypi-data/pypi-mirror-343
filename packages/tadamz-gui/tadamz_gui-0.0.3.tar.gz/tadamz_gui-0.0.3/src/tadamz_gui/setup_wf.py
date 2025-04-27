import os
from glob import glob

import emzed
import guidata.dataset.dataitems as di
import guidata.dataset.datatypes as dt
import tadamz
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget

import tadamz_gui.gui_functions as gui_functions
from tadamz_gui.processing_steps import add_processing_steps_ExCalIntStd
from tadamz_gui.run_wf import RunWorkflowWindow


class SetupWFWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Select workflow type to setup")

        button_setup_ExCalIntStd = QPushButton(
            "External calibration with internal standard"
        )

        button_setup_ExCalIntStd.clicked.connect(self.show_ExCalIntStd_window)

        layout = QVBoxLayout()
        layout.addWidget(button_setup_ExCalIntStd)
        self.setLayout(layout)

    def show_ExCalIntStd_window(self, checked):
        wf_dataset = SetupWFExCalIntStd()

        if wf_dataset.edit(size=(600, 600)):
            config = gui_functions.create_config_dict(wf_dataset)

            config = add_processing_steps_ExCalIntStd(config)

            peak_table = tadamz.in_out.load_peaks_table(
                wf_dataset.config__input__target_table_path
            )
            sample_table = emzed.io.load_excel(
                wf_dataset.config__input__sample_table_path
            )
            calibration_table = emzed.io.load_excel(
                wf_dataset.config__input__calibration_table_path
            )

            samples = glob(
                os.path.join(
                    wf_dataset.config__input__sample_folder__path,
                    "*" + wf_dataset.config__input__sample_folder__extension,
                )
            )

            # run workflow
            self.run_window = RunWorkflowWindow(
                peak_table,
                samples,
                config,
                sample_table,
                calibration_table,
                # wf_dataset.project_folder,
            )
            self.run_window.show()


class SetupWFExCalIntStd(dt.DataSet):
    """Setup workflow"""

    # Tab group
    _btg_main_tab = dt.BeginTabGroup("Main settings")

    _bg_input = dt.BeginGroup("Input")

    # Group: Project settings
    # _bg_project = dt.BeginGroup("Project settings")
    # project_folder = di.DirectoryItem(
    #     "Project folder",
    #     default="/Users/jethro/Coding/targeted_wf_gui/test_data/example",
    # )
    # _eg_project = dt.EndGroup("Project settings")

    # Group: Input tables
    _bg_input_tables = dt.BeginGroup("Input tables")
    config__input__target_table_path = di.FileOpenItem(
        "Target table (.xlsx)",
        formats="xlsx",
    )
    config__input__sample_table_path = di.FileOpenItem(
        "Sample table (.xlsx)",
        formats="xlsx",
    )
    config__input__calibration_table_path = di.FileOpenItem(
        "Calibration table (.xlsx)",
        formats="xlsx",
    )
    _eg_input_tables = dt.EndGroup("Input tables")

    # Group: Samples
    _bg_samples = dt.BeginGroup("Samples")
    config__input__sample_folder__path = di.DirectoryItem(
        "Sample folder",
    )
    config__input__sample_folder__extension = di.StringItem(
        "Sample extension",
        notempty=True,
        default=".mzML",
        help="Extension must include the . and is case-sensitive on Unix",
    )
    # sample_folder_ignore_blanks = di.BoolItem("Ignore blanks", default=True)
    _eg_samples = dt.EndGroup("Samples")

    _eg_input = dt.EndGroup("Input")

    # Group: Peak extraction
    _bg_extr = dt.BeginGroup("Peak extraction")
    config__extract_peaks__ms_data_type = di.ChoiceItem(
        "MS data type",
        [("Spectra", "Spectra"), ("MS_Chromatogram", "Chromatogram only")],
        default="MS_Chromatogram",
    )
    config__extract_peaks__integration_algorithm = di.ChoiceItem(
        "Integration algorithm",
        [
            ("linear", "Linear"),
            ("emg", "EMG"),
            ("sgolay", "Savitzky-Golay"),
            ("asym_gauss", "Asym. Gauss"),
            ("no_integration", "No integration"),
        ],
        default="emg",
    )
    config__extract_peaks__mz_tol_abs = di.FloatItem(
        "Absolute m/z tolerance", default=0.3, unit="Th"
    )
    config__extract_peaks__mz_tol_rel = di.FloatItem(
        "Relative m/z tolerance", default=0, unit="ppm"
    )
    config__extract_peaks__precursor_mz_tol = di.FloatItem(
        "Precursor absolute m/z tolerance",
        default=0.3,
        unit="Th",
        help="Only required for MS2 / MRM",
    )
    config__extract_peaks__subtract_baseline = di.BoolItem(
        "Subtract baseline", default=False
    )
    # config__extract_peaks__chromatogram_boundary_factor = di.FloatItem(
    #    "Chromatogram boundary factor", default=3
    # )
    _eg_extr = dt.EndGroup("Peak extraction")

    # Group: Peak classification
    _bg_classifier = dt.BeginGroup("Peak classification")
    config__classify_peaks__scoring_model = di.StringItem(
        "Scoring model", default="random_forest_classification", notempty=True
    )
    config__classify_peaks__scoring_model_params__classifier_name = di.StringItem(
        "Classifier name", default="srm_peak_classifier", notempty=True
    )
    _eg_classifier = dt.EndGroup("Peak classification")

    # Group: Co-elution
    _bg_coelution = dt.BeginGroup("Co-elution analysis")
    config__coeluting_peaks__only_use_ref_peaks = di.BoolItem(
        "Only use reference peaks",
        default=True,
        help="If set to true, only target(s) flagged with is_coelution_ref_peak will be used to check for co-elution. If set to false, all peaks of the compound will be used.",
    )
    _eg_coelution = dt.EndGroup("Co-elution analysis")

    # Group: Calibrate
    _bg_calibrate = dt.BeginGroup("Calibration")
    config__calibrate__calibration_model_name = di.StringItem(
        "Calibration model", default="linear"
    )
    config__calibrate__alpha_model = di.FloatItem("Alpha value for model", default=0.05)
    config__calibrate__alpha_lodq = di.FloatItem(
        "Alpha value for LODQ", default=0.00135
    )
    config__calibrate__evaluate_model = di.BoolItem("Evaluate model", default=False)
    config__calibrate__calibration_weight = di.ChoiceItem(
        "Weight type",
        [("none", "none"), ("1/x", "1/x"), ("1/x^2", "1/x^2"), ("1/s^2", "1/s^2")],
        default="1/x^2",
    )
    # Subgroup: sample types
    _bg_sample_types = dt.BeginGroup("Sample types")
    config__calibrate__sample_types__sample = di.StringItem("Sample", default="Unknown")
    config__calibrate__sample_types__standard = di.StringItem(
        "Standard", default="Standard"
    )
    config__calibrate__sample_types__blank = di.StringItem("Blank", default="Blank")
    config__calibrate__sample_types__qc = di.StringItem("QC", default="Control")
    _eg_sample_types = dt.EndGroup("Sample types")

    _eg_calibrate = dt.EndGroup("Calibration")

    _etg_main_tab = dt.EndTabGroup("Main settings")

    # buttons below
    button_load_config = di.ButtonItem(
        "Load existing parameters", callback=gui_functions.load_parameters
    )
    button_save_config = di.ButtonItem(
        "Save parameters", callback=gui_functions.save_parameters
    )
