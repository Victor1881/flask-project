from resources.auth import Register, LoginResource
from resources.donation import CreateDonation

routes = (
    (Register, "/register/"),
    (LoginResource, "/login/"),
    (CreateDonation, "/create/"),
)