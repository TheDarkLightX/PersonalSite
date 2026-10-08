#!/usr/bin/env python3
"""Ensure verification refuses modes that disable its assertion gates."""
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parent


class VerificationModeTests(unittest.TestCase):
    def test_optimized_execution_refuses_before_verification(self):
        for name in ('check_case.py', 'check_lean.py', 'replay.py'):
            for flags, setting in ((['-O'], ''), (['-OO'], ''), ([], '1')):
                with self.subTest(script=name, flags=flags, environment=setting):
                    env = dict(os.environ)
                    env.pop('PYTHONOPTIMIZE', None)
                    if setting:
                        env['PYTHONOPTIMIZE'] = setting
                    result = subprocess.run(
                        [sys.executable, *flags, str(ROOT / name)],
                        env=env, text=True, capture_output=True, timeout=10)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn('Verification requires assertions', result.stderr)
                    self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
