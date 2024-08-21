from datetime import date, timedelta


class DateIterator:
    """
    Gets the current date and iterates through the future dates
    """

    def __init__(self):
        self.index = 0
        self.current_date = date.today()

    def next(self):
        future_date = self.current_date + timedelta(days=self.index + 1)
        self.index = self.index + 1
        output = self.current_date.strftime("%b %d, %Y")
        self.current_date = future_date
        return output
