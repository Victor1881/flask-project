from resources.auth import Register, LoginResource
from resources.donation import CreateDonation, Donate, Reward, DeleteUser

routes = (
    (Register, "/register/"),
    (LoginResource, "/login/"),
    (CreateDonation, "/create/"),
    (Donate, "/donate/"),
    (Reward, "/user/<int:id>/reward/"),
    (DeleteUser, "/user/<int:id>/delete/"),
)