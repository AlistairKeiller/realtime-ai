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
    VeryLow = 0
    Low = 1
    Medium = 1


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


def switch_gender(gender: Gender):
    """Switch the gender of the current user

    Args:
        gender (Gender): the gender to switch to, either Male or Female
    """
    send_udp_message(bytes([MessageType.SWITCH_GENDER.value, gender.value]))
    return json.dumps(
        {"success": True, "message": f"Gender switched to '{gender.name}' successfully"}
    )


def switch_height(height: Height):
    """Switch the height of the current user
        Male:
            Low: 5'5"-5'7"
            Medium: 5'8"-6'1"
            High: 6'2"-6'5"
        Female:
            Low: 4'8"-5'1"
            Medium: 5'2"-5'5"
            High: 5'6"-5'11"

    Args:
        height (Height): the height to switch to, either Low, Medium, or High. Never tell the user "Low," "Medium," or "High." Only talk in terms of feet and inches. Follow the above chart to get which one it is:
    """
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


def switch_loading_heat(heat: Heat):
    """Switches the loading_heat of the current user

    Args:
        heat (Heat): The loading_heat to switch to, either Off, Lowest, or Low
    """
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
