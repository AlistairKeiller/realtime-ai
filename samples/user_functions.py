import json
import socket
from typing import Any, Callable, Set
from enum import Enum

UDP_SERVER_ADDRESS = ("127.0.0.1", 9000)


class MessageType(Enum):
    NEXT = 0
    PREVIOUS = 1
    SELECT_USER_GUEST = 2
    SELECT_USER = 3
    ADD_USER = 4
    SWITCH_NAME = 5
    SWITCH_GENDER = 6
    SWITCH_HEIGHT = 7
    SWITCH_LOADING_ANGLE = 8
    SWITCH_LOADING_HEAT = 9
    SWITCH_TRACTION_ADJUST = 10
    DELETE_USER = 11
    SELECT_MODE = 12


class Gender(Enum):
    Male = 0
    Female = 1


class Heat(Enum):
    Off = 0
    VeryLow = 1
    Low = 1


class Height(Enum):
    Low = 0
    Medium = 1
    High = 2


def send_udp_message(data: bytes) -> None:
    """
    Sends a byte-encoded UDP message to main.rs.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(data, UDP_SERVER_ADDRESS)
    except Exception as e:
        print(f"Error sending UDP message: {e}")


def next():
    """Moves to the next screen"""

    send_udp_message(bytes([MessageType.NEXT.value]))
    return json.dumps(
        {"success": True, "message": "Moved to the next screen successfully"}
    )


def previous():
    """Moves to the previous screen"""
    send_udp_message(bytes([MessageType.PREVIOUS.value]))
    return json.dumps(
        {"success": True, "message": "Moved to the previous screen successfully"}
    )


def select_user_guest():
    """Sets the current user to be the guest user"""
    send_udp_message(bytes([MessageType.SELECT_USER_GUEST.value]))
    return json.dumps({"success": True, "message": "Guest user selected successfully"})


def select_user(name: str):
    """Sets the current user based on name

    Args:
        name (str): the name of the user to select
    """
    send_udp_message(bytes([MessageType.SELECT_USER.value]) + name.encode("utf-8"))
    return json.dumps(
        {"success": True, "message": f"User '{name}' selected successfully"}
    )


def add_user():
    """Adds a new empty user"""
    send_udp_message(bytes([MessageType.ADD_USER.value]))
    return json.dumps({"success": True, "message": "New user added successfully"})


def switch_name(name: str):
    """Switch the name of the current user to the selected name

    Args:
        name (str): the name to switch to
    """
    send_udp_message(bytes([MessageType.SWITCH_NAME.value]) + name.encode("utf-8"))
    return json.dumps(
        {"success": True, "message": f"Name switched to '{name}' successfully"}
    )


def switch_gender(gender_str: str):
    """Switch the gender of the current user

    Args:
        gender_str (str): the gender to switch to, either Male or Female
    """
    match gender_str.lower():
        case "male":
            gender = Gender.Male
        case "female":
            gender = Gender.Female
        case _:
            return json.dumps(
                {
                    "success": False,
                    "message": f"Invalid gender f{gender_str}, please use Male or Female",
                }
            )
    send_udp_message(bytes([MessageType.SWITCH_GENDER.value, gender.value]))
    return json.dumps(
        {
            "success": True,
            "message": f"Gender switched to '{gender.name}' successfully",
        }
    )


def switch_height(height_str: str, gender_str: str):
    """Switch the height of the current user

    Args:
        height_str (Height): the height to switch to, in the format feet'inches".
    """
    try:
        feet, inches = map(int, height_str[:3].split("'"))
    except (ValueError, IndexError):
        return json.dumps(
            {
                "success": False,
                "message": f"Invalid height format '{height_str}', please use the format feet'inches\"",
            }
        )

    if gender_str.lower() == "male":
        if feet == 5 and 5 <= inches <= 7:
            height = Height.Low
        elif feet == 5 and 8 <= inches <= 11 or feet == 6 and 0 <= inches <= 1:
            height = Height.Medium
        elif feet == 6 and 2 <= inches <= 5:
            height = Height.High
        else:
            return json.dumps(
                {
                    "success": False,
                    "message": f"Invalid height '{height_str}', please use a height between 5'5\" and 6'5\"",
                }
            )
    elif gender_str.lower() == "female":
        if feet == 4 and 8 <= inches <= 11 or feet == 5 and 0 <= inches <= 1:
            height = Height.Low
        elif feet == 5 and 2 <= inches <= 5:
            height = Height.Medium
        elif feet == 5 and 6 <= inches <= 11:
            height = Height.High
        else:
            return json.dumps(
                {
                    "success": False,
                    "message": f"Invalid height '{height_str}', please use a height between 4'8\" and 5'11\"",
                }
            )
    else:
        return json.dumps(
            {
                "success": False,
                "message": f"Invalid gender '{gender_str}', please use Male or Female",
            }
        )

    send_udp_message(bytes([MessageType.SWITCH_HEIGHT.value, height.value]))
    return json.dumps(
        {"success": True, "message": f"Height switched to '{height.name}' successfully"}
    )


def switch_loading_angle(angle: int):
    """Switches the loading_angle of the current user

    Args:
        angle (int): The loading_angle to switch to
    """
    send_udp_message(bytes([MessageType.SWITCH_LOADING_ANGLE.value, angle]))
    return json.dumps(
        {"success": True, "message": f"Loading angle switched to {angle} successfully"}
    )


def switch_loading_heat(heat_str: str):
    """Switches the loading_heat of the current user

    Args:
        heat_str (str): The loading_heat to switch to, either Off, VeryLow, or Low
    """
    match heat_str.lower():
        case "off":
            heat = Heat.Off
        case "verylow":
            heat = Heat.VeryLow
        case "low":
            heat = Heat.Low
        case _:
            return json.dumps(
                {
                    "success": False,
                    "message": f"Invalid heat '{heat_str}', please use VeryLow, Low, or Medium",
                }
            )
    send_udp_message(bytes([MessageType.SWITCH_LOADING_HEAT.value, heat.value]))
    return json.dumps(
        {
            "success": True,
            "message": f"Loading heat switched to '{heat.name}' successfully",
        }
    )


def switch_traction_adjust(index: int, value: int):
    """Switches the traction_adjust of the current user

    Args:
        index (int): The index of the traction unit to adjust
        value (int): The value in mm to adjust the traciton unit to
    """
    send_udp_message(bytes([MessageType.SWITCH_TRACTION_ADJUST.value, index, value]))
    return json.dumps(
        {
            "success": True,
            "message": f"Traction adjusted at index {index} to value {value} successfully",
        }
    )


def delete_user():
    """Deletes the current user"""
    send_udp_message(bytes([MessageType.DELETE_USER.value]))
    return json.dumps({"success": True, "message": "User deleted successfully"})


def select_mode(mode: str):
    """Selects a dynamic mode

    Args:
        mode (str): The name of the mode to switch to. Will be Inversion, Percussion, Traction, Heat, or Infrared.
    """
    send_udp_message(bytes([MessageType.SELECT_MODE.value]) + mode.encode("utf-8"))
    return json.dumps(
        {"success": True, "message": f"Mode '{mode}' selected successfully"}
    )


user_functions: Set[Callable[..., Any]] = {
    next,
    previous,
    select_user,
    select_user_guest,
    add_user,
    switch_name,
    switch_gender,
    switch_height,
    switch_loading_angle,
    switch_loading_heat,
    switch_traction_adjust,
    delete_user,
    select_mode,
}
