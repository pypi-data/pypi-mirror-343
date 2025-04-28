import os
from prompt_hot_reloading.prompt_registry.prompt_registry import PromptRegistry
from prompt_hot_reloading.prompt_source.file_system_source import FileSystemSource
from prompt_hot_reloading.prompt_source.s3_polling_source import S3PollingSource

def create_prompt_registry() -> PromptRegistry:
    """
    Factory that picks FileSystemSource vs. S3PollingSource based on PROMPT_SOURCE env
    """
    source_type = os.getenv("PROMPT_SOURCE", "fs").lower()

    if source_type == "s3":
        bucket   = os.environ["PROMPT_S3_BUCKET"]
        prefix   = os.getenv("PROMPT_S3_PREFIX", "")
        interval = int(os.getenv("PROMPT_S3_POLL_INTERVAL", "30"))
        source   = S3PollingSource(bucket=bucket, prefix=prefix, poll_interval=interval)

    else:
        prompt_dir = os.getenv("PROMPT_DIR", "prompts")
        source     = FileSystemSource(prompt_dir)


    return PromptRegistry(source=source)
