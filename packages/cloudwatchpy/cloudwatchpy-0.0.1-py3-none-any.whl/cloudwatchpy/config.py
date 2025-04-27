from .utils import get_env_variable

class Config:
    @property
    def AWS_ACCESS_KEY_ID(self):
        return get_env_variable("AWS_ACCESS_KEY_ID")

    @property
    def AWS_SECRET_ACCESS_KEY(self):
        return get_env_variable("AWS_SECRET_ACCESS_KEY")

    @property
    def AWS_REGION(self):
        return get_env_variable("AWS_REGION", "us-east-1")

    @property
    def LOG_GROUP(self):
        return get_env_variable("CLOUDWATCH_LOG_GROUP")

    @property
    def LOG_BATCH_SIZE(self):
        return int(get_env_variable("LOG_BATCH_SIZE", "10"))

    @property
    def ENABLE_COMPRESSION(self):
        return get_env_variable("LOG_COMPRESSION", "true").lower() == "true"

    def is_cloudwatch_enabled(self):
        return all([
            self.AWS_ACCESS_KEY_ID,
            self.AWS_SECRET_ACCESS_KEY,
            self.LOG_GROUP
        ])


# Use Config instance instead of class attributes now:
Config = Config()
