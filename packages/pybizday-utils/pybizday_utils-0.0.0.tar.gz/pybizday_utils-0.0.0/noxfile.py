import nox


@nox.session(venv_backend="uv", python=["3.10", "3.11", "3.12", "3.13"])
def test(session):
    session.install("-e", ".[dev]")
    session.run("pytest", *session.posargs)


@nox.session(venv_backend="uv", python=["3.10", "3.11", "3.12", "3.13"])
def lint(session):
    session.install("-e", ".[dev]")
    session.run("ruff", "check", *session.posargs)


@nox.session(venv_backend="uv", python=["3.10", "3.11", "3.12", "3.13"])
def mypy(session):
    session.install("-e", ".[dev]")
    session.run("mypy", "src", "tests")
