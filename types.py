from csv import unregister_dialect
from typing_extensions import TypedDict

class Measurements:
    """ A measurements for a user from the RENPHO API  """
    def __init__ (self, weight: str, created_at: str, bodyfat: str, water: str, bmr: str, bodyage: str, bone: str,
                        subfat: str, visfat: str, bmi: str, sinew: str, protein: str, fat_free_weight: str, muscle: str, 
                        user_id: str, account_name: str, unit_of_measurements: str):
        
        self.weight = weight
        self.visfat = visfat
        self.created_at = created_at
        self.bodyfat = bodyfat
        self.water = water
        self.bmr = bmr
        self.bodyage = bodyage
        self.bone = bone
        self.subfat = subfat
        self.bmi = bmi
        self.sinew = sinew
        self.protein = protein
        self.fat_free_weight = fat_free_weight
        self.muscle = muscle
        
        self.user_id = user_id
        self.account_name = account_name
        self.unit_of_measurements = unit_of_measurements
