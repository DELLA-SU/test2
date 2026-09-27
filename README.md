# Laya Mac 앱 실행 스킬

macOS에서 자연어로 앱을 여는 [Codex 스킬](skills/laya-mac-apps/SKILL.md)입니다. Photo Booth, 메모, Chrome 같은 요청은 Laya-Mac의 빠른 규칙 경로처럼 로컬에서 처리합니다. Python 표준 라이브러리와 macOS `open`만 사용하며, 모델 다운로드나 계정이 필요하지 않습니다.

## 설치

```bash
git clone https://github.com/hyun2xyz/test2.git
mkdir -p ~/.codex/skills
ln -s "$(pwd)/test2/skills/laya-mac-apps" ~/.codex/skills/laya-mac-apps
```

Codex를 새로 시작한 뒤 “포토부스 켜줘”, “메모 열어줘”, “크롬 실행해”처럼 요청할 수 있습니다. 스킬 설치 없이 CLI만 실행할 수도 있습니다.

```bash
python3 test2/skills/laya-mac-apps/scripts/laya_app.py '포토부스 켜줘' --dry-run
python3 test2/skills/laya-mac-apps/scripts/laya_app.py '메모 열어줘'
python3 test2/skills/laya-mac-apps/scripts/laya_app.py --app 'Google Chrome'
```

`--dry-run`은 앱을 열지 않고 판정만 출력합니다. 기본 제공 별칭 외의 앱은 `--app`으로 macOS 앱 이름을 정확히 지정하세요. 앱이 설치되어 있지 않으면 `open -a` 오류를 반환합니다.

이 공개판은 앱 실행에 필요한 결정론적 경로만 포함합니다. 별도의 비공개 Laya-Mac 프로젝트나 Laya-MLX 모델을 포함하거나 요구하지 않으며, 모호한 명령은 실행하지 않습니다. [MIT 라이선스](skills/laya-mac-apps/LICENSE)는 `skills/laya-mac-apps` 폴더에만 적용됩니다.
