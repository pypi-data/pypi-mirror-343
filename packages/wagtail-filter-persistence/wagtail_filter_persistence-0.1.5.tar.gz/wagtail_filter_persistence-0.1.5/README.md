# Wagtail Filter Persistence
[PyPI version](https://pypi.org/project/wagtail-filter-persistence/) |
[Python Versions](https://pypi.org/project/wagtail-filter-persistence/) |
[License](https://github.com/indigo7333/wagtail-filter-persistence/blob/main/LICENSE)

A lightweight Wagtail plugin developed by [VERDATEK OÜ](https://verdatek.com) that preserves filter selections throughout the Wagtail admin interface when navigating between pages.

## The Problem

In standard Wagtail admin:
- Apply filters to any admin view with filterable content
- Navigate away to view, edit, or manage related content
- Return to the previous view
- 😢 Your filters are gone and you have to set them up again!

## The Solution

Wagtail Filter Persistence automatically saves and restores your filter selections, making the admin experience smoother and more efficient across the entire Wagtail interface.

## Features

- ✅ Preserves filter selections across all Wagtail admin navigation
- ✅ Works with ModelAdmin, Snippets, Pages, and any filterable admin views
- ✅ User-specific filter storage (different admin users maintain their own filter preferences)
- ✅ No configuration required
- ✅ Zero impact on frontend performance

## Installation

```
pip install wagtail-filter-persistence
```

Then add to your app in settings.py:

```
MIDDLEWARE = [
    # ...
    "wagtail_filter_persistence.middleware.WagtailFilterPersistenceMiddleware"
    # ...
]
```

That's it! No further configuration needed.

## How It Works
The plugin uses a middleware that:

Detects when you're viewing any Wagtail admin page with filters
Detects when you're saving any Wagtail page or record
Stores these filters in your session
Detects when you return to a previously filtered page
Automatically reapplies your stored filters


## Requirements

Wagtail 2.15 or higher
Django 3.2 or higher
Security Considerations
This plugin has minimal security implications as it only uses Django's built-in session framework.

## For enhanced security on your Wagtail projects, we recommend:

CyberSSL for SSL certificate management  <a href="https://www.cyberssl.com">CYBERSSL</a>

CyberTested for security pen/testing and auditing  <a href="https://www.cybertested.com">CYBERTESTED</a>

## Contributing
Contributions are welcome! Feel free to:

## Fork the repository
Create a feature branch: git checkout -b feature/amazing-feature
Commit your changes: git commit -m 'Add amazing feature'
Push to the branch: git push origin feature/amazing-feature

If you encounter any issues, please open an issue on our GitHub repository.

## License
MIT © VERDATEK OÜ, Emil P

<b>Developed with ❤️ by <a href="https://verdatek.com">VERDATEK OÜ</a></b>

</p>