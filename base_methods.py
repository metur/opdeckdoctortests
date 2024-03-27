import pytest
from playwright.sync_api import Page, expect


@pytest.fixture
def login(page: Page):
    page.goto("https://opdeckdoctor.up.railway.app/")
    page.get_by_role("link", name="Get Started").click()
    page.get_by_role("link", name="Login", exact=True).click()
    page.get_by_placeholder("Username").click()
    page.get_by_placeholder("Username").fill("Meteor")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("abcd1234")
    page.get_by_role("button", name="Login").click()
    expect(page.get_by_text("Welcome aboard, Meteor")).to_be_visible()