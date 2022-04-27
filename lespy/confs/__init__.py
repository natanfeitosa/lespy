
from lespy.confs.classes import ConfigsManager, MiddlewaresManager

__all__ = (
    'MIDDLEWARES',
    'CONFIGS'
)

MIDDLEWARES: MiddlewaresManager = MiddlewaresManager(request=[], response=[])

CONFIGS: ConfigsManager = ConfigsManager(
    DEBUG=True,
    ALLOWED_HOSTS=[],
    CHARSET='utf-8',
    SECURE_SSL_HEADER=('HTTP_X_FORWARDED_PROTO', 'https')
)
