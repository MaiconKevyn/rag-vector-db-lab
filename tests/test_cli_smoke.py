from pathlib import Path


def test_benchmark_script_exists() -> None:
    script = Path("scripts/benchmark.py")

    assert script.exists()
    assert "run_benchmark" in script.read_text(encoding="utf-8")
