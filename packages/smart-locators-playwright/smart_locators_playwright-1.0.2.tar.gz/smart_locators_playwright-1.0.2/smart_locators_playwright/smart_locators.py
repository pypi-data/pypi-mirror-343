from playwright.sync_api._generated import Locator
from smart_locators_playwright import custom_exceptions
from playwright.sync_api._generated import Page as sync_page
from playwright.async_api._generated import Page as async_page


class SmartLocators:
    def __init__(self, page:sync_page or async_page):
        """Initializes an instance of the Smart Locators class.

        Args:
            page (playwright.sync_api.Page or playwright.async_api.Page): The Playwright "page" instance used to interact with the browser."""

        self._page=page
        self._playwright_allowed_locators=["alt","label","placeholder","role","text","title"]
        self._custom_locators=["css","xpath"]
    
       
    def find(self,id:str=None, name:str=None, css:str=None, xpath:str=None, label:str=None, alt:str=None, placeholder:str=None, role:str=None, text:str=None, title:str=None,first_match:bool=True,**kwargs)->Locator:
        """Finds the web element using provided locators. Tries locators in order until one succeeds.

        Args:
            id (str, optional): ID attribute. Defaults to None.
            name (str, optional): Name attribute. Defaults to None.
            css (str, optional): CSS selector. Defaults to None.
            xpath (str, optional): XPATH selector. Defaults to None.
            label (str, optional): Label attribute. Defaults to None.
            alt (str, optional): Alt attribute. Defaults to None.
            placeholder (str, optional): Placeholder attribute. Defaults to None.
            role (str, optional): Role attribute. Defaults to None.
            text (str, optional): Text content. Defaults to None.
            title (str, optional): Title attribute. Defaults to None.
            first_match (bool, optional): Returns first matching elements if True else returns all matching elements. Defaults to True
            **kwargs: Additional attributes and values if needed.
            
        Returns:
            Locator: The found web element. 
            List of locators if multiple elements are found and first_match is set to False
        
        Raises:
            NoSuchElementException: If no element is found for any of the given locators.
        """
        _locator_strategies_default={"id":id,"name":name,"css":css,"xpath":xpath,"label":label,"alt":alt,"placeholder":placeholder,"role":role,"text":text,"title":title}
        _locator_strategies={**_locator_strategies_default,**kwargs}
        _non_empty_locators={key:value for key,value in _locator_strategies.items() if value not in (None,"")}
        # self.__find_element_internal(_non_empty_locators)
        self.__reformat_locator(_non_empty_locators)
        _playwright_method_mappings={key:f'_get_by_{key}' for key,value in _non_empty_locators.items() if key.lower() in self._playwright_allowed_locators}
        # self.__find_element_internal(locators=_non_empty_locators,mappings=_playwright_method_mappings)
        _custom_method_mappings={key:f'_get_by_locator' for key,value in _non_empty_locators.items() if key.lower() not in self._playwright_allowed_locators}
        
        _locator_mappings={**_playwright_method_mappings,**_custom_method_mappings}
        ele=self.__find_element_internal(locators=_non_empty_locators,mappings=_locator_mappings)
        if ele:
            return ele.nth(0) if first_match else ele
        else:
            raise custom_exceptions.NoSuchElementException
        
    def __find_element_internal(self,locators:dict,mappings:dict,keys:list=None,index:int=0)->Locator:
        """
        Recursively attempts to find an element using a series of locators and their corresponding mapping methods.
        Args:
            locators (dict): A dictionary containing locator types as keys and their corresponding values.
            mappings (dict): A dictionary mapping locator types to method names that handle those locators.
            keys (list, optional): A list of locator key-value pairs. Defaults to None, in which case it is initialized from `locators`.
            index (int, optional): The current index in the `keys` list to process. Defaults to 0.
        Returns:
            Locator: The located element if found, otherwise False.
        """
        # If the method is called first time, initialize 'keys' as a list of key-value pairs (in tuple format) from locators
        if keys is None:
            keys=list(locators.items())
        
        # Base case: If index exceeds the length of keys, return False (element not found)
        if index>=len(keys):
            return False
        
        # Get the current locator type and value from the keys list (unpacking tuple with index)
        locator_type,value=keys[index]
        
        # Retrieve the method name from the mappings dictionary for the current locator type
        method=mappings.get(locator_type)
        
        # Dynamically call the method using getattr and pass the locator value as an argument
        result=getattr(self,method)(value)
        
        # If the result is valid (element found), return it
        # Otherwise, recursively call the function with the next index
        return result if result else self.__find_element_internal(locators,mappings,keys,index+1)   

    def __reformat_locator(self,locators:dict)->None:
        """Generate an XPath for attributes that do not have a native Playwright method. Otherwise, leave the locator unchanged.

        Args:
            locators (dict): A dictionary containing all locators.
        """
        for key,value in locators.items():
            if key.lower() not in self._playwright_allowed_locators and key.lower() not in self._custom_locators:
                locators[key]=(f"//*[@{key}='{value}']")
                
    def _get_by_role(self,locator):
        try:
            ele=self._page.get_by_role(locator)
            return ele if ele.count()>0 else False
        except Exception as e:
            return False
    
    def _get_by_role(self,locator):
        try:
            ele=self._page.get_by_role(locator)
            return ele if ele.count()>0 else False
        except Exception as e:
            return False
        
    def _get_by_alt(self,locator):
        try:
            ele=self._page.get_by_alt_text(locator)
            return ele if ele.count()>0 else False
        except Exception as e:
            return False
    
    def _get_by_label(self,locator):
        try:
            ele=self._page.get_by_label(locator)
            return ele if ele.count()>0 else False
        except Exception as e:
            return False
    
    def _get_by_placeholder(self,locator):
        try:
            ele=self._page.get_by_placeholder(locator)
            return ele if ele.count()>0 else False
        except Exception as e:
            return False
    
    def _get_by_text(self,locator):
        try:
            ele=self._page.get_by_text(locator)
            return ele if ele.count()>0 else False
        except Exception as e:
            return False
        
    def _get_by_title(self,locator):
        try:
            ele=self._page.get_by_title(locator)
            return ele if ele.count()>0 else False
        except Exception as e:
            return False
        
    def _get_by_locator(self,locator):
        try:
            ele=self._page.locator(locator)
            return ele if ele.count()>0 else False
        except Exception as e:
            return False