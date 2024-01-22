# Gemini Discord Bot

 Discord bot that leverages the power of Google's Gemini-Pro API to interact with users in both text and image formats. It processes messages and images sent to it, generating creative and engaging responses.

## Features

- **AI-Driven Text Responses:** Gemini Bot can generate text responses to messages using Google's generative AI.
- **Image Processing:** The bot can also respond to images, combining text and visual inputs for a more engaging interaction. (Images should be under 2.5 Megs)
- **User Message History Management:** It maintains a history of user interactions via discordIDs, allowing for context-aware conversations.
- **Customizable Settings:** Users can adjust various parameters like message history length and AI response settings.

## Setup

### Requirements

- aiohttp
- discord.py
- Google's generativeai library
- python-dotenv


### Installation

1. Install the required Python libraries: run "pip install -U -r requirements.txt" in the Shell Tab
2. Be sure that your Google Gemini AI Api Key and Discord Bot Token are added as Secrets Variables in the Secrets Tab
3. Run (You can use )
The bot will start listening to messages in your Discord server. It responds to direct mentions or direct messages.

## Configuration

1. Open `GeminiBotConfig.py` File

2. Fill in the following values:

- `MAX_HISTORY`: The maximum number of messages to retain in history for each user. 0 will disable history

3. Run `GeminiDiscordBot.py` or to make it easier for you, i made a start.bat file you can just click that

## Commands

- **Mention or DM the bot to activate:** History only works on pure text input
- **Send an Image:** The bot will respond with an AI-generated interpretation or related content.
- **Type 'RESET':** Clears the message history for the user.

## Development

Feel free to fork the project and customize it according to your needs. Make sure to follow the guidelines set by Discord and Google for bot development and API usage.
