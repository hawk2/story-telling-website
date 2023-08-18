from flask import Flask, render_template, request
import openai
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/story', methods=['POST'])
def story():
    name = request.form['name']
    hobbies = request.form['hobbies']
    friends = request.form['friends']
    
    print("Generating...")
    time.sleep(5)
    print("You can now safely leave this tab")

    story_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a children story teller. You write in standard English. You use perfect grammar. You must use capital letters at the beginning of each sentence."},
            {"role": "user", "content": f"Write a story about {name}. {name} likes to {hobbies}. {name}'s best friends are/is {friends}."},
        ]
    )

    story = story_response['choices'][0]['message']['content']

    # Generate a DALL·E prompt
    prompt_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You read stories and then generate a prompt for DALL·E about the stories. Must be kid friendly. Clearly specify no text. Use a cartoon style."},
            {"role": "user", "content": f"Make a DALL·E prompt for this story: {story}"},
        ]
    )

    iprompt = prompt_response['choices'][0]['message']['content']

    # Generate an image
    image_response = openai.Image.create(
        prompt=iprompt,
        n=1,
        size="1024x1024"
    )

    # Save the URL of the generated image
    image_url = image_response['data'][0]['url']

    return render_template('story.html', story=story)

if __name__ == "__main__":
    openai.api_key = 'Your API key here'
    app.run(debug=True)

