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
    "Let's break up, I think we're like oil and water... we just don’t mix, but at least we both look good separately,",

"Let's break up, I’ve decided we’re like socks after laundry, just not a perfect pair anymore,",

"Let's break up, I realized you’re the avocado toast of my life—totally overrated,",

"Let's break up, You're like my phone battery... always draining and never charged,",

"Let's break up, We’re like a missed call... just never meant to be,",

"Let's break up, I think we're like a broken pencil—pointless,",

"Let's break up, I think we need to break up because you’re the Wi-Fi that keeps disconnecting,",

"Let's break up, You’re like the extra baggage I didn’t want to carry,",

"Let's break up, You’re like a snack that’s always out of my reach—tempting but impossible,",

"Let's break up, You’re like the socks that always lose their pair... just not complete without me,",

"Let's break up, I think we're like a song on repeat... fun at first, but I’m over it now,",

"Let's break up, You’re like a parking ticket... expensive, and I’m not sure why I even have you,",

"Let's break up, We’re like a flat tire... always in need of a little air,",

"Let's break up, You’re like a bad coffee—no energy, no fun,",

"Let's break up, You’re like an old text message that I never respond to,",

"Let's break up, I think we're like expired milk... not worth keeping around,",

"Let's break up, You're like the Wi-Fi password I can’t remember,",

"Let's break up, I think we're like two jigsaw pieces that’ll never fit together,",

"Let's break up, You’re like a bad meme… people are laughing at you, not with you,",

"Let's break up, You’re like a one-hit wonder—good for a moment, but that’s it,",

"Let's break up, I think we need a break... you’re like the skip button I always click,",

"Let's break up, You're like an old pair of shoes—worn out and uncomfortable,",

"Let's break up, We’re like a cup of tea that’s gone cold... not worth drinking anymore,",

"Let's break up, I think we're like a traffic jam—stuck, frustrated, and not moving anywhere,",




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
