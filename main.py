import random
import uuid

import store
from gen import model, tokenizer, generate_story

bucket_name = 'ks-stories'
json_folder_path = 'kindle_books/data'

def get_story(bucket_name, story_name):
    filepath =f"kindle_books/stories/{story_name}/confirmed.txt"
    return store.get_text_file(bucket_name, filepath).decode('UTF-8')
##
while True:
    try:
        # get list of stories
        json_list = store.get_file_list(bucket_name, json_folder_path)

        # select a story
        json_path = random.choice(json_list)
        json_data = store.get_json(bucket_name, json_path)
        story_name = json_data['story_name']
        print("Processing", story_name)
        version = json_data['version']
        # ### get story text
        prompt = get_story(bucket_name, story_name)

        ## generate next portion of story
        story = generate_story(model, tokenizer, prompt, 100)
        # save new text
        directory = f"kindle_books/stories/{story_name}/drafts/version {version}/"
        filename = str(uuid.uuid4()) + ".txt"
        filepath = directory + filename
        print("Writing to disk", filepath)
        store.write_file(bucket_name, filepath, story)
    except Exception as e:
        print(e)
