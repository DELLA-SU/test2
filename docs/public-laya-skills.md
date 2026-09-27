# 다른 제작자의 Laya 스킬

2026-09-27 기준 공개 GitHub 저장소의 `SKILL.md`와 프로젝트 설명을 확인했다. 아래는 **코드 실행·성능 재검증 없이 원문을 읽어 분류한 결과**다. 링크는 조사 당시 커밋에 고정했다.

| 스킬 | 확인한 용도 | 이 저장소와의 관계 |
| --- | --- | --- |
| [`laya-integration`](https://github.com/wdobry/laya-playground/blob/5a825ba0472a460830bc937907d43262a87410f8/skills/laya-integration/SKILL.md) · wdobry · MIT | Python Laya로 텍스트 분류·라우팅·점수·예/아니오 판단을 프로젝트에 붙이는 안내 | 판단 모델 사용법 참고. Mac 앱 실행 스킬은 아님. |
| [`decide`](https://github.com/ChenneyZhuang/laya-browser-agent/blob/c71b7c7b3319d0b8e5a93eec150af2e6ba5cfc35/skills/decide/SKILL.md), [`browser-decide`](https://github.com/ChenneyZhuang/laya-browser-agent/blob/c71b7c7b3319d0b8e5a93eec150af2e6ba5cfc35/skills/browser-decide/SKILL.md) · ChenneyZhuang · Apache-2.0 | 별도 `localdecide` 런타임으로 관찰한 웹 요소 중 다음 동작을 고르는 브라우저 판단 스킬 | 후보를 관찰된 요소로 한정하고 실행 후 확인하는 방식이 참고할 만함. macOS 앱 실행기는 아님. |
| [`.mimocode/skills/laya-*`](https://github.com/neko233-com/laya-go/tree/4618ea77265f042a33e07a8ab0f5fdecc95d88bd/.mimocode/skills) · neko233-com · MIT | Go 서버·CLI·MCP 코드 작업용 저장소 내부 스킬 | 이름은 Laya이지만 [프로젝트 설명](https://github.com/neko233-com/laya-go/blob/4618ea77265f042a33e07a8ab0f5fdecc95d88bd/README.md)에 따르면 기본 모델은 규칙·가중치 패턴이며 신경망 체크포인트가 아님. 직접 비교·통합 대상에서 제외. |

**정리:** 확인한 공개 스킬 중 Photo Booth·메모·Chrome을 Laya-MLX로 여는 Codex 스킬은 없었다. 이 저장소의 [`laya-mac-control`](../skills/laya-mac-control/SKILL.md)은 설치된 Laya-Mac CLI를 사용하고, CLI가 없는 환경에서는 앱 열기만 보조한다. Laya의 판단 출력과 실제 실행 권한·결과 확인은 별도로 다룬다.

기본 모델과 API의 출처는 [Laya 원본](https://github.com/NandhaKishorM/laya), Apple Silicon용 포트는 [Laya-MLX](https://github.com/mizorewww/laya-mlx)다. 외부 스킬 파일이나 코드를 이 저장소에 복사하지 않았고, 외부 의존성도 설치하지 않았다.
