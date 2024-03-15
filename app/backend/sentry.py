import sentry_sdk


def report_exception(**kwargs):
    return sentry_sdk.capture_exception()
