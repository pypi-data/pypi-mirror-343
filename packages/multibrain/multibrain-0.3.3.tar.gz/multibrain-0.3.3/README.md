# MultiBrain
MultiBrain is a web app which queries multiple AI servers,
then feeds the responses to another AI,
which checks for accuracy and provides a summary.

* https://spacecruft.org/deepcrayon/multibrain

# Requirements
This application currently uses three different Ollama AI servers.
Two of them for generating the initial responses, and a third
summary server that analyzes the responses.

It uses FastAPI and Streamlit. FastAPI and Streamlit can run on the
same server, or they can each have their own server.

The Ollama servers can run on the same server as FastAPI and Streamlit,
or run on their own servers.

# Install
Set up Python to suit to taste, such as:

```
python -m venv venv
source venv/bin/activate
pip install -U setuptools pip wheel
pip install multibrain
```

# Usage
A FastAPI server is run for the backend,
and a Streamlit server runs for the front end.

## FastAPI
```
multibrain-api
```

The FastAPI server will listen on port `8000`.

## Streamlit
```
multibrain-web
```

## Web
Go to your web page, on port `8501` such as:

* http://127.0.0.1:8501
* http://192.168.100.1:8501

# Development
```
git clone https://spacecruft.org/deepcrayon/multibrain
cd multibrain/
python -m venv venv
source venv/bin/activate
pip install -U setuptools pip wheel
pip install -e .[dev]
python3 -m build
# Optionally, push to PyPi:
# python3 -m twine upload dist/*
```

# Status
Alpha.

Under early development.

# License
Apache 2.0 or Creative Commons CC by SA 4.0 International.
You may use this code, files, and text under either license.

Unofficial project, not related to upstream projects.

Upstream sources under their respective copyrights.

*Copyright &copy; 2025 Jeff Moe.*
