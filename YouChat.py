import requests
import uuid
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto


class ModelNotAvailableError(Exception):
    """Custom exception raised when an unavailable model is requested."""
    pass


class ChatModeNotAvailableError(Exception):
    """Custom exception raised when an unavailable chat mode is selected."""
    pass


class AIModelEnum(Enum):
    """Enum to manage available AI models."""
    OPENAI_O1 = 'openai_o1'
    OPENAI_O1_PREVIEW = 'openai_o1_preview'
    OPENAI_O1_MINI = 'openai_o1_mini'
    GPT_4O_MINI = 'gpt_4o_mini'
    GPT_4O = 'gpt_4o'
    GPT_4_TURBO = 'gpt_4_turbo'
    GPT_4 = 'gpt_4'
    GROK_2 = 'grok_2'
    CLAUDE_3_5_SONNET = 'claude_3_5_sonnet'
    CLAUDE_3_OPUS = 'claude_3_opus'
    CLAUDE_3_SONNET = 'claude_3_sonnet'
    CLAUDE_3_5_HAIKU = 'claude_3_5_haiku'
    CLAUDE_3_HAIKU = 'claude_3_haiku'
    LLAMA_3_3_70B = 'llama3_3_70b'
    LLAMA_3_2_90B = 'llama3_2_90b'
    LLAMA_3_2_11B = 'llama3_2_11b'
    LLAMA_3_1_405B = 'llama3_1_405b'
    LLAMA_3_1_70B = 'llama3_1_70b'
    LLAMA_3 = 'llama3'
    MISTRAL_LARGE_2 = 'mistral_large_2'
    GEMINI_1_5_FLASH = 'gemini_1_5_flash'
    GEMINI_1_5_PRO = 'gemini_1_5_pro'
    DBRX_INSTRUCT = 'databricks_dbrx_instruct'
    QWEN2_5_72B = 'qwen2p5_72b'
    QWEN2_5_CODER_32B = 'qwen2p5_coder_32b'
    COMMAND_R = 'command_r'
    COMMAND_R_PLUS = 'command_r_plus'
    SOLAR_1_MINI = 'solar_1_mini'
    DOLPHIN_2_5 = 'dolphin_2_5'


class ChatModeEnum(Enum):
    """Enum to manage available chat modes."""
    CUSTOM = 'custom'
    RESEARCH = 'research'
    DEFAULT = 'default'


@dataclass
class YouChatConfig:
    """Dataclass to hold configuration for the YouChat request."""
    model: AIModelEnum
    chat_mode: ChatModeEnum
    query: str
    prints: bool = True


class YouChatAPI(ABC):
    """Abstract base class to define a structure for interacting with the YouChat API."""

    @abstractmethod
    def prepare_query(self, query: str) -> str:
        """Prepares and encodes the query string for the API."""
        pass

    @abstractmethod
    def send_request(self, query: str, config: YouChatConfig) -> Dict[str, Any]:
        """Sends the request to the YouChat API and returns the response."""
        pass

    @abstractmethod
    def handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handles the response from the API."""
        pass


class YouChat(YouChatAPI):
    """Concrete implementation of YouChatAPI to interact with YouChat's API."""

    available_models: Dict[str, AIModelEnum] = {model.name: model for model in AIModelEnum}
    available_chat_modes: List[ChatModeEnum] = list(ChatModeEnum)

    def __init__(self, config: YouChatConfig):
        self.config = config
        self.validate_configuration(config)

    def validate_configuration(self, config: YouChatConfig):
        """Validates the configuration for model and chat mode."""
        if not isinstance(config.model, AIModelEnum):
            raise ModelNotAvailableError(f"Model {config.model} is not available.")
        
        if not isinstance(config.chat_mode, ChatModeEnum):
            raise ChatModeNotAvailableError(f"Chatmode {config.chat_mode} is not available.")

    def prepare_query(self, query: str) -> str:
        """Encodes the query to ensure it's properly formatted for the request."""
        replacements = {
            ' ': '%20', '?': '%3F', '&': '%26', '"': '%22', "'": '%27', ',': '%2C',
            ';': '%3B', ':': '%3A', '/': '%2F', '\\': '%5C', '|': '%7C', '=': '%3D', '+': '%2B'
        }
        for char, replacement in replacements.items():
            query = query.replace(char, replacement)
        return query

    def send_request(self, query: str, config: YouChatConfig) -> Dict[str, Any]:
        """Sends the HTTP request to the YouChat API and returns the response."""
        query = self.prepare_query(query)
        cookies = {
            'safesearch_guest': 'Moderate',
            'youchat_personalization': 'true',
            'youchat_smart_learn': 'true',
            'youpro_subscription': 'true',
            'guest_has_seen_legal_disclaimer': 'true',
            'ai_model': str(config.model.value),
            'you_subscription': 'premium',
            'DS': str(uuid.uuid4())
        }

        response = requests.get(
            f'https://you.com/api/streamingSearch?page=1&count=10&safeSearch=Moderate&utm=brave&mkt=en-IN&enable_worklow_generation_ux=true&domain=youchat&use_personalization_extraction=true&queryTraceId={uuid.uuid4()}&chatId={uuid.uuid4()}&conversationTurnId={uuid.uuid4()}&pastChatLength=0&selectedChatMode={config.chat_mode.value}&selectedAiModel={config.model.value}&enable_agent_clarification_questions=true&traceId={uuid.uuid4()}|{uuid.uuid4()}|{datetime.now().isoformat()}&use_nested_youchat_updates=true&q={query}&chat=%5B%5D',
            cookies=cookies,
            stream=True
        )
        return self.handle_response(response)

    def handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handles the API response and extracts relevant data."""
        response_dict = {'streaming_response': ''}
        
        for value in response.iter_lines(decode_unicode=True, chunk_size=1000):
            if value and 'event:' not in value:
                value = value.replace('data: ', '')
                try:
                    # Attempt to load the JSON response
                    json_value = json.loads(value)
                    
                    # Check if json_value is a list (to handle the structure more flexibly)
                    if isinstance(json_value, list):
                        for item in json_value:
                            if isinstance(item, dict):
                                related_searches = item.get('relatedSearches')
                                if related_searches:
                                    response_dict.update({'relatedSearches': related_searches})

                                query = item.get('query')
                                if query:
                                    response_dict.update({'query': item})

                                you_chat_token = item.get('youChatToken')
                                if you_chat_token:
                                    content = you_chat_token
                                    response_dict['streaming_response'] += content
                                    if self.config.prints:
                                        print(content, end='', flush=True)
                    elif isinstance(json_value, dict):
                        # Handle when the response is directly a dictionary
                        related_searches = json_value.get('relatedSearches')
                        if related_searches:
                            response_dict.update({'relatedSearches': related_searches})

                        query = json_value.get('query')
                        if query:
                            response_dict.update({'query': json_value})

                        you_chat_token = json_value.get('youChatToken')
                        if you_chat_token:
                            content = you_chat_token
                            response_dict['streaming_response'] += content
                            if self.config.prints:
                                print(content, end='', flush=True)
                except json.JSONDecodeError:
                    continue
        return response_dict

def main():
    """Main function to demonstrate YouChat interaction."""
    config = YouChatConfig(
        model=AIModelEnum.GPT_4O,  # Example model
        chat_mode=ChatModeEnum.DEFAULT,  # Example chat mode
        query="What is current AQI in New Delhi?"
    )
    
    youchat = YouChat(config)
    response = youchat.send_request(config.query, config)
    print("\nStreaming Response:", response.get('streaming_response', 'No content'))
    print("\nQuery:", response.get('query', 'No query found'))

    related_searches = response.get('relatedSearches', [])
    for search in related_searches:
        print("\nRelated Search:", search)


if __name__ == '__main__':
    main()
