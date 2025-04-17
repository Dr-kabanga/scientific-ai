import os
from gtts import gTTS
import pyttsx3
from transformers import pipeline
import openai

# Initialize OpenAI API
openai.api_key = "your_openai_api_key"

# Function to convert text to speech using gTTS
def text_to_speech_gtts(text, output_file="output.mp3"):
    tts = gTTS(text)
    tts.save(output_file)
    print(f"Voiceover saved to {output_file}")
    os.system(f"start {output_file}")

# Function to convert text into cinematic script using OpenAI
def cinematic_script_generator(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a screenplay writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500,
        top_p=0.9,
        frequency_penalty=0,
        presence_penalty=0.6
    )
    script = response['choices'][0]['message']['content']
    return script

# Function to analyze story structure
def analyze_story_structure(story_text):
    nlp = pipeline("summarization")
    summary = nlp(story_text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# Function to convert speech to text using pyttsx3 (local TTS for accessibility)
def text_to_speech_pyttsx3(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Example workflow
if __name__ == "__main__":
    print("Welcome to AI-Assisted Film Studio for Low-Income Countries!")

    # Input story
    story = input("Enter your story or script idea: ")

    # Generate cinematic script
    print("\nGenerating cinematic script...")
    cinematic_script = cinematic_script_generator(story)
    print("\nGenerated Cinematic Script:\n")
    print(cinematic_script)

    # Analyze story structure
    print("\nAnalyzing story structure...")
    story_analysis = analyze_story_structure(story)
    print("\nStory Analysis:\n")
    print(story_analysis)

    # Convert script to voiceover
    print("\nConverting script to voiceover...")
    text_to_speech_gtts(cinematic_script)