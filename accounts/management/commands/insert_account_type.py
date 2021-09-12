from django.core.management.base import BaseCommand

from .account_type import insert_account_type

class Command(BaseCommand):
	help = 'Insert account type from json'

	def handle(self, *args, **kwargs):
		print("--START INSERTING ACCOUNT TYPE--")
		insert_account_type()
		print("--END INSERTING ACCOUNT TYPE--")
		

