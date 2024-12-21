# YouChat AI Python Client 🤖💬

## 🚀 Description

**YouChat AI Python Client** is a powerful Python client that lets you easily integrate with the YouChat API, allowing you to interact with multiple AI models and chat modes. This project demonstrates how to send queries to the YouChat API and retrieve intelligent responses using cutting-edge AI technology.

With this Python client, you can seamlessly integrate the YouChat API into your applications, such as chatbots, personal assistants, and data retrieval systems.

### Key Features:
- 🌐 Integrates with multiple AI models like GPT-4, Claude, Llama, and more.
- ⚡ Supports various chat modes such as "research", "custom", and "default".
- 📊 Real-time query handling and response streaming.
- 🛠️ Configurable settings to personalize your chatbot experience.

---

## 🏗️ How It Works

1. **Setup Configuration:**
   - Define which AI model you want to use (e.g., GPT-4, Claude 3).
   - Select the desired chat mode for the interaction (e.g., default, research, or custom).
   - Provide a query or question that you'd like the AI to answer.

2. **API Interaction:**
   - The `YouChat` class sends your query to the YouChat API with the selected model and chat mode.
   - The API processes the query and returns real-time responses in a streaming format.

3. **Response Handling:**
   - The response is parsed, and relevant data like the query result and related searches are extracted.
   - You can adjust how the responses are printed or processed based on your needs.

---

## 🛠️ How to Use

### Prerequisites

Before running the project, ensure you have Python 3.x installed on your system. You can install the necessary dependencies using `pip`:

```bash
pip install requests
```

## Running the Code
Clone this repository:
```bash
git clone https://github.com/sujalrajpoot/YouChat-AI-Python-Client.git
```

Navigate to the project directory:
```bash
cd YouChat-AI-Python-Client
```

Create and modify the YouChatConfig with your desired AI model, chat mode, and query.

## 🤖 Example Use Case
```python
from YouChat import YouChat, YouChatConfig, AIModelEnum, ChatModeEnum

config = YouChatConfig(
    model=AIModelEnum.GPT_4O,  # Use the GPT-4O model
    chat_mode=ChatModeEnum.DEFAULT,  # Set chat mode to default
    query="What is the current AQI in New Delhi?"
)

youchat = YouChat(config)
response = youchat.send_request(config.query, config)
print("\nStreaming Response:", response.get('streaming_response', 'No content'))
print("\nQuery:", response.get('query', 'No query found'))
```

## 🎯 How It Can Help Users
- 🧠 AI-Powered Assistance: Seamlessly interact with AI models to get intelligent, real-time answers for various use cases like chatbots, personal assistants, and data retrieval.
- 📈 Personalization: Choose from a variety of AI models and chat modes to suit your specific needs.
- 💻 Integration: Easily integrate YouChat into your existing projects to provide powerful conversational capabilities.

---

## 🛠️ Technologies Used
- Python 3.x
- requests library
- YouChat API
- Various AI models (GPT-4, Claude, Llama)

### Key Updates:
- **Project Name**: The project name is now **YouChat AI Python Client**.
- **README Structure**: The structure remains the same, with detailed sections for usage, contribution, and more.

This README gives a professional and clear overview of the project while incorporating engaging elements like emojis. Feel free to further customize it to suit your needs!

---

# Created with ❤️ by **Sujal Rajpoot**

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact
For questions or support, please open an issue or reach out to the maintainer.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
