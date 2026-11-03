# FastAPI Learning Project

This project is a small learning-based application built with FastAPI and Streamlit to explore:

- REST API development with FastAPI
- Data validation with Pydantic
- CRUD operations for patient records
- Machine learning model integration with an API
- Simple frontend development with Streamlit

## Project Overview

The project contains three main parts:

1. `main.py` - Patient management API with CRUD endpoints
2. `app.py` - Insurance premium prediction API using a trained machine learning model
3. `frontend.py` - Streamlit interface for sending prediction requests to the API

## Features

### Patient Management API
- Create patient records
- View all patients
- Fetch a single patient
- Update patient information
- Delete patient records
- Sort patients by height, weight, or BMI

### Premium Prediction API
- Accepts patient details such as age, weight, height, salary, smoking status, city, and occupation
- Calculates derived fields like BMI and age group
- Uses a saved ML model to predict premium category

### Streamlit Frontend
- User-friendly form to input health and income details
- Sends request to the FastAPI backend
- Displays the predicted premium category

## Project Structure

```text
fastApi-tutorial/
├── app.py              # Insurance prediction API
├── frontend.py         # Streamlit frontend
├── main.py             # Patient management API
├── model.pkl           # Trained machine learning model
├── patients.json       # JSON database for patients
├── README.md           # Project documentation
└── myenv/              # Virtual environment
```

## Technologies Used

- Python
- FastAPI
- Pydantic
- Streamlit
- Pandas
- Pickle (for loading the ML model)

## Setup

Create and activate a virtual environment:

```bash
python -m venv myenv
myenv\Scripts\activate
```

Install the required dependencies:

```bash
pip install fastapi uvicorn streamlit pandas
```

If needed, also install `scikit-learn` if your model or project requires it:

```bash
pip install scikit-learn
```

## Running the Applications

### 1. Start the insurance prediction API

```bash
uvicorn app:app --reload --port 8000
```

### 2. Start the patient management API

```bash
uvicorn main:app --reload --port 8001
```

### 3. Run the Streamlit UI

```bash
streamlit run frontend.py
```

Then open the local Streamlit URL in your browser to use the prediction interface.

## API Endpoints

### Patient API (`main.py`)

- `GET /` - Welcome message
- `GET /about` - About the API
- `GET /view` - View all patient records
- `GET /patient/{patient_id}` - View a single patient
- `GET /sort` - Sort patient records by height, weight, or BMI
- `POST /create` - Add a new patient
- `PUT /update/{patient_id}` - Update a patient record
- `DELETE /delete/{patient_id}` - Delete a patient record

### Prediction API (`app.py`)

- `POST /predict` - Predict insurance premium category based on input data

## Example Prediction Payload

```json
{
  "age": 30,
  "weight": 70,
  "height": 1.75,
  "income_lpa": 12,
  "smoker": false,
  "city": "Delhi",
  "occupation": "private_job"
}
```

## Notes

This project is meant primarily for learning and experimentation. It demonstrates the integration of FastAPI APIs, model-based prediction, and simple UI development in a practical workflow.

## Future Improvements

- Add database integration using PostgreSQL or SQLite
- Improve ML model accuracy
- Add authentication and user management
- Add frontend styling and better forms
- Add tests for API endpoints

## License

This project is for educational purposes only.
