import re
from asyncio import run, sleep
from enum import StrEnum
from os.path import dirname
from typing import Literal
from playwright.async_api import async_playwright, Page, BrowserContext
from pyotp import TOTP
from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from playwright._impl._errors import TimeoutError
from x_model import init_db
from xync_schema import models
from xync_schema.enums import UserStatus

from xync_client.TgWallet.pyro import PyroClient
from xync_client.loader import PG_DSN


class ExtraCaptchaException(Exception): ...


async def login(pg: Page):
    await pg.locator("input#j_username").fill("mixartemev@gmail.com")
    await pg.locator("input#j_password").fill("mixfixX98")
    await pg.click("input#loginToAdvcashButton")
    code = await wait_for_code("login")
    await pg.locator("input#otpId").fill(code)
    await pg.click("input#checkOtpButton")
    await pg.wait_for_url(Pages.HOME)


async def captcha_click(pg: Page):
    captcha_url = pg.url
    cbx = pg.frame_locator("#main-iframe").frame_locator("iframe").first.locator("div#checkbox")
    await cbx.wait_for(state="visible"), await pg.wait_for_timeout(500)
    await cbx.click(delay=94)
    try:
        await pg.wait_for_url(lambda url: url != captcha_url)
    except TimeoutError:  # if page no changed -> captcha is undone
        await pg.screenshot(path=dirname(__file__) + "/xtr_captcha.png")
        raise ExtraCaptchaException(pg.url)


class Pages(StrEnum):
    base_url = "https://account.volet.com/"
    LOGIN = base_url + "login"
    OTP = base_url + "login/otp"
    HOME = base_url + "pages/transaction"
    SEND = base_url + "pages/transfer/wallet"
    GMH = "https://mail.google.com/mail/u/0/"


def parse_transaction_info(text: str) -> dict[str, str] | None:
    # Поиск ID транзакции
    transaction_id_match = re.search(r"Transaction ID:\s*([\w-]+)", text)
    # Поиск суммы и валюты
    amount_match = re.search(r"Amount:\s*([+-]?[0-9]*\.?[0-9]+)\s*([A-Z]+)", text)
    # Поиск email отправителя
    sender_email_match = re.search(r"Sender:\s*([\w.-]+@[\w.-]+)", text)

    if transaction_id_match and amount_match and sender_email_match:
        return {
            "transaction_id": transaction_id_match.group(1),
            "amount": amount_match.group(1),
            "currency": amount_match.group(2),
            "sender_email": sender_email_match.group(1),
        }
    return None


async def got_msg(_, msg: Message):
    if "Your OTP code:" in msg.text:
        bot_msgs["otp_login"] = msg.text[-6:]
    if "Confirmation code:" in msg.text:
        bot_msgs["otp_send"] = msg.text[-6:]
    elif "Status: Completed. Sender:" in msg.text:
        bot_msgs["got_payment"] = parse_transaction_info(msg.text)


volet_listen = MessageHandler(got_msg, filters.chat(["ProtectimusBot"]))

bot_msgs: dict = {"otp_send": None}


async def wait_for_code(typ: Literal["login", "send"], past: int = 0, timeout: int = 5) -> str:
    while past < timeout:
        if code := bot_msgs.pop(f"otp_{typ}", None):
            return code
        await sleep(1)
        past += 1
        return await wait_for_code(typ, past)


async def wait_for_payment(page: Page, user_id: int, interval: int = 29):
    while (await models.User[user_id]).status > UserStatus.SLEEP:
        await page.reload()
        await page.wait_for_timeout(interval * 1000)


async def send(dest: str, amount: float, pg: Page, agent: models.PmAgent, ub: PyroClient):
    await vlt_go(pg, Pages.SEND, ub)
    await pg.click("[class=combobox-account]")
    await pg.click('[class=rf-ulst-itm] b:has-text("Ruble ")')
    await pg.wait_for_timeout(200)
    await pg.fill("#srcAmount", str(amount))
    await pg.fill("#destWalletId", dest)
    await pg.wait_for_timeout(300)
    await pg.locator("input[type=submit]", has_text="continue").click()
    if otp := agent.auth.get("otp"):
        totp = TOTP(otp)
        code = totp.now()
    elif agent.auth.get("sess"):
        if not (code := await wait_for_code("send")):  # todo: why no get code?
            gpage = await gmail_page(pg.context, agent, ub)
            await mail_confirm(gpage, ub)
    else:
        raise Exception(f"PmAgent {agent.user.id} has No OTP data")
    if not code:
        await ub.send_img("no code!", await pg.screenshot())
        raise Exception("no code!")
    await pg.fill("#securityValue", code)
    await pg.locator("input[type=submit]", has_text="confirm").click()
    await pg.wait_for_url(Pages.SEND)
    await pg.get_by_role("heading").click()
    slip = await pg.screenshot(clip={"x": 440, "y": 205, "width": 420, "height": 360})
    await ub.send_img(f"{amount} to {dest} sent", slip)


async def gmail_page(ctx: BrowserContext, agent: models.PmAgent, ub: PyroClient) -> Page:
    gp = await ctx.new_page()
    await gp.goto(Pages.GMH)
    if not gp.url.startswith(Pages.GMH):
        # если надо выбрать акк
        if await gp.locator("h1#headingText", has_text="Choose an account").count():
            await gp.locator("li").first.click()
        # если надо c 0 залогиниться
        elif await gp.locator("h1#headingText", has_text="Sign In").count():
            await gp.fill("input[type=email]", agent.user.gmail_auth["login"])
            await gp.locator("button", has_text="Next").click()
        # осталось ввести пороль:
        await gp.fill("input[type=password]", agent.user.gmail_auth["password"])
        await gp.locator("button", has_text="Next").click()
        await ub.send_img("Аппрувни гмейл, у тебя 1.5 минуты", await gp.screenshot())
    await gp.wait_for_url(lambda u: u.startswith(Pages.GMH), timeout=90 * 1000)  # убеждаемся что мы в почте
    return gp


async def mail_confirm(gp: Page, ub: PyroClient):
    lang = await gp.get_attribute("html", "lang")
    labs = {
        "ru": "Оповещения",
        "en-US": "Updates",
    }
    tab = gp.get_by_role("heading").get_by_label(labs[lang]).last
    await tab.click()
    rows = gp.locator("tbody>>nth=4 >> tr")
    row = rows.get_by_text("Volet.com").and_(rows.get_by_text("Please Confirm Withdrawal"))
    if not await row.count():
        return await ub.send_img("А нет запросов от волета", await gp.screenshot())
    await row.click()
    await gp.wait_for_load_state()
    btn = gp.locator('a[href^="https://account.volet.com/verify/"]', has_text="confirm").first
    await btn.click()


async def vlt_go(pg: Page, url: Pages, ub: PyroClient):
    try:
        resp = await pg.goto(url)
        if resp.headers.get("content-length", 1000) < 1000:  # is cap page
            await captcha_click(pg)
    except Exception as e:
        await ub.send_img(repr(e), await pg.screenshot())
        raise e


async def main():
    _ = await init_db(PG_DSN, models, True)
    agent = await models.PmAgent.get(user__role=6, user__status__gt=0, pm__norm="volet").prefetch_related("user")
    ubot = PyroClient(agent)
    await ubot.app.start()
    ubot.app.add_handler(volet_listen)

    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        channel="chrome",
        headless=True,
        timeout=3000,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-web-security",
            "--disable-infobars",
            "--disable-extensions",
            "--start-maximized",
        ],
    )
    context = await browser.new_context(storage_state=agent.auth.get("state", {}), locale="en-US")
    context.set_default_navigation_timeout(5000)
    context.set_default_timeout(4000)
    page = await context.new_page()
    # gp = await gmail_page(context, agent, ubot)
    await vlt_go(page, Pages.HOME, ubot)
    if page.url == Pages.LOGIN:
        await login(page)
    if page.url == Pages.HOME:
        await send("alena.artemeva25@gmail.com", 8.3456, page, agent, ubot)
        # await wait_for_payment(page, agent.user_id)
    else:
        await page.screenshot(path=dirname(__file__) + "/unknown.png")
        raise Exception("Unknown")
    # save state
    if state := await context.storage_state():
        agent.auth["state"] = state
        await agent.save()
    # closing
    await context.close()
    await browser.close()
    ubot.app.remove_handler(volet_listen)
    await ubot.app.stop()
    await _.close()


if __name__ == "__main__":
    run(main())
