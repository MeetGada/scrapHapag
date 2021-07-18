from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import datetime, json

driver = webdriver.Chrome('./chromedriver2.exe')

# called to click button
def btnClick(path):
    conButton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, path)))
    conButton.click()

# called to send input
def sendInput(path, data):
    location = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, path)))
    location.clear()
    location.send_keys(data)


def get_schedule(origin = 'INNSA', destination = 'BEANR', departure_date = datetime.datetime.now()):
    driver.get('https://www.hapag-lloyd.com/en/online-business/schedule/interactive-schedule/interactive-schedule-solution.html')

    btnClick('//button[text()="Confirm My Choices"]')                                               # confirms the choices
    sendInput('//input[@id="schedules_interactive_f:hl19"]', origin)                                # inputs origin name
    btnClick('//div[@class="combo-name"]')                                                          # confirms origin input
    sendInput('//input[@id="schedules_interactive_f:hl29"]', str(departure_date)[:10])              # inputs departure date
    sendInput('//input[@id="schedules_interactive_f:hl62"]', destination)                           # inputs the destination
    btnClick('//div[@id="ext-gen297"]//div[@class="combo-name"]')                                   # confirms destiantion input
    btnClick('//button[@id="schedules_interactive_f:hl116"]')                                       # clicks find button

    driver.implicitly_wait(5)
    tableData = driver.find_elements_by_xpath('//table[@id="schedules_interactive_f:hl135"]//tbody//tr')    # gets result table
    index = [2, 6, 5]                                                                                       # indexes of origin, transit_time and destination
    keys = ['origin_port', 'etd', 'destination_port', 'eta']                                                # keys for results
    cols = [data.find_elements_by_tag_name('td') for data in tableData]                                     # shortlists results data
    results = []
    for col in  cols:
        endData = {'transit_time':col[6].text}
        for i in range(0,4,2):
            strDate = col[index[i]].text.split('\n')
            intDate = list(map(int, strDate[1].split('-')))
            endData.update({
                keys[i]:strDate[0], keys[i+1]:datetime.datetime(intDate[0],intDate[1],intDate[2],0,0,0).timestamp()
            })
        results.append(endData)
    driver.close()

    return json.dumps({'results': results, 'total_results': len(results)},indent=4)

