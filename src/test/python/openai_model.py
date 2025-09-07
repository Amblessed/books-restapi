from enum import Enum
from collections import namedtuple

ModelSpec = namedtuple("ModelSpec", ["model_name", "model_type", "tpm", "rpm", "tpd"])

class OpenAIModel(Enum):
    # GPT-3.5
    GPT_3_5_TURBO = ModelSpec("gpt-3.5-turbo", "chat", 200_000, 500, 2_000_000)
    GPT_3_5_TURBO_0125 = ModelSpec("gpt-3.5-turbo-0125", "chat", 200_000, 500, 2_000_000)
    GPT_3_5_TURBO_1106 = ModelSpec("gpt-3.5-turbo-1106", "chat", 200_000, 500, 2_000_000)
    GPT_3_5_TURBO_16K = ModelSpec("gpt-3.5-turbo-16k", "chat", 200_000, 500, 2_000_000)
    GPT_3_5_TURBO_INSTRUCT = ModelSpec("gpt-3.5-turbo-instruct", "chat", 90_000, 3_500, 200_000)

    # GPT-4
    GPT_4 = ModelSpec("gpt-4", "chat", 10_000, 500, 100_000)
    GPT_4_0613 = ModelSpec("gpt-4-0613", "chat", 10_000, 500, 100_000)
    GPT_4_TURBO = ModelSpec("gpt-4-turbo", "chat", 30_000, 500, 90_000)
    
    # GPT-4o
    GPT_4O = ModelSpec("gpt-4o", "chat", 30_000, 500, 90_000)
    GPT_4O_MINI = ModelSpec("gpt-4o-mini", "chat", 200_000, 500, 2_000_000)
    GPT_4O_AUDIO_PREVIEW = ModelSpec("gpt-4o-audio-preview", "audio", 250_000, 3_000, None)
    GPT_4O_MINI_SEARCH_PREVIEW = ModelSpec("gpt-4o-mini-search-preview", "search", 6_000, 100, None)
    GPT_4O_MINI_TRANSCRIBE = ModelSpec("gpt-4o-mini-transcribe", "transcribe", 50_000, 500, None)
    GPT_4O_SEARCH_PREVIEW = ModelSpec("gpt-4o-search-preview", "search", 6_000, 100, None)
    GPT_4O_TRANSCRIBE = ModelSpec("gpt-4o-transcribe", "transcribe", 10_000, 500, None)

    # GPT-4.1
    GPT_4_1 = ModelSpec("gpt-4.1", "chat", 30_000, 500, 900_000)
    GPT_4_1_MINI = ModelSpec("gpt-4.1-mini", "chat", 200_000, 500, 2_000_000)
    GPT_4_1_NANO = ModelSpec("gpt-4.1-nano", "chat", 200_000, 500, 2_000_000)
    GPT_4_1_MINI_LONG = ModelSpec("gpt-4.1-mini-long", "chat", 400_000, 200, 4_000_000)
    GPT_4_1_NANO_LONG = ModelSpec("gpt-4.1-nano-long", "chat", 400_000, 200, 4_000_000)

    # GPT-5
    GPT_5_MAIN = ModelSpec("gpt-5-main", "chat", 30_000, 500, 900_000)
    GPT_5_MAIN_MINI = ModelSpec("gpt-5-main-mini", "chat", 200_000, 500, 2_000_000)
    GPT_5_THINKING = ModelSpec("gpt-5-thinking", "chat", 30_000, 500, 900_000)
    GPT_5_THINKING_MINI = ModelSpec("gpt-5-thinking-mini", "chat", 200_000, 500, 2_000_000)
    GPT_5_THINKING_NANO = ModelSpec("gpt-5-thinking-nano", "chat", 200_000, 500, 2_000_000)

    # o-series reasoning
    O1_PREVIEW = ModelSpec("o1-preview", "chat", 10_000, 500, 100_000)
    O1_MINI = ModelSpec("o1-mini", "chat", 200_000, 500, 2_000_000)
    O1_PRO = ModelSpec("o1-pro", "chat", 30_000, 500, 900_000)
    O3_MINI = ModelSpec("o3-mini", "chat", 200_000, 500, 2_000_000)
    O3_MINI_HIGH = ModelSpec("o3-mini-high", "chat", 200_000, 500, 2_000_000)
    O3 = ModelSpec("o3", "chat", 30_000, 500, 900_000)
    O3_PRO = ModelSpec("o3-pro", "chat", 30_000, 500, 900_000)
    O4_MINI = ModelSpec("o4-mini", "chat", 200_000, 500, 2_000_000)
    O4_MINI_HIGH = ModelSpec("o4-mini-high", "chat", 200_000, 500, 2_000_000)

    # Properties to access attributes
    @property
    def model_name(self): return self.value.model_name

    @property
    def model_type(self): return self.value.model_type

    @property
    def tpm(self): return self.value.tpm

    @property
    def rpm(self): return self.value.rpm

    @property
    def tpd(self): return self.value.tpd

    # Convenience type checks
    def is_chat_model(self): return self.model_type == "chat"
    def is_audio_model(self): return self.model_type == "audio"
    def is_realtime_model(self): return self.model_type == "realtime"
    def is_search_model(self): return self.model_type == "search"
    def is_transcribe_model(self): return self.model_type == "transcribe"


# Optional helper function to get the cheapest model by TPM
def get_cheapest_model(models, task_type="chat"):
    filtered = [m for m in models if m.model_type == task_type]
    if not filtered:
        raise ValueError(f"No models found for task type '{task_type}'")
    return min(filtered, key=lambda m: m.tpm)


def get_learning_model(models):
    """
    Returns the cheapest chat model suitable for online learning/practice.
    """
    return get_cheapest_model(models, task_type="chat")