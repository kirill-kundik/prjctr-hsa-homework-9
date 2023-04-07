from faker import Faker

faker = Faker()


def fake_user():
    return {
        "full_name": faker.name(),
        "birth_date": fake_date(),
    }


def fake_date(minimum_age=5, maximum_age=115):
    return faker.date_of_birth(minimum_age=minimum_age, maximum_age=maximum_age)
