from django.http import HttpRequest, JsonResponse

from .mail_services import *
from ..models import CommonMailingList

import json

def newsletter_service(request: HttpRequest):
    data = json.loads(request.body)

    if data["email"] != request.user.email:
        return JsonResponse({"status": "error", "message": f"Incorect email address: {data["email"]}"}, status=400)
    else:
        status_code, respond_data = subscribe_user_to_mailchimp(email=data["email"], first_name=data["Fname"], last_name=data["Lname"])

        if status_code == 200:
            CommonMailingList.objects.create(email=data["email"], user=request.user)
    
    return JsonResponse(respond_data, status=status_code)