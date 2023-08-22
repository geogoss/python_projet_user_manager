import re
import string
from tinydb import TinyDB, where
from pathlib import Path

class User: 

    DB = TinyDB(Path(__file__).resolve().parent / 'db json', indent=4)

    def __init__(self, first_name: str, last_name: str, phone_number: str="", address: str=""):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address


    def __repr__(self):
        return f"User({self.first_name}, {self.last_name})"

    def __str__(self):
        return f"{self.full_name}\n{self.phone_number}\n{self.address}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def db_instance(self):
        return User.DB.get((where('first_name') == self.first_name) & (where('last_name') == self.last_name))

    # ici on va faire une méthode pour appeler les deux méthodes en une fois
    def _check(self):
        self._check_phone_number()
        self._check_names()

    def _check_phone_number(self):
        phone_number = re.sub(r"[+()\s]*", "", self.phone_number)
        if len(phone_number) < 10 or not phone_number.isdigit():
            raise ValueError(f"Numéro de téléphone {self.phone_number} est invalide")
        print(phone_number)


    def _check_names(self):
        if not (self.first_name and self.last_name):
            raise ValueError("Le prénom et le nom ne peuvent pas être vides")
        special_characters = string.punctuation + string.digits
        # on pourrait faire une boucle comme ceci mais il y a une meilleurs façon
        for character in self.first_name + self.last_name:
            if character in special_characters:
                raise ValueError(f"Nom invalide {self.full_name}")



    def exists(self):
        return bool(self.db_instance)

    def delete(self) -> list[int]:
        if self.exists():
            return User.DB.remove(doc_ids=[self.db_instance.doc_id])
        return []

    def save(self, validate_data: bool=False) -> int:
        if validate_data:
            self._check
        # ici on utilise la méthode self.__dict__ qui permet de créer un dictionnaire avec tous les attributs de nos instances et de ne pas le faire à la main
        return User.DB.insert(self.__dict__)


def get_all_users():
    return [User(**user) for user in User.DB.all()]
    # Fait avec une compréhension de liste
    # for user in User.DB.all():
    #     each_user = User(**user)
  


if __name__ == "__main__":
    from faker import Faker
    fake = Faker(locale="fr_FR")
    for _ in range(10):
        user = User(first_name=fake.first_name(), 
                    last_name=fake.last_name(),
                    phone_number=fake.phone_number(),
                    address=fake.address())
        # user._check_phone_number()
        # user._check_names()
        # user._check()
        print(user.save())
        # print(user)
        print("-" * 10)
    # print(get_all_users())
    # si on a un nom/prenom et qu'on veut chercher le phone_number
    # il faut créer le property db_instance
    luce = User("Luce", "Morel")
    print(luce.db_instance)
