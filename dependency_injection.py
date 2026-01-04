from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

router = APIRouter()

class Logger:
    def log(self, message: str):
        print(f"Logging message: {message}")


def get_logger():
    return Logger()


logger_dependency = Annotated[Logger, Depends(get_logger)]


# logger:Logger = Depends(get_logger)

@router.get("/log/{message}")
def log_message(message: str, logger: logger_dependency):
    logger.log(message);
    return message


class EmailService:
    def send_email(self, recipient: str, message: str):
        print(f"Sending email to {recipient}: {message}")

def get_email_Service():
    return EmailService()

email_service_dependency = Annotated[EmailService, Depends(get_email_Service)]

def send_email(recipient: str, message: str, email_service: email_service_dependency):
    email_service.send_email(recipient, message)


class AuthService:
    def authenticate(self, token: str):
        if token == "valid":
            return True
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

def get_auth_service():
    return AuthService()

auth_service_dependency = Annotated[AuthService, Depends(get_auth_service)]

@router.get("/secure-data")
def authenticate(token: str, auth_service: auth_service_dependency):
    if auth_service.authenticate(token):
        return {"message": "Authenticated"}