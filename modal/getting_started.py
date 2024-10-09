import modal

app = modal.App("getting-started")


@app.function()
def get_platform_info():
    import platform

    machine_name = platform.node()
    print("Hello from a remote server running on Modal")
    print(f"Machine name: {machine_name}")
    return machine_name


@app.local_entrypoint()
def main():
    output = get_platform_info.remote()
    print(f"hello from {output}")
    print("hello from kestra")
