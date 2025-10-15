from django.http import HttpResponse
from django.shortcuts import render,redirect
from OBmP.models import NewAccount, StaffLogData,Transaction
from django.contrib import messages
from OBmP.models import StaffLogData  
from django.db.models import Q
from django.contrib.auth.hashers import check_password

def Staff(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            StaffLogData.objects.get(username=username, password=password)
            # Login Success: Redirect or display success
            return render(request,'UserLog.html')  
        except StaffLogData.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return redirect('Staff')
    else:
        return render(request, 'staff.html')
    
def UserLog(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = NewAccount.objects.get(username=username, password=password)

            # Store user info in session
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['photo_url'] = user.photo.url

            return redirect('DebitCredit')  # Go to DebitCredit page

        except NewAccount.DoesNotExist:
            messages.error(request, "Invalid username or password")
            return render(request, 'UserLog.html')
    return  render(request,"UserLog.html")


def DebitCredit(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('UserLog')

    user = NewAccount.objects.get(id=user_id)

    # Transactions jekhane user sender or recipient
    transactions = Transaction.objects.filter(
        Q(user_id=user.id) | Q(recipient_id=user.id)
    ).order_by('-date')

    # Balance calculate
    balance = 0
    for t in transactions:
        if t.transaction_type == 'Deposit':
            balance += t.amount
        elif t.transaction_type == 'Withdraw':
            balance -= t.amount
        elif t.transaction_type == 'Transfer':
            if t.user_id == user.id:        # Sender
                balance -= t.amount
            elif t.recipient_id == user.id: # Recipient
                balance += t.amount

    context = {
        'username': user.username,
        'photo_url': user.photo.url,
        'transactions': transactions[:5],  # last 5 transactions
        'balance': balance
    }

    return render(request, "DebitCredit.html", context)

def about(request):
    return render(request, "about.html")


def homePage(request):
    return render(request, "home.html")


def NewAcc(request):
    return render(request, "NewAcc.html")

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import StaffLogData

def AccountRecord(request):
    if request.method == 'POST':
        if all([
            request.POST.get('name'),
            request.POST.get('aadhar'),
            request.POST.get('email'),
            request.POST.get('phone'),
            request.POST.get('dob'),
            request.POST.get('password'),
            request.POST.get('gender'),
            request.POST.get('username'),
            request.FILES.get('photo')
        ]):
            saverecord = NewAccount(
                name=request.POST.get('name'),
                aadhar=request.POST.get('aadhar'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                dob=request.POST.get('dob'),
                password=request.POST.get('password'),
                gender=request.POST.get('gender'),
                username=request.POST.get('username'),
                photo=request.FILES['photo']
            )
            saverecord.save()
            messages.success(request, "Record saved successfully!")
            return render(request, 'UserLog.html')
        else:
            messages.error(request, "All fields are required!")
            return render(request, 'NewAcc.html')
def deposit(request):
    if request.method == 'POST':
        user = NewAccount.objects.get(id=request.session['user_id'])
        amount = float(request.POST.get('amount', 0))
        if amount > 0:
            Transaction.objects.create(user=user, transaction_type='Deposit', amount=amount)
            messages.success(request, f"${amount} deposited successfully")
        else:
            messages.error(request, "Invalid amount")
    return redirect('DebitCredit')


def withdraw(request):
    if request.method == 'POST':
        user = NewAccount.objects.get(id=request.session['user_id'])
        amount = float(request.POST.get('amount', 0))

        transactions = Transaction.objects.filter(Q(user=user) | Q(recipient=user))
        balance = 0
        for t in transactions:
            if t.transaction_type == 'Deposit':
                balance += t.amount
            elif t.transaction_type == 'Withdraw':
                balance -= t.amount
            elif t.transaction_type == 'Transfer':
                if t.user == user:
                    balance -= t.amount
                elif t.recipient == user:
                    balance += t.amount

        if amount > 0 and amount <= balance:
            Transaction.objects.create(user=user, transaction_type='Withdraw', amount=amount)
            messages.success(request, f"${amount} withdrawn successfully")
        else:
            messages.error(request, "Insufficient balance")
    return redirect('DebitCredit')


def transfer(request):
    user = NewAccount.objects.get(id=request.session['user_id'])
    users = NewAccount.objects.exclude(id=user.id)

    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        amount = float(request.POST.get('amount', 0))
        recipient = NewAccount.objects.get(id=recipient_id)

        # Balance calculation
        transactions = Transaction.objects.filter(Q(user=user) | Q(recipient=user))
        balance = 0
        for t in transactions:
            if t.transaction_type == 'Deposit':
                balance += t.amount
            elif t.transaction_type == 'Withdraw':
                balance -= t.amount
            elif t.transaction_type == 'Transfer':
                if t.user == user:
                    balance -= t.amount
                elif t.recipient == user:
                    balance += t.amount

        if amount > 0 and amount <= balance:
            # Deduct from sender
            Transaction.objects.create(
                user=user,
                transaction_type='Transfer',
                amount=amount,
                recipient=recipient
            )
            # Deposit for recipient
            Transaction.objects.create(
                user=recipient,
                transaction_type='Deposit',
                amount=amount
            )
            messages.success(request, f'Transferred ₹{amount} to {recipient.username}')
        else:
            messages.error(request, 'Insufficient balance')

        return redirect('Transaction')

    context = {
        'users': users,
        'username': user.username,
        'photo_url': user.photo.url,
    }
    return render(request, 'Transaction.html', context)


def history(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('UserLog')  # যদি user session না থাকে

    user = NewAccount.objects.get(id=user_id)
    
    # সব transaction যেখানে sender বা recipient
    transactions = Transaction.objects.filter(
        Q(user_id=user.id) | Q(recipient_id=user.id)
    ).order_by('-date')

    # Recipient id -> username mapping তৈরি
    recipient_ids = [t.recipient_id for t in transactions if t.recipient_id]
    recipient_accounts = NewAccount.objects.filter(id__in=recipient_ids)
    recipient_map = {acc.id: acc.username for acc in recipient_accounts}

    context = {
        'transactions': transactions,
        'username': user.username,
        'photo_url': user.photo.url,
        'recipient_map': recipient_map
    }

    return render(request, 'History.html', context)
