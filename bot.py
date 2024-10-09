
import telebot
from linkedin_automation import run_linkedin_automation
from internshala_automation import run_internshala_automation

bot = telebot.TeleBot('7598441515:AAHhvLSNlXKKJbmuFPLrqTw2sGAXmnewEhI')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Use /apply_linkedin or /apply_internshala to start applying for jobs.")

@bot.message_handler(commands=['apply_linkedin'])
def handle_apply_linkedin(message):
    bot.reply_to(message, "Please provide your LinkedIn cookies in the format: li_at=VALUE;JSESSIONID=VALUE")
    bot.register_next_step_handler(message, process_linkedin_cookies)

@bot.message_handler(commands=['apply_internshala'])
def handle_apply_internshala(message):
    bot.reply_to(message, "Please provide your Internshala cookies.")
    bot.register_next_step_handler(message, process_internshala_cookies)

def process_linkedin_cookies(message):
    cookie_string = message.text
    cookies = [{'name': cookie.split('=')[0], 'value': cookie.split('=')[1]} for cookie in cookie_string.split(';')]
    bot.reply_to(message, "Cookies received. Please provide the job search keyword.")
    bot.register_next_step_handler(message, lambda m: ask_for_resume_linkedin(m, cookies))

def process_internshala_cookies(message):
    cookie_string = message.text
    cookies = [{'name': cookie.split('=')[0], 'value': cookie.split('=')[1]} for cookie in cookie_string.split(';')]
    bot.reply_to(message, "Cookies received. Please provide the internship search keyword.")
    bot.register_next_step_handler(message, lambda m: ask_for_resume_internshala(m, cookies))

def ask_for_resume_linkedin(message, cookies):
    search_keyword = message.text
    bot.reply_to(message, "Please upload your resume (PDF format).")
    bot.register_next_step_handler(message, lambda m: start_linkedin_application(m, cookies, search_keyword))

def ask_for_resume_internshala(message, cookies):
    search_keyword = message.text
    bot.reply_to(message, "Please upload your resume (PDF format).")
    bot.register_next_step_handler(message, lambda m: start_internshala_application(m, cookies, search_keyword))

def start_linkedin_application(message, cookies, search_keyword):
    if message.content_type == 'document':
        resume_file = message.document
        resume_path = f'resumes/{resume_file.file_id}_resume.pdf'  # Store in resumes directory
        file_info = bot.get_file(resume_file.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Save the file to local storage
        with open(resume_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, f"Starting job application process for LinkedIn with keyword: {search_keyword}")
        try:
            result = run_linkedin_automation(cookies, search_keyword, resume_path)
            bot.reply_to(message, result)
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {str(e)}")
    else:
        bot.reply_to(message, "Please upload a valid PDF resume.")

def start_internshala_application(message, cookies, search_keyword):
    if message.content_type == 'document':
        resume_file = message.document
        resume_path = f'resumes/{resume_file.file_id}_resume.pdf'  # Store in resumes directory
        file_info = bot.get_file(resume_file.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Save the file to local storage
        with open(resume_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, f"Starting internship application process for Internshala with keyword: {search_keyword}")
        try:
            result = run_internshala_automation(cookies, search_keyword, resume_path)
            bot.reply_to(message, result)
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {str(e)}")
    else:
        bot.reply_to(message, "Please upload a valid PDF resume.")

if __name__ == "__main__":
    bot.polling()