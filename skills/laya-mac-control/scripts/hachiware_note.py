"""Place one new official Hachiware photo at the top of a dedicated Apple Note."""

import datetime
import fcntl
import hashlib
import json
import re
import subprocess
import tempfile
import time
import urllib.parse
import urllib.request
from pathlib import Path


TITLE = "Laya 하치왕왕 사진 모음"
COLLECTION_URL = "https://chiikawamarket.jp/en/collections/hachiware/products.json?limit=250&page={}"
STATE_DIR = Path.home() / "Library" / "Application Support" / "Laya"
IMAGE_DIR = Path.home() / "Pictures" / "Laya" / "Hachiware"
SCRIPT = Path(__file__).with_name("append_hachiware.applescript")
CHECK_SCRIPT = Path(__file__).with_name("check_hachiware.applescript")
DEDUPE_SCRIPT = Path(__file__).with_name("dedupe_hachiware.applescript")
SHOW_SCRIPT = Path(__file__).with_name("show_hachiware.applescript")
USER_AGENT = "Laya-Mac-Control/1.0"


def _get_json(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def _candidates(page):
    products = _get_json(COLLECTION_URL.format(page)).get("products", [])
    for product in products:
        if not re.search(r"Hachiware|ハチワレ", product.get("title", ""), re.IGNORECASE):
            continue
        images = product.get("images") or []
        if not images:
            continue
        image_url = images[0].get("src", "")
        parsed = urllib.parse.urlparse(image_url)
        if (parsed.scheme != "https" or parsed.hostname != "cdn.shopify.com" or
                not parsed.path.startswith("/s/files/1/0626/7142/1681/files/") or
                not re.search(r"\.(?:jpe?g|png)$", parsed.path, re.IGNORECASE)):
            continue
        yield product, image_url


def _download(url, handle):
    extension = Path(urllib.parse.urlparse(url).path).suffix.lower()
    safe_handle = re.sub(r"[^a-zA-Z0-9_-]", "-", str(handle))[:40]
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:10]
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    destination = IMAGE_DIR / f"{timestamp}-{safe_handle}-{digest}{extension}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=30) as response, destination.open("wb") as output:
            content_type = response.headers.get_content_type()
            if content_type not in ("image/jpeg", "image/png"):
                raise RuntimeError("이미지 형식이 JPEG 또는 PNG가 아닙니다.")
            total = 0
            while True:
                chunk = response.read(65536)
                if not chunk:
                    break
                total += len(chunk)
                if total > 15 * 1024 * 1024:
                    raise RuntimeError("이미지가 15MB를 초과합니다.")
                output.write(chunk)
        if not total:
            raise RuntimeError("빈 이미지가 내려왔습니다.")
    except Exception:
        destination.unlink(missing_ok=True)
        raise
    return destination


def _append_to_notes(image_path, note_id):
    try:
        completed = subprocess.run(
            ["osascript", str(SCRIPT), note_id or "", str(image_path)],
            capture_output=True, text=True, timeout=90, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("메모 앱 응답 시간이 초과되었습니다. macOS 자동화 권한을 확인해 주세요.") from exc
    if completed.returncode:
        raise RuntimeError(completed.stderr.strip() or "메모에 사진을 추가하지 못했습니다.")
    parts = completed.stdout.strip().split("\t")
    if len(parts) != 2 or not parts[0].startswith("x-coredata://") or not parts[1].isdigit():
        raise RuntimeError("메모 앱에서 예상하지 못한 결과가 왔습니다.")
    return parts[0], int(parts[1])


def _wait_for_single_attachment(note_id, filename, previous_count):
    stable = 0
    duplicate_stable = 0
    deduped = False
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        completed = subprocess.run(
            ["osascript", str(CHECK_SCRIPT), note_id, filename],
            capture_output=True, text=True, timeout=30, check=False,
        )
        if completed.returncode:
            raise RuntimeError(completed.stderr.strip() or "메모 첨부 확인에 실패했습니다.")
        parts = completed.stdout.strip().split("\t")
        if len(parts) != 3 or not all(part.isdigit() for part in parts):
            raise RuntimeError("메모 첨부 확인 결과가 올바르지 않습니다.")
        total, matches, first_matches = map(int, parts)
        if total == previous_count + 1 and matches == 1 and first_matches == 1:
            stable += 1
            duplicate_stable = 0
            if stable >= 4:
                return
        else:
            stable = 0
            if total == previous_count + 2 and matches == 2 and not deduped:
                duplicate_stable += 1
                if duplicate_stable >= 4:
                    _remove_duplicate(note_id, filename, previous_count)
                    deduped = True
                    duplicate_stable = 0
            else:
                duplicate_stable = 0
        time.sleep(1)
    raise RuntimeError("메모 앱에서 사진 한 장만 추가됐는지 확인하지 못했습니다.")


def _remove_duplicate(note_id, filename, previous_count):
    completed = subprocess.run(
        ["osascript", str(DEDUPE_SCRIPT), note_id, filename, str(previous_count)],
        capture_output=True, text=True, timeout=30, check=False,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr.strip() or "메모의 중복 사진을 제거하지 못했습니다.")


def _show_note(note_id):
    completed = subprocess.run(
        ["osascript", str(SHOW_SCRIPT), note_id],
        capture_output=True, text=True, timeout=30, check=False,
    )
    return completed.returncode == 0


def append_hachiware_photo():
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state_path = STATE_DIR / "hachiware-note.json"
    with (STATE_DIR / "hachiware-note.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        state = json.loads(state_path.read_text()) if state_path.exists() else {}
        used = set(state.get("used_images", []))
        selection = None
        for page in range(1, 6):
            candidates = list(_candidates(page))
            selection = next(((product, url) for product, url in candidates if url not in used), None)
            if selection:
                break
            if len(candidates) < 1:
                break
        if not selection:
            raise RuntimeError("새로운 하치와레 사진을 찾지 못했습니다.")

        product, url = selection
        image_path = _download(url, product.get("handle", "hachiware"))
        note_id, previous_count = _append_to_notes(image_path, state.get("note_id", ""))
        _wait_for_single_attachment(note_id, image_path.name, previous_count)

        state["note_id"] = note_id
        state["used_images"] = state.get("used_images", []) + [url]
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=STATE_DIR, delete=False) as output:
            json.dump(state, output, ensure_ascii=False, indent=2)
            temp_path = Path(output.name)
        temp_path.replace(state_path)
        opened = _show_note(note_id)
        return {
            "note": TITLE,
            "photos_added": len(state["used_images"]),
            "saved_image": str(image_path),
            "source": "https://chiikawamarket.jp/en/products/" + str(product["handle"]),
            "opened": opened,
        }
