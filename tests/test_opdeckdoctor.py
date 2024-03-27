import pytest
from playwright.sync_api import Page, expect


@pytest.mark.usefixtures("login")
def test_decklist_browser(page: Page, login):
    page.get_by_role("link", name="Decklist browser").click()
    page.get_by_role("heading", name="Color").click()
    page.get_by_text("Red").click()
    page.get_by_role("heading", name="Set").click()
    page.get_by_text("OP01", exact=True).click()
    page.get_by_placeholder("Search by name").click()
    page.get_by_placeholder("Search by name").fill("Luffy")
    expect(page.get_by_role("main").get_by_role("link")).to_have_count(1)
    page.get_by_role("button", name="Reset filters").click()
    expect(page.get_by_role("main").get_by_role("link")).not_to_have_count(1)


@pytest.mark.usefixtures("login")
def test_card_browser(page: Page, login):
    page.get_by_role("link", name="Card browser").click()
    page.get_by_role("heading", name="Color", exact=True).click()
    page.get_by_text("Red", exact=True).click()
    page.get_by_role("heading", name="Type").click()
    page.get_by_text("Character").click()
    page.get_by_role("heading", name="Utility").click()
    page.get_by_text("Counter 2000").click()
    page.get_by_placeholder("Search by name").click()
    page.get_by_placeholder("Search by name").fill("J")
    expect(page.locator(".grid-item:visible").filter(has_text="Sanji")).to_be_visible()
    expect(page.locator(".grid-item:visible").filter(has_text="Jozu")).to_be_visible()
    expect(page.locator(".grid-item:visible").filter(has_text="Jinbe")).to_be_visible()


@pytest.mark.usefixtures("login")
def test_statistics(page: Page, login, assert_snapshot):
    page.get_by_role("link", name="Statistics").click()
    page.locator("div").filter(has_text="OP02 - Paramount War TCG Red").locator("canvas").first.click(
        position={"x": 171, "y": 116})
    # if this fails run pytest --update-snapshots and try again
    page.wait_for_timeout(1000)
    assert_snapshot(page.screenshot(), "screne.png")


@pytest.mark.usefixtures("login")
def test_teste(page: Page, login, assert_snapshot):
    def get_queen5c():
        page.get_by_role("heading", name="Color", exact=True).click()
        page.get_by_text("Purple").click()
        page.get_by_role("heading", name="Type").click()
        page.get_by_text("Character").click()
        page.get_by_role("heading", name="Cost").click()
        page.get_by_text("5", exact=True).click()
        page.get_by_role("heading", name="Set").click()
        page.get_by_text("Starters").click()
        page.get_by_role("heading", name="Utility").click()
        page.get_by_text("Blocker").click()
        page.get_by_placeholder("Search by name").fill("Q")
    page.get_by_role("link", name="Card Collector").click()
    get_queen5c()
    card_count = page.locator(".number-owned:visible").input_value()
    page.locator(".number-owned:visible").fill(str(int(card_count) + 1))
    page.locator(".number-owned:visible").press("Enter")
    page.reload()
    get_queen5c()
    expect(page.locator("a").filter(has_text="Queen").nth(1)).to_be_visible()
    expect((page.locator(".number-owned:visible"))).to_have_value(str(int(card_count) + 1))