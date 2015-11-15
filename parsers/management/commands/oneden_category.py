from django.core.management import BaseCommand
from parsers.tasks import CrawlOneden, CrawlOnCategories


class Command(BaseCommand):
	def handle(self, *args, **options):
		CrawlOnCategories().run()

