from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

HOME = Path.home().expanduser()
PROJECT_CONFIG_ROOT = HOME / ".ga"
WORKSPACE_ROOT = PROJECT_CONFIG_ROOT / "workspace"
OUTPUT_ROOT = PROJECT_CONFIG_ROOT / "output"


class Config:
    token_path = PROJECT_CONFIG_ROOT / "azure_token"
    workspace_path = WORKSPACE_ROOT / f"{Path.cwd().name}"
    output_callback_path = OUTPUT_ROOT / f"{Path.cwd().name}.md"

    def read_token(cls) -> str:
        if cls.token_path.exists():
            return cls.token_path.read_text()
        else:
            return ""

    def write_token(cls, token: str):
        cls.token_path.write_text(token)


settings = Config()
