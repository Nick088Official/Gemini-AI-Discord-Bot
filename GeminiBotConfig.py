import os
#Create at https://makersuite.google.com/
GOOGLE_AI_KEY = os.environ['GOOGLE_API_KEY_GEMINI']
#Create at https://discord.com/developers/applications
DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN_']
Owner_User_Discord_ID = os.environ['DISCORD_OWNER_ID']

System_Prompt = "You are Gemini AI."

Bot_Info = "Nick088 is the name of your creator."

Temperature_Text = 0.6

#Disable history by setting to 0
MAX_HISTORY = 10

Top_P_Text = 1

Top_K_Text = 1

Max_Output_Tokens_Text = 1000

Temperature_Image = 0.4

Top_P_Image = 1

Top_K_Image = 32

Max_Output_Tokens_Image = 1000
