from itertools import product

from faker import Faker

fake = Faker(locale='pt-BR')
domains = [
    'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com', 'icloud.com', 'mail.com', 'protonmail.com',
    'zoho.com', 'yandex.com', 'inbox.com', 'gmx.com', 'live.com', 'me.com', 'fastmail.com', 'tutanota.com',
    'rocketmail.com', 'aim.com', 'mail.ru', 'earthlink.net'
]

co = [
    '.br', '.us', '.mx', '.ca', '.uk', '.de', '.fr', '.it', '.es', '.jp', '.cn', '.in', '.ru', '.au', '.kr', '.sa',
    '.ae', '.nz', '.ch', '.sg', '.id', '.th', '.nl', '.ar', '.tr', '.co', '.ph', '.se', '.vn', '.cl', '.my'
]


async def make_random_user(password_length=9):
    return {
        "email": fake.email(domain=fake.random_element([f'{domain}{c}' for domain, c in product(domains, co)])),
        "password": fake.password(
            length=password_length, special_chars=True, digits=True, upper_case=True, lower_case=True
        ),
        'admin': False,
        'email_confirmed': False,
    }
