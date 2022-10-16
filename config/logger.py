import sys
from config.config import parse_args
args = parse_args()


log_config = {
            "handlers": [
                {
                    "sink": sys.stdout,
                    # "format": "<green>{time:YYYY-MM-DDTHH:mm:ss.SSSZ}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                    "diagnose": False,
                    "level": args.log
                },
            ]
        }
