from __future__ import annotations

import asyncio
import time
from colorama import Fore, init
from typing import TYPE_CHECKING, Optional

from ..exceptions import AiobaleError
from ..enums import SendCodeType
from ..types.responses import PhoneAuthResponse

if TYPE_CHECKING:
    from .client import Client


init(autoreset=True)


class PhoneLoginCLI:
    def __init__(self, client: Client):
        self.client = client

    async def start(self):
        """Entry point to start the login flow."""
        while True:
            phone_number = await self._request_phone_number()
            try:
                resp = await self._send_login_request(phone_number)
            except AiobaleError:
                print(Fore.RED + "🚫 This phone number is banned. Please try another number.\n")
                continue

            success = await self._handle_code_entry(resp, phone_number)
            if success:
                break  # Exit on successful login

    async def _request_phone_number(self):
        print(Fore.CYAN + "📱 Enter your phone number in international format:\n"
                          "   Example for Iran: 98XXXXXXXXXX (without the + sign)\n")
        while True:
            phone = input(Fore.YELLOW + "Phone number: ")
            if phone.isdigit():
                return int(phone)
            print(Fore.RED + "❌ Invalid input. Please enter digits only.\n")

    async def _send_login_request(self, phone_number: int, code_type: Optional[SendCodeType]=SendCodeType.DEFAULT):
        return await self.client.login(phone_number, code_type=code_type)

    async def _handle_code_entry(self, resp: PhoneAuthResponse, phone_number: int):
        max_attempts = 3
        attempts = 0
        expiration_timestamp = resp.code_expiration_date.value / 1000
        code_timeout = resp.code_timeout.value
        last_sent_time = time.time()

        print(Fore.GREEN + f"✅ Code sent! You have {code_timeout} seconds per attempt.")
        print(Fore.CYAN + "🔑 Enter your code. Available commands:\n"
                          "   'resend' - request a new code\n"
                          "   'restart' - enter your phone number again\n")

        while True:
            if time.time() > expiration_timestamp:
                print(Fore.RED + "⌛ Code expired. Restarting phone entry...\n")
                return False

            try:
                remaining_time = expiration_timestamp - time.time()
                print(Fore.YELLOW + f"⏳ Time left before expiration: {int(remaining_time)} sec")
                print(Fore.YELLOW + f"⌛ Entry timeout: {code_timeout} sec\n")

                try:
                    code = await asyncio.wait_for(
                        asyncio.to_thread(input, Fore.BLUE + "Enter code: "),
                        timeout=code_timeout
                    )
                except asyncio.TimeoutError:
                    print(Fore.RED + f"⏰ Code entry timed out ({code_timeout} sec). Please try again.\n")
                    continue  # Timeout does NOT count as a failed attempt

                code = code.strip().lower()

                if code == "restart":
                    print(Fore.MAGENTA + "🔄 Restarting phone entry...\n")
                    return False

                if code == "resend":
                    cooldown = resp.code_timeout.value
                    elapsed = time.time() - last_sent_time

                    if elapsed < cooldown:
                        wait_seconds = int(cooldown - elapsed)
                        print(Fore.RED + f"⚠️ Wait {wait_seconds} sec before requesting a new code.\n")
                        continue

                    try:
                        resp = await self._send_login_request(phone_number, code_type=resp.next_send_code_type)
                        last_sent_time = time.time()
                        print(Fore.GREEN + "✅ Code resent!\n")
                    except AiobaleError:
                        print(Fore.RED + "🚫 Phone number is banned. Restarting phone entry...\n")
                        return False
                    continue

                # Validate the code
                try:
                    res = await self.client.validate_code(code, resp.transaction_hash)
                    print(Fore.GREEN + f"🎉 Login successful! Welcome {res.user.name}")
                    return True
                except AiobaleError:
                    print(Fore.RED + "❌ Incorrect code. Please try again.\n")
                    attempts += 1
                    if attempts >= max_attempts:
                        print(Fore.RED + "❌ Too many failed attempts. Restarting phone entry...\n")
                        return False

            except Exception as e:
                print(Fore.RED + f"⚠️ Unexpected error: {e}\n")
                return False
