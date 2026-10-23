"""Tests for the enforcement layer (scripts/checks). Seed for the TDD invariant in AGENTS.md."""

from __future__ import annotations

from pathlib import Path

from scripts.checks import config
from scripts.checks.file_sizes import count_lines
from scripts.checks.secret_scan import build_patterns, scan_content, scan_files


def _patterns():
    return build_patterns(config.load()["extraPatterns"])


def test_config_json_merges_over_defaults():
    cfg = config.load()
    assert cfg["limit"] == 300
    assert cfg["sizePolicy"] == "ratchet"
    # Tuya shapes are configured for this repo
    names = {p["name"] for p in cfg["extraPatterns"]}
    assert "Tuya local key" in names
    assert "Tuya access id" in names


def test_tuya_local_key_is_detected():
    content = 'TUYA_LOCAL_KEY="1234567890abcdef1234567890abcdef"\n'  # pragma: allowlist secret (fixture literal, value is fake)
    findings = scan_content(content, "app.py", _patterns())
    assert [f.pattern for f in findings] == ["Tuya local key"]


def test_tuya_local_key_in_test_fixture_with_pragma_is_allowed():
    content = 'TUYA_LOCAL_KEY="1234567890abcdef1234567890abcdef"  # pragma: allowlist secret\n'
    assert scan_content(content, "tests/test_fixtures.py", _patterns()) == []


def test_generic_credential_assignment_is_detected():
    content = 'access_secret = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"\n'  # pragma: allowlist secret (fixture literal, value is fake)
    findings = scan_content(content, "src/adapters/tuya/client.py", _patterns())
    assert any(f.pattern == "Credential assignment" for f in findings)


def test_placeholder_assignment_is_not_flagged():
    content = 'TUYA_ACCESS_ID = "changeme"\n'
    assert scan_content(content, "src/config.py", _patterns()) == []


def test_short_or_low_variance_strings_are_not_flagged():
    content = 'local_key = "k" * 32  # runtime fixture\n'
    assert scan_content(content, "tests/test_client.py", _patterns()) == []


def test_scan_files_applies_secret_skip_rules():
    env_example = Path("does-not-exist-dir/.env.example")
    assert config.load()["secretSkip"]  # skip rules exist
    findings = scan_files(
        [str(env_example)],
        lambda p: 'access_secret = "a1b2c3d4e5f6g7h8"\n',  # pragma: allowlist secret (fake fixture)
        ["\\.env\\.example$"],
    )
    assert findings == []


def test_count_lines_counts_final_line_without_trailing_newline():
    assert count_lines("a\nb\n") == 2
    assert count_lines("a\nb") == 2
    assert count_lines("") == 0
