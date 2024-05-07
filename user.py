
from datetime import date
import os
import csv 
PATH = "Data/resultados_formularios.csv"
AVAILABLE_FIELDS = ["ASPECTO", "OLOR", "TEXTURA", "SABOR", "COLOR", "DUREZA", "DULZOR"]

class User:
    def __init__(self):
        self.consumer_code = None
        self.cookie_code = None
        self.opinion = None
        self.fields = {
            "date": date.today().strftime("%d/%m/%Y"),
            "consumer_code": None,
            "cookie_code": None,
            "aspecto": None,
            "olor": None,
            "textura": None,
            "sabor": None,
            "color": None,
            "dureza": None,
            "dulzor": None
        }
        self.missing_fields = []
    def set_consumer_code(self, consumer_code):
        self.consumer_code = consumer_code
        self.set_field("consumer_code", consumer_code)
    
    def set_cookie_code(self, cookie_code):
        self.cookie_code = cookie_code
        self.set_field("cookie_code", cookie_code)

    def get_consumer_code(self):
        return self.consumer_code
    
    def get_cookie_code(self):
        return self.cookie_code
    
    def get_date(self):
        return self.date
    
    def set_opinion(self, opinion):
        self.opinion = opinion

    def get_opinion(self):
        return self.opinion
    
    def get_fields(self):
        return self.fields
    
    def set_missing_fields(self, missing_fields):
        for field in missing_fields:
            self.missing_fields.append(field)
    def set_field(self, field, value):
        self.fields[field] = value

    def set_available_fields(self, field, value):
        self.fields[field] = value

    def get_missing_fields(self):
        return self.missing_fields
    
    def save_user(self):
        os.makedirs(os.path.dirname(PATH), exist_ok=True)
        file_exists = os.path.exists(PATH)
        with open(PATH, mode = 'a' if file_exists else 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=list(self.fields.keys()))
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(self.fields)
        print("Usuario guardado...")
            