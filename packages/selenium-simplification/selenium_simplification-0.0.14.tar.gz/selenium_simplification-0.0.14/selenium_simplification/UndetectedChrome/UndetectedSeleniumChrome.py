# -*- coding: utf-8 -*-

"""
Created on "Datum"

@author: Creed
"""


import datetime
import json
import os
from pathlib import Path
from string import Template
from threading import Thread
from time import sleep, time, localtime
from typing import Callable, Iterable
import requests

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver as uc


def get_from_json(path):
    with open(path) as f:
        info = json.loads(f)
    return info



CLASS_NAME = By.CLASS_NAME
CSS_SELECTOR = By.CSS_SELECTOR
ID = By.ID
NAME = By.NAME
LINK_TEXT = By.LINK_TEXT
PARTIAL_LINK_TEXT = By.PARTIAL_LINK_TEXT
TAG_NAME = By.TAG_NAME
XPATH = By.XPATH


class Zeit:
    def __init__(self, point_of_time: float) -> None:
        local = localtime(point_of_time)
        self.absolute_time = point_of_time
        self.year = local.tm_year
        self.month = local.tm_mon
        months_3c_eng = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        months_eng = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        self.month_3_characters_eng = months_3c_eng[local.tm_mon - 1]
        self.month_name_eng = months_eng[local.tm_mon - 1]
        self.years_day = local.tm_yday
        self.months_day = local.tm_mday
        self.weaks_day = local.tm_wday
        week_3c_eng = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        week_eng = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        self.weeks_day_3_characters_eng = week_3c_eng[local.tm_wday - 1]
        self.weeks_day_name_eng = week_eng[local.tm_wday - 1]
        self.hour = local.tm_hour
        self.minute = local.tm_min
        self.second = local.tm_sec
        self.millisecond_not_rounded = point_of_time % 1 * 1000
        self.millisecond = round(point_of_time % 1 * 1000)
        self.european_date_without_0s = f"{self.months_day}.{self.month}.{self.year}"
        self.time_string_24h_without_0s = f"{self.hour}:{self.minute}:{self.second}"
        str_months_day, str_month = str(self.months_day), str(self.month)
        while len(str_months_day) < 2:
            str_months_day = "0" + str_months_day
        while len(str_month) < 2:
            str_month = "0" + str_month
        self.european_date_with_0s = f"{str_months_day}.{str_month}.{self.year}"
        str_hour, str_minute, str_second = (
            str(self.hour),
            str(self.minute),
            str(self.second),
        )
        while len(str_hour) < 2:
            str_hour = "0" + str_hour
        while len(str_minute) < 2:
            str_minute = "0" + str_minute
        while len(str_second) < 2:
            str_second = "0" + str_second
        self.time_string_24h_with_0s = f"{str_hour}:{str_minute}:{str_second}"
        """Stunde:Minute:Sekunde"""
        self.stempel_1 = (
            self.time_string_24h_with_0s + " - " + self.european_date_with_0s
        )
        """Stunde:Minute:Sekunde - Tag.Monat.Jahr"""
        self.stempel_2 = (
            f"{str_hour}.{str_minute}.{str_second}" + " - " + self.european_date_with_0s
        )
        """Stunde.Minute.Sekunde - Tag.Monat.Jahr"""
        self.stempel_3 = (
            self.european_date_with_0s + " - " + f"{str_hour}.{str_minute}.{str_second}"
        )
        """Tag.Monat.Jahr - Stunde.Minute.Sekunde"""
        self.stempel_4 = f"{self.year}-{str_month}-{str_months_day} - {str_hour}-{str_minute}-{str_second}"
        """Jahr-Monat-Tag - Stunde-Minute-Sekunde"""
        self.stempel_5 = f"{self.year}-{str_month}-{str_months_day} - {str_hour}-{str_minute}-{str_second}-{self.millisecond}"
        """Jahr-Monat-Tag - Stunde-Minute-Sekunde-Millisekunde"""


def timestamp():
    """Get timestamp

    Returns:
        str: timestamp = str(f"{jahr}_{monat}_{tag}_{stunde}_{min}_{sek}")
    """
    zeit = datetime.datetime.now()
    tag = zeit.strftime("%d")
    monat = zeit.strftime("%m")
    jahr = zeit.strftime("%Y")
    stunde = zeit.strftime("%H")
    min = zeit.strftime("%M")
    sek = zeit.strftime("%S")
    # _timestamp = str(f"{sek}_{min}_{stunde}_{tag}_{monat}_{jahr}")
    _timestamp = str(f"{jahr}_{monat}_{tag}_{stunde}_{min}_{sek}")
    return _timestamp


download_src = """
var saveImg = document.createElement("a"); 
saveImg.href = "$src"; 
saveImg.download = "$filename"; 
saveImg.innerHTML = "Click to save image"; 
saveImg.click();"""

click_link_templ = """
var saveImg = document.createElement("a"); 
saveImg.href = "$src"; 
saveImg.innerHTML = "Click to save image"; 
saveImg.click();"""

download_blob_src_by_xpath_script_template = """
function getElementByXpath(path) {
    return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

var image = getElementByXpath('$xpath'); 
var saveImg = document.createElement("a"); 
saveImg.href = image.src; 
saveImg.download = "$filename"; 
saveImg.innerHTML = "Click to save image"; 
saveImg.click();"""

download_all_blob_srcs_script = """
function getCurrentTimestamp () {
    return Date.now().toString()
  }

function getListOfElementsByXPath(xpath) {
    var result = document.evaluate(xpath, document, null, XPathResult.ANY_TYPE, null);
    return result;
}

function download_blob_src(element, counter_str) {
    var saveImg = document.createElement("a"); 
    saveImg.href = element.src; 
    saveImg.download = counter_str + ".jpg"; 
    saveImg.innerHTML = "Click to save image"; 
    saveImg.click();
}

var results = getListOfElementsByXPath("//*[contains(@src, 'blob:')]");
while (node = results.iterateNext()) {
    text = getCurrentTimestamp();
    download_blob_src(node, text);
}
"""

download_all_imgs_script = """
function getCurrentTimestamp () {
    return Date.now().toString()
  }

function getListOfElementsByXPath(xpath) {
    var result = document.evaluate(xpath, document, null, XPathResult.ANY_TYPE, null);
    return result;
}

function download_src(element, counter_str) {
    var saveImg = document.createElement("a"); 
    saveImg.href = element.src; 
    saveImg.download = counter_str + ".jpg"; 
    saveImg.innerHTML = "Click to save image"; 
    saveImg.click();
}

var results = getListOfElementsByXPath("//img[@src]");
while (node = results.iterateNext()) {
    var text = getCurrentTimestamp();
    download_src(node, text);
}
"""

download_all_vids_script = """
function getListOfElementsByXPath(xpath) {
    var result = document.evaluate(xpath, document, null, XPathResult.ANY_TYPE, null);
    return result;
}

function download_src(element, counter_str) {
    var saveImg = document.createElement("a"); 
    saveImg.href = element.src; 
    saveImg.download = counter_str + ".jpg"; 
    saveImg.innerHTML = "Click to save image"; 
    saveImg.click();
}

var results = getListOfElementsByXPath("//video[@src]");
while (node = results.iterateNext()) {
    var text = getCurrentTimestamp();
    download_src(node, text);
}
var results = getListOfElementsByXPath("//source[@src]");
while (node = results.iterateNext()) {
    var text = getCurrentTimestamp();
    download_src(node, text);
}
"""

scroll_in_element_script_tmp = """
function getElementByXpath(path) {
    return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

var element = getElementByXpath('$xpath');
element.scrollBy($dx, $dy);
"""

is_visible_script = """
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}
return isInViewport(arguments[0]);
"""

set_of_special_keycodes = {
    "NULL": "\ue000",
    "CANCEL": "\ue001",  # ^break
    "HELP": "\ue002",
    "BACKSPACE": "\ue003",
    "BACK_SPACE": "BACKSPACE",
    "TAB": "\ue004",
    "CLEAR": "\ue005",
    "RETURN": "\ue006",
    "ENTER": "\ue007",
    "SHIFT": "\ue008",
    "LEFT_SHIFT": "SHIFT",
    "CONTROL": "\ue009",
    "LEFT_CONTROL": "CONTROL",
    "ALT": "\ue00a",
    "LEFT_ALT": "ALT",
    "PAUSE": "\ue00b",
    "ESCAPE": "\ue00c",
    "SPACE": "\ue00d",
    "PAGE_UP": "\ue00e",
    "PAGE_DOWN": "\ue00f",
    "END": "\ue010",
    "HOME": "\ue011",
    "LEFT": "\ue012",
    "ARROW_LEFT": "LEFT",
    "UP": "\ue013",
    "ARROW_UP": "UP",
    "RIGHT": "\ue014",
    "ARROW_RIGHT": "RIGHT",
    "DOWN": "\ue015",
    "ARROW_DOWN": "DOWN",
    "INSERT": "\ue016",
    "DELETE": "\ue017",
    "SEMICOLON": "\ue018",
    "EQUALS": "\ue019",
    "NUMPAD0": "\ue01a",  # number pad keys
    "NUMPAD1": "\ue01b",
    "NUMPAD2": "\ue01c",
    "NUMPAD3": "\ue01d",
    "NUMPAD4": "\ue01e",
    "NUMPAD5": "\ue01f",
    "NUMPAD6": "\ue020",
    "NUMPAD7": "\ue021",
    "NUMPAD8": "\ue022",
    "NUMPAD9": "\ue023",
    "MULTIPLY": "\ue024",
    "ADD": "\ue025",
    "SEPARATOR": "\ue026",
    "SUBTRACT": "\ue027",
    "DECIMAL": "\ue028",
    "DIVIDE": "\ue029",
    "F1": "\ue031",  # function  keys,
    "F2": "\ue032",
    "F3": "\ue033",
    "F4": "\ue034",
    "F5": "\ue035",
    "F6": "\ue036",
    "F7": "\ue037",
    "F8": "\ue038",
    "F9": "\ue039",
    "F10": "\ue03a",
    "F11": "\ue03b",
    "F12": "\ue03c",
    "META": "\ue03d",
    "COMMAND": "\ue03d",
    "ZENKAKU_HANKAKU": "\ue040",
}

set_of_special_keycodes_lower = {
    "null": "\ue000",
    "cancel": "\ue001",
    "help": "\ue002",
    "backspace": "\ue003",
    "back_space": "backspace",
    "tab": "\ue004",
    "clear": "\ue005",
    "return": "\ue006",
    "enter": "\ue007",
    "shift": "\ue008",
    "left_shift": "shift",
    "control": "\ue009",
    "left_control": "control",
    "alt": "\ue00a",
    "left_alt": "alt",
    "pause": "\ue00b",
    "escape": "\ue00c",
    "space": "\ue00d",
    "page_up": "\ue00e",
    "page_down": "\ue00f",
    "end": "\ue010",
    "home": "\ue011",
    "left": "\ue012",
    "arrow_left": "left",
    "up": "\ue013",
    "arrow_up": "up",
    "right": "\ue014",
    "arrow_right": "right",
    "down": "\ue015",
    "arrow_down": "down",
    "insert": "\ue016",
    "delete": "\ue017",
    "semicolon": "\ue018",
    "equals": "\ue019",
    "numpad0": "\ue01a",
    "numpad1": "\ue01b",
    "numpad2": "\ue01c",
    "numpad3": "\ue01d",
    "numpad4": "\ue01e",
    "numpad5": "\ue01f",
    "numpad6": "\ue020",
    "numpad7": "\ue021",
    "numpad8": "\ue022",
    "numpad9": "\ue023",
    "multiply": "\ue024",
    "add": "\ue025",
    "separator": "\ue026",
    "subtract": "\ue027",
    "decimal": "\ue028",
    "divide": "\ue029",
    "f1": "\ue031",
    "f2": "\ue032",
    "f3": "\ue033",
    "f4": "\ue034",
    "f5": "\ue035",
    "f6": "\ue036",
    "f7": "\ue037",
    "f8": "\ue038",
    "f9": "\ue039",
    "f10": "\ue03a",
    "f11": "\ue03b",
    "f12": "\ue03c",
    "meta": "\ue03d",
    "command": "\ue03d",
    "zenkaku_hankaku": "\ue040",
}


class UndetectedSeleniumChrome(uc.Chrome):
    """
    Creates a new instance of the chrome driver. Starts the service and then creates new instance of chrome driver. You could also use Selenium as is but I think this makes it easier.


        Args:

        • headless (bool, optional) Defaults to False. 
            Defaults to False. Headless mode with 4 options:
                ∘ False ⇾ deactivate
                 ∘ True ⇾ options.add_argument("--headless=new")
                ∘ "headless" ⇾ options.add_argument("--headless")
                 ∘ "old" ⇾ options.add_argument("--headless=old")
    
        • keep_alive (bool, optional) Defaults to False. 
            Keeps the python script running as long as driver.window_handles is accessible.
    
        • log_level_3 (bool, optional) Defaults to True. 
            Reducing log.
    
        • muted (bool, optional) Defaults to True. 
            Mute the browser.
    
        • start_maximized (bool, optional) Defaults to False. 
            Start the browser maximized.
    
        • window_position (str, optional) Defaults to None. 
            Set the window position using a string e.g. "1000,1000".
    
        • window_size (str, optional) Defaults to None. 
            Set the window size using a string e.g. "1000,1000".
    
        • profile (bool | str, optional) Defaults to False. 
            Path to your chrome profile which should be in the directory 
             "C:\\Users\\USER_NAME\\AppData\\Local\\Google\\Chrome\\User Data". 
            True equals "Profile 1".
    
        • incognito (bool, optional) Defaults to False. 
            Use incognito mode when True.
    
        • log_capabilities (bool, optional) Defaults to False. 
            Set True to access logs e.g. network logs. [options.set_capability("goog:loggingPrefs",
             {"performance": "ALL"}); options.add_argument("--log-capabilities=ALL")]
    
        • page_load_strategy (str, optional) Defaults to "normal". 
            Browser page load strategy. 
                ∘ "normal": Used by default, waits for all resources to download                
                 ∘ "eager": DOM access is ready, but other resources like images may still be loading                
                ∘ "none": Does not block WebDriver at all
    
        • extensions (tuple, optional) Defaults to (). 
            List of paths to .crx files. They will be installed right after launch. 
    
        • chromedriver_path (str, optional) Defaults to None. 
            May be the path to the chromium driver or an Service instance. Should work with None otherwise I recommend 
             `webdriver_manager` with 
            `selenium.webdriver.chrome.service.Service(ChromeDriverManager().install())`. 
    
        • chrome_profile_user_data (str, optional) Defaults to None. 
            Path to Chrome user data directory. Should look like 
             "C:\\Users\\USER_NAME\\AppData\\Local\\Google\\Chrome\\User Data".
    
        • user_agent (str, optional) Defaults to 'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'. 
            By default "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) 
             Chrome/109.0.0.0 Safari/537.36". 
    
        • proxy (str, optional) Defaults to None. 
            Proxy address. 
    
        • undetected (bool, optional) Defaults to False. 
            Be a bit less bot like. Uses:
                ∘ options.add_argument("--disable-blink-features=AutomationControlled")
                 ∘ options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
                ∘ options.add_experimental_option("useAutomationExtension", False) 
    
        • disable_gpu (bool, optional) Defaults to False. 
            Disables the gpu usage, automatically used in the headless mode. 
    
        • disable_web_security (bool, optional) Defaults to False. 
            Uses "options.add_argument(f"--disable-web-security")".
    
        • browser_version (str, optional) Defaults to None. 
            Older versions like 117 can be nicer. 
    
    
    Returns:
    
        webdriver.Chrome: 
            The driver instance.
    """

    standard_log_types = [
        "browser",
        "client",
        "driver",
        "performance",
        "profiler",
        "server",
    ]
    """These log types can be aquied py driver.get_log(<log_type: str>) - types are: "browser", "client", "driver", "performance", "profiler", "server" """

    def __init__(
        self,
        headless: bool = False,
        keep_alive: bool = False,
        log_level_3: bool = True,
        muted: bool = True,
        start_maximized: bool = False,
        window_position: str = None,
        window_size: str = None,
        profile: bool | str = False,
        incognito: bool = False,
        log_capabilities: bool = False,
        page_load_strategy: str = "normal",
        extensions: tuple = (),
        chromedriver_path: str = None,
        chrome_profile_user_data: str = None,
        user_agent: str = 'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        proxy: str = None,
        undetected: bool = False,
        disable_gpu: bool = False,
        disable_web_security: bool = False,
        browser_version: str = None,
    ):
        """
        Creates a new instance of the chrome driver. Starts the service and then creates new instance of chrome driver. You could also use Selenium as is but I think this makes it easier.


            Args:

            • headless (bool, optional) Defaults to False. 
                Defaults to False. Headless mode with 4 options:
                    ∘ False ⇾ deactivate
                     ∘ True ⇾ options.add_argument("--headless=new")
                    ∘ "headless" ⇾ options.add_argument("--headless")
                     ∘ "old" ⇾ options.add_argument("--headless=old")
        
            • keep_alive (bool, optional) Defaults to False. 
                Keeps the python script running as long as driver.window_handles is accessible.
        
            • log_level_3 (bool, optional) Defaults to True. 
                Reducing log.
        
            • muted (bool, optional) Defaults to True. 
                Mute the browser.
        
            • start_maximized (bool, optional) Defaults to False. 
                Start the browser maximized.
        
            • window_position (str, optional) Defaults to None. 
                Set the window position using a string e.g. "1000,1000".
        
            • window_size (str, optional) Defaults to None. 
                Set the window size using a string e.g. "1000,1000".
        
            • profile (bool | str, optional) Defaults to False. 
                Path to your chrome profile which should be in the directory 
                "C:\\Users\\USER_NAME\\AppData\\Local\\Google\\Chrome\\User Data". 
                True equals "Profile 1".
        
            • incognito (bool, optional) Defaults to False. 
                Use incognito mode when True.
        
            • log_capabilities (bool, optional) Defaults to False. 
                Set True to access logs e.g. network logs. [options.set_capability("goog:loggingPrefs",
                {"performance": "ALL"}); options.add_argument("--log-capabilities=ALL")]
        
            • page_load_strategy (str, optional) Defaults to "normal". 
                Browser page load strategy. 
                    ∘ "normal": Used by default, waits for all resources to download                
                     ∘ "eager": DOM access is ready, but other resources like images may still be loading                
                    ∘ "none": Does not block WebDriver at all
        
            • extensions (tuple, optional) Defaults to (). 
                List of paths to .crx files. They will be installed right after launch. 
        
            • chromedriver_path (str, optional) Defaults to None. 
                May be the path to the chromium driver or an Service instance. Should work with None otherwise I recommend 
                `webdriver_manager` with 
                `selenium.webdriver.chrome.service.Service(ChromeDriverManager().install())`. 
        
            • chrome_profile_user_data (str, optional) Defaults to None. 
                Path to Chrome user data directory. Should look like 
                "C:\\Users\\USER_NAME\\AppData\\Local\\Google\\Chrome\\User Data".
        
            • user_agent (str, optional) Defaults to 'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'. 
                By default "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) 
                Chrome/109.0.0.0 Safari/537.36". 
        
            • proxy (str, optional) Defaults to None. 
                Proxy address. 
        
            • undetected (bool, optional) Defaults to False. 
                Be a bit less bot like. Uses:
                    ∘ options.add_argument("--disable-blink-features=AutomationControlled")
                     ∘ options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
                    ∘ options.add_experimental_option("useAutomationExtension", False) 
        
            • disable_gpu (bool, optional) Defaults to False. 
                Disables the gpu usage, automatically used in the headless mode. 
        
            • disable_web_security (bool, optional) Defaults to False. 
                Uses "options.add_argument(f"--disable-web-security")".
        
            • browser_version (str, optional) Defaults to None. 
                Older versions like 117 can be nicer. 
        
        
        Returns:
        
            webdriver.Chrome: 
                The driver instance.
        """

        self.tabs = {}
        """Dictionary for tabs; first tab is called 0."""

        # caps = DesiredCapabilities.CHROME  # deprecated
        options = uc.ChromeOptions()
        
        # prefs = {}
        if headless:
            if headless == "old":
                options.add_argument("--headless=old")
            elif headless == "headless":
                options.add_argument("--headless")
            else:
                options.add_argument("--headless=new")
            disable_gpu = True
        if log_level_3:
            options.add_argument("--log-level=3")
        if muted:
            options.add_argument("--mute-audio")
        if disable_gpu:
            options.add_argument("--disable-gpu")
        elif start_maximized:
            options.add_argument("–-start-maximized")
        if window_position != None:
            options.add_argument(f"--window-position={window_position}")
        if window_size != None:
            options.add_argument(f"--window-size={window_size}")
        if profile != False:
            use_profile = "Profile 1"
            if profile != True:
                use_profile = profile
            options.add_argument("user-data-dir=" + chrome_profile_user_data)
            options.add_argument("profile-directory=" + use_profile)
            options.add_argument("--user-data-dir=" + chrome_profile_user_data)
            options.add_argument("--profile-directory=" + use_profile)
        if incognito:
            options.add_argument("--incognito")
        if log_capabilities:
            options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
            options.add_argument("--log-capabilities=ALL")
        options.page_load_strategy = page_load_strategy
        for ext in extensions:
            options.add_extension(ext)
        if chromedriver_path:
            service = Service(chromedriver_path)
        elif isinstance(chromedriver_path, Service):
            service = chromedriver_path
        else:
            service = Service()
        if user_agent:
            options.add_argument(user_agent)
        # if download_directory:
        #     prefs["download.default_directory"] = download_directory
        # if allow_multiple_downloads:
        #     prefs["profile.default_content_settings.popups"] = 0
        #     prefs["profile.default_content_setting_values.automatic_downloads"] = 1
        #     prefs["download.prompt_for_download"] = False
        if proxy:
            options.add_argument(f"--proxy-server={proxy}") 
        if undetected:
            # Adding argument to disable the AutomationControlled flag 
            options.add_argument("--disable-blink-features=AutomationControlled")
            # Exclude the collection of enable-automation switches 
            enable_automation = True
            # Turn-off userAutomationExtension 
            options.add_experimental_option("useAutomationExtension", False) 
        if disable_web_security:
            options.add_argument(f"--disable-web-security") 
        if browser_version:
            options.set_capability("browserVersion", browser_version)

        
        ### uc.Chrome doesn't support these
        # if enable_automation:
        #     options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # if enable_logging:
        #     options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # options.add_experimental_option("prefs", prefs)
    

        super().__init__(options=options, service=service)

        self.tabs[0] = self.current_window_handle

        def keep_driver_alive(driver):
            def isBrowserAlive(driver: UndetectedSeleniumChrome):
                try:
                    driver.window_handles
                    return True
                except:
                    return False

            while isBrowserAlive(driver):
                sleep(0.1)

        if keep_alive:
            t = Thread(target=keep_driver_alive, args=[self], daemon=False)
            t.start()

    def get_titel(self):
        """Returns webpage title

        Returns
        -------
        str
            webpage title
        """
        return self.title

    def get_links(self):
        """Collects all links from href attribute of a tags.

        Returns
        -------
        list
            A list containing all urls
        """
        links = []
        try:
            for l in self.find_elements(by=By.XPATH, value="//a[@href]"):
                try:
                    v = l.get_attribute("href")
                    links.append(v)
                except:
                    pass
        except:
            pass
        return links

    def get_header_h1(self):
        """Returns the text of the first h1 element or None if there is none.

        Returns
        -------
        str
            Text of the first h1 element

        None
            If no h1 element found
        """
        try:
            header = [
                l.get_attribute("textContent")
                for l in self.find_elements(by=By.XPATH, value="//h1")
            ][0]
            return header
        except:
            return None

    def get_current_scroll_position(self):
        """Returns the current scroll position aka the window page offset.

        Returns
        -------
        tuple of floats
            x, y
        """
        x = self.execute_script("return window.pageXOffset;")
        y = self.execute_script("return window.pageYOffset;")
        return (x, y)

    def get_current_scroll_position_of_webelement(self, element: WebElement):
        """Returns the current scroll position aka the window page offset.

        Returns
        -------
        tuple of floats
            x, y
        """
        x = self.execute_script("return arguments[0].pageXOffset;", element)
        y = self.execute_script("return arguments[0].pageYOffset;", element)
        return (x, y)

    def get_all_attributes_selenium(self, element: WebElement):
        """Get all attributes with values as a dictionary.

        Uses Selenium -> might not find all, but is less prone to errors.
        Why? I don't know....

        Parameters
        ----------
        element : selenium.webdriver.remote.webelement.WebElement
            Needed to access the element.

        Returns
        -------
        dict
            Contains attributes as keys and their values.
        """
        attrs = self.execute_script(
            "var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;",
            element,
        )
        return attrs

    def get_all_attributes_bs4(self, element: WebElement):
        """Get all attributes with values as a dictionary.

        Uses BeautifulSoup -> should find all, but is more prone to errors.
        Why? I don't know....

        Parameters
        ----------
        element : selenium.webdriver.remote.webelement.WebElement
            Needed to access the element.

        Returns
        -------
        dict
            Contains attributes as keys and their values.
        """
        from bs4 import BeautifulSoup

        html = element.get_attribute("outerHTML")
        attrs = BeautifulSoup(html, "html.parser").a.attrs
        return attrs

    def get_all_attributes(self, element: WebElement):
        """Get all attributes with values as a dictionary.

        Tries to use BeautifulSoup, on error it uses Selenium.

        Parameters
        ----------
        element : selenium.webdriver.remote.webelement.WebElement
            Needed to access the element.

        Returns
        -------
        dict
            Contains attributes as keys and their values.
        """
        try:
            attrs = self.get_all_attributes_bs4(element)
        except:
            attrs = self.get_all_attributes_selenium(element)
        return attrs

    def get_parent_of_element(self, element: WebElement) -> WebElement:
        parent_element = element.find_element(XPATH, "..")
        return parent_element

    def highlight(self, element: WebElement, effect_time, color="red", border=3):
        """Highlights (blinks) a Selenium Webdriver element

        Parameters
        ----------
        element : WebElement
            Needed to access the element
        color : Any
            JavaScript Style color Property
        border : Any
            JavaScript Style border Property
        """

        def apply_style(s):
            self.execute_script(
                "arguments[0].setAttribute('style', arguments[1]);", element, s
            )

        original_style = element.get_attribute("style")
        apply_style("border: {0}px solid {1};".format(border, color))
        sleep(effect_time)
        apply_style(original_style)

    def perma_highlight(self, element: WebElement, color="red", border=3):
        """Highlights a Selenium Webdriver element permanently.

        Reversable with the method undo_highlight.

        Parameters
        ----------
        element : WebElement
            Needed to access the element
        color : Any
            JavaScript Style color Property
        border : Any
            JavaScript Style border Property

        Returns
        -------
        str
            Value of the style property.
            If non-existent, None is returned.
        """

        def apply_style(s):
            self.execute_script(
                "arguments[0].setAttribute('style', arguments[1]);", element, s
            )

        original_style = element.get_attribute("style")
        apply_style("border: {0}px solid {1};".format(border, color))
        return original_style

    def undo_highlight(self, element: WebElement, original_style: str):
        """Undo the perma_highlight method.

        Parameters
        ----------
        element : WebElement
            Needed to access the element
        original_style : str
            Value of the style property
        """

        def apply_style(s):
            self.execute_script(
                "arguments[0].setAttribute('style', arguments[1]);", element, s
            )

        apply_style(original_style)

    def get_max_body_scroll_height(self):
        """Returns the scroll height of the body.

        Returns:
            int: scroll height of the body
        """
        return int(self.execute_script("return document.body.scrollHeight"))

    def open_new_tab(self, tab_name: str = None):
        """Create a new tab and switches to it and adds it to self.tabs.
        Returns the tabs name for self.tabs.
        """
        try:
            self.switch_to.new_window("tab")
        except:
            tbs = [] + self.window_handles
            self.execute_script("window.open('about:blank','_blank');")
            for t in self.window_handles:
                if t not in tbs:
                    self.switch_to.window(t)
        if tab_name == None:
            n = 0
            while n in self.tabs.keys():
                n += 1
            tab_name = n
        self.tabs[tab_name] = self.current_window_handle
        return tab_name

    def open_new_window(self):
        """Create a new tab and switches to it and adds it to self.tabs."""
        self.switch_to.new_window("window")
        if tab_name == None:
            names = []
            for tn in self.tabs:
                names.append(tn)
            numbs = []
            for n in names:
                if n.startswith("Window_"):
                    try:
                        n = int(n.replace("Window_"))
                        numbs.append(n)
                    except:
                        pass
            if len(numbs) != 0:
                numbs = sorted(numbs)
                highest_numb = numbs[-1] + 1
            else:
                highest_numb = 1
            tab_name = f"Window_{highest_numb}"
        self.tabs[tab_name] = self.current_window_handle

    def scroll_in_webelement(
        self,
        element: WebElement,
        x: float = None,
        y: float = None,
        max_down: bool = False,
        max_up: bool = False,
        relative: bool = True,
        really_max_down: bool = False,
    ):
        """Scroll within the webelement.

        With x or y you can scroll to a certain x- or y-coordinate.
        If only one of x and y is given the other one stays in place.

        Parameters
        x : float, optional
            Either dedicated x-coordinate or the relative x displacement. If None it stays as it was, by default None
        y : float, optional
            Either dedicated y-coordinate or the relative y displacement. If None it stays as it was, by default None
        max_down : bool, optional
            Scroll as far down as possible. Won't reach the end of infinite loading webpages, by default False
        max_up : bool, optional
            Scroll to y=0, by default False
        relative : bool, optional
            Needs to be True for relative displacements, by default False
        """
        if relative:
            if x == None and y != None:
                x = 0
            elif x != None and y == None:
                y = 0
            else:
                x = y = 0
            self.execute_script(f"arguments[0].scrollBy({x},{y})", element)
        else:
            if x == None and y != None:
                x = self.execute_script("return arguments[0].scrollLeft;", element)
            elif x != None and y == None:
                y = self.execute_script("return arguments[0].scrollTop;", element)
            else:
                x = self.execute_script("return arguments[0].scrollLeft;", element)
                y = self.execute_script("return arguments[0].scrollTop;", element)
            self.execute_script(f"window.scrollTo({x},{y})")
        if max_down:
            x = self.execute_script("return arguments[0].scrollLeft;", element)
            self.execute_script(f"window.scrollTo({x},document.body.scrollHeight)")
        elif max_up:
            x = self.execute_script("return arguments[0].scrollLeft;", element)
            self.execute_script(f"window.scrollTo({x},0)")
        elif really_max_down:
            heights = []
            while True:
                self.scroll(max_down=True)
                height = self.get_current_scroll_position()[1]
                heights.append(height)
                boos = [x == height for x in heights[-1000:-1]]
                if len(heights) > 1000 and all(boos):
                    break

    def scroll_alt(
        self,
        x: float = None,
        y: float = None,
        max_down: bool = False,
        max_up: bool = False,
        relative: bool = False,
        really_max_down: bool = False,
    ):
        """Scroll within the webpage.

        With x or y you can scroll to a certain x- or y-coordinate.
        If only one of x and y is given the other one stays in place.

        Parameters
        x : float, optional
            Either dedicated x-coordinate or the relative x displacement. If None it stays as it was, by default None
        y : float, optional
            Either dedicated y-coordinate or the relative y displacement. If None it stays as it was, by default None
        max_down : bool, optional
            Scroll as far down as possible. Won't reach the end of infinite loading webpages, by default False
        max_up : bool, optional
            Scroll to y=0, by default False
        relative : bool, optional
            Needs to be True for relative displacements, by default False
        """
        if x != None or y != None:
            if relative:
                # if x == None: x = 0
                # if y == None: y = 0
                # self.execute_script(f"window.scroll({x},{y})")
                if x == None:
                    x = self.execute_script("return window.pageXOffset;")
                    y = self.execute_script("return window.pageYOffset;") + y
                if y == None:
                    x = self.execute_script("return window.pageXOffset;") + x
                    y = self.execute_script("return window.pageYOffset;")
                self.execute_script(f"window.scrollTo({x},{y})")
            else:
                if x == None:
                    x = self.execute_script("return window.pageXOffset;")
                if y == None:
                    y = self.execute_script("return window.pageYOffset;")
                self.execute_script(f"window.scrollTo({x},{y})")
        else:
            if max_down:
                x = self.execute_script("return window.pageXOffset;")
                self.execute_script(f"window.scrollTo({x},document.body.scrollHeight)")
            elif max_up:
                x = self.execute_script("return window.pageXOffset;")
                self.execute_script(f"window.scrollTo({x},0)")
            if really_max_down:
                # same_heights = []
                # stime = time()
                # rate = 1000
                # while True:
                #     old_height = self.get_current_scroll_position()[1]
                #     self.scroll(max_down=True)
                #     new_height = self.get_current_scroll_position()[1]
                #     same_heights.append(old_height == new_height)
                #     if time()-stime < 10: rate = len(same_heights)/(time()-stime)
                #     if len(same_heights) > rate*20:
                #         same_heights.pop(0)
                #     if all(same_heights): break
                heights = []
                while True:
                    self.scroll(max_down=True)
                    height = self.get_current_scroll_position()[1]
                    heights.append(height)
                    boos = [x == height for x in heights[-1000:-1]]
                    if len(heights) > 1000 and all(boos):
                        break

    def scroll(
        self,
        x: float = None,
        y: float = None,
        max_down: bool = False,
        max_up: bool = False,
        relative: bool = True,
        really_max_down: bool = False,
    ):
        """Scroll within the webpage.

        With x or y you can scroll to a certain x- or y-coordinate.
        If only one of x and y is given the other one stays in place.

        Parameters
        x : float, optional
            Either dedicated x-coordinate or the relative x displacement. If None it stays as it was, by default None
        y : float, optional
            Either dedicated y-coordinate or the relative y displacement. If None it stays as it was, by default None
        max_down : bool, optional
            Scroll as far down as possible. Won't reach the end of infinite loading webpages, by default False
        max_up : bool, optional
            Scroll to y=0, by default False
        relative : bool, optional
            Needs to be True for relative displacements, by default True
        """
        if relative:
            if x == None and y != None:
                x = 0
            elif x != None and y == None:
                y = 0
            else:
                x = y = 0
            self.execute_script(f"window.scrollBy({x},{y})")
        else:
            if x == None and y != None:
                x = self.execute_script("return window.pageXOffset;")
            elif x != None and y == None:
                y = self.execute_script("return window.pageYOffset;")
            else:
                x = self.execute_script("return window.pageXOffset;")
                y = self.execute_script("return window.pageYOffset;")
            self.execute_script(f"window.scrollTo({x},{y})")
        if max_down:
            x = self.execute_script("return window.pageXOffset;")
            self.execute_script(f"window.scrollTo({x},document.body.scrollHeight)")
        elif max_up:
            x = self.execute_script("return window.pageXOffset;")
            self.execute_script(f"window.scrollTo({x},0)")
        elif really_max_down:
            heights = []
            while True:
                self.scroll(max_down=True)
                height = self.get_current_scroll_position()[1]
                heights.append(height)
                boos = [x == height for x in heights[-1000:-1]]
                if len(heights) > 1000 and all(boos):
                    break

    def scroll_with_action(
        self,
        funktion: Callable,
        scroll_step=200,
        args: Iterable = ("Keine Args", None),
        execute_every_x_sec: Callable = None,
        x_sec: int = 10,
        break_height_repeat: int = 10,
    ):
        """Scroll down the page and execute a function after every scrolling step.
        You can also execute a function every x seconds if you wish.
        The scrolling will be stopped when the (presumably) final hight can repeatedly be called.
        How often it has to be called can be changed with break_height_repeat.

        Args:
            funktion (function): Function to execute after every scroll step. If this function returns anything you will recieve it with this functions return.
            scroll_step (int, optional): Scroll distance for each step. Defaults to 200.
            args (Iterable, optional): Args for your function. Defaults to ("Keine Args", None) which means no args get send.
            execute_every_x_sec (function, optional): If not None, this function will get executed every x seconds. Defaults to None.
            x_sec (int, optional): Interval for the time repeated function in seconds. Defaults to 10.
            break_height_repeat (int, optional): How often the (presumably) final hight needs to be called before the loop breaks. Defaults to 10.

        Returns:
            If your scroll-step-function returns anything, it will get returned by this function.
        """
        heights = []
        stime = time()
        p = True
        while True:
            self.scroll(y=scroll_step, relative=True)
            if args == ("Keine Args", None):
                result = funktion()
            else:
                result = funktion(*args)
            height = self.get_current_scroll_position()[1]
            heights.append(height)
            boos = [h == height for h in heights[-break_height_repeat:-1]]
            if len(heights) > break_height_repeat and all(boos):
                break
            if execute_every_x_sec != None:
                if int(time() - stime) % x_sec == 0 and p:
                    execute_every_x_sec()
                    p = False
                if int(time() - stime) - 0.5 % x_sec == 0:
                    p = True
        return result

    def scroll_with_action_timed(
        self,
        funktion: Callable,
        scroll_step=200,
        args: Iterable = ("Keine Args", None),
        execute_every_x_sec: Callable = None,
        x_sec: int = 10,
        break_same_height_time: int = 15,
    ):
        """Scroll down the page and execute a function after every scrolling step.
        You can also execute a function every x seconds if you wish.
        The scrolling will be stopped when the scrolling height doesn't change over the time span of <break_same_height_time>.

        Args:
            funktion (function): Function to execute after every scroll step. If this function returns anything you will recieve it with this functions return.
            scroll_step (int, optional): Scroll distance for each step. Defaults to 200.
            args (Iterable, optional): Args for your function. Defaults to ("Keine Args", None) which means no args get send.
            execute_every_x_sec (function, optional): If not None, this function will get executed every x seconds. Defaults to None.
            x_sec (int, optional): Interval for the time repeated function in seconds. Defaults to 10.
            break_same_height_time (int, optional): Time span in seconds which needs to be exceeded with only one scolling height messurable to break the loop. Defaults to 15.

        Returns:
            If your scroll-step-function returns anything, it will get returned by this function.
        """
        heights = []
        stime = time()
        p = True
        same_time = 0
        not_same_time = 0
        while True:
            self.scroll(y=scroll_step, relative=True)
            if args == ("Keine Args", None):
                result = funktion()
            else:
                result = funktion(*args)
            height = self.get_current_scroll_position()[1]
            heights.append(height)
            if execute_every_x_sec != None:
                if int(time() - stime) % x_sec == 0 and p:
                    execute_every_x_sec()
                    p = False
                if int(time() - stime) - 0.5 % x_sec == 0:
                    p = True
            try:
                if height == heights[-2]:
                    same_time = time()
                else:
                    not_same_time = time()
                if (
                    same_time - not_same_time > break_same_height_time
                    and same_time != 0
                    and not_same_time != 0
                ):
                    break
            except:
                pass
        return result

    def scroll_with_action_conditional(
        self,
        funktion: Callable,
        conditional_function: Callable,
        scroll_step=200,
        args: Iterable = ("Keine Args", None),
        con_func_args: Iterable = ("Keine Args", None),
        execute_every_x_sec: Callable = None,
        x_sec: int = 10,
    ):
        """Scroll down the page and execute a function after every scrolling step.
        You can also execute a function every x seconds if you wish.
        The scrolling will be stopped when the <conditional_function> returns False.


        Args:
            funktion (function): Function to execute after every scroll step. If this function returns anything you will recieve it with this functions return.
            conditional_function (Callable): Function for loop control. Return True to keep the loop alive, False to break.
            scroll_step (int, optional): Scroll distance for each step. Defaults to 200.
            args (Iterable, optional): Args for your function. Defaults to ("Keine Args", None) which means no args get send.
            con_func_args (Iterable, optional): Args for your conditional_function. Defaults to ("Keine Args", None).
            execute_every_x_sec (function, optional): If not None, this function will get executed every x seconds. Defaults to None.
            x_sec (int, optional): Interval for the time repeated function in seconds. Defaults to 10.

        Returns:
            _type_: _description_
        """
        heights = []
        stime = time()
        p = True
        last_execution = time()
        while True:
            self.scroll(y=scroll_step, relative=True)
            if args == ("Keine Args", None):
                result = funktion()
            else:
                result = funktion(*args)
            height = self.get_current_scroll_position()[1]
            heights.append(height)
            if execute_every_x_sec != None:
                # if int(time()-stime) % x_sec == 0 and p:
                #     execute_every_x_sec()
                #     p = False
                # if int(time()-stime)-0.5 % x_sec == 0: p = True
                if time() - last_execution > x_sec:
                    execute_every_x_sec()
                    last_execution = time()
            if con_func_args == ("Keine Args", None):
                con_result = conditional_function()
            else:
                con_result = conditional_function(*con_func_args)
            if not con_result:
                break
        return result

    def try_to_do_this_with_timeout(
        self,
        funktion: Callable,
        timeout: float = 60,
        args: Iterable = None,
        time_between_tries: float = 0,
        print_exception: bool = False,
        loop_function: Callable = None,
        loop_function_intervall: int = 1,
    ):
        """Tries until timeout or successfull

        Args:
            funktion (Callable): your function
            timeout (float, optional): timeout. Defaults to 60.
            args (Iterable, optional): args. Defaults to None.
            time_between_tries (float, optional): sleep?. Defaults to 0.
            print_exception (bool, optional): want to know?. Defaults to False.

        Returns:
            _type_: result of your function
        """
        stime = time()
        loop_time_correction = True
        result = None
        while time() - stime < timeout:
            try:
                try:
                    result = funktion(*args)
                except:
                    result = funktion()
                break
            except Exception as e:
                if time_between_tries > 0:
                    sleep(time_between_tries)
                if print_exception:
                    print(e)
            if loop_function != None:
                if (
                    time() - stime % loop_function_intervall == 0
                    and loop_time_correction
                ):
                    loop_function()
                    loop_time_correction = False
                if (
                    time() - stime + 1 % loop_function_intervall == 0
                    and not loop_time_correction
                ):
                    loop_time_correction = True
        return result

    def process_browser_logs_for_network_events(self, logs=None):
        """
        Return only logs which have a method that start with "Network.response", "Network.request", or "Network.webSocket"
        since we're interested in the network events specifically.

        logs: logs = driver.get_log("performance")
        """
        if logs == None:
            logs = self.get_log("performance")
        for entry in logs:
            log = json.loads(entry["message"])["message"]
            if (
                "Network.response" in log["method"]
                or "Network.request" in log["method"]
                or "Network.webSocket" in log["method"]
            ):
                yield log

    def zoom(self, percentage: float | str):
        """Change the zoom on the page.

        Args:
            percentage (float|str): The percentage you want without the %-sign, e.g. 10 for 10 %.
        """
        self.execute_script(f"document.body.style.zoom='{percentage}%'")

    def wait_for_element(
        self,
        tag: str | WebElement,
        by: str = XPATH,
        timeout: float = 10,
        raise_Exception: bool = False,
    ) -> WebElement | None:
        """The driver should wait until the element is found. I still have some trouble with this one.

        Args:
            tag (str | WebElement): Identification like xpath or the element itself.
            by (str, optional): No need to use xpath if you don't want to. Defaults to XPATH.
            timeout (float, optional): Wait max this in seconds. Defaults to 10.
            raise_Exception (bool, optional): On timeout you can have an exception, if you want to. Defaults to False.

        Returns:
            WebElement | None: It should return the WebElement but often times it doesn't ... I don't know why, since I didn't want to look at WebDriverWait too much.
        """

        def task():
            if type(tag) == str:
                element = WebDriverWait(self, timeout).until(
                    EC.element_to_be_clickable((by, tag))
                )
            elif type(tag) == WebElement:
                element = WebDriverWait(self, timeout).until(
                    EC.element_to_be_clickable(tag)
                )
            return element

        if not raise_Exception:
            try:
                element = task()
                return element
            except:
                return None
        else:
            return task()

    def wait_for_element_improvised(
        self,
        by: str = XPATH,
        tag: str = None,
        timeout: float = 10,
        raise_Exception: bool = False,
        return_timeout: bool = False,
    ) -> WebElement | None:
        """Winged version, baased on trial and error. The driver should wait until the element is found. I still have some trouble with this one.

        Args:
            by (str, optional): No need to use xpath if you don't want to. Defaults to XPATH.
            tag (str | WebElement): Identification like xpath or the element itself.
            timeout (float, optional): Wait max this in seconds. Defaults to 10.
            raise_Exception (bool, optional): On timeout you can have an exception, if you want to. Defaults to False.
            return_timeout (bool, optional): On timeout return the string 'timeout'. Defaults to False.

        Returns:
            WebElement | None: It should return the WebElement but often times it doesn't ... I don't know why, since I didn't want to look at WebDriverWait too much.
        """
        if tag == XPATH:
            tag, by = by, tag

        def task():
            try:
                element = self.find_element(by, tag)
            except:
                element = None
            return element

        start = time()
        element = task()
        while element == None:
            if time() - start > timeout:
                break
            element = task()
        if element:
            return element
        elif element == None and raise_Exception:
            raise NoSuchElementException
        elif time() - start > timeout and return_timeout:
            return "timeout"

    def wait_for_clickable(
        self,
        tag: str | WebElement,
        by=XPATH,
        timeout: float = 10,
        raise_Exception: bool = False,
    ) -> WebElement | None:
        def task():
            if type(tag) == str:
                element = WebDriverWait(self, timeout).until(
                    EC.element_to_be_clickable((by, tag))
                )
            elif type(tag) == WebElement:
                element = WebDriverWait(self, timeout).until(
                    EC.element_to_be_clickable(tag)
                )
            return element

        if not raise_Exception:
            try:
                element = task()
                return element
            except:
                return None
        else:
            return task()

    def wait_for_visibility(
        self,
        tag: str | WebElement,
        by=XPATH,
        timeout: float = 10,
        raise_Exception: bool = False,
    ) -> WebElement | None:
        def task():
            if type(tag) == str:
                element = WebDriverWait(self, timeout).until(
                    EC.visibility_of_element_located((by, tag))
                )
            elif type(tag) == WebElement:
                element = WebDriverWait(self, timeout).until(
                    EC.visibility_of_element_located(tag)
                )
            return element

        if not raise_Exception:
            try:
                element = task()
                return element
            except:
                return None
        else:
            return task()

    def action_chain(
        self,
        keys_actiontype_dict: dict[str:str],
        element: WebElement = None,
        duration_ms: int = 250,
    ):
        """Send an action chain.
        For the possible keys either look up the keycode (set_of_special_keycodes) or write the letter itself.
        For the actiontype use one of the following three:
        - 'press' | 'down' | 'key_down'
        - 'release' | 'up' | 'key_up'
        - 'press_and_release' | 'send' | 'send_keys'

        Args:
            keys_actiontype_dict (dict[str:str]): see general desciption

        Raises:
            ValueError: if you don't choose any of the possible actiontypes
        """
        ac = ActionChains(self, duration=duration_ms)
        for key, actiontype in keys_actiontype_dict.items():
            match actiontype:
                case "press" | "down" | "key_down":
                    try:
                        ac.key_down(set_of_special_keycodes_lower[key], element)
                    except:
                        try:
                            ac.key_down(set_of_special_keycodes[key], element)
                        except:
                            ac.key_down(key, element)
                case "release" | "up" | "key_up":
                    try:
                        ac.key_up(set_of_special_keycodes_lower[key], element)
                    except:
                        try:
                            ac.key_up(set_of_special_keycodes[key], element)
                        except:
                            ac.key_up(key, element)
                case "press_and_release" | "send" | "send_keys":
                    if element == None:
                        try:
                            ac.send_keys(set_of_special_keycodes_lower[key])
                        except:
                            try:
                                ac.send_keys(set_of_special_keycodes[key])
                            except:
                                ac.send_keys(key)
                    else:
                        try:
                            ac.send_keys_to_element(
                                element, set_of_special_keycodes_lower[key]
                            )
                        except:
                            try:
                                ac.send_keys_to_element(
                                    element, set_of_special_keycodes[key]
                                )
                            except:
                                ac.send_keys_to_element(element, key)
                case _:
                    raise ValueError(
                        f"actiontype {actiontype} is not an option. Choose from 'press' | 'down' | 'key_down', 'release' | 'up' | 'key_up', 'press_and_release' | 'send' | 'send_keys'"
                    )
        ac.perform()

    def download_src(
        self, src: str, filename: str = "index.jpg", rename_to_timestamp: bool = False
    ):
        if rename_to_timestamp:
            # filename = timestamp() + "." + filename.split(".")[-1]
            filename = Zeit(time()).stempel_5 + "." + filename.split(".")[-1]
        s = Template(download_src)
        script = s.substitute(src=src, filename=filename)
        self.execute_script(script)

    def click_link(
        self, link: str
    ):
        filename = Zeit(time()).stempel_5 + "." + filename.split(".")[-1]
        s = Template(click_link_templ)
        script = s.substitute(src=link, filename=filename)
        self.execute_script(script)

    def download_blob_src_by_xpath(
        self, xpath: str, filename: str = "index.jpg", rename_to_timestamp: bool = False
    ):
        if rename_to_timestamp:
            # filename = timestamp() + "." + filename.split(".")[-1]
            filename = Zeit(time()).stempel_5 + "." + filename.split(".")[-1]
        s = Template(download_blob_src_by_xpath_script_template)
        script = s.substitute(xpath=xpath, filename=filename)
        self.execute_script(script)

    def download_all_blob_srcs(self):
        self.execute_script(download_all_blob_srcs_script)

    def download_all_img_srcs(self):
        self.execute_script(download_all_imgs_script)

    def download_all_video_srcs(self):
        self.execute_script(download_all_vids_script)

    def scroll_in_container(self, container_xpath: str, dx=0, dy=0):
        script_template = Template(scroll_in_element_script_tmp)
        script = script_template.substitute(xpath=container_xpath, dx=dx, dy=dy)
        self.execute_script(script)

    def trigger_event_webelement(
        self, element: WebElement, type: str = "mousedown", bubbles: bool = True
    ):
        ka, kz = "{", "}"
        if bubbles:
            bubls = "true"
        else:
            bubls = "false"
        self.execute_script(
            f"arguments[0].dispatchEvent(new Event('{type}', {ka} 'bubbles': {bubls} {kz}));",
            element,
        )

    def is_visible(self, element: WebElement):
        return self.execute_script(is_visible_script, element)

    def get_WebElement_parent(self, element: WebElement, tier: int = 1) -> WebElement:
        def _get_WebElement_parent(element: WebElement) -> WebElement:
            return element.find_element(XPATH, "..")

        for i in range(tier):
            element = _get_WebElement_parent(element)
        return element

    def get_xpath_of_element_alpha_version(self, element: WebElement):
        tags = [
            element.tag_name,
        ]
        try:
            parent = self.get_parent_of_element(element)
            tags.append(parent.tag_name)
            for i in range(100):
                try:
                    parent = self.get_parent_of_element(parent)
                    tags.append(parent.tag_name)
                except:
                    break
        except:
            pass
        xpath = "/".join(tags[::-1])
        return xpath

    def get_xpath_of_element_beta_version(self, element: WebElement) -> str:
        tags = []
        posi = []
        try:
            for i in range(1000):
                try:
                    try:
                        child
                        child = parent
                    except:
                        child = element
                    parent = self.get_parent_of_element(child)
                    # print(len(parent.find_elements(XPATH, f"./{child.tag_name}")))
                    posi.append(len(parent.find_elements(XPATH, f"./{child.tag_name}")))
                    tags.append(child.tag_name)
                except:
                    tags.append(parent.tag_name)
                    posi.append(0)
                    break
        except:
            pass
        tags = tags[::-1]
        posi = posi[::-1]
        parts = []
        for i, e in enumerate(tags):
            p = posi[i]
            if p > 1:
                e += f"[{p}]"
            parts.append(e)
        xpath = "/".join(parts)
        return xpath

    def get_xpath_of_element_v3(self, element: WebElement) -> str:
        tags = []
        posi = []
        try:
            for i in range(1000):
                try:
                    try:
                        child
                        child = parent
                    except:
                        child = element
                    parent = self.get_parent_of_element(child)
                    # print(len(parent.find_elements(XPATH, f"./{child.tag_name}")))
                    same_tags = parent.find_elements(XPATH, f"./{child.tag_name}")
                    for sti, st in enumerate(same_tags):
                        if st == child:
                            posi.append(sti + 1)
                    tags.append(child.tag_name)
                except:
                    tags.append(parent.tag_name)
                    posi.append(0)
                    break
        except:
            pass
        tags = tags[::-1]
        posi = posi[::-1]
        parts = []
        for i, e in enumerate(tags):
            p = posi[i]
            if p > 1:
                e += f"[{p}]"
            parts.append(e)
        xpath = "/".join(parts)
        return xpath

    def get_xpath_of_element(self, element: WebElement) -> str:
        return self.get_xpath_of_element_v3(element)

    def get_xpath_of_element_no_positions(self, element: WebElement) -> str:
        tags = []
        try:
            for i in range(1000):
                try:
                    try:
                        child
                        child = parent
                    except:
                        child = element
                    parent = self.get_parent_of_element(child)
                    tags.append(child.tag_name)
                except:
                    tags.append(parent.tag_name)
                    break
        except:
            pass
        tags = tags[::-1]
        xpath = "/" + "/".join(tags)
        return xpath

    def close_all_tabs_except_tab_0(self):
        for h in self.window_handles:
            if h != self.tabs[0]:
                self.switch_to.window(h)
                self.close()
        self.switch_to.window(self.tabs[0])

    def close_all_tabs_except_tab_x(self, tab_x):
        for h in self.window_handles:
            if h != tab_x:
                self.switch_to.window(h)
                self.close()
        self.switch_to.window(tab_x)

    def switch_to_window(self, window):
        self.switch_to.window(window)

    def switch_to_window_0(self):
        self.switch_to.window(self.window_handles[0])

    def get_CookieJar(self, cookies=None):
        if cookies == None:
            cookies = self.get_cookies()
        c_jar = requests.cookies.RequestsCookieJar()
        for cookie in cookies:
            c_jar.set(
                cookie["name"],
                cookie["value"],
                domain=cookie["domain"],
                path=cookie["path"],
            )
        return c_jar


if __name__ == "__main__":
    driver = UndetectedSeleniumChrome(keep_alive=True)
    driver.get("https://google.com")
    sleep(10)
    driver.quit()

