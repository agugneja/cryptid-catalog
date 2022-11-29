from src.models import Post, db

class PostRepository:
    
    def get_post_by_id(self, _post_id):
        post_by_id = Post.query.filter_by(post_id=_post_id).first()
        return post_by_id
    
    def get_all_posts(self):
        return Post.query.all()
    
    def get_posts_by_creature(self, _creature):
        return Post.query.filter_by(creature=_creature)

    #add photo later
    def create_post(self, title, creature, dt, user_id, place, description, picture, likes, dislikes):
        post = Post(title, creature, dt, user_id, place, description, picture, likes, dislikes)
        db.session.add(post)
        db.session.commit()
        return post

# Singleton to be used in other modules
post_repository_singleton = PostRepository()
