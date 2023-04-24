# Django unicorn
from django_unicorn.components import UnicornView

# Instagram models
from instagram.posts.models import Post
from instagram.posts.models import Like


class LikeView(UnicornView):
    
    likes: int = Like.objects.none()
    
    def mount(self) -> None:
        self.likes = Like.objects.count()
    
    def add_like(self, post_id: int = None) -> None:
        post = Post.objects.get(id=post_id)
        like = Like.objects.filter(user=self.request.user, post=post).first()

        if like:
            like.delete()
        else:
            Like.objects.create(user=self.request.user, post=post)
        
        self.likes = Like.objects.count()