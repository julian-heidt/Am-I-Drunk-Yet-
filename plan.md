# "Are You Drunk Yet?" - BAC Calculator Development Plan

## 1. Objective

To create a web application that takes user inputs (weight, height, age, gender, and number of alcoholic drinks consumed) to:
1.  Calculate the number of additional standard drinks required to reach a Blood Alcohol Content (BAC) of 0.1%.
2.  Estimate the time it will take for the user's BAC to return to zero (i.e., become sober).

**Disclaimer:** This tool will be for educational and entertainment purposes only and should not be used to determine an individual's fitness to drive or operate machinery. A prominent disclaimer will be visible on the web page.

## 2. Technology Stack

*   **Backend:** Python with the Flask web framework.
*   **Frontend:** HTML, CSS, and plain JavaScript (no framework).

## 3. Development Phases

### Phase 1: Project Setup & Core Logic (Backend)

*   **Task 1.1: Create Project Structure**
    *   Initialize a new project directory.
    *   Create the following structure:
        ```
        /AreYouDrunkYet
        |-- app.py             # Main Flask application
        |-- calculator.py      # Core BAC calculation logic
        |-- templates/
        |   |-- index.html     # Frontend HTML
        |-- static/
        |   |-- css/
        |   |   |-- style.css  # Stylesheet
        |   |-- js/
        |       |-- script.js  # Frontend JavaScript
        |-- requirements.txt   # Python dependencies
        |-- plan.md            # This file
        ```

*   **Task 1.2: Setup Python Virtual Environment**
    *   Create a virtual environment to manage project dependencies.
    *   Create a `requirements.txt` file and add `Flask`.
    *   Install the dependencies.

*   **Task 1.3: Implement BAC Calculation Logic (`calculator.py`)**
    *   Create a Python module to encapsulate the calculation logic.
    *   **Function 1: `calculate_drinks_to_target_bac`**
        *   **Formula:** The Widmark formula will be used: `BAC = (Alcohol in grams / (Body weight in grams * r)) * 100`
        *   **Inputs:** `weight` (in kg), `gender` ('male' or 'female').
        *   **Constants:**
            *   Widmark factor (`r`): `0.68` for men, `0.55` for women.
            *   Grams of alcohol in a US standard drink: `14` grams.
            *   Target BAC: `0.1`.
        *   **Logic:** Rearrange the formula to solve for the number of drinks.
            *   `Total Alcohol (g) = (Target BAC / 100) * Body Weight (g) * r`
            *   `Number of Drinks = Total Alcohol (g) / 14`
        *   **Return:** The number of drinks, rounded to a reasonable number of decimal places.
    *   **Function 2: `calculate_time_to_sober`**
        *   **Inputs:** `current_drinks`, `weight` (in kg), `gender`.
        *   **Constants:**
            *   Alcohol metabolism rate: `0.015` (% per hour).
        *   **Logic:**
            1.  First, calculate the *current* BAC based on the number of drinks consumed.
            2.  Then, calculate the time to sober using: `Time (hours) = Current BAC / 0.015`.
        *   **Return:** The time in hours.

### Phase 2: API Endpoint (Backend)

*   **Task 2.1: Create Flask App (`app.py`)**
    *   Set up a basic Flask application.
    *   Create a route (`/`) to serve the main HTML page (`index.html`).
    *   Create an API route (`/api/calculate`) that accepts `POST` requests.

*   **Task 2.2: Develop the API Endpoint**
    *   The `/api/calculate` endpoint will:
        1.  Receive a JSON payload with `weight`, `height`, `age`, `gender`, and `current_drinks`.
        2.  Perform basic validation on the input data (e.g., check for numeric types, positive values).
        3.  Call the functions from `calculator.py` to get the results.
        4.  Return the results in a JSON object, e.g., `{ "drinks_to_reach_target": 5, "time_to_sober": 8.5 }`.
        5.  Handle potential errors gracefully and return an appropriate error message.

### Phase 3: User Interface (Frontend)

*   **Task 3.1: Create HTML Structure (`templates/index.html`)**
    *   Create a form with input fields for:
        *   Weight (with a selector for lbs/kg).
        *   Height (with a selector for cm/in - although not used in the core calculation, it's a standard user expectation).
        *   Age.
        *   Gender (radio buttons for Male/Female).
        *   Number of drinks consumed (numeric input).
    *   Add a "Calculate" button.
    *   Create a dedicated `div` to display the results and the disclaimer.

*   **Task 3.2: Style the Page (`static/css/style.css`)**
    *   Apply clean, modern, and responsive CSS to make the application usable on different screen sizes.
    *   Style the form, inputs, button, and result display area.

*   **Task 3.3: Implement Client-Side Logic (`static/js/script.js`)**
    *   Add an event listener to the form to handle submission.
    *   On submit:
        1.  Prevent the default form submission behavior.
        2.  Get the values from all input fields.
        3.  Perform unit conversions if necessary (e.g., lbs to kg).
        4.  Perform client-side validation (e.g., ensure fields are not empty).
        5.  Use the `fetch` API to send a `POST` request to the `/api/calculate` endpoint with the user data in a JSON payload.
        6.  Await the JSON response from the server.
        7.  Dynamically update the result `div` with the calculated values in a user-friendly format (e.g., "You need approximately 5 more drinks to reach a 0.1% BAC. It will take about 8.5 hours until you are sober.").
        8.  Handle and display any errors returned by the API.

### Phase 4: Integration and Testing

*   **Task 4.1: End-to-End Testing**
    *   Run the Flask application.
    *   Open the web page in a browser and test the full workflow with various valid and invalid inputs.
    *   Verify that calculations are correct and the UI updates as expected.
    *   Check browser developer tools for any console errors.

*   **Task 4.2: Final Review**
    *   Ensure the disclaimer is clearly visible.
    *   Review the code for clarity and add comments where necessary.
    *   Finalize the `README.md` with instructions on how to set up and run the project. 