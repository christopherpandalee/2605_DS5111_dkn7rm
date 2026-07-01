"""
This module only checks for valid Youtube IDs. See function docstring for valid ID parameters.
"""

import sys
import logging

def main():
    """This function checks whether or not a string is a valid Youtube ID
    - Valid ID parameters:
        - Exactly 11 characters
        - Allowed characters are upper and lowercase characters, dash (-), and underscore(_)
    - Logs invalid strings in log file
    """
    try:
        for line in sys.stdin:
            allowed_in_yt_id = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-'
            line = line.strip()

            if len(line) == 11 and all(c in allowed_in_yt_id for c in line):
                print(line)
            else:
                logging.basicConfig(
                filename='pipeline_audit.log',
                level=logging.ERROR,
                format='%(asctime)s %(message)s'
                )

                logging.error("Invalid ID: %s", line)

    except KeyboardInterrupt:
        sys.exit(0)

if __name__=="__main__":
    main()
