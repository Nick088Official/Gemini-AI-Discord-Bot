import os
#Create at https://makersuite.google.com/
GOOGLE_AI_KEY = os.environ['GOOGLE_API_KEY_GEMINI']
#Create at https://discord.com/developers/applications
DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN_']
Owner_User_Discord_ID = os.environ['DISCORD_OWNER_ID']
#Disable history by setting to 0
MAX_HISTORY = 15

System_Prompt = "you are Gemini AI, act as you are on discord,like you are an ai discord chatbot, be short and normal as always, you have ethic morals and don't help with anything bad or illegal or immoral"

Temperature_Text = 0.7

Top_P_Text = 1

Top_K_Text = 1

Max_Output_Tokens_Text = 1000

Temperature_Image = 0.4

Top_P_Image = 1

Top_K_Image = 32

Max_Output_Tokens_Image = 1000
