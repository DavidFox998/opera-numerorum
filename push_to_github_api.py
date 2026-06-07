#!/usr/bin/env python3
"""push_to_github_api.py -- Opera Numerorum: push to GitHub via Git Tree API

Replaces the tar-export + git-init approach in push_to_github.sh.
Uses GitHub REST API (Git Data endpoints) exclusively -- no local git
operations, no temp-directory disk usage.

Usage:
    python3 push_to_github_api.py [--dry-run] [--release] [--tag TAG]

Options:
    --dry-run    List files that would be pushed; do not call API.
    --release    Create a GitHub release after the push.
    --tag TAG    Tag name for the release (default: v1.6.0).
"""

import base64, hashlib, json, os, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

PAT  = os.environ.get("GITHUB_PAT", "")
USER = "DavidFox998"
REPO = "opera-numerorum"
BRANCH = "main"
WORKSPACE = os.path.dirname(os.path.abspath(__file__))

COMMIT_MSG = (
    "Opera Numerorum -- {date}\n\n"
    "Certified mathematical chain: M1-M7 manifest, RH/BSD/NS/MS/PvsNP towers.\n"
    "Clay seal (frozen): 5b80b84d1d3d13e216eeecd8155c1edc854d578e7d2dae9c4bc72fcbf7ebe3c9\n"
    "120-cell H4 geometry (M8G): ffea07ae... (600 vertices, 720 vias, H4_CERT VALID).\n"
    "Author: David J. Fox | ORCID 0009-0008-1290-6105"
)

RELEASE_BODY = """\
## Opera Numerorum v1.6 -- David J. Fox

**Internal title:** Battle Plan v1.6
**Date:** May 21, 2026 (chain frozen) / June 7, 2026 (release)
**Author:** David J. Fox | ORCID 0009-0008-1290-6105

### Certified Chain (SHA-256)

| Tower | Claim | Status |
|-------|-------|--------|
| M7 manifest | SHA256(cat m1..m6.out) -- FROZEN | LOCKED |
| RH Tower | GRH for X_0(143) + all 147 X_0(N), g in [1,33] | RH_TOWER_CERTIFIED |
| BSD Tower | BSD for J_0(143): rank=1, Omega/R~12 (0.59%) | BSD_TOWER_CERTIFIED |
| NS Tower | NS(J_0(143)): Hodge+Tate PROVEN, Clay OPEN | NS_TOWER_CERTIFIED |
| MS Tower | Aureum GREEN^7, B_M=21.768MHz, RTT=18.635ns | MS_TOWER_CERTIFIED |
| P vs NP Tower | BDP Phase Reversal at p_5=3,993,746,143,633; Clay OPEN | PVSNP_TOWER_CERTIFIED |

### M8G 120-Cell H4 Geometry (new in v1.6)

- `generate_120cell.py` -- 600-cell dual projection, rotation+global_scale
- `120cell_vertices.csv` -- 600 unique 3D vertices (R_mean=42.44mm)
- `720_vias.csv` -- 720 unique 3D via locations + 4D coords (H4_sym_check)
- H4_CERT: VALID -- 32,400/32,400 angle checks, 0.0000 deg max deviation

### Release Assets

- **OperaNumerorum_AllCerts.zip** -- 86 certificate PDFs (95 MB)
- **Field_Report_Morningstar.pdf** -- full field report (~170 pages)
- **Essays_Appendices_2026_06_06.zip** -- extended theory and appendices

Clay seal: `5b80b84d1d3d13e2...`
"""

EXCLUDE_DIRS = {
    '.git', 'AUREUM_REPO', 'AUREUM_STAGE', 'M_DRAFT', 'M_FINAL',
    'node_modules', '.pnpm-store', '__pycache__', '.local',
    'artifacts', 'lib', 'scripts', '.cache', '.pythonlibs',
    'attached_assets', 'HISTORICAL',
}
EXCLUDE_FILES = {
    'CLAY_REPO.tar.gz', 'AUREUM_REPO.tar.gz', 'M_FINAL.zip',
    'MORNING_STAR_REPO.tar.gz', 'HISTORICAL.zip',
    'opera_numerorum_section8.zip',
    'certificates/OperaNumerorum_AllCerts.zip',
    'certificates/Opera_Numerorum_All_Certs_2026_06_04.zip',
    'certificates/MorningStar_Complete_2026_06_04.zip',
    'certificates/ClaySubmission_2026_06_04.zip',
    'certificates/Essays_Appendices_2026_06_06.zip',
    'certificates/ExtendedTheory_2026_06_06.zip',
}
# Files to attach as release assets (not committed to repo -- too large or wrong category)
RELEASE_ASSETS = [
    'certificates/OperaNumerorum_AllCerts.zip',
    'certificates/Field_Report_Morningstar.pdf',
    'certificates/Essays_Appendices_2026_06_06.zip',
]
MAX_BLOB_BYTES = 50 * 1024 * 1024  # 50 MB -- GitHub API limit per blob

# ── HTTP helper ───────────────────────────────────────────────────────────────

def gh(method, path, body=None, base="https://api.github.com/repos/{U}/{R}"):
    url = base.format(U=USER, R=REPO) + path
    data = json.dumps(body).encode() if body is not None else None
    headers = {
        "Authorization": f"token {PAT}",
        "Accept":        "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if data:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read()), r.status
    except urllib.error.HTTPError as e:
        return json.loads(e.read()), e.code

def gh_upload_asset(upload_url_prefix, name, content, mime="application/octet-stream"):
    """Upload a release asset (separate upload.github.com endpoint)."""
    url = f"{upload_url_prefix}?name={urllib.parse.quote(name)}"
    req = urllib.request.Request(url, data=content, method="POST")
    req.add_header("Authorization", f"token {PAT}")
    req.add_header("Content-Type", mime)
    req.add_header("Accept", "application/vnd.github.v3+json")
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read()), r.status
    except urllib.error.HTTPError as e:
        return json.loads(e.read()), e.code

import urllib.parse  # needed by gh_upload_asset

# ── File collection ───────────────────────────────────────────────────────────

def collect_files():
    """Walk workspace and return list of (relpath, abspath) after exclusions."""
    result = []
    for dirpath, dirnames, filenames in os.walk(WORKSPACE):
        # Prune excluded dirs in-place
        dirnames[:] = [
            d for d in dirnames
            if d not in EXCLUDE_DIRS
        ]
        for fname in filenames:
            abspath = os.path.join(dirpath, fname)
            relpath = os.path.relpath(abspath, WORKSPACE)
            if relpath in EXCLUDE_FILES:
                continue
            # Skip files > 50 MB (too large for blob API)
            try:
                size = os.path.getsize(abspath)
            except OSError:
                continue
            if size > MAX_BLOB_BYTES:
                print(f"  SKIP (>50MB): {relpath}  ({size//1024//1024}MB)")
                continue
            result.append((relpath, abspath))
    result.sort()
    return result

# ── Git blob SHA computation ──────────────────────────────────────────────────

def git_blob_sha(content: bytes) -> str:
    """Compute the git blob SHA1 for a given file content."""
    header = f"blob {len(content)}\0".encode()
    return hashlib.sha1(header + content).hexdigest()

# ── Main push logic ───────────────────────────────────────────────────────────

def get_current_state():
    """Return (commit_sha, tree_sha, existing_blobs: {path: sha})."""
    ref, code = gh("GET", f"/git/refs/heads/{BRANCH}")
    if code != 200:
        sys.exit(f"ERROR: cannot read branch {BRANCH}: {ref}")
    commit_sha = ref["object"]["sha"]

    commit, _ = gh("GET", f"/git/commits/{commit_sha}")
    tree_sha = commit["tree"]["sha"]

    tree, _ = gh("GET", f"/git/trees/{tree_sha}?recursive=1")
    existing = {
        item["path"]: item["sha"]
        for item in tree.get("tree", [])
        if item["type"] == "blob"
    }
    if tree.get("truncated"):
        print("WARNING: GitHub tree response was truncated -- all files will be treated as new.")
        existing = {}
    return commit_sha, tree_sha, existing

def create_blob(relpath, abspath):
    """Create a blob on GitHub for the given file. Returns (relpath, blob_sha)."""
    with open(abspath, "rb") as f:
        content = f.read()
    b64 = base64.b64encode(content).decode()
    resp, code = gh("POST", "/git/blobs", {"content": b64, "encoding": "base64"})
    if code not in (200, 201):
        return relpath, None, f"HTTP {code}: {resp.get('message', '?')}"
    return relpath, resp["sha"], None

def run_push(dry_run=False):
    if not PAT:
        sys.exit("ERROR: GITHUB_PAT environment variable is not set.")

    print("==> Collecting local files ...")
    files = collect_files()
    print(f"    {len(files)} files in push scope")

    if dry_run:
        for rel, _ in files:
            print(f"  {rel}")
        print("Dry run complete -- no API calls made.")
        return None

    print("==> Reading current GitHub state ...")
    commit_sha, tree_sha, existing = get_current_state()
    print(f"    current commit: {commit_sha[:12]}")
    print(f"    existing blobs: {len(existing)}")

    # Determine which files need new blobs
    to_upload = []
    unchanged = 0
    for relpath, abspath in files:
        with open(abspath, "rb") as f:
            content = f.read()
        local_sha = git_blob_sha(content)
        if existing.get(relpath) == local_sha:
            unchanged += 1
        else:
            to_upload.append((relpath, abspath))

    print(f"    unchanged:  {unchanged}")
    print(f"    new/changed: {len(to_upload)}")

    if not to_upload:
        print("==> Nothing changed -- GitHub is already up to date.")
    else:
        print(f"==> Creating {len(to_upload)} blobs (parallel, 8 workers) ...")
        blob_map = {}  # relpath -> blob_sha
        errors = []
        with ThreadPoolExecutor(max_workers=8) as pool:
            futures = {pool.submit(create_blob, rel, ab): rel for rel, ab in to_upload}
            done = 0
            for fut in as_completed(futures):
                rel, sha, err = fut.result()
                done += 1
                if err:
                    errors.append((rel, err))
                    print(f"  FAIL [{done}/{len(to_upload)}]: {rel} -- {err}")
                else:
                    blob_map[rel] = sha
                    if done % 50 == 0 or done == len(to_upload):
                        print(f"  ... {done}/{len(to_upload)} blobs created")

        if errors:
            print(f"WARNING: {len(errors)} blob(s) failed -- proceeding with {len(blob_map)} successes")

        # Build tree entries: all local files (use existing blob SHA for unchanged)
        tree_entries = []
        for relpath, abspath in files:
            with open(abspath, "rb") as f:
                content = f.read()
            local_sha = git_blob_sha(content)
            if relpath in blob_map:
                blob_sha = blob_map[relpath]
            else:
                blob_sha = existing.get(relpath, local_sha)
            tree_entries.append({
                "path": relpath,
                "mode": "100644",
                "type": "blob",
                "sha":  blob_sha,
            })

        print(f"==> Creating tree ({len(tree_entries)} entries) ...")
        new_tree, code = gh("POST", "/git/trees", {"tree": tree_entries})
        if code not in (200, 201):
            sys.exit(f"ERROR creating tree: HTTP {code}: {new_tree}")
        new_tree_sha = new_tree["sha"]
        print(f"    tree SHA: {new_tree_sha[:12]}")

        print("==> Creating commit ...")
        from datetime import datetime
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        msg = COMMIT_MSG.format(date=date_str)
        new_commit, code = gh("POST", "/git/commits", {
            "message": msg,
            "tree":    new_tree_sha,
            "parents": [commit_sha],
            "author": {
                "name":  "David Fox",
                "email": "david@opera-numerorum",
                "date":  datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
        })
        if code not in (200, 201):
            sys.exit(f"ERROR creating commit: HTTP {code}: {new_commit}")
        new_commit_sha = new_commit["sha"]
        print(f"    commit SHA: {new_commit_sha[:12]}")

        print("==> Updating branch ref (force) ...")
        upd, code = gh("PATCH", f"/git/refs/heads/{BRANCH}", {
            "sha":   new_commit_sha,
            "force": True,
        })
        if code not in (200, 201):
            sys.exit(f"ERROR updating ref: HTTP {code}: {upd}")
        print(f"    branch '{BRANCH}' updated.")
        print()
        print(f"SUCCESS: {len(to_upload)} file(s) pushed to github.com/{USER}/{REPO}")
        print(f"  Commit: https://github.com/{USER}/{REPO}/commit/{new_commit_sha}")
        return new_commit_sha

    return commit_sha

# ── Release logic ─────────────────────────────────────────────────────────────

def run_release(tag_name, commit_sha):
    print(f"\n==> Creating annotated tag '{tag_name}' ...")
    tag_obj, code = gh("POST", "/git/tags", {
        "tag":     tag_name,
        "message": f"Opera Numerorum {tag_name} -- Battle Plan v1.6\n\n"
                   f"Clay seal: 5b80b84d1d3d13e216eeecd8155c1edc854d578e7d2dae9c4bc72fcbf7ebe3c9",
        "object":  commit_sha,
        "type":    "commit",
        "tagger": {
            "name":  "David Fox",
            "email": "david@opera-numerorum",
            "date":  __import__("datetime").datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
    })
    if code not in (200, 201):
        print(f"  WARNING: tag object creation returned HTTP {code}: {tag_obj.get('message','?')}")
    else:
        tag_sha = tag_obj.get("sha", commit_sha)
        ref_body = {"ref": f"refs/tags/{tag_name}", "sha": tag_sha}
        ref_resp, rcode = gh("POST", "/git/refs", ref_body)
        if rcode in (200, 201):
            print(f"    tag ref created: refs/tags/{tag_name}")
        elif rcode == 422 and "already exists" in str(ref_resp):
            print(f"    tag already exists -- updating ...")
            gh("PATCH", f"/git/refs/tags/{tag_name}", {"sha": tag_sha, "force": True})
        else:
            print(f"  WARNING: tag ref: HTTP {rcode}: {ref_resp.get('message','?')}")

    print(f"==> Creating GitHub release '{tag_name}' ...")
    release, code = gh("POST", "/releases", {
        "tag_name":         tag_name,
        "target_commitish": BRANCH,
        "name":             f"Opera Numerorum {tag_name} -- Battle Plan v1.6",
        "body":             RELEASE_BODY,
        "draft":            False,
        "prerelease":       False,
    })
    if code not in (200, 201):
        if code == 422 and "already_exists" in str(release):
            print(f"  Release already exists for tag {tag_name}.")
            rels, _ = gh("GET", f"/releases/tags/{tag_name}")
            return rels.get("upload_url", "").split("{")[0]
        sys.exit(f"ERROR creating release: HTTP {code}: {release}")

    upload_url = release["upload_url"].split("{")[0]
    release_url = release["html_url"]
    print(f"    Release URL: {release_url}")

    print(f"==> Uploading release assets ...")
    for asset_relpath in RELEASE_ASSETS:
        asset_path = os.path.join(WORKSPACE, asset_relpath)
        if not os.path.exists(asset_path):
            print(f"  SKIP (not found): {asset_relpath}")
            continue
        name = os.path.basename(asset_path)
        size = os.path.getsize(asset_path)
        print(f"  Uploading {name} ({size//1024//1024} MB) ...")
        with open(asset_path, "rb") as f:
            content = f.read()
        resp, code = gh_upload_asset(upload_url, name, content)
        if code in (200, 201):
            print(f"    OK: {resp.get('browser_download_url', name)}")
        else:
            print(f"    FAIL ({code}): {resp.get('message','?')}")

    print(f"\nRelease complete: {release_url}")
    return upload_url

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    do_release = "--release" in sys.argv

    tag_name = "v1.6.0"
    for i, arg in enumerate(sys.argv):
        if arg == "--tag" and i + 1 < len(sys.argv):
            tag_name = sys.argv[i + 1]

    print("=" * 70)
    print("Opera Numerorum -- GitHub push via Git Tree API")
    print(f"Target: github.com/{USER}/{REPO}  branch={BRANCH}")
    print("=" * 70)

    commit_sha = run_push(dry_run=dry_run)

    if do_release and not dry_run and commit_sha:
        run_release(tag_name, commit_sha)
