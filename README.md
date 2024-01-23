# Gemini Discord Bot

 Discord bot that leverages the power of Google's Gemini-Pro API to interact with users in both text and image formats. It processes messages and images sent to it, generating creative and engaging responses.

## Features

- **AI-Driven Text Responses:** Gemini Bot can generate text responses to messages using Google's generative AI.
- **Image Processing:** The bot can also respond to images, combining text and visual inputs for a more engaging interaction. (Images should be under 2.5 Megs)
- **User Message History Management:** It maintains a history of user interactions via discordIDs, allowing for context-aware conversations.
- **Customizable Settings:** Users can adjust various parameters like message history length and AI response settings.

### Setup:

## Installation

1. FORK this Repo & Login at https://render.com and do create new Web Service
2. Do Build and Deploy from a Git Repository and continue putting the link of the forked repo
3. Give it a name, Select the free Plan,Put "pip install -U -r requirements.txt" as Build Command & "python main.py" as Start Command
4. Add 3 Enviroment Variables:[Your Discord Bot Token](https://www.writebots.com/discord-bot-token/), Your [Gemini Api Key](https://makersuite.google.com/app/apikey), and [Your Own Discord Id](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID#:~:text=On%20Android%20press%20and%20hold,name%20and%20select%20Copy%20ID.) ![image](https://github.com/Nick088Official/Gemini-AI-Discord-Bot/assets/91847579/bf6e719b-94fc-4162-b663-b12a7a4c9f09)
5. Create Web Service, then Deploy Last Commitment and your ready! in some time the bot will be online and stay like that for free 24/7

## Configuration

Use the /change_settings & /show_settings

OR

1. Open `GeminiBotConfig.py` File

2. Fill in the following values:

- `MAX_HISTORY`: The maximum number of messages to retain in history for each user. 0 will disable history
- `System_Prompt`: A special Prompt that instructs the Gemini Pro AI model to follow a certain behavior or interaction style when generating text or image responses.
- `Temperature_Text`: A parameter that controls the creativity or randomness of the text generated by Gemini Pro. A higher temperature results in more diverse and creative output, while a lower temperature makes the output more deterministic and focused.
- `Top_P_Text`: A parameter that controls the tokens that are considered for text generation by Gemini Pro. Only the tokens that have a cumulative probability mass equal to or higher than top_p are kept for sampling. A lower top_p value makes the output more constrained by the most probable tokens, while a higher top_p value allows for more diversity and exploration.
- `Top_K_Text`: A parameter that controls the number of highest probability tokens that are considered for text generation by Gemini Pro. Only the top_k tokens are kept for sampling. A lower top_k value makes the output more deterministic and focused, while a higher top_k value allows for more diversity and creativity.
- `Max_Output_Tokens_Text`: A parameter that controls the maximum number of tokens that Gemini Pro can generate for a text response. A lower max_output_tokens_text value makes the output shorter and more concise, while a higher max_output_tokens_text value allows for longer and more detailed output.
- `Temperature_Text`: A parameter that controls the creativity or randomness of the text generated by Gemini Pro Vision based on the image it has seen. A higher temperature results in more diverse and creative output, while a lower temperature makes the output more deterministic and focused.
- `Top_P_Text`: A parameter that controls the tokens that are considered for text generation by Gemini Pro. Only the tokens that have a cumulative probability mass equal to or higher than top_p are kept for sampling. A lower top_p value makes the output more constrained by the most probable tokens, while a higher top_p value allows for more diversity and exploration.
- `Top_K_Text`: A parameter that controls the number of highest probability tokens that are considered for text generation by Gemini Pro Vision based on the image it has seen. Only the top_k tokens are kept for sampling. A lower top_k value makes the output more deterministic and focused, while a higher top_k value allows for more diversity and creativity.
- `Max_Output_Tokens_Text`: A parameter that controls the maximum number of tokens that Gemini Pro Vision can generate for a text response based on the image it has seen. A lower max_output_tokens_text value makes the output shorter and more concise, while a higher max_output_tokens_text value allows for longer and more detailed output.


3. Run it all again after the modifications

## Commands

- **Mention or DM the bot to activate:** History only works on pure text input
- **Send an Image:** The bot will respond with an AI-generated interpretation or related content.
- **Type 'RESET':** Clears the message history for the user.
- **/change_settings:** For changing the bots settings (only for owner)
- **/show_settings:** For showing the bots settings (only for owner)

## Development

Feel free to fork the project and customize it according to your needs (Like i did lol). Make sure to follow the guidelines set by Discord and Google for bot development and API usage.
