import modal

app = modal.App("getting-started")


@app.function()
def get_platform_info():
    import socket
    import platform
    import os
    machine_name = platform.node()
    system = platform.system()
    release = platform.release()
    version = platform.version()
    architecture = platform.machine()
    processor = platform.processor()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    environment = os.environ

    print("Hello from a remote server running on Modal")
    print(f"Machine name: {machine_name}")
    print(f"System: {system}")
    print(f"Release: {release}")
    print(f"Version: {version}")
    print(f"Architecture: {architecture}")
    print(f"Processor: {processor}")
    print(f"Hostname: {hostname}")
    print(f"IP Address: {ip_address}")
    print(f"Environment Variables: {environment}")

    return {
        "machine_name": machine_name,
        "system": system,
        "release": release,
        "version": version,
        "architecture": architecture,
        "processor": processor,
        "hostname": hostname,
        "ip_address": ip_address,
        "environment_variables": dict(environment)
    }


@app.local_entrypoint()
def main():
    output = get_platform_info.remote()
    print("Platform information:")
    for key, value in output.items():
        print(f"{key}: {value}")
    print("Hello from kestra ✨")