import time
import random
import logging
import threading
import os
import pickle
from datetime import datetime
import msvcrt  # Windows-specific module for keyboard input

try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, ClientError
except ImportError:
    print("Instagrapi library not found. Installing...")
    import subprocess
    subprocess.check_call(["pip", "install", "instagrapi"])
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, ClientError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='instagram_sender_log.txt',
    filemode='a'
)

# Target Instagram username
TARGET_USERNAME = "roshanip209"

# File to store session data
SESSION_FILE = "instagram_session.pkl"

# List of cute messages to send (all prefixed with "sorry, ")
MESSAGES = [
    "sorry, I just wanted to brighten your day with this message! 🌞",
    "sorry, I couldn't help but send you a virtual hug! 🤗",
    "sorry, just checking if you're having a wonderful day! ✨",
    "sorry, I'm just sending some positive vibes your way! 🌈",
    "sorry, I just wanted to remind you that you're awesome! 🌟",
    "sorry, just dropping by to say you're doing great! 👍",
    "sorry, I just wanted to send you a smile! 😊",
    "sorry, just wanted to say you're amazing just the way you are! 💫",
    "sorry, I just wanted to send you some sparkles to brighten your day! ✨",
    "sorry, just sending you a little ray of sunshine! ☀️",
    "sorry, I just wanted to say hi and hope you're having a good day! 👋",
    "sorry, just sending you a virtual high five! ✋",
    "sorry, I just wanted to remind you that you matter! 💖",
    "sorry, just wanted to send you some good luck today! 🍀",
    "sorry, I just wanted to say you're one in a melon! 🍉",
    "sorry, just sending you a little bit of magic! ✨",
    "sorry, I just wanted to remind you to stay pawsitive! 🐾",
    "sorry, just wanted to say you're tea-riffic! ☕",
    "sorry, I just wanted to remind you that you're purr-fect! 🐱",
    "sorry, just sending you a beary nice message! 🐻",
    "sorry, Every time I think of you, my heart smiles.",
"sorry, You're the sunshine in my cloudy days.",
"sorry, Just hearing your name makes me smile.",
"sorry, You make everything better just by being you.",
"sorry, I think the universe made you just to brighten my life.",
"sorry, If I could bottle up your smile, I'd never be sad again.",
"sorry, You're my favorite hello and my hardest goodbye.",
"sorry, You're the reason my heart beats a little faster.",
"sorry, I didn’t believe in magic until I met you.",
"sorry, Falling for you was the easiest thing I’ve ever done.",
"sorry, You're the sparkle in my eye and the smile on my face.",
"sorry, Whenever I talk to you, I forget all my worries.",
"sorry, I don’t need the whole world, just you in mine.",
"sorry, Your laughter is my favorite sound.",
"sorry, I hope your day is as amazing as your smile.",
"sorry, I like you a little more than I originally planned.",
"sorry, I catch myself smiling when I think of you.",
"sorry, Being with you feels like home.",
"sorry, If I had a flower for every time I thought of you, I’d walk in a garden forever.",
"sorry, I could talk to you all day and never get bored.",
"sorry, You're the reason butterflies still exist in my stomach.",
"sorry, You’re not just a crush, you’re a heart-melter.",
"sorry, You're the reason I believe in beautiful coincidences.",
"sorry, I never believed in soulmates until I met you.",
"sorry, You’re my favorite person to think about.",
"sorry, You make my heart feel light and full at the same time.",
"sorry, When I see your name pop up on my screen, my whole day lights up.",
"sorry, I’d choose you, over and over, without a second thought.",
"sorry, You’re the sweetest part of my life right now.",
"sorry, You're not just cute, you're everything warm and wonderful.",
"sorry, If smiles were stars, yours would light up the galaxy.",
"sorry, I can’t explain it, but being around you feels like magic.",
"sorry, You’ve got a way of making ordinary moments feel special.",
"sorry, You don’t even realize how amazing you are, do you?",
"sorry, My heart does a happy dance every time I see you.",
"sorry, I’m not sure what I did to deserve you crossing my path, but I’m grateful.",
"sorry, Even your texts make me blush.",
"sorry, You’re the kind of person that poems try to describe.",
"sorry, How do you make my heart beat and calm it at the same time?",
"sorry, You’re like my favorite song — I can’t get you out of my head.",
"sorry, You’re the reason I check my phone so much.",
"sorry, If being cute was a crime, you’d be serving life.",
"sorry, You must be a shooting star, because you light up the sky.",
"sorry, You're proof that the best things in life aren’t things — they’re people like you.",
"sorry, Just so you know, you're really special to me.",
"sorry, You’ve got a smile that makes everything okay.",
"sorry, My heart has a favorite person — it’s you.",
"sorry, I could spend forever just looking into your eyes.",
"sorry, I don’t know how, but you make everything feel so calm and beautiful.",
"sorry, I didn’t know what butterflies felt like until I met you.",
"sorry, You’re the one I wish I could tell all my secrets to.",
"sorry, Even a simple ‘hi’ from you makes my day.",
"sorry, You don’t have to say anything — your presence is enough.",
"sorry, Sometimes I just smile at my phone, because of you.",
"sorry, You’re my favorite part of every day.",
"sorry, You're not just in my heart, you're my heart.",
"sorry, If I had one wish, it would be to spend more time with you.",
"sorry, Being near you feels like holding sunshine in my hands.",
"sorry, You give me the kind of feelings people write love songs about.",
"sorry, You're not just on my mind, you're in my dreams too.",
"sorry, I think the stars aligned just so I could meet you.",
"sorry, You’re not just someone I like — you’re someone I admire deeply.",
"sorry, You’re the cozy blanket to my cold nights.",
"sorry, You make awkward moments feel cute.",
"sorry, Every love song reminds me of you.",
"sorry, You’re the kind of person I’d tell my grandkids about.",
"sorry, Can I keep you forever?",
"sorry, You’re the calm in my chaos.",
"sorry, You're a walking heart emoji — but better.",
"sorry, You're effortlessly wonderful.",
"sorry, Being around you is like a warm hug for my soul.",
"sorry, You're my safe place and my happy place.",
"sorry, If smiles had a flavor, yours would taste like joy.",
"sorry, Even when you're not around, you're all I think about.",
"sorry, You've got this quiet kind of magic that I can't get enough of.",
"sorry, You're the dream I didn’t know I had until I met you.",
"sorry, Just wanted to remind you how adorable you are.",
"sorry, You're more than a crush — you're a constant smile in my life.",
"sorry, I didn’t choose to like you — my heart did all the work.",
"sorry, You're the best part of my day, every day.",
"sorry, You make my heart feel like it’s dancing.",
"sorry, I think you might be my favorite human.",
"sorry, I’d write your name in the stars if I could.",
"sorry, Your smile could rival the sunrise.",
"sorry, You're the best 'what if' I’ve ever had.",
"sorry, You're the chapter I never want to end.",
"sorry, I want to make you feel as special as you make me feel.",
"sorry, You're the one I want to share my ice cream and secrets with.",
"sorry, I’d choose you even if I had a million options.",
"sorry, You’re the inspiration behind my happiest thoughts.",
"sorry, You’re the sweetest part of my favorite memories.",
"sorry, I like you. A lot. Like, a-lot-a-lot.",
"sorry, Your voice is my favorite melody.",
"sorry, You're the peanut butter to my jelly, the moon to my stars.",
"sorry, You’re the kind of person I hope to see in every tomorrow.",
"sorry, I’ve got a little crush on you… okay, maybe a big one.",
"sorry, You’re the cutest plot twist life ever gave me.",
"sorry, Talking to you feels like finding a four-leaf clover — rare and lucky.",
"sorry, You're my favorite reason to smile for no reason.",
"sorry, You're the best thing I didn’t know I was looking for.",
"sorry, You're basically the definition of adorable.",
"sorry, Your presence makes my world more colorful.",
"sorry, You're not just cute — you're heart-meltingly lovely.",
"sorry, Everything feels better when you're around.",
"sorry, You’re the kind of person I hope never leaves my life.",
"sorry, You're my sunshine on even the cloudiest days.",
"sorry, Every time I see you, it feels like the first time.",
"sorry, You're the one I can’t wait to tell everything to.",
"sorry, You're the one who always makes my heart skip a beat.",
"sorry, My heart is full when you're around.",
"sorry, You're the reason I wake up with a smile on my face.",
"sorry, You're the reason I believe in love at first sight.",
"sorry, I hope you know how much you mean to me.",
"sorry, You're the best part of my life.",
"sorry, I hope you know how much you mean to me.",
"sorry, You're the best part of my life.",
"sorry, I hope you know how much you mean to me.",
"sorry, You're the best part of my life.",
"sorry, I hope you know how much you mean to me.",


]

class InstagramSender:
    def __init__(self):
        self.client = Client()
        self.logged_in = False
        self.message_count = 0
        self.target_user_id = None
        self.running = False
        self.thread = None
        self.username = None

    def load_session(self):
        """Load session from file if it exists."""
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, 'rb') as f:
                    session_data = pickle.load(f)
                    self.client.set_settings(session_data)
                    self.username = session_data.get('username')

                # Verify the session is still valid
                try:
                    self.client.get_timeline_feed()
                    self.logged_in = True
                    logging.info(f"Successfully loaded session for {self.username}")
                    return True
                except Exception:
                    logging.warning("Saved session is invalid or expired")
                    return False
            except Exception as e:
                logging.error(f"Error loading session: {str(e)}")
                return False
        return False

    def save_session(self):
        """Save session to file."""
        if self.logged_in:
            try:
                session_data = self.client.get_settings()
                session_data['username'] = self.username
                with open(SESSION_FILE, 'wb') as f:
                    pickle.dump(session_data, f)
                logging.info("Session saved successfully")
                return True
            except Exception as e:
                logging.error(f"Error saving session: {str(e)}")
                return False
        return False

    # Removed browser login function

    def login(self, username, password):
        """Login to Instagram."""
        # First try to load existing session
        if self.load_session():
            return True

        # If no session or session invalid, try direct login
        try:
            self.client.login(username, password)
            self.username = username
            self.logged_in = True
            self.save_session()
            logging.info(f"Successfully logged in as {username}")
            return True
        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            return False

    def get_user_id(self, username):
        """Get user ID from username."""
        try:
            user = self.client.user_info_by_username(username)
            return user.pk
        except Exception as e:
            logging.error(f"Failed to get user ID for {username}: {str(e)}")
            return None

    def send_message(self, message):
        """Send a message to the target user."""
        if not self.logged_in:
            logging.error("Not logged in. Cannot send message.")
            return False

        if not self.target_user_id:
            self.target_user_id = self.get_user_id(TARGET_USERNAME)
            if not self.target_user_id:
                logging.error(f"Could not find user ID for {TARGET_USERNAME}")
                return False

        try:
            # Add timestamp to make each message unique
            timestamped_message = f"{message} [{datetime.now().strftime('%H:%M:%S')}]"

            # Send the direct message
            self.client.direct_send(text=timestamped_message, user_ids=[self.target_user_id])

            self.message_count += 1
            logging.info(f"Message #{self.message_count} sent: '{message}'")
            return True
        except LoginRequired:
            logging.error("Login session expired. Please log in again.")
            self.logged_in = False
            return False
        except Exception as e:
            logging.error(f"Error sending message: {str(e)}")
            return False

    def start_background_sender(self, num_messages, delay_seconds):
        """Start sending messages in the background."""
        if self.running:
            logging.warning("Background sender is already running.")
            return False

        self.running = True
        self.thread = threading.Thread(
            target=self._background_sender_task,
            args=(num_messages, delay_seconds)
        )
        self.thread.daemon = True  # Allow the thread to exit when the main program exits
        self.thread.start()
        return True

    def _background_sender_task(self, num_messages, delay_seconds):
        """Background task to send messages."""
        try:
            for i in range(num_messages):
                if not self.running:
                    break

                # Choose a random message
                message = random.choice(MESSAGES)

                # Send the message
                success = self.send_message(message)

                if not success:
                    logging.error(f"Failed to send message #{i+1}. Stopping background sender.")
                    break

                # Sleep before sending the next message
                if i < num_messages - 1:  # Don't sleep after the last message
                    time.sleep(delay_seconds)

        except Exception as e:
            logging.error(f"Background sender error: {str(e)}")
        finally:
            self.running = False
            logging.info(f"Background sender finished. Sent {self.message_count} messages.")

    def stop_background_sender(self):
        """Stop the background sender."""
        if not self.running:
            logging.warning("Background sender is not running.")
            return False

        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)  # Wait for the thread to finish

        logging.info("Background sender stopped.")
        return True

def send_messages_in_terminal(sender, num_messages, delay_seconds):
    """Send messages in the terminal with a visible counter."""
    print("\nStarting to send messages in terminal...")
    print(f"Will send {num_messages} messages with {delay_seconds} seconds delay between each.")
    print("Press Ctrl+C at any time to stop the program.")
    print("-" * 50)

    try:
        for i in range(num_messages):
            # Choose a random message
            message = random.choice(MESSAGES)

            # Send the message
            success = sender.send_message(message)

            if success:
                print(f"Message #{sender.message_count}/{num_messages} sent: '{message}'")
            else:
                print(f"Failed to send message #{i+1}. Check the log file for details.")
                break

            # If we've sent all messages, break out of the loop
            if sender.message_count >= num_messages:
                break

            # Show countdown for next message
            if i < num_messages - 1:  # Don't show countdown after the last message
                print(f"Next message will be sent in {delay_seconds} seconds...")
                for remaining in range(delay_seconds, 0, -1):
                    print(f"\rTime remaining: {remaining} seconds...", end="")
                    time.sleep(1)
                print("\r" + " " * 40 + "\r", end="")  # Clear the countdown line

    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        print(f"An error occurred: {str(e)}")

    # Final summary
    print("\n" + "=" * 50)
    print(f"Summary: Sent {sender.message_count} out of {num_messages} messages")
    print("=" * 50)

def main():
    """Main function to run the Instagram message sender."""
    print("=" * 50)
    print("Instagram Message Sender (Terminal Mode)")
    print("=" * 50)
    print(f"Target: {TARGET_USERNAME}")
    print()

    # Create the sender
    sender = InstagramSender()

    # Get Instagram credentials
    username = input("Enter your Instagram username: ")
    print("Enter your Instagram password (your typing will be hidden for security): ", end="", flush=True)
    password = ""
    while True:
        char = msvcrt.getch().decode('utf-8', errors='ignore')
        if char == '\r' or char == '\n':  # Enter key
            print()  # Move to next line after password entry
            break
        elif char == '\b':  # Backspace
            if password:
                password = password[:-1]
                print('\b \b', end='', flush=True)  # Erase character from terminal
        elif char.isprintable():
            password += char
            print('*', end='', flush=True)  # Show * for each character

    # Login to Instagram
    print("\nAttempting to login to Instagram...")
    if not sender.login(username, password):
        print("Login failed. Check the log file for details.")
        return

    print("Login successful!")

    # Ask user for the number of messages to send
    while True:
        try:
            num_messages = input("How many messages do you want to send? ")
            num_messages = int(num_messages)
            if num_messages <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    # Ask user for the delay between messages
    while True:
        try:
            delay_seconds = input("Delay between messages (seconds, minimum 10): ")
            delay_seconds = int(delay_seconds)
            if delay_seconds < 10:
                print("Delay must be at least 10 seconds to avoid rate limiting.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    # Ask user whether to send in terminal or background
    while True:
        mode = input("\nSend messages in [T]erminal or [B]ackground? (T/B): ").strip().upper()
        if mode == 'T':
            send_messages_in_terminal(sender, num_messages, delay_seconds)
            break
        elif mode == 'B':
            print("\nStarting background message sender...")
            print(f"Will send {num_messages} messages with {delay_seconds} seconds delay between each.")

            # Start the background sender
            if sender.start_background_sender(num_messages, delay_seconds):
                print("Background sender started successfully!")
                print("You can continue with your work while messages are being sent.")
                print("The program will exit when all messages have been sent.")
                print("Press Ctrl+C at any time to stop the program.")

                try:
                    # Wait for the background sender to finish
                    while sender.running:
                        time.sleep(1)

                    print("\n" + "=" * 50)
                    print(f"Summary: Sent {sender.message_count} out of {num_messages} messages")
                    print("=" * 50)

                except KeyboardInterrupt:
                    print("\nStopping background sender...")
                    sender.stop_background_sender()
                    print(f"Summary: Sent {sender.message_count} out of {num_messages} messages")
            else:
                print("Failed to start background sender. Check the log file for details.")
            break
        else:
            print("Please enter 'T' for Terminal or 'B' for Background.")

if __name__ == "__main__":
    main()
