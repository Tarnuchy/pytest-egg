WHOLE_EGG_ASCII = r"""
   ___
  /   \
 /     \
|       |
 \     /
  \___/
"""

BROKEN_EGG_ASCII = r"""
   ___
  /   \
 /_/\_\
 \ \/ /
 / /\ \
 \_\/_/
"""


def pytest_sessionfinish(session, exitstatus):
    """Attach exit status to config so it can be used in pytest_unconfigure."""
    setattr(session.config, "exitstatus", exitstatus)


def pytest_unconfigure(config):
    """Show egg art if enabled."""
    if not config.option.egg:
        return

    if not hasattr(config, "exitstatus"):
        return

    tw = config.get_terminal_writer()
    if getattr(config, "exitstatus") == 0:
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
