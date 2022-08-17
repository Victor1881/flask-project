from enum import Enum


class UserRole(Enum):
    user = 'User'
    admin = 'Admin'


class DonatorsRewards(Enum):
    novice = "Novice"
    normal = "Normal Donator"
    super = "Super Donator"
    elite = "Elite Donator"
    vip = "V.I.P Donator"
    legendary = "Legendary Donator"
    mythic = "Mythic Donator"