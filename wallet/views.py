from django.conf import settings
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view

from .models import Transaction, TransferReceipient, Wallet

from .serializers import DepositSerializer, UserSerializer, WalletSerializer


class Login(APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key, "username": username})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class Register(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class WalletInfo(APIView):

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        data = WalletSerializer(wallet).data
        return Response(data)


class DepositFunds(APIView):

    def post(self, request):
        serializer = DepositSerializer(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        resp = serializer.save()
        return Response(resp)

class VerifyDeposit(APIView):

    def get(self, request, reference):
        transaction = Transaction.objects.get(
        payment_reference=reference, wallet__user=request.user)
        reference = transaction.payment_reference
        url = 'https://api.paystack.co/transaction/verify/{}'.format(reference)
        headers = {"authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        r = requests.get(url, headers=headers)
        resp = r.json()
        if resp['data']['status'] == 'success':
            status = resp['data']['status'],
            amount = resp['data']['amount'],
            Transaction.objects.filter(payment_ref=reference).update(status=status,amount=amount)
            return Response(resp)
        return Response(resp)
    

class TransferRecep(APIView):
    def post(self):
        user = self.context['request'].user
        data = self.validated_data
        url = 'https://api.paystack.co/transferrecipient/'
        headers = {"authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        r = requests.post(url, headers=headers, data=data)
        response = r.json()
        TransferReceipient.objects.create(
            type="nuban",
            name=user,
            account_number= data["account_number"],
            bank_code  = data["bank_code"],
            currency = data["currency"],
        )
        return response

class ListReceipients(APIView):

    def get(self):
        url = 'https://api.paystack.co/transferrecipient'
        headers = {"authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        r = requests.get(url, headers=headers)
        resp = r.json()
        return Response(resp)

class FetchReceipients(APIView):

    def get(self, request):
        transaction = TransferReceipient.objects.get(name__user=request.user)
        reference = transaction.trans_ref
        url = 'https://api.paystack.co/transferrecipient{}'.format(reference)
        headers = {"authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        r = requests.get(url, headers=headers)
        resp = r.json()
        return Response(resp)
    

class InitiateTransfer(APIView):
    
    def post(self):
        user = self.context['request'].user
        rec = self.validated_data
        data = {
            "source" : "balance",
            "reason" : "Transfer",
            "amount" : rec["account_number"],
            "recipient" : rec["trans_ref"]
        }
        url = 'https://api.paystack.co/transfer'
        headers = {"authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        r = requests.post(url, headers=headers, data=data)
        response = r.json()
        return response

