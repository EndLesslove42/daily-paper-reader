"""Integration tests use disposable local bare remotes; never push to GitHub."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / "tools/windows/workflow.py"
spec = importlib.util.spec_from_file_location("windows_workflow", SOURCE)
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)

class WindowsSyncTests(unittest.TestCase):
    def git(self, directory, *args):
        p = subprocess.run(["git", *args], cwd=directory, capture_output=True)
        if p.returncode:
            raise AssertionError(p.stderr.decode("utf-8", "replace"))
        return p.stdout.decode("utf-8", "replace").strip()
    def put(self, root, name, content):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="dpr windows test ")
        self.base = Path(self.temp.name)
        self.remote = self.base / "remote.git"
        self.local = self.base / "local repo"
        self.peer = self.base / "actions"
        self.git(self.base, "init", "--bare", "--initial-branch=main", str(self.remote))
        self.git(self.base, "clone", str(self.remote), str(self.local))
        self.git(self.local, "config", "user.name", "Fixture")
        self.git(self.local, "config", "user.email", "fixture@example.invalid")
        self.put(self.local, ".gitignore", ".env\n*.log\nlogs/\n.local_backup/\nsecret.private\n")
        self.put(self.local, "config.yaml", "query: old\n\n\n\n\n\nlimit: 10\n")
        self.put(self.local, "docs/report.md", "old")
        self.git(self.local, "add", ".gitignore", "config.yaml", "docs/report.md")
        self.git(self.local, "commit", "-m", "fixture")
        self.git(self.local, "push", "origin", "main")
        self.git(self.base, "clone", str(self.remote), str(self.peer))
        self.git(self.peer, "config", "user.name", "Actions fixture")
        self.git(self.peer, "config", "user.email", "fixture@example.invalid")
        self.previous = w.ROOT
        w.ROOT = self.local
    def tearDown(self):
        w.ROOT = self.previous
        self.temp.cleanup()
    def publish(self, changes):
        for name, value in changes.items():
            self.put(self.peer, name, value)
            self.git(self.peer, "add", "--", name)
        self.git(self.peer, "commit", "-m", "remote update")
        self.git(self.peer, "push", "origin", "main")
    def sync(self):
        with contextlib.redirect_stdout(io.StringIO()):
            w.sync()
    def test_generated_collision_and_only_config_committed(self):
        self.put(self.local, "config.yaml", "query: local\n")
        self.put(self.local, "docs/report.md", "local tracked output")
        self.put(self.local, "docs/new/result.md", "local untracked output")
        self.put(self.local, ".env", "DO_NOT_COMMIT=fixture")
        self.put(self.local, "logs/test.log", "private log")
        encrypted = json.dumps(dict(version=1, salt="YWJj", iv="YWJj", ciphertext="YWJj"))
        self.put(self.local, "secret.private", encrypted)
        self.publish({"docs/report.md":"remote output", "docs/new/result.md":"remote collision"})
        self.sync()
        self.assertEqual((self.local/"config.yaml").read_text(), "query: local\n")
        self.assertEqual((self.local/"docs/new/result.md").read_text(), "remote collision")
        self.assertEqual((self.local/"docs/report.md").read_text(), "remote output")
        tracked = self.git(self.local, "ls-files").splitlines()
        self.assertIn("secret.private", tracked)
        self.assertNotIn(".env", tracked)
        self.assertFalse(any(p.startswith(("logs/",".local_backup/")) for p in tracked))
        changed = self.git(self.local,"diff-tree","--no-commit-id","--name-only","-r","HEAD").splitlines()
        self.assertEqual(set(changed), {"config.yaml","secret.private"})
        self.assertTrue(list((self.local/".local_backup").glob("*/generated/docs/new/result.md")))
    def test_no_changes_is_success(self):
        before = self.git(self.local,"rev-parse","HEAD")
        self.sync()
        self.assertEqual(before,self.git(self.local,"rev-parse","HEAD"))
    def test_same_line_conflict_keeps_both(self):
        self.put(self.local,"config.yaml","query: local\n")
        self.publish({"config.yaml":"query: remote\n"})
        with self.assertRaisesRegex(RuntimeError, "冲突"):
            self.sync()
        self.assertEqual((self.local/"config.yaml").read_text(),"query: local\n")
        self.assertTrue(list((self.local/".local_backup").glob("*/remote/config.yaml")))
    def test_nonoverlapping_config_merge(self):
        self.put(self.local,"config.yaml","query: local\n\n\n\n\n\nlimit: 10\n")
        self.publish({"config.yaml":"query: old\n\n\n\n\n\nlimit: 30\n"})
        self.sync()
        self.assertIn("query: local",(self.local/"config.yaml").read_text())
        self.assertIn("limit: 30",(self.local/"config.yaml").read_text())
    def test_tracked_env_blocks_before_backup(self):
        self.put(self.local,".env","PRIVATE=fixture")
        self.git(self.local,"add","-f",".env")
        self.git(self.local,"commit","-m","unsafe fixture")
        with self.assertRaisesRegex(RuntimeError, "敏感"):
            self.sync()
        self.assertFalse((self.local/".local_backup").exists())
    def test_staged_unrelated_file_blocks(self):
        self.put(self.local,"other.txt","preserve")
        self.git(self.local,"add","other.txt")
        with self.assertRaisesRegex(RuntimeError, "暂存"):
            self.sync()
        self.assertEqual(self.git(self.local,"diff","--cached","--name-only"),"other.txt")
    def test_plaintext_secret_and_config_rejected(self):
        with self.assertRaises(RuntimeError):
            w.check_secret(b'{"apiKey":"private"}')
        with self.assertRaises(RuntimeError):
            w.check_config(b"github:\n  token: private\n")
    def test_push_race_rebases_automatically(self):
        self.put(self.local,"config.yaml","query: local\n")
        real_git = w.git
        raced = False
        def racing_git(*args, **kwargs):
            nonlocal raced
            if args[0] == "push" and not raced:
                raced = True
                self.publish({"docs/race.md":"concurrent Actions output"})
            return real_git(*args,**kwargs)
        with patch.object(w,"git",side_effect=racing_git):
            self.sync()
        self.assertTrue((self.local/"docs/race.md").exists())
        self.assertEqual(self.git(self.local,"rev-parse","HEAD"),self.git(self.remote,"rev-parse","main"))
    def test_nonconfig_outgoing_commit_blocks(self):
        self.put(self.local,"code.txt","preserve")
        self.git(self.local,"add","code.txt")
        self.git(self.local,"commit","-m","unpublished code")
        with self.assertRaisesRegex(RuntimeError, "非配置"):
            self.sync()
if __name__ == "__main__":
    unittest.main()
