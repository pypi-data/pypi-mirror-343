from prompt_hot_reloading.prompt_registry.prompt_map import PromptMap
from prompt_hot_reloading.prompt_source.prompt_source import PromptSource

class PromptRegistry(PromptMap):
    def __init__(self, prompt_source: PromptSource):
        super().__init__()
        self.prompt_source = prompt_source
        self.prompts = prompt_source.load_all()
        self.prompt_source.watch(self._update_prompt)

    def _update_prompt(self, name: str, text: str):
        self.prompts[name] = text
