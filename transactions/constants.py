DEPOSIT = 1
WITHDRAWAL = 2
INTEREST = 3
TRANSFER = 4
WITHDRAWALFSA = 5
DEPOSITTSA = 6

TRANSACTION_TYPE_CHOICES = (
    (DEPOSIT, 'Deposit'),
    (WITHDRAWAL, 'Withdrawal'),
    (INTEREST, 'Interest'),
    (TRANSFER, 'Transfer'),
    (WITHDRAWALFSA, 'Withdrawal from SA'),
    (DEPOSITTSA, 'Deposit to SA'),
)
