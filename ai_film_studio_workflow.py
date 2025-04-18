import os
from TTS.api import TTS
from googletrans import Translator
from diffusers import StableDiffusionPipeline
import firebase_admin
from firebase_admin import credentials, db
import openai

# Initialize OpenAI API
openai.api_key = "your_openai_api_key"

# Initialize Firebase for collaboration
cred = credentials.Certificate("path/to/your-firebase-credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-database-name.firebaseio.com/'
})

# Initialize Stable Diffusion for scene visualization
stable_diffusion_model = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
stable_diffusion_model = stable_diffusion_model.to("cuda")  # Use GPU if available

# Initialize Translator
translator = Translator()

# Function to generate cinematic script using OpenAI
def generate_cinematic_script(prompt):
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
    return response['choices'][0]['message']['content']

# Function to translate text
def translate_text(text, src_lang="en", dest_lang="es"):
    translated = translator.translate(text, src=src_lang, dest=dest_lang)
    return translated.text

# Function to generate voiceover using Coqui TTS
def generate_voiceover(text, output_file="voiceover.wav"):
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True, gpu=False)
    tts.tts_to_file(text=text, file_path=output_file)
    print(f"Voiceover saved to {output_file}")

# Function to visualize a scene using Stable Diffusion
def generate_scene_visualization(description, output_file="scene.png"):
    image = stable_diffusion_model(description).images[0]
    image.save(output_file)
    print(f"Scene visualization saved to {output_file}")

# Function to save script to Firebase for collaboration
def save_script_to_firebase(script_title, script_content):
    script_data = {
        "title": script_title,
        "content": script_content
    }
    db.reference(f"scripts/{script_title}").set(script_data)
    print(f"Script '{script_title}' saved to Firebase for collaboration.")

# Function to retrieve script from Firebase
def retrieve_script_from_firebase(script_title):
    return db.reference(f"scripts/{script_title}").get()

# Main workflow
if __name__ == "__main__":
    print("Welcome to the AI-Assisted Film Studio Tool!")

    # Step 1: Input story idea
    story_idea = input("Enter your story idea: ")

    # Step 2: Generate cinematic script
    print("\nGenerating cinematic script...")
    cinematic_script = generate_cinematic_script(story_idea)
    print("\nGenerated Cinematic Script:\n")
    print(cinematic_script)

    # Step 3: Save cinematic script for collaboration
    save_script_to_firebase("My Cinematic Script", cinematic_script)

    # Step 4: Translate script (optional)
    translate_option = input("\nDo you want to translate the script? (yes/no): ")
    if translate_option.lower() == "yes":
        target_language = input("Enter the target language code (e.g., es for Spanish): ")
        translated_script = translate_text(cinematic_script, dest_lang=target_language)
        print("\nTranslated Script:\n")
        print(translated_script)

    # Step 5: Generate scene visualization
    print("\nGenerating scene visualization...")
    scene_description = input("Enter a scene description: ")
    generate_scene_visualization(scene_description)

    # Step 6: Generate voiceover
    print("\nGenerating voiceover...")
    generate_voiceover(cinematic_script)

    print("\nWorkflow complete! Your cinematic script, voiceover, and visualizations are ready.")