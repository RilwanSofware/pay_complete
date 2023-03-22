from django.urls import path
from .views import DepositFunds, InitiateTransfer, ListReceipients, Login, Register, TransferRecep, VerifyDeposit, WalletInfo


urlpatterns = [
    path('register/', Register.as_view()),
    path('login/', Login.as_view()),
    path('wallet_info/', WalletInfo.as_view()),
    path('deposit/', DepositFunds.as_view()),
    path('deposit/verify/<str:reference>/', VerifyDeposit.as_view()),
    path('transferrecipient/', TransferRecep.as_view()),
    path('list_transfer/', ListReceipients.as_view()),
    path('transfer/', InitiateTransfer.as_view()),
]