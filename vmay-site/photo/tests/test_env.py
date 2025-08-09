import os


def test_env():
    required_envs = [
        'POSTGRES_DB',
        'POSTGRES_USER',
        'POSTGRES_PASSWORD',
        'POSTGRES_HOST',
        'POSTGRES_PORT'
    ]
    for var in required_envs:
        assert os.getenv(var), f"Environment variable {var} is not set"
