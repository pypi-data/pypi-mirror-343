import torch
from transformers import AutoModelForCausalLM

class EridaSpeedOptimizer:
    def __init__(self, quantization_bits=8, sparsity_threshold=0.01):
        self.quantization_bits = quantization_bits
        self.sparsity_threshold = sparsity_threshold

    def quantize_tensor(self, tensor):
        qmin = -(2 ** (self.quantization_bits - 1))
        qmax = 2 ** (self.quantization_bits - 1) - 1
        max_val = tensor.abs().max()
        scale = max_val / qmax if max_val != 0 else 1.0
        tensor_q = torch.clamp((tensor / scale).round(), qmin, qmax)
        tensor_deq = tensor_q * scale
        return tensor_deq

    def apply_sparsity(self, tensor):
        mask = tensor.abs() >= self.sparsity_threshold
        return tensor * mask

    def optimize_module(self, module):
        if hasattr(module, 'weight') and module.weight is not None:
            with torch.no_grad():
                w = module.weight.data
                w = self.apply_sparsity(w)
                w = self.quantize_tensor(w)
                module.weight.data.copy_(w)

    def optimize(self, model):
        for module in model.modules():
            self.optimize_module(module)
        return model

def from_pretrained(cls, pretrained_model_name_or_path, *model_args, **kwargs):
    quantization_bits = kwargs.pop("quantization_bits", None)
    sparsity_threshold = kwargs.pop("sparsity_threshold", None)

    model = super(AutoModelForCausalLM, cls).from_pretrained(pretrained_model_name_or_path, *model_args, **kwargs)

    if quantization_bits is not None or sparsity_threshold is not None:
        optimizer = EridaSpeedOptimizer(quantization_bits or 8, sparsity_threshold or 0.01)
        model = optimizer.optimize(model)

    return model

# Патчим метод у AutoModelForCausalLM
AutoModelForCausalLM.from_pretrained = classmethod(from_pretrained)

