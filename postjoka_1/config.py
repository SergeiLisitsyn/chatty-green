from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_name: str = "chattydb_v1"
    db_user: str = "chattydb_v1_user"
    db_password: str = "cd4gpaNSyycyHFqJrXXTdqfeg7pZQeg"
    db_host: str = "dpg-d0vutevdiees73f95v70-a"
    db_port: int = 5432
    post_limit: int = 10000

    data_source: str = "file"  # 'file' or 'database'
    data_path: str = "./data/posts.json"

    class Config:
        env_file = ".env"


settings = Settings()
