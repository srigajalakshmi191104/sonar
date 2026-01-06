import logging
from typing import Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Calculator:
    """
    Simple calculator class.
    This code follows secure and clean coding practices.
    """

    def divide(self, a: float, b: float) -> Optional[float]:
        """
        Safely divide two numbers.
        Returns None if division is not possible.
        """
        if b == 0:
            logger.warning("Division by zero attempted")
            return None
        return a / b


def get_user_greeting(username: str) -> str:
    """
    Returns a greeting message for the user.
    """
    if not username:
        return "Hello, User!"
    return f"Hello, {username}!"


def main():
    calc = Calculator()

    result = calc.divide(10, 2)
    if result is not None:
        logger.info("Division result: %s", result)

    greeting = get_user_greeting("Srigajalakshmi")
    logger.info(greeting)


if __name__ == "__main__":
    main()
