# Prompt Hot Reloading

Prompt hot reloading is a technique that allows you to update your prompts without restarting your application. This is useful for development and testing, as you can make changes to your prompts and see the results immediately.

## Getting Started

### Installation

```bash
pip install prompt-hot-reloading
```

### Usage

The prompt registry is a simple dictionary that maps prompt names to prompt text. It listens for changes to the prompt source and updates the registry accordingly.

```python
from prompt_hot_reloading.prompt_source.file_system_source import FileSystemSource
from prompt_hot_reloading import PromptRegistry

prompt_source = FileSystemSource("prompts")
prompt_registry = PromptRegistry(prompt_source)

def handle_message(user_message: str):
    completion = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "developer", "content": prompt_registry["system_prompt"]},
            {"role": "user", "content": user_message}
        ]
    )

    return completion.choices[0].message.content
```

### Deployment

The `create_prompt_registry` function is a factory that picks the appropriate prompt source based on the `PROMPT_SOURCE` environment variable. Today, we support `fs` (file system) and `s3` (S3 polling).

```python
from prompt_hot_reloading import create_prompt_registry

prompt_registry = create_prompt_registry()
```

### Environment Variables

- `PROMPT_SOURCE`: The type of prompt source to use. Currently, we support `fs` (file system) and `s3` (S3 polling).
- `PROMPT_DIR`: The path to the directory containing the prompt files.
- `PROMPT_S3_BUCKET`: The name of the S3 bucket containing the prompt files.
- `PROMPT_S3_PREFIX`: The prefix of the S3 key containing the prompt files.
- `PROMPT_S3_POLL_INTERVAL`: The interval in seconds to poll the S3 bucket for changes.


## Miscellaneous

### Creator

Steve Krawczyk

- [github/steventkrawczyk](https://github.com/steventkrawczyk)
- [linkedin/steventkrawczyk](https://www.linkedin.com/in/steventkrawczyk/)
- [x/KrawfyS](https://x.com/KrawfyS)

### Contributing

Contributions are welcome! Please feel free to submit a pull request.

### License

[MIT](LICENSE)
