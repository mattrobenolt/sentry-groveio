# sentry-groveio
A plugin for [Sentry](https://www.getsentry.com/) that logs errors to an IRC room on [Grove.io](https://grove.io)

## Installation
`$ pip install sentry-groveio`

Add `sentry_groveio` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    #...
    'sentry',
    'sentry_groveio',
)
```
