from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
import threading
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv(override=True)
print("INITIAL BOOT UP *************************")
app = Flask(__name__)
scheduler_started = False

@app.route("/sms", methods=['POST'])
def sms_reply():
    global scheduler_started
    
    # 1. Extract incoming message
    incoming_msg = request.values.get('Body', '').strip().lower()
    from_number = request.values.get('From', '')

    # Log the message
    app.logger.info(f"Received SMS from {from_number}: {incoming_msg}")
    
    
    if not scheduler_started:
        # Start the scheduler in a separate thread
        threading.Thread(target=start_monitoring).start()
        scheduler_started = True
        
        # Configure response
        resp = MessagingResponse()
        resp.message("✨💖 OMG HIIII BIRTHDAY QUEEN!!! 💖✨\n\n"
                    "Surprise!! Your boyf got you the MOST iconic birthday gift ever — me!! I'm Delila your personal shopping bestie now!! 💅\n\n"
                    "I'll be spilling ALL the tea about the hottest deals from your fave stores the second they drop! 🛍️👀\n\n" 
                    "No more FOMO on those must-have pieces because I'll text you IMMEDIATELY when there's a price drop on something cute! 🏃‍♀️💨\n\n"
                    "Consider me your 24/7 shopping sidekick who's OBSESSED with saving you coin while keeping you looking fabulous! 💯\n\n"
                    "Can't wait to start sending you the juiciest discounts!! Happy Birthday, babe!! 🎂🎁\n\n"
                    "XOXO,\n"
                    "Your Deal Detective 🕵️‍♀️💕") 
               
        app.logger.info(f"Scheduler activated by {from_number}")
        return Response(str(resp), mimetype="application/xml")
    
    # 3. Handle other messages
    resp = MessagingResponse()
    
    if scheduler_started:
        resp.message("Sorry Diva! Jake hasn't got his lazy ass around to doing conversations yet :(((")
    
    return Response(str(resp), mimetype="application/xml")

def start_monitoring():
    """Start the scheduler process in a separate thread"""
    from scheduler import start_scheduler
    app.logger.info("Starting discount monitoring scheduler...")
    start_scheduler()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)