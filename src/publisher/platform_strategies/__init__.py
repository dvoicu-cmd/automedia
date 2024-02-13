"""
package __init__: publisher.platform_strategies
"""

# Export strategies
from .yt_upload import YtUpload
from .local_publish import LocalPublish

__all__ = ['YtUpload', 'LocalPublish']
