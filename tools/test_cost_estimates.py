import math
import subprocess
import tempfile
import unittest
from pathlib import Path

from collect_cost_estimates import collect, model

SCENARIOS = {
    "low": {"coefficient": 2.4, "exponent": 1.05, "annual_wage_usd": 135980, "labor_multiplier": 1.5},
    "high": {"coefficient": 3.0, "exponent": 1.12, "annual_wage_usd": 214670, "labor_multiplier": 1.38},
}


class CostEstimatesTest(unittest.TestCase):
    def test_one_ksloc_uses_person_months_not_years(self):
        result = model(1000, SCENARIOS)
        self.assertEqual(result['low'], {'person_months': 2.4, 'cost_usd': 40794})
        self.assertEqual(result['high'], {'person_months': 3.0, 'cost_usd': 74061})
        self.assertEqual(model(0, SCENARIOS)['low']['cost_usd'], 0)
        self.assertEqual(model(4000, SCENARIOS, .25), result)

    def test_invalid_cost_inputs_fail(self):
        for lines, fraction in [(-1, 1), (1000, -1), (1000, math.nan), (1000, 1.1)]:
            with self.assertRaises(ValueError):
                model(lines, SCENARIOS, fraction)
        with self.assertRaises(ValueError):
            model(1000, {'bad': dict(SCENARIOS['low'], annual_wage_usd=math.inf)})

    def test_count_reads_pinned_objects_and_retains_documented_filters(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            def git(*args):
                return subprocess.check_output(['git', '-C', tmp, *args], stderr=subprocess.DEVNULL).decode().strip()
            git('init', '-q')
            for path, content in {
                'src/app.py': '# A comment\nx = 1\n\n',
                'tests/test_app.py': '# A comment\nx = 1\n\n',
                'proofs/example.lean': '-- comment\nexample : True := True.intro\n',
                'vendor/library.py': 'excluded = True\n',
                'generated/output.py': 'excluded = True\n',
                'data/input.py': 'excluded = True\n',
                'README.md': 'Not a source file\n',
            }.items():
                target = root/path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content)
            (root/'link.py').symlink_to('src/app.py')
            git('add', '.')
            git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'fixture')
            repo = {'name': 'MPRD', 'commit': git('rev-parse', 'HEAD'), 'tree': git('rev-parse', 'HEAD^{tree}')}
            (root/'src/app.py').write_text('changed locally\n' * 100)
            (root/'untracked.py').write_text('untracked\n' * 100)
            git('add', 'src/app.py')
            result, manifest = collect(root, repo)
            self.assertEqual(result['selected_files'], 3)
            self.assertEqual(result['selected_nonblank_lines'], 6)
            self.assertEqual(result['exact_duplicate_nonblank_lines_within_repo'], 2)
            self.assertEqual({row['path'] for row in manifest}, {'src/app.py', 'tests/test_app.py', 'proofs/example.lean'})
            with self.assertRaises(ValueError):
                collect(root, dict(repo, tree='0'*40))
            with self.assertRaises(ValueError):
                collect(root, dict(repo, commit='HEAD'))


if __name__ == '__main__':
    unittest.main()
