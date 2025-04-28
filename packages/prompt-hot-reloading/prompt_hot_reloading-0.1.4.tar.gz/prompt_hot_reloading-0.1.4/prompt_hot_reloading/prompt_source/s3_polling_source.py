import time
import boto3
from prompt_hot_reloading.prompt_source.prompt_source import PromptSource
import threading

class S3PollingSource(PromptSource):
    def __init__(self, bucket: str, prefix: str = "", poll_interval: int = 30):
        self.bucket = bucket
        self.prefix = prefix.rstrip("/") + "/"
        self.poll_interval = poll_interval
        self._client = boto3.client("s3")
        # track last‐seen modification times
        self._mtimes: dict[str, float] = {}

    def load_all(self):
        prompts = {}
        resp = self._client.list_objects_v2(Bucket=self.bucket, Prefix=self.prefix)
        for obj in resp.get("Contents", []):
            key = obj["Key"]
            name = key[len(self.prefix) :].rsplit(".", 1)[0]
            text = (
                self._client.get_object(Bucket=self.bucket, Key=key)["Body"]
                .read()
                .decode()
            )
            self._mtimes[name] = obj["LastModified"].timestamp()
            prompts[name] = text
        return prompts

    def watch(self, on_change):
        def _poll():
            while True:
                resp = self._client.list_objects_v2(
                    Bucket=self.bucket, Prefix=self.prefix
                )
                for obj in resp.get("Contents", []):
                    key = obj["Key"]
                    name = key[len(self.prefix) :].rsplit(".", 1)[0]
                    mtime = obj["LastModified"].timestamp()
                    if mtime > self._mtimes.get(name, 0):
                        text = (
                            self._client.get_object(Bucket=self.bucket, Key=key)["Body"]
                            .read()
                            .decode()
                        )
                        self._mtimes[name] = mtime
                        on_change(name, text)
                time.sleep(self.poll_interval)

        t = threading.Thread(target=_poll, daemon=True)
        t.start()
