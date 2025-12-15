from app.main import main


def test_health_runs(capsys):
    """Ensure the app entrypoint runs and prints the expected greeting."""
    main()
    captured = capsys.readouterr()
    assert "Hello from investing-app (stockmcp)" in captured.out
