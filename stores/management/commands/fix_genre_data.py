from django.core.management.base import BaseCommand
from stores.models import Store, Genre

class Command(BaseCommand):
    help = 'Fix genre data for stores'

    def handle(self, *args, **kwargs):
        # Step 1: 必要なジャンルデータを Genre テーブルに追加
        genre_names = ['cafe', 'restaurant', 'bar', 'shop']  # 必要なジャンルリスト
        for name in genre_names:
            genre, created = Genre.objects.get_or_create(name=name)
            if created:
                self.stdout.write(f'Created genre: {name}')
            else:
                self.stdout.write(f'Genre already exists: {name}')

        # Step 2: Storeテーブルのジャンルフィールドを修正
        stores = Store.objects.all()
        for store in stores:
            if store.genre and not Genre.objects.filter(name=store.genre).exists():
                self.stdout.write(f"Fixing genre for store '{store.name}' (id: {store.id})")
                # `Genre` に存在しないジャンルは無効化
                store.genre = None
                store.save()
                self.stdout.write(f"Set genre to None for store '{store.name}' (id: {store.id})")
        
        self.stdout.write('Genre data fixed successfully!')
