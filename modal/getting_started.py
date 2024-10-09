import modal

app = modal.App("getting-started")
image = modal.Image.debian_slim().pip_install("kestra")


@app.function()
def get_platform_info():
    import platform
    from kestra import Kestra

    machine_name = platform.node()
    system = platform.system()
    architecture = platform.machine()

    print("Hello from a remote server running on Modal")
    print(f"Machine name: {machine_name}")
    print(f"System: {system}")
    print(f"Architecture: {architecture}")

    result = {
        "machine_name": machine_name,
        "system": system,
        "architecture": architecture,
    }
    Kestra.outputs(result)
    return result


@app.local_entrypoint()
def main():
    output = get_platform_info.remote()
    print("Platform information:")
    for key, value in output.items():
        print(f"{key}: {value}")
    print("Hello from kestra ✨")
