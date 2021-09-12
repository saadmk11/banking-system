from accounts.models import BankAccountType

from .account_type_json import account_types

def insert_account_type():
	for key, account_type in account_types.items():

		# importing account types from json
		name = account_type['name']
		maximum_withdrawal_amount = account_type['maximum_withdrawal_amount']
		annual_interest_rate = account_type['annual_interest_rate']
		interest_calculation_per_year = account_type['interest_calculation_per_year']

		if not BankAccountType.objects.filter(name=name).exists():
			BankAccountType.objects.create(
				name = name,
				maximum_withdrawal_amount = maximum_withdrawal_amount,
				annual_interest_rate = annual_interest_rate,
				interest_calculation_per_year = interest_calculation_per_year
			)
		else:
			print(f"{name} already exists!")