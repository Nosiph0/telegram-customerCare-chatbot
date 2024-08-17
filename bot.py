#!/usr/bin/env python3

import spacy
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from telegram.ext import CallbackContext
import sys
import logging

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Define states
STATE0 = 0

# Load SpaCy model
nlp = spacy.load('en_core_web_sm')

# Define handlers
async def state0_handler(update: Update, context: CallbackContext) -> int:
    """Handle order tracking queries and general questions."""
    doc = nlp(update.message.text.lower())
    order_keywords = ["order", "tracking", "status", "shipment"]
    response = None

    # Check for order-related keywords
    if any(token.text in order_keywords for token in doc):
        response = "Could you please provide your order number so I can check the status for you?"
    elif doc[0].tag_ in ['WDT', 'WP', 'WP$', 'WRB']:
        response = "This looks like a question. How can I assist with your order?"
    else:
        response = random.choice([
            "I'm here to help with your order. Could you provide more details?",
            "Please let me know if you need help with your order or anything else.",
            "Feel free to ask about your order status or any other inquiries.",
        ])
    
    await update.message.reply_text(response)
    return STATE0

async def start(update: Update, context: CallbackContext) -> int:
    """Welcome the user and prompt for service."""
    await update.message.reply_text("Welcome to our customer service bot! How can I assist you with your order today?")
    return STATE0

async def cancel(update: Update, context: CallbackContext) -> int:
    """Exit the conversation."""
    await update.message.reply_text("Thank you for using our service. If you need any further assistance, feel free to ask!")
    return ConversationHandler.END

async def help(update: Update, context: CallbackContext) -> None:
    """Provide help information."""
    await update.message.reply_text("You can ask me about your order status, tracking information, or any other inquiries related to your purchase.")

def main() -> None:
    """Set up and run the bot."""
    application = Application.builder().token('7104023664:AAEtVCLAFEUeuMurz5moD_QAWol-_H1ZO18').build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            STATE0: [MessageHandler(filters.TEXT & ~filters.COMMAND, state0_handler)],
        },
        fallbacks=[CommandHandler('cancel', cancel), CommandHandler('help', help)]
    )
    
    application.add_handler(conv_handler)
    
    application.run_polling()

if __name__ == '__main__':
    main()
