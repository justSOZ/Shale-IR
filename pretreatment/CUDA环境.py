import torch

def print_torch_environment():
    print("Is CUDA available:", torch.cuda.is_available())
    print("CUDA version:", torch.version.cuda)
    print("cuDNN version:", torch.backends.cudnn.version())
    print("Number of GPUs:", torch.cuda.device_count())
    print("Current GPU name:", torch.cuda.get_device_name(torch.cuda.current_device()))
    print("PyTorch version:", torch.__version__)

if __name__ == "__main__":
    print_torch_environment()



