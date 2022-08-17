from resources.auth import Register, LoginResource
from resources.donation import CreateDonation, Donate, Reward

routes = (
    (Register, "/register/"),
    (LoginResource, "/login/"),
    (CreateDonation, "/create/"),
    (Donate, "/donate/"),
    (Reward, "/user/<int:id>/reward/"),
)