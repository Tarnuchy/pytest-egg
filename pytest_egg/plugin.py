from pytest_egg.arts import BROKEN_EGG_ASCII, WHOLE_EGG_ASCII

EXITSTATUS_ATTR = "_pytest_egg_exitstatus"


def pytest_sessionfinish(session, exitstatus):
    """Attach exit status to config so it can be used in pytest_unconfigure."""
    setattr(session.config, EXITSTATUS_ATTR, exitstatus)


def pytest_unconfigure(config):
    """Show egg art if enabled."""
    if not config.option.egg:
        return

    if not hasattr(config, EXITSTATUS_ATTR):
        return

    tw = config.get_terminal_writer()
    if getattr(config, EXITSTATUS_ATTR) == 0:
        tw.write(WHOLE_EGG_ASCII, green=True)
    else:
        tw.write(BROKEN_EGG_ASCII, red=True)


def pytest_addoption(parser):
    """Add a CLI flag to enable egg output."""
    group = parser.getgroup("egg")
    group.addoption(
        "--egg",
        action="store_true",
        default=False,
        help="Show egg ASCII art when tests complete.",
    )
