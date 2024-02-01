import discord
import google.generativeai as genai
from pathlib import Path
import re
import os
import subprocess
import requests
from discord.ext import tasks, commands
from discord import app_commands
import aiohttp
import base64
import json

from GeminiBotConfig import GOOGLE_AI_KEY
from GeminiBotConfig import DISCORD_BOT_TOKEN
from GeminiBotConfig import MAX_HISTORY
from GeminiBotConfig import System_Prompt
from GeminiBotConfig import Bot_Info
from GeminiBotConfig import Temperature_Text
from GeminiBotConfig import Top_P_Text
from GeminiBotConfig import Top_K_Text
from GeminiBotConfig import Max_Output_Tokens_Text
from GeminiBotConfig import Temperature_Image
from GeminiBotConfig import Top_P_Image
from GeminiBotConfig import Top_K_Image
from GeminiBotConfig import Max_Output_Tokens_Image
from GeminiBotConfig import Owner_User_Discord_ID
from GeminiBotConfig import github_username
from GeminiBotConfig import github_repo
from GeminiBotConfig import github_token
from GeminiBotConfig import git_url

message_history = {}
# ---------------------------------------------AI Configuration-------------------------------------------------

# Configure the generative AI model
genai.configure(api_key=GOOGLE_AI_KEY)
text_generation_config = {
    "temperature": Temperature_Text,
    "top_p": Top_P_Text,
    "top_k": Top_K_Text,
    "max_output_tokens": Max_Output_Tokens_Text,
}
image_generation_config = {
    "temperature": Temperature_Image,
    "top_p": Top_P_Image,
    "top_k": Top_K_Image,
    "max_output_tokens": Max_Output_Tokens_Image,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_LOW_AND_ABOVE"}
]

text_model = genai.GenerativeModel(
    model_name="gemini-pro", generation_config=text_generation_config, safety_settings=safety_settings)
image_model = genai.GenerativeModel(
    model_name="gemini-pro-vision", generation_config=image_generation_config, safety_settings=safety_settings)


# ---------------------------------------------Discord Code-------------------------------------------------
# Initialize Discord bot
bot = discord.Client(command_prefix="!", intents=discord.Intents.default())
tree = app_commands.CommandTree(bot)


@bot.event
async def on_ready():
    await tree.sync()
    print("----------------------------------------")
    print(f'Gemini AI Logged in as {bot.user} on Discord!')
    print("----------------------------------------")

# On Message Function


@bot.event
async def on_message(message):
    # Ignore messages sent by the bot
    if message.author == bot.user:
        return
    # Check if the bot is mentioned or the message is a DM
    if bot.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
        # Start Typing to seem like something happened
        cleaned_text = clean_discord_message(message.content)

        async with message.channel.typing():
            # Check for image attachments
            if message.attachments:
                print("New Image Message FROM:" +
                      str(message.author.id) + ": " + cleaned_text)
                # Currently no chat history for images
                for attachment in message.attachments:
                    # these are the only image extentions it currently accepts
                    if any(attachment.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']):
                        await message.add_reaction('🎨')

                        async with aiohttp.ClientSession() as session:
                            async with session.get(attachment.url) as resp:
                                if resp.status != 200:
                                    await message.channel.send('Unable to download the image.')
                                    return
                                image_data = await resp.read()
                                response_text = await generate_response_with_image_and_text(image_data, cleaned_text)
                                # Split the Message so discord does not get upset
                                await split_and_send_messages(message, response_text, 2000)
                                return
            # Not an Image do text response
            else:
                print("New Message FROM:" +
                      str(message.author.id) + ": " + cleaned_text)
                # Check for Keyword Reset
                if "RESET" in cleaned_text:
                    # End back message
                    if message.author.id in message_history:
                        del message_history[message.author.id]
                    await message.channel.send("🤖 History Reset for user: " + str(message.author.name))
                    return
                await message.add_reaction('💬')

                # Check if history is disabled just send response
                if (MAX_HISTORY == 0):
                    response_text = await generate_response_with_text(cleaned_text)
                    # add AI response to history
                    await split_and_send_messages(message, response_text, 2000)
                    return
                # Add users question to history
                update_message_history(message.author.id, cleaned_text)
                response_text = await generate_response_with_text(get_formatted_message_history(message.author.id))
                # add AI response to history
                update_message_history(message.author.id, response_text)
                # Split the Message so discord does not get upset
                await split_and_send_messages(message, response_text, 2000)

# ---------------------------------------------AI Generation History-------------------------------------------------


async def generate_response_with_text(message_text):
    prompt_parts = [System_Prompt, "You are a custom AI, you learn info to add to your already made knowledge, remember to use this info only when asked to, for example if user just says hi you dont mention your learned info unless you find the user request related to it, learn the following info to your knowledge to use only when asked to:", Bot_Info, "Now Reply to this ignoring everything before unless asked:", message_text]
    print("Got textPrompt: " + message_text)
    response = text_model.generate_content(prompt_parts)
    if (response._error):
        print("Gemini AI Error: " + str(response._error))
        return "❌" + str(response._error) + "\nPlease do /reset and try again later."
    print("Gemini AI Replied: " + response.text)
    return response.text


async def generate_response_with_image_and_text(image_data, text):
    image_parts = [{"mime_type": "image/jpeg", "data": image_data}]
    prompt_parts = [image_parts[0], f"\n{text if text else 'What is this a picture of?'}"]
    response = image_model.generate_content(prompt_parts)
    if (response._error):
        return "❌" + str(response._error)
    return response.text

# ---------------------------------------------Message History-------------------------------------------------


def update_message_history(user_id, text):
    # Check if user_id already exists in the dictionary
    if user_id in message_history:
        # Append the new message to the user's message list
        message_history[user_id].append(text)
        # If there are more than 12 messages, remove the oldest one
        if len(message_history[user_id]) > MAX_HISTORY:
            message_history[user_id].pop(0)
    else:
        # If the user_id does not exist, create a new entry with the message
        message_history[user_id] = [text]


def get_formatted_message_history(user_id):
    """
    Function to return the message history for a given user_id with two line breaks between each message.
    """
    if user_id in message_history:
        # Join the messages with two line breaks
        return '\n\n'.join(message_history[user_id])
    else:
        return "No messages found for this user."

# ---------------------------------------------Sending Messages-------------------------------------------------


async def split_and_send_messages(message_system, text, max_length):
    # Mention the user


    # Split the string into parts
    messages = []
    for i in range(0, len(text), max_length):
        sub_message = text[i:i+max_length]
        messages.append(sub_message)

    # Send each part as a separate message
    for string in messages:
        await message_system.reply(f"{string}")


def clean_discord_message(input_string):
    # Create a regular expression pattern to match text between < and >
    bracket_pattern = re.compile(r'<[^>]+>')
    # Replace text between brackets with an empty string
    cleaned_content = bracket_pattern.sub('', input_string)
    return cleaned_content

# ---------------------------------------------Slash Commands--------------------------------------

# RESET SLASH COMMAND
@tree.command(name="reset", description="Reset your Chat History with the AI Bot")
async def reset(interaction):
    if interaction.user.id in message_history:
        del message_history[interaction.user.id]
    await interaction.response.send_message("🤖 History Reset for user: " + str(interaction.user.name))
    print(str(interaction.user.id) + " Has Resetted their AI Chat History")
    

# Import necessary libraries
import requests
import base64
import re
import json

# Dictionary to store changed variables
changed_variables = {}

# Change Settings Slash Command
@tree.command(description="Change the Settings of Gemini AI")
async def change_settings(interaction, apply: bool, new_system_prompt: str = System_Prompt, new_bot_info: str = Bot_Info, new_max_history: float = float(MAX_HISTORY), new_temperature_text: float = float(Temperature_Text), new_top_p_text: float = float(Top_P_Text), new_top_k_text: float = float(Top_K_Text), new_max_output_tokens_text: float = float(Max_Output_Tokens_Text), new_temperature_image: float = float(Temperature_Image), new_top_p_image: float = float(Top_P_Image), new_top_k_image: float = float(Top_K_Image), new_max_output_tokens_image: float = float(Max_Output_Tokens_Image)):

    # Check if the user is the owner
    if float(interaction.user.id) != float(Owner_User_Discord_ID):
        await interaction.response.send_message("Only the Owner can Change Bots Settings.", ephemeral=True)
        return

    # Check if apply is True and at least one setting is changed
    if not apply:
        await interaction.response.send_message("The apply option must be set to yes, and you must change one of the settings at least", ephemeral=True)
        return

    # Update global variables and store changed variables in the dictionary
    global System_Prompt, Temperature_Text, MAX_HISTORY, Top_P_Text, Top_K_Text, Max_Output_Tokens_Text, Temperature_Image, Top_P_Image, Top_K_Image, Max_Output_Tokens_Image
    changed_variables["System_Prompt"] = new_system_prompt
    changed_variables["Bot_Info"] = new_bot_info
    changed_variables["MAX_HISTORY"] = new_max_history
    changed_variables["Temperature_Text"] = new_temperature_text
    changed_variables["Top_P_Text"] = new_top_p_text
    changed_variables["Top_K_Text"] = new_top_k_text
    changed_variables["Max_Output_Tokens_Text"] = new_max_output_tokens_text
    changed_variables["Temperature_Image"] = new_temperature_image
    changed_variables["Top_P_Image"] = new_top_p_image
    changed_variables["Top_K_Image"] = new_top_k_image
    changed_variables["Max_Output_Tokens_Image"] = new_max_output_tokens_image

    # Make a GET request to the GitHub API to retrieve the contents of the file
    response = requests.get("https://api.github.com/repos/Nick088Official/Gemini-AI-Discord-Bot/contents/GeminiBotConfig.py")
    
    # Check if the response contains 'content'
    try:
        response_json = response.json()
        content = base64.b64decode(response_json["content"]).decode("utf-8")
    except KeyError:
        await interaction.response.send_message("Error fetching file content from GitHub.", ephemeral=True)
        return

    # Replace the old value of the variable with the new value
    new_content = content
    for var_name, new_value in changed_variables.items():
        pattern = re.compile(rf'{var_name}\s*=\s*".*?"')
        new_content = re.sub(pattern, f'{var_name} = "{new_value}"', new_content)

    # Make a PUT request to the GitHub API to update the contents of the file
    data = {
        "message": "Update variable value",
        "content": base64.b64encode(new_content.encode("utf-8")).decode("utf-8"),
        "sha": response_json["sha"]
    }

    # Add your GitHub token in the Authorization header
    headers = {
        "Authorization": "Bearer " + github_token,
    }

    # Make the PUT request
    put_response = requests.put("https://api.github.com/repos/Nick088Official/Gemini-AI-Discord-Bot/contents/GeminiBotConfig.py", data=json.dumps(data), headers=headers)

    await interaction.response.send_message(str(interaction.user.name) + f" Has Changed Bots Settings! Please do /reset to instantly make the changes work.")
    print((str(interaction.user.id) + f" Has Changed Bots Settings! Please do /reset to instantly make the changes work."))




#Show Settings Slash Command
@tree.command(description="Show the Settings of Gemini AI")
async def show_settings(interaction):
  if float(interaction.user.id) != float(Owner_User_Discord_ID):
      await interaction.response.send_message("Only the Owner can Show Bots Settings.", ephemeral=True)
  else:
      global System_Prompt, Temperature_Text, Top_P_Text, Top_K_Text, Max_Output_Tokens_Text, Temperature_Image, Top_P_Image, Top_K_Image, Max_Ouptut_Tokens_Image
      with open("GeminiBotConfig.py", "r") as file:
          filedata = file.read()
      settings = {
          "**System Prompt**": System_Prompt,
          "**Bot Info**": Bot_Info,
          "**Max History**": MAX_HISTORY,
          "**Temperature Text**": Temperature_Text,
          "**Top P Text**": Top_P_Text,
          "**Top K Text**": Top_K_Text,
          "**Max Output Tokens Text**": Max_Output_Tokens_Text,
          "**Temperature Image**": Temperature_Image,
          "**Top P Image**": Top_P_Image,
          "**Top K Image**": Top_K_Image,
          "**Max Output Tokens Image**": Max_Output_Tokens_Image,
      }
      messages = []
      for setting_name, setting_value in settings.items():
          message = f"{setting_name}: {setting_value}\n"
          if len(message) > 2000:
              messages.extend([message[i:i+2000] for i in range(0, len(message), 2000)])
          else:
              messages.append(message)
      for message in messages:
          await interaction.channel.send(message)
      print((str(interaction.user.id) + f" Has Showed: {settings}"))

#Meaning Settings Slash Command
@tree.command(description="Meaning of the Settings of Gemini AI")
async def meaning_settings(interaction):
  if float(interaction.user.id) != float(Owner_User_Discord_ID):
      await interaction.response.send_message("Only the Owner can Show Bots Settings.", ephemeral=True)
  else:
          await interaction.response.send_message("- `System_Prompt`: A special Prompt that instructs the Gemini Pro AI model to follow a certain behavior or interaction style when generating text or image responses.\n- `Bot_Info`: A paramenter where you could put Extra Knowledge to the bot.\n- `MAX_HISTORY`: The maximum number of messages to retain in history for each user. 0 will disable history.\nThere are **2** Types for the following parameters, `Text` for **Gemini Pro AI** and `Image` for **Pro Vision**.\n- `Temperature`: A parameter that controls the creativity or randomness of the text generated by Gemini Pro. A higher temperature results in more diverse and creative output, while a lower temperature makes the output more deterministic and focused.\n- `Top_P`: A parameter that controls the tokens that are considered for text generation by Gemini Pro. Only the tokens that have a cumulative probability mass equal to or higher than top_p are kept for sampling. A lower top_p value makes the output more constrained by the most probable tokens, while a higher top_p value allows for more diversity and exploration.\n- `Top_K`: A parameter that controls the number of highest probability tokens that are considered for text generation by Gemini Pro. Only the top_k tokens are kept for sampling. A lower top_k value makes the output more deterministic and focused, while a higher top_k value allows for more diversity and creativity.\n- `Max_Output_Tokens`: A parameter that controls the maximum number of tokens that Gemini Pro can generate for a text response. A lower value makes the output shorter and more concise, while a higher max_output_tokens_text value allows for longer and more detailed output.", ephemeral=True)
          print((str(interaction.user.id) + f" Has Seen the Meaning of the Settings."))

# ---------------------------------------------Run Bot-------------------------------------------------
bot.run(DISCORD_BOT_TOKEN)
