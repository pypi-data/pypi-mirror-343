import time
import sys
import pathlib
import importlib
import traceback
import mlx.core as mx
import mlx.nn as nn
from typing import Union


########################################################
# Baseline
########################################################
class Model(nn.Module):
    """
    Model that performs a 2D convolution.

    Args:
        in_channels (int): Number of input channels.
        out_channels (int): Number of output channels.
        kernel_size (Union[int, tuple]): Size of the convolution kernel.
        stride (Union[int, tuple]): Stride of the convolution. Default is 1.
    """

    def __init__(self, in_channels: int, out_channels: int, kernel_size: Union[int, tuple], stride: Union[int, tuple] = 1):
        super(Model, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size, stride)

    def __call__(self, x):
        """
        Args:
            x (mx.array): Input tensor of shape (batch_size, height, width, in_channels).
        Returns:
            mx.array: Output tensor of shape (batch_size, height, width, out_channels).
        """
        return self.conv(x)


########################################################
# Weco Solution
########################################################
def load_module_from_path(module_path: str, add_to_sys_modules: bool = False):
    # Clean out all old compiled extensions to prevent namespace collisions during build
    module_path = pathlib.Path(module_path)
    name = module_path.stem
    spec = importlib.util.spec_from_file_location(name, module_path)
    mod = importlib.util.module_from_spec(spec)  # type: ignore
    if add_to_sys_modules:
        sys.modules[name] = mod
    spec.loader.exec_module(mod)  # type: ignore
    return mod


########################################################
# Benchmark
########################################################
def get_inputs(batch_size, img_height, img_width, img_channels):
    # MLX doesn't use device parameter like PyTorch, as it automatically uses Metal
    return mx.random.normal(shape=(batch_size, img_height, img_width, img_channels), dtype=mx.float32)


def bench(f, inputs, n_warmup, n_rep):
    # Warm up
    for _ in range(n_warmup):
        result = f(inputs)
        mx.eval(result)  # Force computation due to lazy evaluation

    t_avg = 0.0
    for _ in range(n_rep):
        # Clear cache before timing
        mx.clear_cache()

        start_time = time.time()
        result = f(inputs)
        mx.eval(result)  # Force computation
        mx.synchronize()  # Wait for all computations to complete
        t_avg += time.time() - start_time

    t_avg /= n_rep * 1e-3
    return t_avg


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--solution-path", type=str, required=True)
    args = parser.parse_args()

    # init and input parameters
    batch_size = 4
    img_height = 224
    img_width = 224
    img_channels = 3
    out_channels = 64
    kernel_size = 3
    stride = 1

    # Set the default device to 0
    mx.set_default_device(mx.gpu)

    # load solution module
    try:
        mx.random.seed(0)
        solution_module = load_module_from_path(args.solution_path, add_to_sys_modules=False)
        solution_model = solution_module.Model(img_channels, out_channels, kernel_size, stride)
        assert hasattr(solution_model, "__call__")
    except Exception:
        print(f"Candidate module initialization failed: {traceback.format_exc()}")
        exit(1)

    mx.random.seed(0)
    baseline_model = Model(img_channels, out_channels, kernel_size, stride)

    # measure correctness
    n_correctness_trials = 10
    max_diff_avg = 0
    for _ in range(n_correctness_trials):
        inputs = get_inputs(batch_size, img_height, img_width, img_channels)
        baseline_output = baseline_model(inputs)
        optimized_output = solution_model(inputs)
        max_diff = mx.max(mx.abs(optimized_output - baseline_output))
        mx.eval(max_diff)  # Force computation
        max_diff_avg += max_diff.item()  # Convert to Python scalar
    max_diff_avg /= n_correctness_trials
    print(f"max float diff between values of baseline and optimized model: {max_diff_avg}")

    # measure performance
    inputs = get_inputs(batch_size, img_height, img_width, img_channels)
    n_warmup = 1000
    n_rep = 5000

    # baseline
    t_avg_baseline = bench(baseline_model, inputs, n_warmup, n_rep)
    print(f"baseline time: {t_avg_baseline:.2f}ms")

    # optimized
    t_avg_optimized = bench(solution_model, inputs, n_warmup, n_rep)
    print(f"optimized time: {t_avg_optimized:.2f}ms")

    print(f"speedup: {t_avg_baseline / t_avg_optimized:.2f}x")
