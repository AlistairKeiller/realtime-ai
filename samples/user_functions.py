import json
from typing import Callable, Any, Set


# These are the user-defined functions that can be called by the agent.


# def fetch_current_datetime() -> str:
#     """
#     Get the current time as a JSON string.

#     :return: The current time in JSON format.
#     :rtype: str
#     """
#     current_time = datetime.datetime.now()
#     time_json = json.dumps({"current_time": current_time.strftime("%Y-%m-%d %H:%M:%S")})
#     return time_json


# def fetch_weather(location: str) -> str:
#     """
#     Fetches the weather information for the specified location.

#     :param location (str): The location to fetch weather for.
#     :return: Weather information as a JSON string.
#     :rtype: str
#     """
#     # In a real-world scenario, you'd integrate with a weather API.
#     # Here, we'll mock the response.
#     mock_weather_data = {
#         "New York": "Sunny, 25°C",
#         "London": "Cloudy, 18°C",
#         "Tokyo": "Rainy, 22°C",
#     }
#     weather = mock_weather_data.get(
#         location, "Weather data not available for this location."
#     )
#     weather_json = json.dumps({"weather": weather})
#     return weather_json


# def send_email(recipient: str, subject: str, body: str) -> str:
#     """
#     Sends an email with the specified subject and body to the recipient.

#     :param recipient (str): Email address of the recipient.
#     :param subject (str): Subject of the email.
#     :param body (str): Body content of the email.
#     :return: Confirmation message.
#     :rtype: str
#     """
#     # In a real-world scenario, you'd use an SMTP server or an email service API.
#     # Here, we'll mock the email sending.
#     print(f"Sending email to {recipient}...")
#     print(f"Subject: {subject}")
#     print(f"Body:\n{body}")

#     message_json = json.dumps({"message": f"Email successfully sent to {recipient}."})
#     return message_json


# def _generate_chat_completion(ai_client, model, messages):
#     print(f"generate_chat_completion, messages: {messages}")
#     print(f"generate_chat_completion, model: {model}")

#     try:
#         # Generate the chat completion
#         response = ai_client.chat.completions.create(model=model, messages=messages)
#         print(f"generate_chat_completion, response: {response}")

#         # Extract the content of the first choice
#         if response.choices and response.choices[0].message:
#             message_content = response.choices[0].message.content
#         else:
#             message_content = "No response"

#         return json.dumps({"result": message_content})
#     except Exception as e:
#         error_message = f"Failed to generate chat completion: {str(e)}"
#         print(error_message)
#         return json.dumps({"function_error": error_message})


# def _screenshot_to_bytes() -> bytes:
#     """
#     Captures a screenshot and returns it as binary data.

#     :return: The screenshot as binary data.
#     :rtype: bytes
#     """
#     from PIL import Image
#     import mss

#     with mss.mss() as sct:
#         monitor = sct.monitors[
#             0
#         ]  # 0 is the first monitor; adjust if multiple monitors are used
#         screenshot = sct.grab(monitor)
#         img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")

#     # Convert the image to binary data
#     img_byte_arr = io.BytesIO()
#     img.save(img_byte_arr, format="PNG")
#     img_byte_arr.seek(0)
#     img_bytes = img_byte_arr.read()
#     return img_bytes


# def _analyze_image(
#     img_base64: str, system_input: str, user_input: str, filename: str
# ) -> str:
#     """
#     Analyzes the given image and returns the analysis result.

#     :param img_base64 (str): Base64 encoded image data.
#     :param system_input (str): System input for the analysis.
#     :param user_input (str): User input for the analysis.
#     :return: The analysis result.
#     :rtype: str
#     """

#     try:
#         openai_client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
#     except Exception as e:
#         print(f"Error initializing OpenAI client: {e}")
#         return None

#     messages = [
#         {
#             "role": "system",
#             "content": [{"type": "text", "text": system_input}],
#             "role": "user",
#             "content": [
#                 {"type": "text", "text": user_input},
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": f"data:image/png;base64,{img_base64}",
#                         "detail": "high",
#                     },
#                 },
#             ],
#         }
#     ]

#     try:
#         response = openai_client.chat.completions.create(
#             model="gpt-4o", messages=messages, temperature=0.5, max_tokens=2000
#         )

#         # Extract the analysis result from the response
#         analysis = response.choices[0].message.content
#         print(f"User input: {user_input}")
#         print(f"Analysis: {analysis}")

#         # Create user message using the user input and the analysis result
#         # user_message = f"User input: {user_input}\nAnalysis: {analysis}"
#         # o1_messages = [{"role": "user", "content": user_message}]
#         # o1_response = _generate_chat_completion(openai_client, "o1-mini", o1_messages)
#         # print(f"O1 response: {o1_response}")

#         # Show the analysis result in code
#         with open(filename, "w") as f:
#             f.write(analysis)
#         os.system(f"code {filename}")

#         return json.dumps({"analysis": analysis})

#     except Exception as e:
#         error_message = f"An error occurred: {e}"
#         print(error_message)
#         return json.dumps({"function_error": error_message})


# def review_highlighted_code() -> str:
#     """
#     Captures a screenshot, sends it to the specified OpenAI model for analysis,
#     and returns the analysis result.

#     :return: The analysis result as a JSON string.
#     :rtype: str
#     """
#     # Capture a screenshot and convert it to base64
#     img_bytes = _screenshot_to_bytes()
#     img_base64 = base64.b64encode(img_bytes).decode("utf-8")
#     return _analyze_image(
#         img_base64=img_base64,
#         system_input="You are expert in analyzing images to text. If the image contains highlighted part, focus on that.",
#         user_input="Review the highlighted code and provide detailed feedback.",
#         filename="highlighted_code_analysis.md",
#     )


# def translate_highlighted_text(language: str) -> str:
#     """
#     Captures a screenshot, sends it to the specified OpenAI model for analysis,
#     and returns the analysis result.

#     :return: The analysis result as a JSON string.
#     :rtype: str
#     """
#     # Capture a screenshot and convert it to base64
#     img_bytes = _screenshot_to_bytes()
#     img_base64 = base64.b64encode(img_bytes).decode("utf-8")
#     return _analyze_image(
#         img_base64=img_base64,
#         system_input=f"You are expert in translating text to different languages.",
#         user_input=f"Translate the highlighted text to {language}.",
#         filename="highlighted_text_translation.md",
#     )


# def explain_highlighted_text() -> str:
#     """
#     Captures a screenshot, sends it to the specified OpenAI model for analysis,
#     and returns the analysis result.

#     :return: The analysis result as a JSON string.
#     :rtype: str
#     """
#     # Capture a screenshot and convert it to base64
#     img_bytes = _screenshot_to_bytes()
#     img_base64 = base64.b64encode(img_bytes).decode("utf-8")
#     return _analyze_image(
#         img_base64=img_base64,
#         system_input="You are expert in explaining text. If the image contains highlighted text, provide the explanation of that.",
#         user_input="Explain the highlighted text in detail, in understandable language.",
#         filename="highlighted_text_explanation.md",
#     )


# def take_screenshot_and_analyze(user_input: str) -> str:
#     """
#     Captures a screenshot, sends it to the specified OpenAI model for analysis,
#     and returns the analysis result.

#     :param user_input (str): User input request as it was given by user for screenshot analysis and actions.

#     :return: The analysis result as a JSON string.
#     :rtype: str
#     """
#     # Capture a screenshot and convert it to base64
#     img_bytes = _screenshot_to_bytes()
#     img_base64 = base64.b64encode(img_bytes).decode("utf-8")
#     return _analyze_image(
#         img_base64=img_base64,
#         system_input="Analyze the screenshot and provide all details from it. If the image contains e.g. code or highlighted parts, provide the exact analysis of that.",
#         user_input=user_input,
#         filename="screenshot_analysis.md",
#     )


# def take_screenshot_and_show() -> str:
#     """
#     Captures a screenshot and displays it to the user.

#     :return: The path to the saved screenshot.
#     :rtype: str
#     """
#     from PIL import Image
#     import mss

#     print("Capturing screenshot...")
#     with mss.mss() as sct:
#         monitor = sct.monitors[
#             0
#         ]  # 0 is the first monitor; adjust if multiple monitors are used
#         screenshot = sct.grab(monitor)
#         img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")

#     # open the saved image in the default image viewer
#     img.show()

#     return json.dumps({"result": "Screenshot captured and displayed."})


_inversion_angle = 0

_traction_units = {i: 0 for i in range(1, 7)}

_vibration_units = {i: "Off" for i in range(1, 7)}

_infrared_strength = "Off"
_VIBRATION_LEVELS = ["Off", "Lowest", "Low", "Medium", "High", "Highest"]


def set_inversion(angle: int) -> str:
    """
    Sets the inversion angle of the invibratrac machine.

    :param angle (int): The desired angle in degrees, between -55 and 55.
    :return: Confirmation message as a JSON string.
    :rtype: str
    """
    global _inversion_angle

    # Validate the input angle
    if not isinstance(angle, int):  # type: ignore
        return json.dumps({"error": "Angle must be an integer"})

    # Ensure the angle is within the valid range
    if angle < -55 or angle > 55:
        return json.dumps({"error": "Angle must be between -55 and 55 degrees"})

    # Set the inversion angle
    _inversion_angle = angle

    return json.dumps(
        {
            "success": True,
            "message": f"Inversion angle set to {_inversion_angle} degrees",
        }
    )


def get_inversion() -> str:
    """
    Gets the current inversion angle of the invibratrac machine.

    :return: Current inversion angle as a JSON string.
    :rtype: str
    """
    global _inversion_angle

    return json.dumps({"angle": _inversion_angle, "units": "degrees"})


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
    global _traction_units

    # Validate unit_id
    if unit_id < 1 or unit_id > 6:
        return json.dumps({"error": "Unit ID must be between 1 and 6"})

    # Validate length
    if not isinstance(length, int):
        return json.dumps({"error": "Length must be an integer"})

    if length < 0:
        return json.dumps({"error": "Length must be a positive value"})

    # Get unit name
    unit_names = {
        1: "Leg traction unit",
        2: "Arm traction unit",
        3: "Neck traction unit",
        4: "Back traction unit",
        5: "Shoulder traction unit",
        6: "Hip traction unit",
    }

    # Update the traction unit settings
    _traction_units[unit_id] = length

    return json.dumps(
        {
            "success": True,
            "message": f"Traction unit {unit_id} ({unit_names[unit_id]}) set to {length} mm",
        }
    )


def get_traction_settings() -> str:
    """
    Gets the current settings for all traction units.

    Unit IDs:
    1: Leg traction unit
    2: Arm traction unit
    3: Neck traction unit
    4: Back traction unit
    5: Shoulder traction unit
    6: Hip traction unit

    :return: Current traction settings as a JSON string.
    :rtype: str
    """
    global _traction_units

    # Add names for display purposes
    unit_names = {
        1: "Leg traction unit",
        2: "Arm traction unit",
        3: "Neck traction unit",
        4: "Back traction unit",
        5: "Shoulder traction unit",
        6: "Hip traction unit",
    }

    result = {
        id: {"name": unit_names[id], "length": length}
        for id, length in _traction_units.items()
    }

    return json.dumps({"traction_units": result})


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
    global _vibration_units, _VIBRATION_LEVELS

    # Validate unit_id
    if unit_id < 1 or unit_id > 6:
        return json.dumps({"error": "Unit ID must be between 1 and 6"})

    # Validate strength
    if strength not in _VIBRATION_LEVELS:
        return json.dumps(
            {"error": f"Strength must be one of: {', '.join(_VIBRATION_LEVELS)}"}
        )

    # Get unit name
    unit_names = {
        1: "Leg vibration unit",
        2: "Arm vibration unit",
        3: "Neck vibration unit",
        4: "Back vibration unit",
        5: "Shoulder vibration unit",
        6: "Hip vibration unit",
    }

    # Update the vibration unit settings
    _vibration_units[unit_id] = strength

    return json.dumps(
        {
            "success": True,
            "message": f"Vibration unit {unit_id} ({unit_names[unit_id]}) set to {strength}",
        }
    )


def get_vibration_settings() -> str:
    """
    Gets the current settings for all vibration units.

    Unit IDs:
    1: Leg vibration unit
    2: Arm vibration unit
    3: Neck vibration unit
    4: Back vibration unit
    5: Shoulder vibration unit
    6: Hip vibration unit

    :return: Current vibration settings as a JSON string.
    :rtype: str
    """
    global _vibration_units

    # Add names for display purposes
    unit_names = {
        1: "Leg vibration unit",
        2: "Arm vibration unit",
        3: "Neck vibration unit",
        4: "Back vibration unit",
        5: "Shoulder vibration unit",
        6: "Hip vibration unit",
    }

    result = {
        id: {"name": unit_names[id], "strength": strength}
        for id, strength in _vibration_units.items()
    }

    return json.dumps({"vibration_units": result})


def set_infrared_strength(strength: str) -> str:
    """
    Sets the infrared strength.

    :param strength (str): The desired strength level (Off, Lowest, Low, Medium, High, or Highest).
    :return: Confirmation message as a JSON string.
    :rtype: str
    """
    global _infrared_strength, _VIBRATION_LEVELS

    # Validate strength
    if strength not in _VIBRATION_LEVELS:
        return json.dumps(
            {"error": f"Strength must be one of: {', '.join(_VIBRATION_LEVELS)}"}
        )

    # Update the infrared strength
    _infrared_strength = strength

    return json.dumps(
        {"success": True, "message": f"Infrared strength set to {_infrared_strength}"}
    )


def get_infrared_strength() -> str:
    """
    Gets the current infrared strength.

    :return: Current infrared strength as a JSON string.
    :rtype: str
    """
    global _infrared_strength
    return json.dumps({"infrared_strength": _infrared_strength})


# Statically defined user functions for fast reference
user_functions: Set[Callable[..., Any]] = {
    set_inversion,
    get_inversion,
    set_traction_length,
    get_traction_settings,
    set_vibration_strength,
    get_vibration_settings,
    get_infrared_strength,
    set_infrared_strength,
}
