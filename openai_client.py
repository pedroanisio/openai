import logging
from openai import OpenAI
from env_loader import DotenvEnvLoader

class OpenAIClient:
    _instance = None

    def __new__(cls, env_loader=None, logger=None):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, env_loader=None, logger=None):
        """
        Initialize the OpenAI client with credentials from environment variables.
        """
        if self._initialized:
            return

        if logger is None:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

        self.logger.info("Initializing OpenAI client")

        if env_loader is None:
            env_loader = DotenvEnvLoader()

        self.env_loader = env_loader

        api_key = self.env_loader.get_api_key()
        organization = self.env_loader.get_organization()
        project = self.env_loader.get_project()

        if not api_key:
            self.logger.error("OpenAI API key not found.")
            raise ValueError("OpenAI API key not found.")
        
        if not organization:
            self.logger.warning("OpenAI organization ID not found.")
        
        if not project:
            self.logger.warning("OpenAI project ID not found.")

        # Initialize OpenAI client with the obtained credentials
        self.client = OpenAI(
            api_key=api_key,
            organization=organization,
            project=project
        )

        self._initialized = True
        self.logger.info("OpenAI client initialized successfully.")

# Example usage:
# env_loader = DotenvEnvLoader()
# client = OpenAIClient(env_loader)
