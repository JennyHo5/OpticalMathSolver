"""
    app.py will contain the Flask app and route definitions.
"""
import cv2
from flask import Flask, request, jsonify
from flask_cors import CORS
from solver import solve_math
from processor import parse_equation, recognize_math
import base64
import numpy as np
import json
from sympy import latex

app = Flask(__name__)
CORS(app) # enable CORS for all routes

@app.route('/solve', methods=['GET', 'POST'])
def solve():
    try:
        print("Request Headers:", request.headers)

        byteOfImage = request.get_data()
        # Convert bytes data to numpy array
        nparr = np.frombuffer(byteOfImage, np.uint8)
        # Decode the numpy array into an image
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # save it locally
        cv2.imwrite('saved_image.jpg', image)

        processed_img, equation_regions = parse_equation(image)
        equations = []

        for (x, y, w, h) in equation_regions:
            equation_region = processed_img[y:y+h, x:x+w]
            _, buffer = cv2.imencode('.jpg', equation_region)
            image_base64 = base64.b64encode(buffer).decode()
            try:
                latex_format = recognize_math(image_base64)
            except ValueError as e:
                continue
            try:
                answer = solve_math(latex_format)
            except Exception as e:
                continue
            print("solve_math: ", answer)
            equations.append({"question": latex_format, "answer": latex(answer)})
            
        if len(equations) == 0:
            raise ValueError("Can't recognize any equation. Try again with a different image. ")

        equations.reverse()

        return jsonify(equations)
    except Exception as e:
        print("error: ", str(e))
        # Return error message if an exception occurs
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    
    # app.run(debug=True)
    
    """
        For running locally
    """
    image = cv2.imread('images/image1.jpg')
    # image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE) # for loading in memeory
    """
        TODO: error handling if processing img fail
    """
    processed_img, equation_regions = parse_equation(image)
    for (x, y, w, h) in equation_regions:
        equation_region = processed_img[y:y+h, x:x+w]
        _, buffer = cv2.imencode('.jpg', equation_region)
        image_base64 = base64.b64encode(buffer).decode()
        try:
            """
                TODO: frontend need to render both of the equation in latex_format and its result
            """
            latex_format = recognize_math(image_base64)
            result = solve_math(latex_format)
            print(latex_format, ": ", result)
        except Exception as e:
            """
                TODO: error handeling, display proper msg to frontend
            """
            print(f"Error occurred: {e}")