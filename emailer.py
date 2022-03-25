class Emailer:

    sender_address = ""  # class variable
    _sole_instance = None  # class variable

    @classmethod
    def configure(cls, sender_address):
        cls.sender_address = sender_address

    @classmethod
    def instance(cls):
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    def send_plain_email(self, recipients, subject, message):  # has to be an instance method. don't think I need to do
        # anything with the subject and message bits yet. probably next project.
        for recipient in recipients:
            print(f"Sending mail to {recipient}")
            # print(f"Sending mail to {recipient} about {subject} saying {message}")


if __name__ == '__main__':
    e = Emailer.instance()
    e.configure("LaurelWalkerDavis@gmail.com")
    _recipients = ("lwd@gmail.com", "mbeth@hotmail.com", "sdavis@yahoo.com")
    e.send_plain_email(_recipients, "Tournament", "This is a reminder about the tournament coming up this weekend!")

