"""
Module to generate random users
"""

import faker
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
logging.basicConfig(filename=BASE_DIR/'user.log', level=logging.INFO)


fake = faker.Faker()

def get_user():
    """Generate a single user

    Returns:
        str: user
    """
    logging.info("Generating user.")
    return f"{fake.first_name()} {fake.last_name()}"


def get_users(n):
    """generate a list of users

    Args:
        n (int): Number of user to generate

    Returns:
        list[str]: users
    """
    logging.info(f"Generating a list of {n} user.")
    return [get_user() for _ in range(n)]

    # users = []
    # for _ in range(n):
    #     users.append(get_user())

    # return users

if __name__ == "__main__":
    user = get_users(n=5)
    print(user)

