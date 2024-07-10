import os
from abc import ABC, abstractmethod
import logging
from dotenv import load_dotenv

class EnvLoader(ABC):
    def __init__(self, env_file='.env', logger=None):
        """
        Load environment variables from the specified .env file.
        """
        self.env_file = env_file

        # Configure logging
        if logger is None:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

        self.load_env()

    @abstractmethod
    def load_env(self):
        """
        Load environment variables from the .env file.
        """
        pass

    @abstractmethod
    def get_api_key(self):
        """
        Return the API key.
        """
        pass

    @abstractmethod
    def get_organization(self):
        """
        Return the organization ID.
        """
        pass

    @abstractmethod
    def get_project(self):
        """
        Return the project ID.
        """
        pass

class DotenvEnvLoader(EnvLoader):
    def load_env(self):
        """
        Load environment variables from the .env file.
        """
        load_dotenv(self.env_file)
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.organization = os.getenv("OPENAI_ORG_ID")
        self.project = os.getenv("OPENAI_PROJECT_ID")

        if not self.api_key:
            self.logger.error("OpenAI API key not found in environment variables.")
            raise ValueError("OpenAI API key not found in environment variables.")

        # Check if need to change log level after loading .env file
        log_level = os.getenv("LOG_LEVEL")
        if log_level:
            self.logger.setLevel(log_level.upper())
            self.logger.info(f"Log level set to {log_level.upper()}")

    def get_api_key(self):
        return self.api_key

    def get_organization(self):
        return self.organization

    def get_project(self):
        return self.project
