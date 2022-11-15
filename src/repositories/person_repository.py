from src.models import Person

class PersonRepository:
    
    def get_person_by_id(self, _person_id):
        person_by_id = Person.query.filter_by(user_id=_person_id).first()
        return person_by_id

# Singleton to be used in other modules
person_repository_singleton = PersonRepository()
