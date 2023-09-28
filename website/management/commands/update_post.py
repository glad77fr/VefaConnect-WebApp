from django.core.management.base import BaseCommand
from forum.models import ForumPost
from django.db.models import Q

class Command(BaseCommand):
    help = 'Generate slugs for existing ForumPosts'

    def handle(self, *args, **options):
        posts = ForumPost.objects.filter(Q(slug__isnull=True) | Q(slug=''))

        # Afficher le nombre total de posts sans slug
        self.stdout.write(f"Number of posts without slugs: {posts.count()}")

        if not posts.exists():
            self.stdout.write(self.style.SUCCESS('All posts already have slugs. No action required.'))
            return

        for post in posts:
            post.save()  # This will trigger the pre_save signal to generate a slug
            self.stdout.write(self.style.SUCCESS('Slug generated for post id %s' % post.id))