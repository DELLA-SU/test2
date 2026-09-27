---
name: laya-mac-apps
description: Open macOS apps from Korean or English requests with a local Laya-Mac-style fast path. Use for requests to launch Photo Booth, Notes, Chrome, or another named Mac app; not for editing app contents or controlling the browser.
---

# Laya Mac 앱 실행

Use this skill when the user asks to open or foreground a macOS application. Resolve the requested app, then run `scripts/laya_app.py` from this skill directory. This public skill uses a deterministic local fast path; it does not invoke Laya-MLX or download a model.

```bash
python3 scripts/laya_app.py '포토부스 켜줘'
python3 scripts/laya_app.py '메모 열어줘'
python3 scripts/laya_app.py '크롬 실행해'
```

- For an app outside the built-in aliases, use `python3 scripts/laya_app.py --app 'Exact macOS App Name'`. Use the user's exact target, and clarify only if multiple apps fit.
- Use `--dry-run` to inspect the chosen app before execution when the request is ambiguous. The script refuses unrecognized, multiple-app, and non-launch requests.
- `open -a` requests launch or foreground. Check its exit result and report a missing app or macOS error accurately. Do not claim that the app's window or in-app content was visually verified unless you checked it.
- Opening an app does not authorize creating notes, accessing the camera, searching in Chrome, changing files, or quitting apps. Perform those actions only when separately requested and supported by an appropriate tool.

The script needs macOS and Python 3. It has no third-party dependencies. For direct CLI use and installation, see the repository README.
