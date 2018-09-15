from django.db.models import Manager


class LikeManager(Manager):
    def user_like(self, user, article):
        """Check user like this article"""
        return self.filter(user=user, article=article).exists()

    def likes(self, user):
        """Count of all user likes"""
        return self.filter(user=user).count()

    def article_likes(self, article):
        """Count of all article likes"""
        return self.filter(article=article).count()
