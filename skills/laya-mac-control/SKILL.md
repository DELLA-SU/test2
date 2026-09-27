---
name: laya-mac-control
description: Use the local `laya` terminal command and macOS built-in tools for basic Mac actions from Codex. Handles Korean requests such as `laya 메모 켜줘`, battery status, system info, volume, clipboard, screenshot, and file search. Do not use for writing inside apps or unrelated Laya desktop software.
---

# Laya Mac Control

This is a **Codex skill** with a small terminal command at `scripts/laya`. It translates a supported Korean request into one macOS built-in action. It does not call an LLM or install a desktop app.

## Use from Codex

1. Confirm this is macOS. Locate `laya` on `PATH`; if unavailable, run `python3 scripts/laya` from this skill directory. Do not assume an unrelated `laya` command has this skill's behavior; inspect `laya --help` when the target is unclear.
2. Pass the user's requested phrase as command arguments. Use `--dry-run --json` first for a state-changing or ambiguous action, inspect `action` and `params`, then execute the same request. The command also accepts the legacy form `laya run '메모 켜줘'`.
3. Inspect command output. For app launch, a successful `open -a` reports that launch was requested; verify the app window with an available native app tool before claiming it opened.

## Supported requests

| Terminal example | Action |
| --- | --- |
| `laya 메모 켜줘` | Open Notes. Also supports Photo Booth, Chrome, Safari, Finder, Calendar. |
| `laya 배터리 상태 알려줘` | Read battery status. |
| `laya 맥 정보 알려줘` | Read macOS version and architecture. |
| `laya 볼륨 알려줘` / `laya 볼륨 30으로 설정해` | Read or set output volume. |
| `laya 클립보드 보여줘` / `laya 클립보드에 안녕 복사해줘` | Read or set clipboard text. |
| `laya 스크린샷 찍어줘` | Save a PNG in the current directory. |
| `laya 파일 보고서 찾아줘` | Search Spotlight by filename (first 20 matches). |

Use macOS built-in commands directly for another clearly requested basic operation when the local command has no route; do not present that as a `laya` command. Ask for missing paths or content when needed. Opening Notes does not authorize writing a note; opening Chrome does not authorize browsing. Do not invent support for unsupported phrases.

The `engine: fast-path-rule` result means deterministic routing, not Laya-MLX inference. Never report model inference for these actions. Treat clipboard output and screenshots as potentially private; show their contents only when requested. A macOS permission or Codex sandbox denial is a real limit to report, not something to work around.

Requires macOS and Python 3. The scripts have no third-party dependencies.
