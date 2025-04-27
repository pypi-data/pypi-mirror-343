def add_processing_steps_ExCalIntStd(config):
    config["processing_steps"] = [
        "extract_peaks",
        "classify_peaks",
        "coeluting_peaks",
    ]
    config["postprocessings"] = ["postprocessing1", "quantification"]
    config["postprocessing1"] = [
        "classify_peaks",
        "coeluting_peaks",
        "normalize_peaks",
    ]
    config["quantification"] = ["quantify"]

    return config
