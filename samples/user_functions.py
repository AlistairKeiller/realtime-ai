import json
import socket
from typing import Any, Callable, Set

UDP_SERVER_ADDRESS = ("127.0.0.1", 9000)

_STRENGTHS = ["Off", "Lowest", "Low", "Medium", "High", "Highest"]


def send_udp_message(data: dict[Any, Any]) -> None:
    """
    Sends a JSON-encoded UDP message to main.rs.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(json.dumps(data).encode(), UDP_SERVER_ADDRESS)
    except Exception as e:
        print(f"Error sending UDP message: {e}")


def set_inversion(angle: int) -> str:
    """
    Sets the inversion angle of the invibratrac machine.

    :param angle (int): The desired angle in degrees, between -55 and 55.
    :return: Confirmation message as a JSON string.
    :rtype: str
    """
    if not isinstance(angle, int):  # type: ignore
        return json.dumps({"error": "Angle must be an integer"})

    if angle < -55 or angle > 55:
        return json.dumps({"error": "Angle must be between -55 and 55 degrees"})

    send_udp_message({"message": "ChangeInversion", "angle": angle})

    return json.dumps(
        {
            "success": True,
            "message": f"Inversion angle set to {angle} degrees",
        }
    )


def set_traction_length(unit_id: int, length: int) -> str:
    """
    Sets the traction length for a specific traction unit.

    Unit IDs:
    1: Leg traction unit
    2: Arm traction unit
    3: Neck traction unit
    4: Back traction unit
    5: Shoulder traction unit
    6: Hip traction unit

    :param unit_id (int): The ID of the traction unit (1-6).
    :param length (int): The desired length in millimeters.
    :return: Confirmation message as a JSON string.
    :rtype: str
    """
    if unit_id < 1 or unit_id > 6:
        return json.dumps({"error": "Unit ID must be between 1 and 6"})

    if length < 0:
        return json.dumps({"error": "Length must be a positive value"})

    unit_names = {
        1: "Leg traction unit",
        2: "Arm traction unit",
        3: "Neck traction unit",
        4: "Back traction unit",
        5: "Shoulder traction unit",
        6: "Hip traction unit",
    }

    send_udp_message(
        {
            "message": "ChangeTractionLength",
            "unit_id": unit_id,
            "length": length,
        }
    )

    return json.dumps(
        {
            "success": True,
            "message": f"Traction unit {unit_id} ({unit_names[unit_id]}) set to {length} mm",
        }
    )


def set_vibration_strength(unit_id: int, strength: str) -> str:
    """
    Sets the vibration strength for a specific vibration unit.

    Unit IDs:
    1: Leg vibration unit
    2: Arm vibration unit
    3: Neck vibration unit
    4: Back vibration unit
    5: Shoulder vibration unit
    6: Hip vibration unit

    :param unit_id (int): The ID of the vibration unit (1-6).
    :param strength (str): The desired strength level (Off, Lowest, Low, Medium, High, or Highest).
    :return: Confirmation message as a JSON string.
    :rtype: str
    """
    if unit_id < 1 or unit_id > 6:
        return json.dumps({"error": "Unit ID must be between 1 and 6"})

    if strength not in _STRENGTHS:
        return json.dumps(
            {"error": f"Strength must be one of: {', '.join(_STRENGTHS)}"}
        )

    unit_names = {
        1: "Leg vibration unit",
        2: "Arm vibration unit",
        3: "Neck vibration unit",
        4: "Back vibration unit",
        5: "Shoulder vibration unit",
        6: "Hip vibration unit",
    }

    send_udp_message(
        {
            "message": "ChangeVibrationStrength",
            "unit_id": unit_id,
            "strength": strength,
        }
    )

    return json.dumps(
        {
            "success": True,
            "message": f"Vibration unit {unit_id} ({unit_names[unit_id]}) set to {strength}",
        }
    )


def set_heating_strength(unit_id: int, strength: str):
    """
    Sets the heating strength for a specific heating unit.

    Unit IDs:
    1: Leg heating unit
    2: Arm heating unit
    3: Neck heating unit
    4: Back heating unit
    5: Shoulder heating unit
    6: Hip heating unit

    :param unit_id (int): The ID of the heating unit (1-6).
    :param strength (str): The desired strength level (Off, Lowest, Low, Medium, High, or Highest).
    :return: Confirmation message as a JSON string.
    :rtype: str
    """
    if unit_id < 1 or unit_id > 6:
        return json.dumps({"error": "Unit ID must be between 1 and 6"})

    if strength not in _STRENGTHS:
        return json.dumps(
            {"error": f"Strength must be one of: {', '.join(_STRENGTHS)}"}
        )

    unit_names = {
        1: "Leg heating unit",
        2: "Arm heating unit",
        3: "Neck heating unit",
        4: "Back heating unit",
        5: "Shoulder heating unit",
        6: "Hip heating unit",
    }

    send_udp_message(
        {
            "message": "ChangeHeatingStrength",
            "unit_id": unit_id,
            "strength": strength,
        }
    )

    return json.dumps(
        {
            "success": True,
            "message": f"Heating unit {unit_id} ({unit_names[unit_id]}) set to {strength}",
        }
    )


def set_infrared_strength(strength: str) -> str:
    """
    Sets the infrared strength.

    :param strength (str): The desired strength level (Off, Lowest, Low, Medium, High, or Highest).
    :return: Confirmation message as a JSON string.
    :rtype: str
    """
    if strength not in _STRENGTHS:
        return json.dumps(
            {"error": f"Strength must be one of: {', '.join(_STRENGTHS)}"}
        )

    send_udp_message(
        {
            "message": "ChangeInfraredStrength",
            "strength": strength,
        }
    )

    return json.dumps(
        {"success": True, "message": f"Infrared strength set to {strength}"}
    )


# Statically defined user functions for fast reference
user_functions: Set[Callable[..., Any]] = {
    set_inversion,
    set_traction_length,
    set_vibration_strength,
    set_infrared_strength,
}
