from fastapi import FastAPI, Header, HTTPException, Depends
from typing import Optional, Annotated
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt
import requests


app = FastAPI()

origins = [
    "http://localhost:3000",]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


invoices = [
    {"id": 1, "user_id": "google-oauth2|102891496487161009468", "amount": 100.0, "status": "paid"},
    {"id": 2, "user_id": "user2", "amount": 200.0, "status": "unpaid"},
    {"id": 3, "user_id": "user1", "amount": 150.0, "status": "paid"},
]

AUTH0_DOMAIN = 'dev-uijkelx4yghj3cp4.us.auth0.com'
AUTH0_API_AUDIENCE = 'https://invoices-api'
ALGORITHMS = ['RS256']


def check_auth(authorization: Annotated[Optional[str], Header()] = None):
    if authorization is None:
        raise HTTPException(status_code=401,detail = "Authorization header missing")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        raise HTTPException(status_code=401,detail = "Invalid authorization header")
    token = parts[1]
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise HTTPException(status_code = 401,detail = "Invalid token header")

    if unverified_header.get("alg") == "HS256":
        raise HTTPException(status_code=401, detail="Invalid algorithm")

    rsa_key = {}
    jwks_url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
    try:
        jwks = requests.get(jwks_url).json()
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
    except Exception:
        raise HTTPException(status_code=401, detail="Unable to fetch JWKS")
    if not rsa_key:
        raise HTTPException(status_code=401, detail="Unable to find appropriate key")

    try:   
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=AUTH0_API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )
            return payload
    except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401,detail="Token expired")
    except jwt.JWTClaimsError:
            raise HTTPException(status_code=401,detail="Incorrect claims")
    except Exception:
            raise Exception("Unable to parse authentication token")
      

@app.get('/invoices')
def get_invoices(payload: dict = Depends(check_auth)):
    user_id=payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found in token")
    user_invoices = [inv for inv in invoices if inv['user_id'] == user_id]

    return user_invoices