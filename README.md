# Laya Mac Control — Codex Skill

이 저장소의 [`laya-mac-control`](skills/laya-mac-control/SKILL.md)은 **Codex 스킬**입니다. Codex에게 “포토부스 켜줘”, “메모 열어줘”, “크롬 실행해”라고 요청할 때 사용합니다. 별도 Mac 앱을 설치하는 프로젝트가 아닙니다.

## Codex에 설치

Codex에서 다음처럼 요청하세요.

> `https://github.com/hyun2xyz/test2/tree/main/skills/laya-mac-control` 스킬을 설치해줘.

또는 Codex의 `skill-installer`를 사용할 수 있습니다.

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo hyun2xyz/test2 --path skills/laya-mac-control
```

설치 후 새 Codex 작업에서 `$laya-mac-control 포토부스 켜줘`처럼 호출할 수 있습니다. 자연어 요청에도 스킬이 선택될 수 있습니다.

## 동작 범위

Codex는 설치된 Laya-Mac CLI가 있으면 그 명령의 라우팅 결과를 먼저 확인한 뒤 요청을 실행합니다. Laya-Mac이 없는 Mac에서도 스킬 안의 작은 로컬 도구로 Photo Booth, 메모, Chrome 등 **앱 열기**를 처리할 수 있습니다. 이 도구는 앱을 만드는 것이 아니라 스킬 내부의 실행 보조 파일입니다.

Laya-Mac CLI와 Laya-MLX 모델은 이 공개 저장소에 포함되지 않습니다. 따라서 앱 실행 외의 시스템 조작은 해당 런타임이 설치된 환경에서만 지원하며, 모델 추론을 사용하지 않은 결과를 Laya-MLX 결과로 표시하지 않습니다. [MIT 라이선스](skills/laya-mac-control/LICENSE)는 스킬 폴더에만 적용됩니다.
