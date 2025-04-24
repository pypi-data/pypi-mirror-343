Пример использования , на примере GPT 2-й версии :

    from transformers import AutoModelForCausalLM

    model = AutoModelForCausalLM.from_pretrained(
        "gpt2",
        quantization_bits=8,       #биты для квантования
        sparsity_threshold=0.02    #обнуление малых весов (0.01 - 0.05)
    )

В разы ускоряет вычисления нейронных сетей (в основном рассматривается как для трансформеров)