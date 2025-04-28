from readerwriterlock import rwlock
from contextlib import contextmanager


class PromptMap:
    def __init__(self):
        self.prompts = {}
        self._lock = rwlock.RWLockFair()

    @contextmanager
    def _read_lock(self):
        with self._lock.gen_rlock():
            yield

    @contextmanager
    def _write_lock(self):
        with self._lock.gen_wlock():
            yield

    def __setitem__(self, key, item):
        with self._write_lock():
            self.prompts[key] = item

    def __getitem__(self, key):
        with self._read_lock():
            return self.prompts[key]

    def __repr__(self):
        with self._read_lock():
            return repr(self.prompts)

    def __len__(self):
        with self._read_lock():
            return len(self.prompts)

    def __delitem__(self, key):
        with self._write_lock():
            del self.prompts[key]

    def clear(self):
        with self._write_lock():
            self.prompts.clear()

    def copy(self):
        with self._read_lock():
            return self.prompts.copy()

    def has_key(self, k):
        with self._read_lock():
            return k in self.prompts

    def update(self, *args, **kwargs):
        with self._write_lock():
            return self.prompts.update(*args, **kwargs)

    def keys(self):
        with self._read_lock():
            return self.prompts.keys()

    def values(self):
        with self._read_lock():
            return self.prompts.values()

    def items(self):
        with self._read_lock():
            return self.prompts.items()

    def pop(self, *args):
        with self._write_lock():
            return self.prompts.pop(*args)

    def __cmp__(self, dict_):
        with self._read_lock():
            return self.__cmp__(self.prompts, dict_)

    def __contains__(self, item):
        with self._read_lock():
            return item in self.prompts

    def __iter__(self):
        with self._read_lock():
            return iter(self.prompts)

    def __unicode__(self):
        with self._read_lock():
            return str(repr(self.prompts))
