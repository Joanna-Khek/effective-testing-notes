import os
import unittest

class TestAddCleanupForEnv(unittest.TestCase):
    def setUp(self) -> None:
        old_mode = os.environ.get("TINYLM_MODE")
        self.addCleanup(self._restore_env, "TINYLM_MODE", old_mode)
        
        
    def _restore_env(self, key: str, old_value) -> None:
        if old_value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = old_value

    def test_env_is_restored_even_on_failure(self) -> None:
        os.environ["TINYLM_MODE"] = "demo"
        self.assertEqual(os.environ["TINYLM_MODE"], "demo")