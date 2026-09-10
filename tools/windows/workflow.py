"""Native Windows Git workflow; backup before modifying user files."""
from __future__ import annotations
import base64, json, os, re, shutil, subprocess, sys
from pathlib import Path
from datetime import datetime
ROOT = Path(__file__).resolve().parents[2]
if os.name == "nt" and not str(ROOT).startswith("\\\\?\\"):
    ROOT = Path("\\\\?\\" + str(ROOT))
CONFIG = {"config.yaml", "secret.private"}
TRAILERS = "\n\nCo-Authored-By: lilmortyj <781113402@qq.com>\nCo-Authored-By: xixi <3495302215@qq.com>\nCo-Authored-By: wy <345619498@qq.com>"
TOKEN = re.compile(rb"(?<![A-Za-z0-9])(?:sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})")
def git(*args, check=True):
    p = subprocess.run(["git", *args], cwd=ROOT, capture_output=True)
    if check and p.returncode:
        conflicts = git("diff", "--name-only", "--diff-filter=U", check=False).stdout.decode("utf-8", "replace")
        raise RuntimeError("Git 操作失败: " + args[0] + " (exit " + str(p.returncode) + ")" +
            ("\n冲突文件:\n" + conflicts if conflicts else "\n请检查网络、Git 登录或仓库状态；备份已保留。"))
    return p
def text(*args):
    return git(*args).stdout.decode("utf-8", "replace").strip()
def paths(*args):
    return [s.decode("utf-8") for s in git(*args, "-z").stdout.split(b"\0") if s]
def safe_path(name):
    p = ROOT / name
    if not p.resolve().is_relative_to(ROOT.resolve()) or p.is_symlink():
        raise RuntimeError("拒绝处理仓库外路径或符号链接: " + name)
    return p
def generated(p):
    return p.startswith(("docs/", "archive/"))
def sensitive(p):
    return ((p == ".env" or p.startswith(".env.")) and p != ".env.example") or p.startswith(("logs/", ".local_backup/")) or p.endswith(".log")
def preflight():
    if text("branch", "--show-current") != "main":
        raise RuntimeError("请在 main 运行日常同步；当前工作分支保持不变。")
    for marker in ("MERGE_HEAD", "rebase-merge", "rebase-apply", "CHERRY_PICK_HEAD"):
        if (ROOT / text("rev-parse", "--git-path", marker)).exists():
            raise RuntimeError("仓库已有未完成的合并/rebase。")
    if paths("diff", "--name-only", "--diff-filter=U"):
        raise RuntimeError("仓库存在未解决冲突。")
    tracked = paths("ls-files")
    bad = [p for p in tracked if sensitive(p)]
    if bad:
        raise RuntimeError("禁止同步，敏感/运行态文件已被跟踪: " + ", ".join(bad))
    if paths("diff", "--cached", "--name-only"):
        raise RuntimeError("已有暂存改动，请先处理暂存区，避免夹带提交。")
    dirty = paths("diff", "--name-only")
    other = [p for p in dirty if p not in CONFIG and not generated(p)]
    if other:
        raise RuntimeError("存在其它代码改动，未自动覆盖: " + ", ".join(other))
    for p in CONFIG:
        if p in tracked and not safe_path(p).exists():
            raise RuntimeError("用户配置被删除，停止同步: " + p)
    return dirty, tracked
def check_config(data):
    if TOKEN.search(data):
        raise RuntimeError("config.yaml 检测到疑似明文密钥，停止提交（不显示内容）。")
    import yaml
    config = yaml.safe_load(data)
    def visit(v):
        if isinstance(v, dict):
            for k, value in v.items():
                key = re.sub(r"[^a-z]", "", str(k).lower())
                if key in {"apikey", "token", "githubtoken", "password", "secret", "servicekey"} and value:
                    if isinstance(value, str) and (value.startswith(chr(36) + "{") or value.startswith("env:")):
                        continue
                    raise RuntimeError("config.yaml 存在非空凭据字段，请移至 .env 或加密配置。")
                visit(value)
        elif isinstance(v, list):
            for item in v:
                visit(item)
    visit(config)
def check_secret(data):
    try:
        s = json.loads(data)
        if set(s) != {"version", "salt", "iv", "ciphertext"}:
            raise ValueError()
        for k in ("salt", "iv", "ciphertext"):
            if not isinstance(s[k], str) or not base64.b64decode(s[k], validate=True):
                raise ValueError()
    except Exception:
        raise RuntimeError("secret.private 不是项目预期的加密载荷，停止提交。") from None
def backup():
    b = ROOT / ".local_backup" / datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    b.mkdir(parents=True)
    print("备份目录: " + str(b))
    return b
def copy_to(b, name):
    p = safe_path(name)
    if p.is_file():
        target = b / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, target)
def blob(ref, name):
    p = git("show", ref + ":" + name, check=False)
    data = p.stdout if p.returncode == 0 else None
    return data.replace(b"\r\n", b"\n") if data is not None and name == "config.yaml" else data
def validate(name, data):
    if data is not None:
        (check_config if name == "config.yaml" else check_secret)(data)
def sync():
    git("config", "--local", "core.longpaths", "true")
    dirty, tracked = preflight()
    print(text("status", "--short"))
    local = {p: safe_path(p).read_bytes() if safe_path(p).exists() else None for p in CONFIG}
    if local["config.yaml"] is not None:
        local["config.yaml"] = local["config.yaml"].replace(b"\r\n", b"\n")
    for p, data in local.items():
        validate(p, data)
    b = backup()
    for p in CONFIG:
        copy_to(b / "local", p)
    git("fetch", "origin")
    outgoing = text("log", "--format=", "--name-only", "origin/main..HEAD").splitlines()
    if any(p and p not in CONFIG for p in outgoing):
        raise RuntimeError("main 存在尚未推送的非配置提交，停止以免夹带推送。")
    base = text("merge-base", "HEAD", "origin/main")
    merged = {}
    for p in CONFIG:
        ancestor, remote, ours = blob(base, p), blob("origin/main", p), local[p]
        for label, data in (("base", ancestor), ("remote", remote)):
            if data is not None:
                target = b / label / p
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
        if ours == ancestor:
            merged[p] = remote
        elif remote == ancestor or remote == ours:
            merged[p] = ours
        else:
            if p == "secret.private" or None in (ancestor, remote, ours):
                raise RuntimeError(p + " 双方均修改，已保留 local/base/remote 版本，请人工确认。")
            candidate = b / "merged-config.yaml"
            candidate.write_bytes(ours)
            result = git("merge-file", str(candidate), str(b / "base" / p), str(b / "remote" / p), check=False)
            if result.returncode:
                raise RuntimeError("config.yaml 冲突；双方版本及冲突预览已保留在备份目录。")
            merged[p] = candidate.read_bytes()
        validate(p, merged[p])
    for p in dirty:
        if generated(p):
            copy_to(b / "generated", p)
    (b / "state.json").write_text(json.dumps({"head": text("rev-parse", "HEAD"), "dirty": dirty}, ensure_ascii=False, indent=2), encoding="utf-8")
    for p in paths("ls-files", "--others", "--exclude-standard"):
        if generated(p):
            source = safe_path(p)
            target = b / "generated" / p
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(target))
    restore = [p for p in dirty if p in CONFIG or generated(p)]
    if restore:
        git("restore", "--worktree", "--", *restore)
    if local["secret.private"] is not None and "secret.private" not in tracked:
        safe_path("secret.private").unlink()  # Durable copy exists in b/local.
    try:
        git("rebase", "origin/main")
    except Exception:
        git("rebase", "--abort", check=False)
        for p, data in local.items():
            if data is not None:
                safe_path(p).write_bytes(data)
        raise
    for p, data in merged.items():
        if data is not None:
            safe_path(p).write_bytes(data)
    git("add", "--", "config.yaml")
    if safe_path("secret.private").exists():
        git("add", "-f", "--", "secret.private")
    staged = paths("diff", "--cached", "--name-only")
    if set(staged) - CONFIG:
        raise RuntimeError("暂存区出现意外文件，停止提交。")
    if staged:
        git("commit", "-m", "Update paper reader config" + TRAILERS)
    else:
        print("没有配置改动需要提交。")
    for attempt in range(3):
        if git("push", "origin", "main", check=False).returncode == 0:
            print("配置已安全同步到 GitHub。")
            return
        git("fetch", "origin")
        if text("rev-list", "--count", "HEAD..origin/main") == "0":
            raise RuntimeError("push 失败；请检查 Git 登录、网络或分支保护。提交与备份已保留。")
        try:
            git("rebase", "origin/main")
        except Exception:
            for p in CONFIG:
                remote = blob("origin/main", p)
                if remote is not None:
                    (b / ("push-remote-" + p)).write_bytes(remote)
            git("rebase", "--abort", check=False)
            raise RuntimeError("远端同时修改配置；已中止 rebase 并保留远端版本，请人工确认。") from None
    raise RuntimeError("远端持续更新，已保留提交，请稍后再运行。")
def update():
    git("config", "--local", "core.longpaths", "true")
    if text("branch", "--show-current") != "main":
        raise RuntimeError("请在 main 执行更新。")
    if paths("diff", "--name-only") or paths("diff", "--cached", "--name-only"):
        raise RuntimeError("请先用菜单 [3] 保存配置；其它代码改动需要先处理。")
    if "upstream" not in text("remote").splitlines():
        git("remote", "add", "upstream", "https://github.com/ziwenhahaha/daily-paper-reader.git")
    git("fetch", "upstream")
    print("main: " + text("rev-parse", "--short", "main"))
    print("upstream/main: " + text("rev-parse", "--short", "upstream/main"))
    print("本地独有 / 上游新增提交: " + text("rev-list", "--left-right", "--count", "main...upstream/main"))
    if text("rev-list", "--count", "HEAD..upstream/main") == "0":
        print("没有上游更新。")
        return
    if input("发现上游更新，是否继续同步？ [Y/N] ").strip().lower() != "y":
        return
    b = backup()
    protected = CONFIG | {"user_settings.json", "DailyPaperReader.cmd", "USER_QUICKSTART.md"}
    protected |= {p.relative_to(ROOT).as_posix() for p in (ROOT / "tools/windows").rglob("*") if p.is_file()}
    for p in protected:
        copy_to(b / "protected", p)
    result = git("merge", "--no-commit", "--no-ff", "upstream/main", check=False)
    if result.returncode:
        raise RuntimeError("更新未完成；双方版本保留在 Git，备份: " + str(b) +
                           "\n冲突文件:\n" + text("diff", "--name-only", "--diff-filter=U"))
    tracked = set(paths("ls-tree", "-r", "--name-only", "HEAD")) | set(paths("ls-files"))
    for p in protected:
        source = b / "protected" / p
        if source.exists():
            safe_path(p).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, safe_path(p))
            if p in tracked:
                git("add", "-f", "--", p)
    if paths("diff", "--cached", "--name-only"):
        git("commit", "-m", "Merge upstream updates; preserve Windows user settings" + TRAILERS)
    else:
        git("merge", "--abort", check=False)
    print("上游更新已合入本地。未推送；代码更新请审阅后发布。")
def audit():
    bad = [p for p in paths("ls-files") if sensitive(p)]
    findings = []
    known = []
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8-sig").splitlines():
            key, sep, value = line.partition("=")
            value = value.strip().strip(chr(34)).strip(chr(39))
            if sep and any(k in key.upper() for k in ("KEY", "TOKEN", "SECRET")) and len(value) >= 16:
                if not value.lower().startswith(("your_", "your-", "replace", "example")):
                    known.append(value.encode())
    entries = {}
    for line in text("rev-list", "--objects", "--all").splitlines():
        parts = line.split(" ", 1)
        if len(parts) == 2:
            oid, name = parts
            entries[oid] = name
            if sensitive(name):
                findings.append("历史敏感路径: " + name)
    # --batch-command avoids one Windows subprocess per object and bounds memory per blob.
    proc = subprocess.Popen(["git", "cat-file", "--batch-command"], cwd=ROOT,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        for oid, name in entries.items():
            proc.stdin.write(("info " + oid + "\n").encode()); proc.stdin.flush()
            info = proc.stdout.readline().split()
            if len(info) != 3 or info[1] != b"blob":
                continue
            proc.stdin.write(("contents " + oid + "\n").encode()); proc.stdin.flush()
            header = proc.stdout.readline().split()
            data = proc.stdout.read(int(header[2]))
            proc.stdout.read(1)
            if TOKEN.search(data) or any(value in data for value in known):
                findings.append("历史疑似密钥: " + name + " (blob " + oid[:10] + ")")
        proc.stdin.close()
        proc.wait()
    finally:
        if proc.poll() is None:
            proc.kill(); proc.wait()
        proc.stdout.close()
    for log in (ROOT / "logs").glob("*.log"):
        data = log.read_bytes()
        if TOKEN.search(data) or any(value in data for value in known):
            findings.append("当前日志疑似密钥: " + log.name)
    print("当前敏感追踪文件: " + (", ".join(bad) or "无"))
    print("\n".join(sorted(set(findings))) if findings else "历史模式扫描未发现疑似 API Key / GitHub Token。")
    return 2 if findings or bad else 0
if __name__ == "__main__":
    os.chdir(ROOT)
    try:
        command = sys.argv[1]
        if command in ("sync", "update"):
            import msvcrt
            (ROOT / ".local_backup").mkdir(exist_ok=True)
            lock = (ROOT / ".local_backup/windows.lock").open("a+b")
            lock.seek(0)
            if lock.read(1) == b"":
                lock.write(b"0"); lock.flush()
            lock.seek(0)
            try:
                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError:
                raise RuntimeError("另一项同步/更新正在运行，请稍后重试。")
        sys.exit({"sync": sync, "update": update, "audit": audit}[command]() or 0)
    except Exception as exc:
        print("错误: " + str(exc), file=sys.stderr)
        sys.exit(1)
