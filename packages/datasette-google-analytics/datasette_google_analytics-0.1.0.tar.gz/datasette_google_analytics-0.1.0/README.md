# datasette-google-analytics

A [Datasette](https://datasette.io/) plugin that adds Google Analytics tracking code to your Datasette instance.

## Installation

Install this plugin in the same environment as Datasette:

```sh
pip install datasette-google-analytics
```

## Usage

Configure the plugin by adding a `metadata.json` file with your Google Analytics tracking ID:

```json
{
    "plugins": {
        "datasette-google-analytics": {
            "tracking_id": "G-XXXXXXXXXX"
        }
    }
}
```

Replace `G-XXXXXXXXXX` with your actual Google Analytics 4 tracking ID.

Then start Datasette with:

```sh
datasette --metadata metadata.json your-database.db
```

## Development

To set up this plugin locally:

```sh
cd datasette-google-analytics
python -m venv venv
source venv/bin/activate
pip install -e '.[test]'
```

## How This Works

1. The plugin creates a custom template that extends the default base template
2. It uses the `extra_template_vars` hook to pass the Google Analytics tracking ID to the template
3. It uses the `prepare_jinja2_environment` hook to modify the Jinjia2 environment by adding our template directories
4. The custom template adds the Google Analytics tracking code in the `extra_head` block

This approach follows Google's recommendations for placing the tracking code immediately after the `<head>` element.
