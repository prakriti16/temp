Here’s the entire README content in code format, including the MIT License:

# Flask Chatbot with Google Generative AI

This project is a simple chatbot application built using Flask, which integrates with Google Generative AI to generate responses based on user input. The application stores chat history in a JSON file, allowing for a persistent chat experience.

## Features

- User-friendly web interface for chatting.
- Integration with Google Generative AI to generate dynamic responses.
- Persistent chat history stored in a JSON file.
- Simple setup and deployment.

## Technologies Used

- Flask: A lightweight WSGI web application framework.
- Google Generative AI: For generating responses.
- HTML/CSS: For frontend design.
- JSON: For storing chat history.

## Requirements

- Python 3.x
- Flask
- google-generativeai library

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. Install the required packages:

   ```bash
   pip install Flask google-generativeai
   ```

3. Set your Google API Key in the `app.py` file:

   ```python
   GOOGLE_API_KEY = 'YOUR_API_KEY'  # Replace with your actual API key
   ```

## Usage

1. Run the Flask application:

   ```bash
   python app.py
   ```

2. Open your web browser and go to `http://127.0.0.1:5000/`.

3. Start chatting with the bot!

## File Structure

```
.
├── app.py                  # Main application file
├── chat_history.json       # File to store chat history
└── templates
    └── index.html          # HTML template for the chat interface
```

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to open an issue or submit a pull request.

## License

MIT License

Copyright (c) [year] [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

2. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Acknowledgments

- Thanks to Google for providing the Generative AI API.
- Flask for the lightweight web framework.
```
