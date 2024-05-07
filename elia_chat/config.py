import os
from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, SecretStr


class EliaChatModel(BaseModel):
    name: str
    """The name of the model e.g. `gpt-3.5-turbo`.
    This must match the name of the model specified by the provider.
    """
    display_name: str | None = None
    """The display name of the model in the UI."""
    provider: str | None = None
    """The provider of the model, e.g. openai, anthropic, etc"""
    api_key: SecretStr | None = None
    """If set, this will be used in place of the environment variable that
    would otherwise be used for this model (instead of OPENAI_API_KEY,
    ANTHROPIC_API_KEY, etc.)."""
    api_base: AnyHttpUrl | None = None
    """If set, this will be used as the base URL for making API calls.
    This can be useful if you're hosting models on a LocalAI server, for
    example."""
    organization: str | None = None
    """Some providers, such as OpenAI, allow you to specify an organization.
    In the case of """
    description: str | None = Field(default=None)
    """A description of the model which may appear inside the Elia UI."""
    product: str | None = Field(default=None)
    """For example `ChatGPT`, `Claude`, `Gemini`, etc."""
    temperature: int = Field(default=1.0)
    """The temperature to use. Low temperature means the same prompt is likely
    to produce similar results. High temperature means a flatter distribution
    when predicting the next token, and so the next token will be more random.
    Setting a very high temperature will likely produce junk output."""
    max_retries: int = Field(default=0)
    """The number of times to retry a request after it fails before giving up."""


def get_builtin_openai_models() -> list[EliaChatModel]:
    return [
        EliaChatModel(
            name="gpt-3.5-turbo",
            display_name="GPT-3.5 Turbo",
            provider="OpenAI",
            product="ChatGPT",
            description="The fastest ChatGPT model, great for most everyday tasks",
        ),
        EliaChatModel(
            name="gpt-4-turbo",
            display_name="GPT-4 Turbo",
            provider="OpenAI",
            product="ChatGPT",
            description="The most powerful ChatGPT model, capable of "
            "complex tasks which require advanced reasoning",
        ),
    ]


def get_builtin_anthropic_models() -> list[EliaChatModel]:
    return [
        EliaChatModel(
            name="claude-3-haiku-20240307",
            display_name="Claude 3 Haiku",
            provider="Anthropic",
            product="Claude 3",
            description=(
                "Fastest and most compact model for near-instant responsiveness"
            ),
        ),
        EliaChatModel(
            name="claude-3-sonnet-20240229",
            display_name="Claude 3 Sonnet",
            provider="Anthropic",
            product="Claude 3",
            description=(
                "Ideal balance of intelligence and speed for enterprise workloads"
            ),
        ),
        EliaChatModel(
            name="claude-3-opus-20240229",
            display_name="Claude 3 Opus",
            provider="Anthropic",
            product="Claude 3",
            description="Most powerful model for highly complex tasks",
        ),
    ]


def get_builtin_models() -> list[EliaChatModel]:
    return get_builtin_openai_models() + get_builtin_anthropic_models()


class LaunchConfig(BaseModel):
    """The config of the application at launch.

    Values may be sourced via command line options, env vars, config files.
    """

    model_config = ConfigDict(frozen=True)

    default_model: str = Field(default="gpt-3.5-turbo")
    system_prompt: str = Field(
        default=os.getenv(
            "ELIA_SYSTEM_PROMPT", "You are a helpful assistant named Elia."
        )
    )
    models: list[EliaChatModel] = Field(default_factory=list)
    builtin_models: list[EliaChatModel] = Field(
        default_factory=get_builtin_models, init=False
    )

    @property
    def all_models(self) -> list[EliaChatModel]:
        return self.models + self.builtin_models