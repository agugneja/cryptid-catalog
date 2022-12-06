from src.models import Person, db

class PersonRepository:
    
    def get_person_by_id(self, _person_id):
        person_by_id = Person.query.filter_by(user_id=_person_id).first()
        return person_by_id

    def get_person_by_username(self, _person_username):
        person_by_id = Person.query.filter_by(username =_person_username).first()
        return person_by_id
    
    # takes in a username, and returns the associated user_id
    def get_user_id_by_username(self, _username):
        user_id = Person.query(user_id).filterby(_username)
        return user_id

    def create_user(self, username, password, email):
        new_user = Person(username = username, password = password, email = email)
        db.session.add(new_user)
        db.session.commit()
        return new_user
# Singleton to be used in other modules
person_repository_singleton = PersonRepository()
