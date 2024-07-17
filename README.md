# Lucy: Your Personal Virtual Assistant

Lucy is a Python-based voice assistant designed to help you with various tasks using speech recognition, text-to-speech, and natural language processing. This assistant can perform a wide range of functions, including setting reminders, performing web searches, opening and closing applications, providing health and fitness tips, and more.

## Features

- **Voice Recognition**: Understands and processes your voice commands.
- **Text-to-Speech**: Responds to your queries with natural-sounding speech.
- **Set Reminders**: Set reminders for various tasks.
- **Date and Time**: Provides current date and time.
- **Application Control**: Opens and closes specified applications.
- **Google Search**: Searches Google for your queries.
- **File Management**: Opens, closes, and deletes specified files.
- **Weather Updates**: Provides weather updates for specified cities.
- **Health and Fitness Tips**: Offers health and fitness tips.
- **YouTube Control**: Plays YouTube videos based on your commands.
- **Integration with Gemini Model**: Uses generative AI for advanced query responses.
- **Persistent Water Reminder**: Sends periodic notifications to drink water.

## Setup

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Installation

1. Clone the repository or download the script file.

2. Install the required libraries:

   ```bash
   pip install google-generativeai dotenv pyttsx3 speechrecognition webbrowser spacy AppOpener plyer requests pywhatkit
   ```

3. Download and install the English language model for spaCy:

   ```bash
   python -m spacy download en_core_web_sm
   ```

4. Set up your environment variables by creating a `.env` file in the root directory and adding your API keys:

   ```
   gemini_api_key=your_gemini_api_key
   open_weather_api=your_open_weather_api_key
   passkey=your_authorization_passkey
   ```

### Running the Assistant

To start the assistant, run the script:

```bash
python Lucy_Assistant.py
```

## Usage

Once you run the script, Lucy will continuously listen for the keyword "Lucy". After recognizing the keyword, you will be prompted to enter your authorization passkey. Once authorized, you can start giving commands.

### Commands

Here are some examples of commands you can give to Lucy:

- **Set a Reminder**: "Lucy, set a reminder to take a break in 30 minutes."
- **Get Date and Time**: "Lucy, what's the current date and time?"
- **Open an Application**: "Lucy, open Notepad."
- **Close an Application**: "Lucy, close Notepad."
- **Google Search**: "Lucy, google the weather in New York."
- **Open a File**: "Lucy, open a file."
- **Close a File**: "Lucy, close a file."
- **Delete a File**: "Lucy, delete a file."
- **Play YouTube Video**: "Lucy, play a video of cute cats on YouTube."
- **Health Tips**: "Lucy, give me some health tips."
- **Fitness Tips**: "Lucy, give me some fitness tips."
- **Weather Updates**: "Lucy, what's the weather in Paris?"

### Custom Responses

Lucy can respond to specific phrases with pre-defined responses:

- "Thank you" -> "You're welcome"
- "How are you?" -> "I am doing well, thanks for asking. What about you?"
- "I am doing fine" -> "That's good to hear"
- "I was talking to someone else" -> "I'm sorry for interrupting your conversation, please continue"

### Exit the Program

To exit the program, simply say "exit".

## Contributing

If you would like to contribute to Lucy, feel free to fork the repository and submit pull requests. All contributions are welcome!

## License

This project is licensed under the GNU General Public License v3.0. See the `LICENSE` file for more details.

## Acknowledgements

- [Google Generative AI](https://cloud.google.com/ai)
- [spaCy](https://spacy.io/)
- [pyttsx3](https://pyttsx3.readthedocs.io/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [AppOpener](https://github.com/gupta-tushar/AppOpener)
- [plyer](https://plyer.readthedocs.io/en/latest/)
- [requests](https://docs.python-requests.org/en/latest/)
- [pywhatkit](https://pypi.org/project/pywhatkit/)

Feel free to reach out if you have any questions or need further assistance. Enjoy using Lucy, your personal virtual assistant!