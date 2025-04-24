# app/web/launch.py

import subprocess


def run_streamlit():
    try:
        subprocess.run(["streamlit", "run", "app/web/streamlit_app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Streamlit: {e}")


if __name__ == "__main__":
    run_streamlit()
