# OpticalMathSolver
### COMP 4102 Computer Vision Final Project
**Project Proposal**

**Title: Optical Math Solver**

**G9 Team Members:**

- Addison Xiong

- Jiayu Hu

- Yousuf Ghanem

**How to run the program:**
Connect the mobile device and the computer running the backend server to the same network (wifi).

Frontend:

1. Connect your mobile device and and computer to the same network (wifi)

2. Under client/OpticalMathSolver directory, add a `.env` file with the following line: 
```bash
EXPO_PUBLIC_HOST=[your_ip_address]
```

3. Run the following command in the terminal:

```bash
cd client/OpticalMathSolver
npm install
npx expo start
```

3. Scan the QR code in the terminal, open the app in Expo Go

Backend:

1. Connect your mobile device and and computer to the same network (wifi)

2. Under server/OpticalMathSolver directory, add a `.env` file with the following line: 
```bash
APP_ID=carleton_49358f_f7b227
APP_KEY=78cd576439a7781b6a29a196cd599842b96f3bfd7a5f3df45843c3dbeb161924
```

3. Run the following command in the terminal:

```bash
cd server
pip install -r requirements.txt
flask run -h [your_ip_address]
```

[Demo Video](https://youtu.be/fKWOTPsrhBs)


**Summary:**

Our project, Optical Math Solver, is designed to create a mobile application that can capture images of mathematical problems (both arithmetic and matrix operations) and solve them instantly. This involves using image processing techniques and Optical Character Recognition (OCR) to extract and interpret mathematical expressions from real-world images.

**Background:**

Existing solutions like Photomath focus primarily on simpler arithmetic problems and struggle with complex expressions or varied handwriting. Our project aims to improve upon this by incorporating advanced OCR technologies and robust parsing algorithms to handle a wider variety of mathematical problems, including complex matrix operations. The project might leverage the computational capabilities of iOS devices:

- NEON Intrinsics: For efficient arithmetic computations.
- Accelerate Framework: Utilized for rapid matrix operations.
- CoreML: For potential custom OCR model integration.

These technologies will enhance the app's performance, making it capable of real-time processing and solution generation.

**The Challenge:**

The challenge lies in accurately parsing and interpreting a wide range of handwritten and printed mathematical expressions under varying image conditions. The project aims to address limitations in current OCR technologies, especially in handling complex mathematical notations. We hope to learn more about image processing in real-world conditions and the integration of OCR with mathematical problem-solving algorithms.

**Goals and Deliverables:**

- **Plan to Achieve:**
  - Create an iOS application that can take images as input and display solved answers.
  - Integrate Tesseract OCR for text extraction from images.
  - Develop an algorithm to parse and solve basic arithmetic problems.
- **Hope to Achieve:**
  - Extend functionality to recognize and solve matrix operations.
  - Improve accuracy in recognizing diverse handwriting styles.

- **Success Evaluation:**
  - Success will be validated through a series of tests with different types of math problems.
  - Demonstrations of the app through screen recordings and live demonstrations.
  - Comparison of app performance with existing solutions.

- **Realism of Goals:**
  - Given the team's expertise in software development, the primary goals are achievable within the given timeframe. The additional goals will be pursued as stretch objectives, contingent on the progress of core functionalities.

**Schedule:**

| **Week** | **Member 1 (OCR and Math Parsing)** | **Member 2 (UI/UX and App Development)** | **Member 3 (Image Preprocessing)** |
| --- | --- | --- | --- |
| Feb 5 - Feb 11 | Research and initial setup of OCR engine. | Design basic UI/UX of the app. | Begin work on image preprocessing module. |
| Feb 12 - Feb 18 | Start integrating OCR with the app. | Develop functionality for image capture/upload. | Implement image enhancement algorithms. |
| Feb 19 - Feb 25 | Initial testing of OCR with arithmetic problems. | - | - |
| Feb 26 - Mar 4 | Develop math problem parsing algorithm. | Enhance user interface for results display. | Optimize image preprocessing for lighting. |
| Mar 5 - Mar 11 | Integration of math solving algorithm with OCR output. | - | - |
| Mar 12 - Mar 18 | - | Conduct user testing with basic arithmetic problems. | Gather user feedback. |
| Mar 19 - Mar 25 | Refine app based on user feedback. | Focus on usability and accuracy improvements. | - |
| Mar 26 - Apr 1 | Implement matrix operation recognition and solving. | Polish final UI/UX elements. | Fine-tune OCR performance and accuracy. |
| Apr 2 - Apr 10 | Presentation prep | Presentation prep | Final testing, bug fixing, and presentation prep. |

By March 25, we aim to have a functional app for solving arithmetic problems, with subsequent weeks dedicated to adding matrix operations and refining the user experience.
