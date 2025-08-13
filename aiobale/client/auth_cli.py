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
    """
    PhoneLoginCLI is a command-line interface (CLI) utility for handling phone-based login flows 
    using the `aiobale` client library. It provides a step-by-step interactive process for users 
    to authenticate via their phone numbers, enter verification codes, and handle password-protected 
    accounts if required.
    Attributes:
        client (Client): The `aiobale` client instance used for handling authentication requests.
    Usage:
        This class is designed to be used in an asynchronous context. Instantiate it with 
        a `Client` object and call the `start()` method to begin the login process.
    """
    
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
        return await self.client.start_phone_auth(phone_number, code_type=code_type)

    async def _handle_code_entry(self, resp: PhoneAuthResponse, phone_number: int):
        max_attempts = 3
        attempts = 0
        expiration_timestamp = resp.code_expiration_date.value / 1000
        last_sent_time = time.time()
        next_code_type = resp.next_send_code_type

        print(Fore.GREEN + f"✅ Code sent!")
        print(Fore.CYAN + "🔑 Enter your code. Available commands:\n"
                          "   'resend' - request a new code\n"
                          "   'restart' - enter your phone number again\n")

        while True:
            if time.time() > expiration_timestamp:
                print(Fore.RED + "⌛ Code expired. Restarting phone entry...\n")
                return False

            try:
                remaining_time = expiration_timestamp - time.time()
                cooldown = resp.code_timeout.value
                elapsed = time.time() - last_sent_time

                print(Fore.YELLOW + f"⏳ Time left before expiration: {int(remaining_time)} sec")
                print(Fore.YELLOW + f"⌛ New code timeout: {int(cooldown - elapsed)} sec\n")

                try:
                    code = await asyncio.wait_for(
                        asyncio.to_thread(input, Fore.BLUE + "Enter code: "),
                        timeout=remaining_time
                    )
                except asyncio.TimeoutError:
                    print(Fore.RED + f"⏰ Code entry timed out. Please try again.\n")
                    return False

                code = code.strip().lower()

                if code == "restart":
                    print(Fore.MAGENTA + "🔄 Restarting phone entry...\n")
                    return False

                if code == "resend":
                    if elapsed < cooldown:
                        wait_seconds = int(cooldown - elapsed)
                        print(Fore.RED + f"⚠️ Wait {wait_seconds} sec before requesting a new code.\n")
                        continue

                    if next_code_type is None:
                        print(Fore.RED + f"⚠️ Resend is not available.\n")
                        continue

                    try:
                        resp = await self._send_login_request(phone_number, code_type=next_code_type)
                        last_sent_time = time.time()
                        expiration_timestamp = resp.code_expiration_date.value / 1000
                        print(Fore.GREEN + "✅ Code resent!\n")
                    except AiobaleError:
                        print(Fore.RED + "🚫 Phone number is banned. Restarting phone entry...\n")
                        return False
                    continue

                # Validate the code
                try:
                    res = await self.client.validate_code(code, resp.transaction_hash)
                    await self._on_login_success(res)
                    return True
                except AiobaleError as e:
                    if str(e) == "Password needed for login":
                        return await self._handle_password_entry(resp.transaction_hash)
                    elif str(e) == "Register":
                        print(Fore.RED + "❌ First sign up using official Bale client.\n")
                        return False
                    
                    print(Fore.RED + "❌ Incorrect code. Please try again.\n")
                    attempts += 1
                    if attempts >= max_attempts:
                        print(Fore.RED + "❌ Too many failed attempts. Restarting phone entry...\n")
                        return False

            except Exception as e:
                print(Fore.RED + f"⚠️ Unexpected error: {e}\n")
                return False
            
    async def _handle_password_entry(self, transaction_hash: str):
        max_attempts = 3
        attempts = 0
        print(Fore.MAGENTA + "🔐 This account requires a password.\n")

        while attempts < max_attempts:
            try:
                password = await asyncio.wait_for(
                    asyncio.to_thread(input, Fore.BLUE + "Enter password: "),
                    timeout=60
                )
            except asyncio.TimeoutError:
                print(Fore.RED + "⏰ Password entry timed out. Restarting...\n")
                return False

            try:
                res = await self.client.validate_password(password.strip(), transaction_hash)
                await self._on_login_success(res)
                return True
            except AiobaleError as e:
                if str(e) == "Wrong password specified.":
                    print(Fore.RED + "❌ Incorrect password. Try again.\n")
                    attempts += 1
                else:
                    print(Fore.RED + f"⚠️ Error: {e}\n")
                    return False

        print(Fore.RED + "❌ Too many failed password attempts. Restarting...\n")
        return False
    
    async def _on_login_success(self, res):
        print(Fore.GREEN + f"🎉 Login successful! Welcome {res.user.name}")
