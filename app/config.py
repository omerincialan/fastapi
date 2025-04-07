from pydantic_settings import BaseSettings



#this is for validation from pydantic

class Settings(BaseSettings):
    database_hostname : str
    database_port : str
    database_password : str
    database_name : str
    database_username : str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int

    model_config = {
        "env_file": ".env"
    }
settings = Settings()

print(settings.database_username)