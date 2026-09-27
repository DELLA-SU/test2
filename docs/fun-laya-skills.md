# 다른 사람들이 만든 재미있는 Laya 스킬·데모

2026-09-27 기준 공개 저장소의 설명과 해당 `SKILL.md`를 읽고 골랐다. **종류**가 `Codex 스킬` 또는 `Codex 호환 스킬`인 항목에는 설치할 수 있는 스킬 파일이 있다. 나머지는 Laya를 활용한 프로젝트·데모다. 여기서 직접 실행하거나 성능을 재검증하지는 않았다.

| 종류 | 프로젝트 | 재미있는 점 |
| --- | --- | --- |
| Codex 스킬 | [system1-agents의 `s1a`](https://github.com/ThinkFlowLab/system1-agents/blob/0e5892dc1391239461182b568fdb6cd793a446e0/skills/s1a/SKILL.md) | Codex가 Laya를 선택지 판단에 써서 **2048·블랙잭·퀴즈쇼** 에이전트를 돌릴 수 있다. 브라우저·데스크톱 에이전트도 있다. Jev·Cua-S1도 지원하므로 Laya 전용은 아니다. |
| Codex 호환 스킬 + 데모 | [laya-playground](https://github.com/wdobry/laya-playground/blob/5a825ba0472a460830bc937907d43262a87410f8/README.md) · [스킬 원문](https://github.com/wdobry/laya-playground/blob/5a825ba0472a460830bc937907d43262a87410f8/skills/laya-integration/SKILL.md) | Laya가 **Flappy·차선 달리기·테트리스**를 플레이한다. 웹의 공개 화면은 기록된 플레이를 재생하고, 로컬 모델을 켜면 실시간으로 볼 수 있다. |
| Codex 호환 스킬 | [browser-decide](https://github.com/ChenneyZhuang/laya-browser-agent/blob/c71b7c7b3319d0b8e5a93eec150af2e6ba5cfc35/skills/browser-decide/SKILL.md) | Laya 계열 모델이 브라우저에서 보이는 버튼 중 다음 클릭 대상을 고른다. 별도 `localdecide` 실행기가 필요하다. |
| Mac 데모 | [Mac Attack](https://github.com/dockndevai/mac-attack/blob/c279aa1f4d98c5439138b679c971c59b387bbd0f/README.md) | 사람을 익명 만화 캐릭터로 바꾸고 Laya가 **오리·거품·색종이** 같은 장난감 효과를 고르는 화면보호기. 카메라 없는 시뮬레이션 모드도 있다. |
| Mac 게임 데모 | [Laya Snake](https://github.com/mizorewww/laya-mlx/blob/0a859518634112655cb97c745dbf04f5191aaf13/docs/SNAKE_DEMO.md) | Apple Silicon 터미널에서 스네이크를 플레이하면서 방향별 Laya 확률과 안전 개입을 보여준다. |
| 게임 실험 | [Laya plays Super Mario Bros. 3](https://github.com/cv/laya-plays-smb3/blob/cf627420999d782620082751ad0ecca6ac408deb/README.md) | Laya가 **점프 타이밍**을 골라 1-1을 통과한 기록을 프레임 단위로 재생·감사할 수 있다. 재현은 DGX Spark와 별도 ROM이 필요하다. |
| 게임 실험 | [doomLaya](https://github.com/azalio/doomLaya) | Laya가 FreeDoom에서 행동·대상·무기를 고르고, 플레이 영상과 결정 기록을 남긴다. |
| 게임 모음 | [arbiter plays](https://github.com/0xBakeer/arbiter/blob/bf71358774c85aeff2051ec7b1dcc4577a87706d/README.md) | 스네이크·장애물 달리기·횡단·패들·지뢰·던전 탐험 **6종**을 모델이 플레이한다. 기록된 플레이는 서버 없이 볼 수 있다. |

**먼저 볼 만한 것:** 가볍게 구경하려면 laya-playground와 arbiter plays, Mac에서 직접 놀려면 Laya Snake, Codex 스킬을 살펴보려면 system1-agents가 좋다. 외부 코드·모델·스킬은 이 저장소에 복사하거나 설치하지 않았다.
