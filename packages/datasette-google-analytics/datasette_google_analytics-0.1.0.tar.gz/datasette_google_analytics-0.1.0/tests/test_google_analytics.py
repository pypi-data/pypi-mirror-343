from datasette.app import Datasette
import pytest
from bs4 import BeautifulSoup as Soup


@pytest.mark.asyncio
async def test_plugin_is_installed():
    datasette = Datasette(
        memory=True,
        metadata={
            "plugins": {"datasette-google-analytics": {"tracking_id": "G-TESTID123"}}
        },
    )
    response = await datasette.client.get("/-/plugins")
    assert response.status_code == 200
    html = response.text
    assert "datasette-google-analytics" in html


@pytest.mark.asyncio
async def test_ga_script_added_when_tracking_id_provided():
    datasette = Datasette(
        memory=True,
        metadata={
            "plugins": {"datasette-google-analytics": {"tracking_id": "G-TESTID123"}}
        },
    )
    response = await datasette.client.get("/")
    assert response.status_code == 200

    # Parse the HTML
    soup = Soup(response.text, "html.parser")

    # Check for GA script tag in head
    scripts = soup.head.find_all("script")
    ga_script = None
    for script in scripts:
        if script.get("src") and "googletagmanager.com/gtag/js" in script["src"]:
            ga_script = script
            break

    assert ga_script is not None, "Google Analytics script tag not found in head"
    assert "G-TESTID123" in ga_script["src"], "Tracking ID not in script src"
    assert ga_script.get("async") is not None, "Script should have async attribute"

    # Check for GA initialization code
    init_script = None
    for script in scripts:
        if script.string and "gtag(" in script.string:
            init_script = script
            break

    assert init_script is not None, "GA initialization script not found"
    assert "G-TESTID123" in init_script.string, "Tracking ID not in initialization code"
    assert "gtag('config'" in init_script.string, (
        "Config call not found in initialization"
    )


@pytest.mark.asyncio
async def test_ga_script_not_added_when_tracking_id_missing():
    datasette = Datasette(
        memory=True,
        metadata={
            "plugins": {
                "datasette-google-analytics": {}  # No tracking_id
            }
        },
    )
    response = await datasette.client.get("/")
    assert response.status_code == 200

    # Parse the HTML
    soup = Soup(response.text, "html.parser")

    # Check that GA script is not present
    scripts = soup.head.find_all("script")
    for script in scripts:
        if script.get("src"):
            assert "googletagmanager.com/gtag/js" not in script["src"], (
                "GA script should not be present"
            )
        if script.string:
            assert "gtag(" not in script.string, (
                "GA initialization should not be present"
            )


@pytest.mark.asyncio
async def test_ga_script_not_added_when_plugin_not_configured():
    datasette = Datasette(memory=True)  # No plugin config
    response = await datasette.client.get("/")
    assert response.status_code == 200

    # Parse the HTML
    soup = Soup(response.text, "html.parser")

    # Check that GA script is not present
    scripts = soup.head.find_all("script")
    for script in scripts:
        if script.get("src"):
            assert "googletagmanager.com/gtag/js" not in script["src"], (
                "GA script should not be present"
            )
        if script.string:
            assert "gtag(" not in script.string, (
                "GA initialization should not be present"
            )
