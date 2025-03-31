from datetime import timedelta
from cryptography.hazmat.primitives import serialization
import os
from cryptography.hazmat.backends import default_backend
from UserManagerApplication.settings import BASE_DIR

DEFAULT_ROLE = "local_system"
STATUS_ACTIVE = 1
STATUS_INACTIVE = 0
CREATION_BY = "system"
HTTP_REQUEST_ID = 'local_id'

DATE_FORMAT = "date_format"
TIME_FORMAT = "time_format"

DATE_YYYY_MM_DD = "%Y-%m-%d"
DATE_YYYY_MM_DD_HH_MM_SS = "%Y-%m-%d %H:%M:%S"
DATE_YYYY_MM = "%Y-%m"
TIME_HH_MM_SS = "%H:%M:%S"
DATE_MM_DD_YYYY = "%-m/%d/%Y"
DATE_DD_MM_YYYY = "%d-%m-%Y"
DATE_YYYY = "%Y"

SALTING_CONSTANT = "_user"

ALGORITHM_OF_JWT = 'RS256'
LIFE_TIME_OF_ACCESS_TOKEN = timedelta(minutes=15)
LIFE_TIME_OF_REFRESH_TOKEN = timedelta(days=365)

# The following Private key made through the OS Environment variables
PRIVATE_KEY_PATH = os.path.join(BASE_DIR, 'private_key.pem')
PUBLIC_KEY_PATH = os.path.join(BASE_DIR, 'public_key.pem')

with open(PRIVATE_KEY_PATH, "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
)

with open(PUBLIC_KEY_PATH, "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )

JWT_KEY_PRIVATE = private_key
STATUS_CODE = 'status_code'
SUCCESS_CODE = 10000
MESSAGE = 'message'

COMMON_CHECK_FORMAT_TYPE = {
    DATE_FORMAT: 10,
    TIME_FORMAT: 11
}

gender_dict = {
    "male": 1,
    "female": 2
}

