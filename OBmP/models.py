from django.db import models

class NewAccount(models.Model):
    name=models.CharField(max_length=100)
    aadhar=models.CharField(max_length=12)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    dob = models.DateField()
    password = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    username = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/') 
    class Meta:
        db_table = "accdata"

class StaffLogData(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    class Meta:
        db_table = "stafflogdata"
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Deposit', 'Deposit'),
        ('Withdraw', 'Withdraw'),
        ('Transfer', 'Transfer'),
    ]

    user = models.ForeignKey(
        'NewAccount',
        on_delete=models.CASCADE,
        related_name='transactions',
        db_column='user_id'
    )
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey(
        'NewAccount',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='received_transactions',
        db_column='recipient_id'
    )

    class Meta:
        db_table = "user_transactions"
