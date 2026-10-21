# Wordpress-slam-bot
AI-Chatgpt-Telegram+Chargpt+Wordpress
import os
import telebot
import openai
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
WP_URL = os.environ.get("WP_URL", "https://selamawitmuluneh425-iufxs.wordpress.com?ref=agent_telegram")
WP_USER = os.environ.get("WP_USER")
WP_PASSWORD = os.environ.get("WP_PASSWORD")

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 
        "ሰላም! 👋 እኔ Wordpress AI Assistant ነኝ!\n\n"
        "📝 /chat [message] - ChatGPT ጋር ተነጋገር\n"
        "🖼️ /image [description] - ምስል ፍጠር\n"
        "📰 /posts - WordPress posts ተመልከት\n"
        "❓ /help - እርዳታ"
    )

# /help command
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message,
        "🤖 Commands:\n"
        "/image ቀይ አበባ - ምስል ፍጠር\n"
        "/chat ሰላም እንዴት ነህ - ChatGPT\n"
        "/posts - WordPress posts"
    )

# 🖼️ IMAGE GENERATION
@bot.message_handler(commands=['image'])
def generate_image(message):
    prompt = message.text.replace('/image', '').strip()
    if not prompt:
        bot.reply_to(message, "❌ ምስል description ጻፍ!\nምሳሌ: /image ቀይ አበባ ሜዳ ላይ")
        return
    
    bot.reply_to(message, "🎨 ምስል እየሰራሁ... ጠብቅ!")
    
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        image_url = response.data[0].url
        
        # Telegram ላይ ምስሉን ላክ
        bot.send_photo(message.chat.id, image_url, 
                      caption=f"🖼️ '{prompt}' - DALL-E 3")
        
        # WordPress ላይ አስቀምጥ (optional)
        save_to_wordpress(prompt, image_url)
        
    except Exception as e:
        bot.reply_to(message, f"❌ ስህተት: {str(e)}")

# WordPress ላይ ምስሉን save አድርግ
def save_to_wordpress(prompt, image_url):
    try:
        img_data = requests.get(image_url).content
        headers = {'Content-Disposition': f'attachment; filename="ai-image.jpg"',
                  'Content-Type': 'image/jpeg'}
        requests.post(
            f"{WP_URL}/wp-json/wp/v2/media",
            auth=(WP_USER, WP_PASSWORD),
            headers=headers,
            data=img_data
        )
    except:
        pass

# 💬 ChatGPT
@bot.message_handler(commands=['chat'])
def chat(message):
    prompt = message.text.replace('/chat', '').strip()
    if not prompt:
        bot.reply_to(message, "❌ Message ጻፍ!\nምሳሌ: /chat ሰላም እንዴት ነህ?")
        return
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        bot.reply_to(message, response.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, f"❌ ስህተት: {str(e)}")

# 📰 WordPress Posts
@bot.message_handler(commands=['posts'])
def get_posts(message):
    try:
        r = requests.get(f"{WP_URL}/wp-json/wp/v2/posts?per_page=5")
        posts = r.json()
        if not posts:
            bot.reply_to(message, "📭 Posts የሉም!")
            return
        text = "📰 WordPress Posts:\n\n"
        for p in posts:
            text += f"• {p['title']['rendered']}\n"
        bot.reply_to(message, text)
    except Exception as e:
        bot.reply_to(message, f"❌ ስህተት: {str(e)}")

# ማንኛውም message — ChatGPT ይልካል
@bot.message_handler(func=lambda m: True)
def handle(message):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": message.text}]
        )
        bot.reply_to(message, response.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, f"❌ ስህተት: {str(e)}")

bot.infinity_polling()
OPENAI_API_KEY=your_openai_key
WP_URL=https://selamawitmuluneh425-iufxs.wordpress.com?ref=agent_telegram
WP_USER=selamawitmuluneh425
WP_PASSWORD=your_app_passwordCommand          ተግባር                  
───────────────────────────────────────
`/image ቀይ አበባ`  🖼️ DALL-E 3 ምስል ይፈጥራል 
`/chat ሰላም`      💬 GPT-4o ይናገራል        
`/posts`         📰 WordPress posts ያሳያል
ማንኛውም text       🤖 GPT-4o ይመልሳል        
