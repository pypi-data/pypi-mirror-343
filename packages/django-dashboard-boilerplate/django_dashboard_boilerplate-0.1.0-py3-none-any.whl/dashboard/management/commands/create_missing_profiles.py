from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dashboard.models import UserProfile


class Command(BaseCommand):
    help = 'Creates missing user profiles for existing users'

    def handle(self, *args, **options):
        users_without_profiles = []
        
        # Find users without profiles
        for user in User.objects.all():
            try:
                # Try to access the profile
                user.profile
            except User.profile.RelatedObjectDoesNotExist:
                users_without_profiles.append(user)
        
        # Create profiles for users without them
        for user in users_without_profiles:
            UserProfile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Created profile for user: {user.username}'))
        
        if not users_without_profiles:
            self.stdout.write(self.style.SUCCESS('All users already have profiles'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Created {len(users_without_profiles)} user profiles'))
