# 🔍 smart-locators-playwright

**A smart, resilient way to locate elements in Playwright for Python — reduce flakiness, simplify locators, and write cleaner test code.**

[![PyPI version](https://badge.fury.io/py/smart-locators-playwright.svg)](https://pypi.org/project/smart-locators-playwright/)

## 🚀 What is it?

`smart-locators-playwright` is a utility wrapper around Playwright’s native locator system. It allows you to define **multiple locator strategies at once**, and it will **automatically try each until one succeeds** — no more writing fallback logic or suffering flaky tests due to minor DOM changes.

## Why Smart Locators?
Element location is often the most brittle part of web automation. Smart Locators provides:

- A unified API for all types of locators
- Automatic fallback between multiple location strategies
- Support for custom attributes alongside Playwright's built-in locators
- Reduced test maintenance when UI changes occur
## Installation

Install smart-locators-playwright with pip

```bash
  pip install smart-locators-playwright
```
    

## ✅ Key Features

### 1. 🔗 Unified Element Location API

Use a single, intuitive `find()` method instead of chaining multiple Playwright locators like `page.get_by_role()`, `page.get_by_text()`, etc.

```python
element = smart.find(id="submit", text="Submit", role="button")
```

---

### 2. 🧩 Multiple Location Strategies

The `find()` method supports all standard Playwright locators, plus custom strategies:

#### ✅ Built-in Playwright Strategies:
- `id`: Element ID attribute
- `text`: Text content
- `role`: ARIA role
- `label`: Associated label text
- `placeholder`: Placeholder text
- `alt`: Alt text (for images)
- `title`: Title attribute

#### 🛠️ Additional Custom Strategies:
- `name`: Name attribute
- `css`: CSS selector
- `xpath`: XPath expression
- `any other attribute`: Will be auto-converted to XPath

---

### 3. 🔄 Automatic Fallback

If a locator fails, the utility tries the next one in the order provided — making your tests resilient to minor UI changes.

```python
element = smart.find(id="loginBtn", name="submitLogin", text="Login")
```

---

### 4. 👥 Support for Multiple Elements

Need to fetch all matching elements instead of just the first? Simply set `first_match=False`.

```python
# Get all matching buttons
all_buttons = smart.find(
    role="button",
    first_match=False
)

# Iterate through all buttons
for button in all_buttons:
    print(button.text_content())
```

---



## Usage/Examples

```python
## Finding single element

from playwright.sync_api import sync_playwright
from smart_locators_playwright import SmartLocators

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")

    smart = SmartLocators(page)

    # Try locating using multiple strategies
    element = smart.find(
        id="submit-btn",
        name="submit",
        text="Submit",
        role="button",
        first_match=True  # Stop at the first successful match
    )

    element.click()
    browser.close()

```


```python
## Finding multiple element

# Return all matching elements instead of just the first
buttons = smart.find(
    role="button",
    first_match=False
)

# Iterate through elements
for button in buttons:
    print(button.text_content())
```

```python
## Custom Attributes

# Find by data attributes or any custom attribute
element = smart.find(
    data_testid="submit-button",  # Converted to XPath
    data_cy="login"               # Converted to XPath
)
```

```python
## Combining with Playwright's Chain API
## The returned object is a standard Playwright Locator that can be further refined:

# Find a button inside a specific container
button = smart.find(role="button", text="Submit").filter(has_text="Submit")
```

```python
# Find all rows in a table
rows = smart.find(
    css="table#users tr",
    first_match=False
)

# Process each row
for row in rows.all():
    username = row.locator("td").nth(0).text_content()
    email = row.locator("td").nth(1).text_content()
    print(f"User: {username}, Email: {email}")
```
## Supported Locators

| Locator Type | Description                                                    |
|--------------|----------------------------------------------------------------|
| `id`         | Locate by `id` attribute.                                    |
| `name`       | Locate by `name` attribute.                                  |
| `css`        | Locate by a CSS selector.                                    |
| `xpath`      | Locate by an XPath expression.                               |
| `label`      | Locate by the associated `label` attribute.                  |
| `alt`        | Locate by `alt` attribute (for images and other media).       |
| `placeholder`| Locate by `placeholder` attribute (for form inputs).         |
| `role`       | Locate by `role` attribute (ARIA roles, such as "button", "textbox", etc.). |
| `text`       | Locate by text content (useful for buttons, links, etc.).    |
| `title`      | Locate by `title` attribute (often used for tooltips, hover text, etc.). |


## 📚 API Reference

#### `SmartLocators(page)`

Initializes the Smart Locators class.

### Parameters:
- `page` (playwright.sync_api.Page or playwright.async_api.Page): The Playwright page instance.

---

## `find(id=None, name=None, css=None, xpath=None, label=None, alt=None, placeholder=None, role=None, text=None, title=None, first_match=True, **kwargs)`

Finds web elements using provided locators, trying them in order until one succeeds.

### Parameters:
- **Standard locator parameters** (id, text, etc.)
- `first_match` (bool): Return only the first match if `True`, all matches if `False`.
- `**kwargs` (dict): Any additional attributes to locate by.

### Returns:
- **Locator**: The found element(s).

### Raises:
- **NoSuchElementException**: If no element is found.
