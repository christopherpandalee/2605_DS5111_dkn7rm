import sys
import logging


try: 
    for line in sys.stdin:
        allowed = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-'
        line = line.strip()

        if len(line) == 11 and all(c in allowed for c in line):
            print(line)
        else:
            logging.basicConfig(
            filename='pipeline_audit.log',
            level=logging.ERROR,
            format='%(asctime)s %(message)s'
            )

            logging.error(f"Invalid ID: {line}")

except KeyboardInterrupt:
    sys.exit(0)
