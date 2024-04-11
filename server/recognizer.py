from dotenv import load_dotenv
import os, requests, json, re

def load_environment_vars():
    load_dotenv()
    app_id = os.getenv('APP_ID')
    app_key = os.getenv('APP_KEY')
    endpoint = 'https://api.mathpix.com/v3/text'
    return app_id, app_key, endpoint

"""
    # if '=' is followed by useless information, e.g. "3 + 1 = "  or "3 + 1 = ?"
    # return everything up to (not including) the first occurrence of '='

"""
def trim_trailing_equal_sign(latex_str):
    # Trim all whitespaces and backslashes from the LaTeX string
    trimmed_str = re.sub(r'[\s\\]+', '', latex_str)
    
    # Search for the first occurrence of '=' that is not followed by a letter or number
    match = re.search(r'=(?![a-zA-Z0-9])', trimmed_str)
    
    if match:
        equal_sign = re.search(r'=', latex_str)
        return latex_str[:equal_sign.start()]
    else:
        return latex_str


"""
    recognize the math equation and expression from the parsed image
    
"""
def recognize_math(image_base64):
    api_id, api_key, endpoint = load_environment_vars()
    res = requests.post(endpoint,
        json={
            "src": f"data:image/jpg;base64,{image_base64}",
            "math_inline_delimiters": ["$", "$"],
            "rm_spaces": True
        },
        headers={
            "app_id": api_id,
            "app_key": api_key
        }
    )
    # Error handling
    if res.status_code == 200:
        print(json.dumps(res.json(), indent=4, sort_keys=True))
        latex_str = res.json().get('latex_styled', '')
        if not latex_str or "text" in latex_str:
            print("recognize_math: No Math LaTeX string found in the response.")
            raise ValueError("No Math LaTeX string found in the response.")
        confidence = res.json().get('confidence_rate', 0)
        if confidence < 0.6:
            print("recognize_math: Confidence level below 60%")
            raise ValueError("Confidence level below 60%")
        trimmed_latex_str = trim_trailing_equal_sign(latex_str)
        print(trimmed_latex_str)
        return trimmed_latex_str
    else:
        handle_api_error(res.status_code, res.text)

def handle_api_error(status_code, error_message):
    if status_code == 400:
        raise ValueError("Bad request. Please check the request format and parameters.")
    elif status_code == 401:
        raise PermissionError("Unauthorized request. Please check your API credentials.")
    elif status_code == 429:
        raise OverflowError("Too many requests. You have reached the rate limit.")
    elif 400 <= status_code < 500:
        raise UserWarning(f"Client error: {error_message}")
    elif 500 <= status_code:
        raise SystemError("Server error. Please try again later.")
    else:
        raise Exception(f"Unexpected error: {error_message}")