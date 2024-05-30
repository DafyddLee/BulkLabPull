from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from re_textfile import extract_lab_results_from_text
from re_textfile import process_text_file_to_excel
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import time



ids =  ["173293317", "112491980", "25653007", "69550929", "117507780", "78026333", "155217649", "43347905", "87526927", "179693049", "132262890", "32999021", "113624845", "111273603", "174161422", "81241341", "122650195", "160631990", "44531325", "68173830", "33162298", "156940744", "33835273", "158777318", "29569290", "37892015", "118004977", "73340788", "38677548", "34639369", "158315986", "115043226", "126942952", "42274845", "28726610", "82827932", "156311722", "125048652", "152588265", "73918815", "139820591", "46221602", "60893625", "54022231", "78192309", "171229974", "114444169", "118567536", "87414181", "162760599", "34529180", "85207959", "40549057", "24151771", "151893989", "87117487", "13257597", "86789799", "78312634", "20557070", "46638342", "43063684", "137072757", "129651204", "113453120", "30252548", "28561157", "78655800", "107140295", "160698684", "105427066", "16809253", "158314294", "111321113", "159455385", "140673179", "117088682", "159110311", "145733101", "47480645", "25783200", "159642180", "253649812", "42211730", "126022870", "85196954", "150930576", "12214243", "133577593", "45088671", "168615607", "48371256", "86955150", "156304370", "79993283", "31414659", "134710573", "40576829", "59443846", "111234886", "72604572", "17677949", "122790447", "174448100", "24042509", "13412119", "122955024", "101669679", "120852074", "106856305", "143085256", "117979484", "32075459", "84044106", "23037757", "114408701", "137444451", "45011012", "60583507", "45028701", "111997524", "68676949", "40502437", "24638660", "78524279", "37892015", "174448100", "174161422", "168615607", "166128512", "126022870", "108391814", "167816099", "51823417", "84328426", "126740505", "15920838", "13294517", "41375940", "42563106", "119477669", "57510828", "84227644", "23520109", "134139641", "12214243", "169068574", "151946902", "35683010", "142079169", "68260850", "75556399", "28084135", "115371619", "71236152"]
surnames = ["ABRAHAMS", "ALEXANDER", "ANTHONY", "APPELS", "ARENDS", "BAADJIES", "BESTENBIER", "BOTHA", "BREDAAR", "CHAUKE", "DANTILE", "DAS", "DE GOEDE", "DE VILLIERS", "DELA", "DIEDERICKS", "DUNA.", "DYANTYI", "FARAO", "FARO", "FEMBERS", "FIELIES", "FILANDER", "FREDERICKS", "GILBERT", "GOSO", "GWAYAGWAYA", "HARKER", "HELDSINGER", "HOYO", "JACOBS", "JANSEN", "JOKA", "JONKERS", "JOOSTEN", "JOSIAS", "JUWELE", "KEMP", "KLAASEN", "LANGLEY", "LEE", "LESCH", "LEWIS", "LOUW", "MAARMAN", "MACHEKANYANGA", "MAJOLA", "MAKOKO", "MANEWIL", "MANGELE", "MANISI", "MATA", "MBUQE", "MDINGI", "MENTOOR", "MEZINI", "MHANA", "MICHAELS", "MNYAYIZA", "MOSANI", "MPINI", "MRAPUKANA", "MUSAPINDA", "NASE", "NDABENI", "NDELENI", "NGABA", "NGOZANA", "NGQESHEMBA", "NKECHIKA", "NKUNKA", "NODIKANA", "NTSHWAXU", "PAMA", "PEDRO", "PETERSEN", "PHILANDER", "PIETERSE", "PIETERSEN", "PIETERSEN", "PLAATJIE", "PONI", "ROBERTSON", "ROUBAIN", "RUDOLF", "SAKAWULI", "SALIMU", "SALVESTER", "SAMSON", "SAMUELS", "SCHEEPERS", "SHOBA", "SKIPPERS", "SKIPPERS", "SMITH", "SMITH", "SOBEKWA", "SODINGA", "STELLENBOOM", "STRUIS", "STUART", "SWARTS", "SWARTZ", "TENGO", "TOFER", "TOKO", "VAN KERWEL", "VAN ROOYEN", "VAN WYK", "VAN ZYL", "VERMEULEN", "WILLIAMS", "WILLIAMS", "WYNGAARDT", "ZENZILE", "ZVINGANA", "DIEDERICKS", "DOLF", "JANTJIES", "KHATSHANE", "MAKHUTU", "MANUEL", "VAN WYK", "WILKONSON", "WILLIAMS", "GOSO", "TENGO", "DELA", "SCHEEPERS", "SONTASHE", "RUDOLF", "XHEGO", "COLVILLE", "BUYS", "SONDLO", "WILLIAMS", "VALENTINE", "MVUKUZO", "DAVIDS", "MBENYANA", "LINTNAAR", "KLAASE", "MAARMAN", "SAMUELS", "CLAASEN", "SALVESTER", "NYELEKA", "NCUBE", "STERRIS", "TOYISI", "KOCK", "MICHAELS", "MXAKA", "KAWADZA", "FRANS"]
    
def write_to_file(patient_id, surname):
    with open("fault_patients.txt", "a") as file:
        file.write(f"Patient ID: {patient_id}, Surname: {surname}\n")

def run_scraper():
    try:
        # Setup Selenium WebDriver
        

        # Update your Chrome WebDriver initialization with these options
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # Navigate to the website
        website = 'https://trakcarelabwebview.nhls.ac.za/trakcarelab/csp/system.Home.cls#/Component/SSUser.Logon'
        driver.get(website)

        # Wait for the login page elements
        wait = WebDriverWait(driver,300)
        username_id = "SSUser_Logon_0-item-USERNAME"
        password_id = "SSUser_Logon_0-item-PASSWORD"
        username_element = wait.until(EC.presence_of_element_located((By.ID, username_id)))
        password_element = wait.until(EC.presence_of_element_located((By.ID, password_id)))

        # Enter the credentials
        username_element.clear()
        username_element.send_keys(username)
        password_element.clear()
        password_element.send_keys(password + Keys.ENTER) 
        ## This is where the credentials are send. If the credentials are wrong there will be an error at STEP 1

        # Add your scraping logic here
        # For demonstration, let's wait for a new page element that indicates a successful login
        length_array = len(ids)
        for i in range(0, length_array):
                try:
                    id = ids[i]
                    surname = surnames[i]
                    print(str(i)  + ' out of 154 : ' +  surname + ' ' +  id)

                    
                    surname_id="web_DEBDebtor_FindList_0-item-SurnameParam"
                    surname_element = wait.until(EC.presence_of_element_located((By.ID,surname_id)))
                    surname_element.clear()

                    surname_element.send_keys(surname)

                    
                    record_id = "web_DEBDebtor_FindList_0-item-HospitalMRN"
                    record_element = wait.until(EC.presence_of_element_located((By.ID, record_id))) ## STEP 1 - IF THIS COMPONENT YIELDS TRUE THEN AUTHETICATION Is right
                    record_element.clear()

                    record_element.send_keys(id + Keys.ENTER) 

                    wait = WebDriverWait(driver,60)
                    
                    testing_id = "web_DEBDebtor_FindList_0-row-0-item-Episodes" ## STEP - IF THIS COMPONENT YIELDS TRUE then both patient and record ID are correct.
                    testing_element =wait.until(EC.element_to_be_clickable((By.ID, testing_id)))
                    wait = WebDriverWait(driver,300)

                
                    rows = driver.find_elements(By.XPATH, '//md-icon[starts-with(@id, "web_DEBDebtor_FindList_0-row-")]')
                    num_of_labs = len(rows)

                    # print("Number of rows:", num_of_labs)

                    if num_of_labs == 0:
                        print(f"Error: Failed to to find patient records: " + str(id))
                        write_to_file(id, surname)

                    else:

                        ## Figure out how many labs the patient has had
                        
                        textfile_content = ''


                        for index, row in enumerate(rows):
                            textfile_content = textfile_content + "\n"+  'Lab: ' + str(index+1) 

                            dropdown_id = "web_DEBDebtor_FindList_0-row-"+ str(index) +"-item-Episodes" ## STEP - IF THIS COMPONENT YIELDS TRUE then both patient and record ID are correct.
                            dropdown_element =wait.until(EC.element_to_be_clickable((By.ID, dropdown_id)))
                            dropdown_element.click()


                            more_action_id = "web_EPVisitNumber_List_"+str(index)+"_0-row-0-misc-actionButton"

                            # Wait for the PDF element to be clickable
                            more_action_element  = wait.until(EC.element_to_be_clickable((By.ID, more_action_id)))
                            
                            # Click the PDF element to trigger the download
                            more_action_element.click()

                            cumulative_history_id = "tc_ActionMenu-link-CumulativeHistory"
                            
                            # Wait for the PDF element to be clickable
                            
                            cumulative_history_element  = wait.until(EC.element_to_be_clickable((By.ID, cumulative_history_id)))
                            
                            # Click the PDF element to trigger the download
                            cumulative_history_element.click()

                            ## Waiting for the Page to load
                            history_page_id = 'web_EPVisitTestSet_CumulativeHistoryView_0-header-caption'
                            history_page_element = wait.until(EC.presence_of_element_located((By.ID,history_page_id)))
                            history_page_element.click()


                            # Perform 'Ctrl+A' to select all content
                            time.sleep(5) ####### THIS NEEDS TO BE CHANDED AND CHECKS FOR PRESENCE FOR TINGS
                            action = ActionChains(driver)
                            action.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()

                            # Perform 'Ctrl+C' to copy the selected content
                            action.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()

                            # Use Pyperclip to access the copied content from the clipboard
                            copied_content = pyperclip.paste()
                            textfile_content = textfile_content+ "\n" + copied_content

                            driver.back()
                    
                            dropdown_id = "web_DEBDebtor_FindList_0-row-"+ str(index) +"-item-Episodes" ## STEP - IF THIS COMPONENT YIELDS TRUE then both patient and record ID are correct.
                            dropdown_element =wait.until(EC.element_to_be_clickable((By.ID, dropdown_id)))
                            dropdown_element.click()
                
                                
                    # Specify the path for your output text file
                        output_file_path =  "textfiles\\" +   id +  '.txt'

                        # Open the file in write mode and write the copied content to it
                        with open(output_file_path, 'w', encoding='utf-8') as file:
                            file.write(textfile_content)

                        print(f"Content successfully copied to {output_file_path}")
                        
                        process_text_file_to_excel(output_file_path,id)

                        home_id = "tc_NavBar-misc-homeButtonIcon"
                        home_element  = wait.until(EC.element_to_be_clickable((By.ID, home_id)))
                        home_element.click()
                        
                except:
                    print("Problems with Patient")
                    write_to_file(id, surname)


        return True  # Return True to indicate success
    except Exception as e:
        print(f"Problems with the scrapper: {e}")
        write_to_file(id, surname)

        # driver.quit()  # Ensure the driver is closed in case of error
        return False  # Return False to indicate failure

run_scraper()
