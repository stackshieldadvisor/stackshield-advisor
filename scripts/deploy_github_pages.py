#!/usr/bin/env python3
"""Deploy StackShield Advisor to GitHub project Pages.

The script deliberately does not contain credentials. Git authentication is
handled through GIT_ASKPASS, backed by a local secret file outside the repo.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
DIST_DIR = PROJECT_DIR / "dist"
BASE_URL = "https://stackshieldadvisor.github.io/stackshield-advisor"
PATH_PREFIX = "/stackshield-advisor"
PUBLIC_URL = "https://stackshieldadvisor.github.io/stackshield-advisor/"
REMOTE_URL = "https://github.com/stackshieldadvisor/stackshield-advisor.git"
ASKPASS_PATH = Path(os.environ.get("STACKSHIELD_GIT_ASKPASS", "/root/.local/share/hemera/secrets/git-askpass-stackshield.sh"))
TOKEN_PATTERN = re.compile(r"(github_pat_|ghp_|gho_|ghu_|ghs_)[A-Za-z0-9_]+")


def sanitize_output(text: str) -> str:
    """Remove GitHub-token-like strings from command output."""
    return TOKEN_PATTERN.sub("[REDACTED_GITHUB_TOKEN]", text)


def deployment_environment() -> dict[str, str]:
    env = os.environ.copy()
    env["SITE_BASE_URL"] = BASE_URL
    env["SITE_PATH_PREFIX"] = PATH_PREFIX
    env["GIT_TERMINAL_PROMPT"] = "0"
    if ASKPASS_PATH.exists():
        env["GIT_ASKPASS"] = str(ASKPASS_PATH)
    return env


def run(command: list[str], cwd: Path = PROJECT_DIR, *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        env=env or deployment_environment(),
        text=True,
        capture_output=True,
        timeout=180,
    )
    if result.returncode != 0:
        output = sanitize_output((result.stdout or "") + "\n" + (result.stderr or ""))
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(command)}\n{output[-2000:]}")
    return result


def verify_dist() -> None:
    index = (DIST_DIR / "en" / "index.html").read_text(encoding="utf-8")
    sitemap = (DIST_DIR / "sitemap.xml").read_text(encoding="utf-8")
    required = {
        "prefixed_css": 'href="/stackshield-advisor/assets/styles.css"' in index,
        "prefixed_backup_link": 'href="/stackshield-advisor/en/best-backup-software-small-business/"' in index,
        "canonical_base": f'{BASE_URL}/en/' in index,
        "sitemap_prefixed": f'{BASE_URL}/en/best-backup-software-small-business/' in sitemap,
    }
    missing = [name for name, ok in required.items() if not ok]
    if missing:
        raise RuntimeError(f"Generated site failed deployment checks: {', '.join(missing)}")


def commit_and_push_source(env: dict[str, str]) -> bool:
    run(["git", "add", "."], env=env)
    status = run(["git", "status", "--porcelain"], env=env).stdout.strip()
    if not status:
        return False
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    run(["git", "commit", "-m", f"Autonomous StackShield update ({timestamp})"], env=env)
    run(["git", "push"], env=env)
    return True


def copy_dist_to(target_dir: Path) -> None:
    for source in DIST_DIR.rglob("*"):
        if source.is_file():
            destination = target_dir / source.relative_to(DIST_DIR)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
    (target_dir / ".nojekyll").write_text("", encoding="utf-8")
    (target_dir / "README.md").write_text(
        "# StackShield Advisor deployment\n\n"
        "Generated static GitHub Pages deployment.\n"
        "Source repository: https://github.com/stackshieldadvisor/stackshield-advisor\n",
        encoding="utf-8",
    )


def deploy_gh_pages(env: dict[str, str]) -> None:
    with tempfile.TemporaryDirectory(prefix="stackshield-gh-pages-") as tmp:
        pages_dir = Path(tmp)
        copy_dist_to(pages_dir)
        run(["git", "init"], cwd=pages_dir, env=env)
        run(["git", "checkout", "-B", "gh-pages"], cwd=pages_dir, env=env)
        run(["git", "config", "user.name", "StackShield Advisor Bot"], cwd=pages_dir, env=env)
        run(["git", "config", "user.email", "stackshieldadvisor@gmail.com"], cwd=pages_dir, env=env)
        run(["git", "remote", "add", "origin", REMOTE_URL], cwd=pages_dir, env=env)
        run(["git", "add", "."], cwd=pages_dir, env=env)
        run(["git", "commit", "-m", "Deploy static site to GitHub Pages"], cwd=pages_dir, env=env)
        run(["git", "push", "-f", "origin", "gh-pages"], cwd=pages_dir, env=env)


def main() -> int:
    env = deployment_environment()
    if not ASKPASS_PATH.exists():
        raise RuntimeError(f"Missing GIT_ASKPASS helper: {ASKPASS_PATH}")

    run(["python3", "-m", "unittest", "discover", "tests", "-v"], env=env)
    run(["python3", "src/generate_site.py"], env=env)
    verify_dist()
    source_committed = commit_and_push_source(env)
    deploy_gh_pages(env)

    print(f"source_committed {source_committed}")
    print(f"public_url {PUBLIC_URL}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(sanitize_output(str(exc)), file=sys.stderr)
        raise SystemExit(1)
