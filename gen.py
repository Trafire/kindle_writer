from transformers import GPTJForCausalLM, AutoTokenizer

from util import total_words, get_last_n_words


def get_input_length(prompt):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids[0]
    return len(input_ids)


def get_input_ids(prompt, max_length, tokenizer):
    input_length = get_input_length(prompt)
    if input_length > max_length:
        disparity = max_length / input_length
        max_words = int(total_words(prompt) * disparity) - 1
        prompt = get_last_n_words(prompt, max_words)
        return get_input_ids(prompt, max_length, tokenizer)
    return tokenizer(prompt, return_tensors="pt").input_ids, prompt, input_length


def generate(model, tokenizer, prompt, max_prompt_length=500, additional=200):
    # prompt can only be 60% of the total length of the
    input_ids, new_prompt, input_length = get_input_ids(prompt, max_prompt_length, tokenizer)
    generated_ids = model.generate(input_ids, do_sample=True, temperature=0.9, max_length=input_length + additional)
    text = tokenizer.decode(generated_ids[0])
    return prompt + text[len(new_prompt):]


def generate_story(model, tokenizer, prompt, additional):
    while additional > 210:
        prompt = generate(model, tokenizer, prompt, max_prompt_length=500, additional=200)
        additional -= 200
    prompt = generate(model, tokenizer, prompt, max_prompt_length=500, additional=additional)
    return prompt


model = GPTJForCausalLM.from_pretrained("EleutherAI/gpt-j-6B")

tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
