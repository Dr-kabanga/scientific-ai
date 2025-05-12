from google.cloud import texttospeech
import firebase_admin
from firebase_admin import credentials, db
from diffusers import StableDiffusionPipeline
from googletrans import Translator
import openai
import threading

# Initialize OpenAI API
openai.api_key = "your_openai_api_key"

# Initialize the Google Cloud Text-to-Speech client
client = texttospeech.TextToSpeechClient()

# Initialize Firebase
# Replace 'path/to/your-firebase-credentials.json' with the actual path to your Firebase Admin SDK JSON file
cred = credentials.Certificate("path/to/your-firebase-credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-database-name.firebaseio.com/'
})

# Load the Stable Diffusion model
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe = pipe.to("cuda")  # Use GPU if available
pipe = pipe.to("cpu")

# Function to generate voiceover
def generate_voiceover(script_text):
    text_input = texttospeech.SynthesisInput(text=script_text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=text_input, voice=voice, audio_config=audio_config)
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
        print("Voiceover saved to output.mp3")

# Function to save script to Firebase
def save_script_to_firebase(title, content):
    script_data = {
        "title": title,
        "content": content
    }
    db.reference(f"scripts/{title}").set(script_data)
    print(f"Script '{title}' saved to Firebase.")

# Function to listen for real-time updates
def listen_to_script_changes(script_id):
    def listener(event):
        print(f"Real-time update detected: {event.data}")
    ref = db.reference(f"scripts/{script_id}")
    ref.listen(listener)

# Function to translate text
def translate_text(text, src_lang="en", dest_lang="es"):
    translator = Translator()
    translated_text = translator.translate(text, src=src_lang, dest=dest_lang).text
    return translated_text

# Function to generate scene visualization
def generate_scene_visualization(description):
    image = pipe(description).images[0]
    image.save("scene.png")
    print("Scene visualization saved to scene.png")

# Function to generate cinematic script
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

# Main workflow
if __name__ == "__main__":
    print("Welcome to the AI-Assisted Film Studio Tool!")
    # Start listening for real-time updates in a separate thread
    script_id = "My Cinematic Script"
    threading.Thread(target=listen_to_script_changes, args=(script_id,), daemon=True).start()
    # Step 1: Input story idea
    story_idea = input("Enter your story idea: ")
    # Step 2: Generate cinematic script
    print("\nGenerating cinematic script...")
    cinematic_script = generate_cinematic_script(story_idea)
    print("\nGenerated Cinematic Script:\n")
    print(cinematic_script)
    # Step 3: Save cinematic script for collaboration
    save_script_to_firebase(script_id, cinematic_script)
    # Additional script saving example
    db.reference("scripts/MyScript").set({"title": "My Script", "content": "This is the script content."})
    # Retrieve and print the saved script
    script = db.reference("scripts/MyScript").get()
    print(script)
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

def listener(event):
    print(f"Change detected: {event.data}")

db.reference("scripts/MyScript").listen(listener)