from fastapi import FastAPI, Path, HTTPException, Query  
from fastapi.responses import JSONResponse 
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json


app = FastAPI()

class Patient(BaseModel):

    id: Annotated[str, Field(..., description='id of patient', example='P001')]
    name: Annotated[str, Field(..., description= 'name of patient', example= 'prince')]
    city: Annotated[str, Field(..., description= 'city where patient lives', example= 'delhi')]
    age: Annotated[int, Field(..., gt=0, lt=120,  description= 'Age of patient', example= 29)]
    gender: Annotated[Literal['male','female','other'], Field(..., description='Gender of patient') ]
    height: Annotated[float, Field(..., gt=0,  description= 'height of patient in meter', example= 1.75)]
    weight: Annotated[float, Field(..., gt=0, description= 'weight of patient in kilograms', example= 45.6)]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:  # here it will trigger the bmi function while trying to get the field value
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else :
            return 'Obese'

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None)]
    gender: Annotated[Optional[Literal['male','female','other']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]        


def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)
        

@app.get("/")
def hello():
    return {'message' : 'Patient Management System API'}

@app.get("/about")
def about():
    return {'message' : 'A fully functional API to manage your patient records'}

@app.get("/view")
def view():
    data = load_data()
    
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description='ID of the patient in DB', example='P001')):
    # load all patient data
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description='sort on the basis of height, weight or bmi'), order: str = Query('asc', description='sort in ascentding or desecnding order')):
    
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')


    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')

    data = load_data()

    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):

    #load existing data
    data = load_data()

    #new patient id already exists or not using get call?
    if patient.id in data:
        raise HTTPException(status_code=400, detail='patient already exists')
    

    #new patient add in case patient is already patient
    data[patient.id] = patient.model_dump(exclude=['id'])


    #save in json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'patient creted successfully'}) 

@app.put('/update/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    #update the patient data

    #so update the patient data with the new data we store the existing data in a variable then convert the new data into dictionary (because existing data is dictionary) and do exclude_unset=True to get only the fields which are updated

    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    #Now we run a for loop based on key and value from the one that we received from new data and update the existing key with new value. This way we will only update the fields that are provided in the request body and leave the rest of the fields unchanged.

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    # now that the value is updated but bmi and verdict are computed fields and we need to update them as well. so we create new patient object based on existing pydantic model (Patient) with the updated data but we need to pass the id as well because it is required field in the Patient model. So we add the id to the existing data and then create a new patient object and then we can get the updated bmi and verdict from that object. 

    existing_patient_info['id'] = patient_id    

    patient_pydantic_object = Patient(**existing_patient_info)

    #once the new patient object is created we can get the updated bmi and verdict from that object and then we can update the existing data with the new bmi and verdict. But we need to exclude the id field because it is not required in the existing data. So we use model_dump with exclude={'id'} to get the updated data without the id field.

    existing_patient_info = patient_pydantic_object.model_dump(exclude='id') 

    #now  adding this dictionary to the existing data with the patient id as the key. This will update the existing data with the new data.

    data[patient_id] = existing_patient_info

    #saving the data

    save_data(data)    

    return JSONResponse(status_code=200, content={'message': 'patient updated successfully'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    #delete the patient from the data
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'patient deleted successfully'})
