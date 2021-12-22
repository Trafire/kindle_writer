def find_nth(s, x, n):
    i = -1
    for _ in range(n):
        i = s.find(x, i + len(x))
        if i == -1:
            break
    return i

def total_words(prompt):
    return prompt.count(" ")


def get_last_n_words(prompt, n):
    total_words = prompt.count(" ")
    target_index = total_words - n
    if target_index < 1:
        return prompt
    index = find_nth(prompt, ' ', target_index)
    return prompt[index:]

