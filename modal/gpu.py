import modal


app = modal.App(
    "example-gpu",
    image=modal.Image.debian_slim().pip_install(
        "torch", find_links="https://download.pytorch.org/whl/cu117"
    ),
)


@app.function(gpu="any")
def print_gpu_info():
    import torch
    import subprocess

    subprocess.run(["nvidia-smi"])
    print("Torch version:", torch.__version__)
    print("CUDA available:", torch.cuda.is_available())
    print("CUDA device count:", torch.cuda.device_count())
    print("CUDA device name:", torch.cuda.get_device_name(0))
    print("CUDA device index:", torch.cuda.current_device())
