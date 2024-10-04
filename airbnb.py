import time
import random
import csv
import uuid
from typing import List
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from selenium.webdriver.chromium.webdriver import ChromiumDriver
from selenium.webdriver.common.by import By
from tqdm import tqdm


class AirBnB:
    def __init__(self) -> None:
        self.driver  = self._get_driver()
        self.csv_header = self._build_csv_writer(
            head=["ID", "title", "facilities", "price"],
            file_name="airbnb_header.csv"
        )
        self.csv_comments = self._build_csv_writer(
            head=["ID", "name", "city", "comment"],
            file_name="airbnb_comments.csv"
        )

    def __enter__(self) -> 'AirBnB':
        return self
    
    def __exit__(self, exc_type, exc_value, exc_attributes) -> bool:
        self.driver.close()
        self.driver.quit()
        return True
    
    def _get_driver(self) -> ChromiumDriver:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--windows-size=1200,1000")
        options.add_argument("--disable_notifications")
        driver = Chrome(options=options)
        return driver
    
    def _build_csv_writer(self, head: List[str], path: str = "data", file_name: str = "airbnb.csv"):
        target = open(f"{path}/{file_name}", mode="w", encoding="utf-8", newline="\n")
        writer = csv.writer(target, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(head)
        return writer

    
    def process(self, url: str) -> None:
        self.driver.get(url)
        time.sleep(random.uniform(1, 3))
        ahrefs = self.driver.find_elements(By.XPATH, "//a[@class='l1ovpqvx atm_1he2i46_1k8pnbi_10saat9 atm_yxpdqi_1pv6nv4_10saat9 atm_1a0hdzc_w1h1e8_10saat9 atm_2bu6ew_929bqk_10saat9 atm_12oyo1u_73u7pn_10saat9 atm_fiaz40_1etamxe_10saat9 bn2bl2p atm_5j_223wjw atm_9s_1ulexfb atm_e2_1osqo2v atm_fq_idpfg4 atm_mk_stnw88 atm_tk_idpfg4 atm_vy_1osqo2v atm_26_1j28jx2 atm_3f_glywfm atm_kd_glywfm atm_3f_glywfm_jo46a5 atm_l8_idpfg4_jo46a5 atm_gi_idpfg4_jo46a5 atm_3f_glywfm_1icshfk atm_kd_glywfm_19774hq atm_uc_aaiy6o_1w3cfyq_oggzyc atm_70_1b8lkes_1w3cfyq_oggzyc atm_uc_glywfm_1w3cfyq_pynvjw atm_uc_aaiy6o_pfnrn2_ivgyl9 atm_70_1b8lkes_pfnrn2_ivgyl9 atm_uc_glywfm_pfnrn2_61fwbc dir dir-ltr']")
        ahrefs = [a.get_attribute("href") for a in ahrefs]

        for i, link in tqdm(enumerate(ahrefs), desc="AirBnB Scraping 🚀 ....", total=len(ahrefs), ncols=120):
            try:
                self.driver.get(link)
                time.sleep(random.uniform(1, 3))
                title = self.driver.find_element(By.XPATH, "//div//section//div//div//div//h1")
                facilities = self.driver.find_element(By.XPATH, "//div//section//div//ol")
                price = self.driver.find_element(By.XPATH, "//div//span//div//span")
                price = price.get_attribute("innerHTML").replace('&nbsp;', ' ') if price.get_attribute("innerHTML") else 'N/A'
    
                unique_id = str(uuid.uuid4())

                self.csv_header.writerow([unique_id, title.text, facilities.text, price])

                comment_blocks = self.driver.find_elements(By.XPATH, "//div[@class='_b7zir4z']")
                for block in comment_blocks:
                    comment = block.find_element(By.XPATH, ".//div//div//div//div//span//span")
                    name = block.find_element(By.XPATH, ".//div//div//div//div//div//h3")
                    city = block.find_element(By.XPATH, ".//div//div//div//div//div//div")

                    comment = comment.get_attribute("innerHTML")
                    name = name.get_attribute("innerHTML")
                    city = city.get_attribute("innerHTML")

                    self.csv_comments.writerow([unique_id, name, city, comment])

            except Exception as ex:
                print(ex)
    
    
if __name__ == "__main__":
    with AirBnB() as airbnb:
        airbnb.process(url="https://www.airbnb.com/s/Punta-Cana--Dominican-Republic/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-11-01&monthly_length=3&monthly_end_date=2025-02-01&price_filter_input_type=0&channel=EXPLORE&query=Punta%20Cana%2C%20Dominican%20Republic&place_id=ChIJd_7LXWSRqI4R8_YS7fociGE&location_bb=QZa6CMKIpVJBk4gIwok%2BdA%3D%3D&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click")



