from src.models import Person, db

class PersonRepository:
    
    def get_person_by_id(self, _person_id):
        person_by_id = Person.query.filter_by(user_id=_person_id).first()
        return person_by_id
    
    def create_user(self, username, password, email):
        new_user = Person(username = username, password = password, email = email)
        db.session.add(new_user)
        db.session.commit()
        return new_user
# Singleton to be used in other modules
person_repository_singleton = PersonRepository()
