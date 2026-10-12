import argparse
import logging
import sys

from app.db.session import SessionLocal
from app.dependencies.container import build_updater_service

logger = logging.getLogger("app.cli")


def update_rates() -> int:
    try:
        with SessionLocal() as session:
            count = build_updater_service(session).update_rates()

    except Exception:
        logger.exception("Не удалось обновить курсы")
        return 1

    logger.info("Обновлено курсов: %d", count)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="python -m app.cli")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("update-rates", help="Загрузить курсы НБУ в базу данных")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    if args.command == "update-rates":
        return update_rates()
    return 2


if __name__ == "__main__":
    sys.exit(main())
