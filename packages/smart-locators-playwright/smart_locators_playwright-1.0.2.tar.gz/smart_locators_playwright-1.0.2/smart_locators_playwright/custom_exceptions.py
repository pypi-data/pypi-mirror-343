
class NoSuchElementException(Exception):
    def __str__(self):
        return "The element could not be located using the provided locator/locators. Please verify the locator or the element's presence on the page."