from resources.auth import Register, LoginResource
from resources.donation import CreateDonation, Donate

routes = (
    (Register, "/register/"),
    (LoginResource, "/login/"),
    (CreateDonation, "/create/"),
    (Donate, "/donate/"),
)