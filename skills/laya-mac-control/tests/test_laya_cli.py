import importlib.machinery
import importlib.util
import pathlib
import sys
import unittest
from unittest.mock import patch


SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "laya"
sys.path.insert(0, str(SCRIPT.parent))
loader = importlib.machinery.SourceFileLoader("laya_cli", str(SCRIPT))
spec = importlib.util.spec_from_loader(loader.name, loader)
laya_cli = importlib.util.module_from_spec(spec)
loader.exec_module(laya_cli)


class LayaCliTests(unittest.TestCase):
    def test_requested_actions_route(self):
        examples = (
            ("메모 켜줘", "launch_app", {"app": "Notes"}),
            ("배터리 상태 알려줘", "battery", {}),
            ("맥 정보 알려줘", "system_info", {}),
            ("볼륨 30으로 설정해", "volume_set", {"level": 30}),
            ("클립보드에 Hello World 복사해줘", "clipboard_set", {"text": "Hello World"}),
            ("파일 Report.PDF 찾아줘", "file_search", {"name": "Report.PDF"}),
            ("스크린샷 찍어줘", "screenshot", {}),
            ("하치왕왕 보여줘", "hachiware_note_append", {}),
            ("Laya 하치왕왕 보여줘", "hachiware_note_append", {}),
        )
        for prompt, action, params in examples:
            with self.subTest(prompt=prompt):
                self.assertEqual(laya_cli.route(prompt), {"action": action, "params": params})

    def test_unsupported_requests_do_not_execute(self):
        for prompt in ("메모에 글 적어줘", "크롬 종료해", "볼륨 120으로 설정해", "앱 켜줘"):
            with self.subTest(prompt=prompt):
                with self.assertRaises(ValueError):
                    laya_cli.route(prompt)

    def test_clipboard_text_is_preserved_and_not_echoed(self):
        action = laya_cli.route("클립보드에 Hello   World 복사해줘")
        self.assertEqual(action["params"]["text"], "Hello   World")
        result = laya_cli.execute(action, dry_run=True)
        self.assertEqual(result["params"], {"text_length": 13})

    @patch.object(laya_cli, "command")
    def test_dry_run_has_no_side_effect(self, command):
        result = laya_cli.execute(laya_cli.route("메모 켜줘"), dry_run=True)
        command.assert_not_called()
        self.assertEqual(result["status"], "dry-run")

    @patch.object(laya_cli.platform, "system", return_value="Darwin")
    @patch.object(laya_cli, "command")
    def test_launch_uses_exact_app(self, command, _system):
        result = laya_cli.execute(laya_cli.route("메모 켜줘"))
        command.assert_called_once_with("open", "-a", "Notes")
        self.assertEqual(result["status"], "launch-requested")


if __name__ == "__main__":
    unittest.main()
