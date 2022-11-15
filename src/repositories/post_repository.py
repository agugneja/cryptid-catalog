from src.models import Post

class PostRepository:
    
    def get_post_by_id(self, _post_id):
        post_by_id = Post.query.filter_by(post_id=_post_id).first()
        return post_by_id

# Singleton to be used in other modules
post_repository_singleton = PostRepository()
