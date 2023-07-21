import threading, subprocess


def generate_data():
    subprocess.call(["python", "Modules\\sensors.py"], shell=True)


def backend():
    subprocess.call(["python", "Modules\\mqtt.py"], shell=True)


def api():
    subprocess.call(["python", "Modules\\flask_api.py"], shell=True)


def frontend():
    subprocess.call(["streamlit", "run", "Modules\\frontend\\app.py"], shell=True)


if __name__ == "__main__":
    generate_data_thread = threading.Thread(target=generate_data)
    backend_thread = threading.Thread(target=backend)
    api_thread = threading.Thread(target=api)
    frontend_thread = threading.Thread(target=frontend)

    generate_data_thread.start()
    backend_thread.start()
    api_thread.start()
    frontend_thread.start()

    generate_data_thread.join()
    backend_thread.join()
    api_thread.join()
    frontend_thread.join()
