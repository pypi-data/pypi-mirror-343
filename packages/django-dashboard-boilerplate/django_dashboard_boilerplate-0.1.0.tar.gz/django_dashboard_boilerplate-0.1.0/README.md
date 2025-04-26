# Django Dashboard Boilerplate

A reusable dashboard boilerplate for Django applications with a modern UI, responsive design, and dark mode support.

## Features

- Modern, responsive UI built with TailwindCSS
- Dark mode support
- Sidebar navigation
- Ready-to-use components
- Easy to customize and extend

## Installation

```bash
pip install django-dashboard-boilerplate
```

## Quick Start

1. Add "dashboard" to your INSTALLED_APPS in settings.py:

```python
INSTALLED_APPS = [
    ...
    'dashboard',
]
```

2. Include the dashboard URLconf in your project urls.py:

```python
urlpatterns = [
    ...
    path('', include('dashboard.urls')),
]
```

3. Configure static and template settings in your settings.py:

```python
import os

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

4. Run migrations and start the development server:

```bash
python manage.py migrate
python manage.py runserver
```

## Customization

### Changing the Theme Colors

The dashboard uses TailwindCSS for styling. You can customize the primary color in your base template:

```html
<script>
    tailwind.config = {
        darkMode: 'class',
        theme: {
            extend: {
                colors: {
                    primary: {
                        // Change these values to your preferred color
                        50: '#f0f9ff',
                        100: '#e0f2fe',
                        200: '#bae6fd',
                        300: '#7dd3fc',
                        400: '#38bdf8',
                        500: '#0ea5e9',
                        600: '#0284c7',
                        700: '#0369a1',
                        800: '#075985',
                        900: '#0c4a6e',
                        950: '#082f49',
                    }
                }
            }
        }
    }
</script>
```

### Adding New Pages

1. Create a new view in your app's views.py
2. Add the URL pattern in your app's urls.py
3. Create a template that extends the base template

Example:

```python
# views.py
def my_new_page(request):
    return render(request, 'my_new_page.html')

# urls.py
urlpatterns = [
    ...
    path('my-new-page/', my_new_page, name='my_new_page'),
]
```

```html
<!-- my_new_page.html -->
{% extends 'dashboard/base.html' %}

{% block title %}My New Page{% endblock %}

{% block content %}
<div class="container mx-auto">
    <h1 class="text-2xl font-bold text-gray-800 dark:text-white">My New Page</h1>
    <!-- Your content here -->
</div>
{% endblock %}
```

### Customizing the Sidebar

To customize the sidebar, create a template override in your project:

1. Create a file at `templates/dashboard/components/sidebar.html` in your project
2. Copy the content from the original sidebar template and modify as needed

## Development

### Setup Development Environment

1. Clone the repository:

```bash
git clone https://github.com/yourusername/django-dashboard-boilerplate.git
cd django-dashboard-boilerplate
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:

```bash
pip install -e ".[dev]"
```

4. Run tests:

```bash
pytest
```

## Example Project

Check out the `example` directory for a complete example of how to use this package in a Django project.

## License

MIT License
