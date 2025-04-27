import guidata
import yaml
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from tadamz_gui.processing_steps import add_processing_steps_ExCalIntStd


def create_config_dict(dataset):
    separator = "__"
    prefix = "config"

    attribute_names = [a for a in dir(dataset) if a.startswith(prefix + separator)]

    result = {}
    for atr in attribute_names:
        value = getattr(dataset, atr)
        parts = atr.split(separator)
        current = result
        for part in parts[1:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
    return result


def save_parameters(dataset, item, value, parent):
    config_path = QFileDialog.getSaveFileName(
        parent, "Save parameters", "", "Workflow config (*.yaml)"
    )[0]

    if config_path != "":
        config = create_config_dict(dataset)

        # add processing steps as well
        config = add_processing_steps_ExCalIntStd(config)

        with open(config_path, "w+") as ff:
            yaml.dump(config, ff)

        QMessageBox(
            QMessageBox.Information,
            "Parameters saved",
            f"Parameters saved as: {config_path}",
        ).exec_()


def load_parameters(dataset, item, value, parent):
    config_path = QFileDialog.getOpenFileName(
        parent, "Load existing parameters", "", "Workflow parameters (*.yaml)"
    )[0]

    if config_path != "":
        try:
            with open(config_path) as ff:
                config_dict = yaml.safe_load(ff)

            attribute_dict = flatten_config(config_dict)
            guidata.utils.update_dataset(dest=dataset, source=attribute_dict)
        except Exception as e:
            QMessageBox(
                QMessageBox.Critical,
                "Error",
                f"Error loading parameters from: {config_path}\n{e}",
            ).exec_()


def flatten_config(config_dict, prefix="config"):
    separator = "__"

    result = {}
    for key, value in config_dict.items():
        new_key = f"{prefix}{separator}{key}"
        if isinstance(value, dict):
            result.update(flatten_config(value, new_key))
        else:
            result[new_key] = value
    return result
