from ..stability import correct_drift


def correct_gps_drift(gps_error):
    """Apply a drift correction based on GPS error estimates."""
    return correct_drift(gps_error)
