"""Input helpers: each one keeps asking until it gets a valid value,
so the program never continues with incomplete data."""


def get_positive_float(prompt: str) -> float:
    """For prices: must be a number greater than zero."""
    while True:
        try:
            value = float(input(prompt))          # can raise ValueError
            if value <= 0:                        # validation
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_non_negative_float(prompt: str) -> float:
    """For weight and download size: zero is allowed, negative is not."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a number that is zero or more.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 1.5")


def get_non_negative_int(prompt: str) -> int:
    """For stock and deliveries: a whole number that is zero or more."""
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter a whole number that is zero or more.")
                continue
            return value
        except ValueError:
            print("Please enter a whole number, e.g. 10")


def get_positive_int(prompt: str) -> int:
    """For order quantities: a whole number greater than zero."""
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a whole number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a whole number, e.g. 2")


def get_non_empty_text(prompt: str) -> str:
    """For IDs and names: cannot be left empty."""
    while True:
        text = input(prompt).strip()
        if text == "":
            print("This cannot be empty. Please try again.")
            continue
        return text


def get_choice(prompt: str, choices: tuple[str, ...]) -> str:
    """Keeps asking until the answer is one of the allowed choices."""
    while True:
        answer = input(prompt).strip()
        if answer in choices:
            return answer
        print(f"Please enter one of: {', '.join(choices)}")
