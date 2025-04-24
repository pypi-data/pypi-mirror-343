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
git clone https://spacecruft.org/deepcrayon/multibrain
cd multibrain/
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
./scripts/run_api.sh
```

The FastAPI server will listen on port `8000`.

## Streamlit
```
./scripts/run_streamlit.sh
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
