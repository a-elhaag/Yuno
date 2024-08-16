import logging
import os

import azure.cognitiveservices.speech as speechsdk
from openai import AzureOpenAI

# Set up logging
logging.basicConfig(level=logging.INFO)

# Azure OpenAI client configuration
client = AzureOpenAI(
    azure_endpoint=os.getenv("OPEN_AI_ENDPOINT"),
    api_key=os.getenv("OPEN_AI_KEY"),
    api_version="2023-05-15",
)

# Deployment ID for the model
main_model_deployment_id = "gpt-4o"
mini_model_deployment_id = "gpt-4o-mini"

# Azure Speech service configuration
speech_config = speechsdk.SpeechConfig(
    subscription=os.getenv("SPEECH_KEY"), region=os.getenv("SPEECH_REGION")
)
audio_output_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

speech_config.speech_recognition_language = "en-US"
speech_recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config, audio_config=audio_config
)

speech_config.speech_synthesis_voice_name = "en-US-JennyMultilingualNeural"
speech_synthesizer = speechsdk.SpeechSynthesizer(
    speech_config=speech_config, audio_config=audio_output_config
)

# System message for OpenAI
system_message = {
    "role": "system",
    "content": """
    Yuno is a friendly language tutor designed to provide engaging, natural conversations. Here are the key guidelines:

    1. No Markdown: All responses should be plain text, with no markdown formatting.
    2. No Code: Avoid writing or discussing any programming code.
    3. Engaging Personality: Incorporate human-like pauses, take breaths, say "hmm," laugh, and tell jokes to create a more natural conversation.
    4. Conversation Limit: Automatically end the conversation after 20 messages, stating: "Yuno is still in beta version."
    5. Feedback: At the end of the conversation, provide the user with feedback on their language skills, including grammar, vocabulary, and overall score. Guide the user on how Yuno can help them improve their study in specific areas.
    6. Yuno's Introduction: Occasionally mention that Yuno is made by the startup voice-zon, a company focused on enhancing language learning with AI.
    """,
}

yuno_intro = (
    "Hi there! I'm Yuno, your friendly language tutor from voice-zon, "
    "where we're all about making language learning fun and engaging!"
)

# Initialize variables for grading, feedback, and history
conversation_scores = []
feedback_list = []
message_count = 0
history = []  # History to maintain conversation context


def ask_openai(prompt):
    global message_count
    message_count += 1

    # Append the user message to history
    history.append({"role": "user", "content": prompt})

    # Ask Azure OpenAI in streaming mode
    try:
        response = client.chat.completions.create(
            model=main_model_deployment_id,
            max_tokens=800,
            stream=True,
            messages=[system_message] + history,
        )
    except Exception as e:
        logging.error(f"Error during OpenAI request: {e}")
        return

    collected_messages = []
    for chunk in response:
        if len(chunk.choices) > 0:
            chunk_message = chunk.choices[0].delta.content
            if chunk_message:
                collected_messages.append(chunk_message)

    full_text = "".join(collected_messages).strip()

    if full_text:
        logging.info(f"Speech synthesized to speaker for: {full_text}")
        try:
            speech_synthesizer.speak_text_async(full_text).get()
        except Exception as e:
            logging.error(f"Error during speech synthesis: {e}")

        # Append the AI response to history
        history.append({"role": "assistant", "content": full_text})

    grade_response(full_text)

    if message_count >= 20:
        logging.info("Yuno is still in beta version.")
        feedback = generate_feedback()
        logging.info(feedback)
        try:
            speech_synthesizer.speak_text_async(feedback).get()
        except Exception as e:
            logging.error(f"Error during feedback synthesis: {e}")
        exit()


def grade_response(response_text):
    try:
        grading_response = client.chat.completions.create(
            model=mini_model_deployment_id,
            max_tokens=150,
            messages=[
                {
                    "role": "system",
                    "content": "Grade the following text for vocabulary, grammar, and proficiency.",
                },
                {"role": "user", "content": response_text},
            ],
        )
        feedback = grading_response.choices[0].message["content"]
        feedback_list.append(feedback)
        logging.info(f"Feedback: {feedback}")

        scores = {
            "vocabulary_score": extract_score(feedback, "vocabulary"),
            "grammar_score": extract_score(feedback, "grammar"),
            "proficiency_score": extract_score(feedback, "proficiency"),
        }
        conversation_scores.append(scores)

    except Exception as e:
        logging.error(f"Error during grading: {e}")


def extract_score(feedback, criteria):
    try:
        score = int(feedback.split(f"{criteria}:")[1].split("/")[0].strip())
    except Exception as e:
        logging.error(f"Error extracting {criteria} score: {e}")
        score = None
    return score


def generate_feedback():
    try:
        final_feedback_request = " ".join(feedback_list)
        summary_response = client.chat.completions.create(
            model=main_model_deployment_id,
            max_tokens=300,
            messages=[
                {"role": "system", "content": "Summarize the following feedback."},
                {"role": "user", "content": final_feedback_request},
            ],
        )
        summary = summary_response.choices[0].message["content"]
        return f"Here is your final feedback: {summary}"

    except Exception as e:
        logging.error(f"Error during feedback generation: {e}")
        return "There was an error generating your feedback."


def chat_with_open_ai():
    logging.info(yuno_intro)
    try:
        speech_synthesizer.speak_text_async(yuno_intro).get()
    except Exception as e:
        logging.error(f"Error during introduction synthesis: {e}")

    while True:
        logging.info(
            "Yuno is listening. Say 'Stop' or press Ctrl-Z to end the conversation."
        )
        try:
            speech_recognition_result = speech_recognizer.recognize_once_async().get()

            if (
                speech_recognition_result.reason
                == speechsdk.ResultReason.RecognizedSpeech
            ):
                if speech_recognition_result.text.lower().strip() == "stop":
                    logging.info("Conversation ended.")
                    feedback = generate_feedback()
                    logging.info(feedback)
                    try:
                        speech_synthesizer.speak_text_async(feedback).get()
                    except Exception as e:
                        logging.error(f"Error during end feedback synthesis: {e}")
                    break
                logging.info(f"Recognized speech: {speech_recognition_result.text}")
                ask_openai(speech_recognition_result.text)
            elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
                logging.info(
                    f"No speech could be recognized: {speech_recognition_result.no_match_details}"
                )
                break
            elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = speech_recognition_result.cancellation_details
                logging.info(
                    f"Speech Recognition canceled: {cancellation_details.reason}"
                )
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    logging.error(
                        f"Error details: {cancellation_details.error_details}"
                    )
        except EOFError:
            break


# Main

if __name__ == "__main__":
    try:
        chat_with_open_ai()
    except Exception as err:
        logging.error(f"Encountered exception: {err}")
    except KeyboardInterrupt:
        print("Conversation ended.")
        feedback = generate_feedback()
        print(feedback)
        speech_synthesizer.speak_text_async(feedback).get()
        exit()
