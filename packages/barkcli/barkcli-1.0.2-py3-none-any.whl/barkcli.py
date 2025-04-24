
import argparse
import os
import sys
from BarkNotificator import BarkNotificator

import requests
requests.Response.is_success = property(lambda self: self.ok)

def main():
    parser = argparse.ArgumentParser(description="Send push notification via Bark.")

    parser.add_argument('title', nargs='?', help='Notification title')
    parser.add_argument('content', nargs='?', help='Notification content')
    parser.add_argument('icon_url', nargs='?', help='Icon URL (optional)')
    parser.add_argument('target_url', nargs='?', help='Target URL (optional)')
    parser.add_argument('category', nargs='?', help='Category (optional)')
    parser.add_argument('ringtone', nargs='?', help='Ringtone (optional)')

    parser.add_argument('--title', dest='title_opt', help='Notification title')
    parser.add_argument('--content', dest='content_opt', help='Notification content')
    parser.add_argument('--token', help='Bark device token (or set BARK_TOKEN env var)')
    parser.add_argument('--icon_url', dest='icon_url_opt', help='Icon URL')
    parser.add_argument('--target_url', dest='target_url_opt', help='Target URL')
    parser.add_argument('--category', dest='category_opt', help='Category')
    parser.add_argument('--ringtone', dest='ringtone_opt', help='Ringtone name')

    args = parser.parse_args()

    title = args.title_opt or args.title
    content = args.content_opt or args.content
    icon_url = args.icon_url_opt or args.icon_url or ""
    target_url = args.target_url_opt or args.target_url or ""
    category = args.category_opt or args.category or ""
    ringtone = args.ringtone_opt or args.ringtone or "bell.caf"
    token = args.token or os.getenv('BARK_TOKEN')

    if not token:
        print("Error: You must provide a device token via --token or BARK_TOKEN env var.")
        sys.exit(1)

    if not title or not content:
        print("Error: Title and content are required.")
        sys.exit(1)

    bark = BarkNotificator(device_token=token)
    bark.send(
        title=title,
        content=content,
        icon_url=icon_url,
        target_url=target_url,
        category=category,
        ringtone=ringtone
    )
