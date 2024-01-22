import os
#Create at https://makersuite.google.com/
GOOGLE_AI_KEY = os.environ['GOOGLE_API_KEY_GEMINI']
#Create at https://discord.com/developers/applications
DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN_']
#Disable history by setting to 0
MAX_HISTORY = 15

System_Prompt = ""

Temperature_Text = 0.7

Top_P_Text = 1

Top_K_Text = 1

Max_Output_Tokens_Text = 1000

Temperature_Image = 0.4

Top_P_Image = 1

Top_K_Image = 32

Max_Output_Tokens_Image = 1000