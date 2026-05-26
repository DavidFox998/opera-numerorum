import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

_HITS = REPO_ROOT / "data" / "hits.txt"
_CHECKPOINT = REPO_ROOT / "data" / "hits.txt.checkpoint"


@pytest.fixture(scope="session", autouse=True)
def _snapshot_ledger_for_session():
    """Snapshot data/hits.txt and data/hits.txt.checkpoint at session
    start; restore at session end (pass or fail).

    Why (task #58): `tests/test_kernel.py` runs real `kernel.probe()`
    calls. The kernel module's module-level constants `kernel.HITS` and
    `kernel.CHECKPOINT` point at the canonical ledger files. Tests
    monkeypatch `kernel.HITS` to a throwaway tmp_path, but
    `kernel.CHECKPOINT` is not monkeypatched, so every probe rewrites
    the real `data/hits.txt.checkpoint` with `(size_of_fake, sha_of_fake)`.
    Other tamper-tests deliberately mutate `data/hits.txt` in place.
    The net effect: after `pytest` finishes, `git status` is dirty on
    both files, and contributors have to remember to
    `git restore data/hits.txt data/hits.txt.checkpoint` by hand.

    This session-scoped autouse fixture snapshots both files once at
    session start (in-memory bytes) and atomically restores them at
    session teardown, regardless of test pass/fail. Per-test fixtures
    (`hits_backup`, `fresh_checkpoint`) keep working unchanged — they
    handle intra-test restore for the tampering body of a single test;
    this fixture is the outer safety net for cross-suite side effects
    like the kernel.CHECKPOINT rewrites.
    """
    hits_snapshot = _HITS.read_bytes() if _HITS.exists() else None
    cp_snapshot = _CHECKPOINT.read_bytes() if _CHECKPOINT.exists() else None
    try:
        yield
    finally:
        if hits_snapshot is not None:
            _atomic_restore(_HITS, hits_snapshot)
        elif _HITS.exists():
            _HITS.unlink()
        if cp_snapshot is not None:
            _atomic_restore(_CHECKPOINT, cp_snapshot)
        elif _CHECKPOINT.exists():
            _CHECKPOINT.unlink()


def _atomic_restore(path: Path, data: bytes) -> None:
    """Restore `path` to `data` via sibling tempfile + os.replace.

    Uses the same atomic-write pattern as tests/test_morningstar.py
    `_atomic_write_bytes` so we don't briefly truncate the ledger
    during teardown — concurrent appender workflows must always see
    either the old bytes or the new bytes, never an empty file.
    """
    import os as _os

    tmp = path.with_name(path.name + ".session-restore.tmp")
    tmp.write_bytes(data)
    _os.replace(tmp, path)
