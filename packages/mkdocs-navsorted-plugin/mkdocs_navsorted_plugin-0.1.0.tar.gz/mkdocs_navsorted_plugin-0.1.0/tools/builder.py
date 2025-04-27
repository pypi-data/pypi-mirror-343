from mkdocs.commands import build
from mkdocs import config


cfg = config.load_config()
cfg.plugins.on_startup(command='build', dirty=False)

try:
    build.build(cfg)

finally:
    cfg.plugins.on_shutdown()
