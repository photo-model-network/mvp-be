from rest_framework.throttling import UserRateThrottle


class SendBankVerificationThrottle(UserRateThrottle):
    rate = "5/day"
