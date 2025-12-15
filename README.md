# investing-app

Small skeleton project for the investing app.

Structure
```
investing-app/
├── app/
│   ├── main.py
│   └── __init__.py
├── pyproject.toml
├── Dockerfile
├── .dockerignore
└── README.md
```

Run locally:

PowerShell
```
python -m venv .venv        # create venv (optional name)
.\.venv\Scripts\Activate.ps1
python -m app.main
```

Docker (build & run):
```
docker build -t investing-app .
docker run --rm investing-app
```
