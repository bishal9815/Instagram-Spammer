# Instagram Message Sender

This script sends messages to a specified Instagram account in the background.

## Features

- Sends messages to a target Instagram account
- Can run in the terminal with a message counter or in the background
- Includes cute messages prefixed with "sorry, "
- Logs all activity to a file
- Saves session data for future use

## Requirements

- Python 3.6 or higher
- Instagrapi library (automatically installed if missing)

## Usage

### Run with Python

```
python instagram_sender.py
```

This will:
1. Prompt for your Instagram username and password
2. Ask how many messages to send
3. Ask for the delay between messages
4. Let you choose between terminal mode or background mode

#### Terminal Mode (T)
- Shows a live counter of messages sent
- Displays a countdown between messages
- Shows the content of each message sent

#### Background Mode (B)
- Runs in the background without requiring interaction
- Allows you to continue using your computer
- Logs all activity to a file

### Run in background (Windows)

```
run_instagram_sender_background.bat
```

This will start the script in a minimized window that won't disturb your work.

## Configuration

You can modify the following in the script:

- `TARGET_USERNAME`: The Instagram username to send messages to
- `MESSAGES`: The list of cute messages to send (all prefixed with "sorry, ")

## Monitoring

- In terminal mode, you'll see live updates in the console
- In background mode, check the `instagram_sender_log.txt` file to monitor progress

## Notes

- Use a reasonable delay between messages (at least 10 seconds) to avoid being rate-limited by Instagram
- Instagram may temporarily block message sending if you send too many messages too quickly
- Your session data is stored locally in `instagram_session.pkl` for convenience
