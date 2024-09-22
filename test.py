import psycopg2
import sys
from database.config import load_config
import database.queries as sql

import logging

NONE_FIELD = None

logger = logging.getLogger(__name__)

logging.basicConfig(
    filename="database/utils.log",
    encoding="utf-8",
    level=logging.DEBUG,
)


config = load_config("/database")

username = "giuxmirtiu"
try:
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql.Q_COUNT_USER_VARIANT,
                        (
                            username,
                        ),
            )

            tot = cur.fetchone()

            print(tot[0])
                        
            # commit the changes to the database
            conn.commit()
except (Exception, psycopg2.DatabaseError) as error:
    logger.debug(error)

