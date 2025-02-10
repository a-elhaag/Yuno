# Yuno - AI Language Tutor 🎙️🤖

Yuno is an **AI-powered voice tutor** designed to help users practice languages through **natural conversations**. Using **Azure OpenAI and Azure Speech Services**, Yuno listens to the user, responds in real-time, and provides **language feedback** on vocabulary, grammar, and proficiency.

## 🚀 Features
- 🎤 **Speech Recognition**: Converts user speech to text using Azure Speech Services.
- 💬 **AI Conversations**: Uses Azure OpenAI (GPT-4o) for generating natural responses.
- 🔊 **Text-to-Speech (TTS)**: Speaks responses back to the user using Azure Speech synthesis.
- 📊 **Language Feedback**: Grades vocabulary, grammar, and proficiency in real-time.
- 🏆 **Conversational Limit**: Ends the session after **20 messages** and provides a final summary.
- 🔧 **Open Source & Extendable**: Contributions are welcome!

## 🛠️ Installation

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/yourusername/Yuno-AI-Tutor.git
cd Yuno-AI-Tutor
```

### **2️⃣ Set Up a Virtual Environment (Optional but Recommended)**
```sh
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate      # For Windows
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Set Up Your Environment Variables**
Create a **.env** file in the project directory and add the following:

```ini
# Azure OpenAI Configuration
OPEN_AI_ENDPOINT=your_openai_endpoint
OPEN_AI_KEY=your_openai_api_key

# Azure Speech Configuration
SPEECH_KEY=your_azure_speech_key
SPEECH_REGION=your_azure_speech_region
```

### **Sample `.env` File**
```
OPEN_AI_ENDPOINT=https://your-azure-openai-endpoint.openai.azure.com/
OPEN_AI_KEY=your_openai_api_key

SPEECH_KEY=your_azure_speech_service_key
SPEECH_REGION=your_speech_region
```


### **5️⃣ Run the Application**
```sh
python main.py
```

## 📌 Usage
1. **Start the script**, and Yuno will introduce itself.
2. **Speak into your microphone**, and Yuno will recognize your speech.
3. **Yuno responds with AI-generated speech** in a natural, conversational way.
4. **Receive real-time feedback** on your grammar, vocabulary, and proficiency.
5. **Say "Stop" to end the session**, and Yuno will summarize your progress.

## 🔧 Technologies Used
- **Python**
- **Azure OpenAI (GPT-4o)**
- **Azure Speech Services (STT & TTS)**
- **Logging (for error handling and debugging)**

## 📌 Future Improvements
- 🌍 **Multi-language support**
- 📊 **User progress tracking**
- 🖥️ **GUI version with PySide6**
- 🔄 **Cloud-based session history storage**

## 👥 Contributions
This project is **open-source**, and contributions are welcome! Feel free to submit **pull requests** or **open issues** for improvements.

## 📄 License
MIT License.

---
<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&pause=1000&color=FBECE4&center=true&vCenter=true&width=500&lines=%F0%9F%92%A1+Made+by+Voicezon;🌍+Enhancing+Language+Learning+with+AI;🚀+Empowering+Education+with+AI!" alt="Typing Animation">
</p>

---
