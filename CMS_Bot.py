import os, sys, time as t, logging as log, PySimpleGUI as sg

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument('--headless')

# SETUP LOGGING
def setup_custom_logger(name):
    fm = log.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%d-%m-%Y %H:%M:%S')
    h = log.FileHandler(name, mode='w')
    h.setFormatter(fm)
    sh = log.StreamHandler(stream=sys.stdout)
    sh.setFormatter(fm)
    l = log.getLogger(name)
    l.setLevel(log.DEBUG)
    l.addHandler(h)
    l.addHandler(sh)
    return l

l = setup_custom_logger(__file__ + '.log')

# set relative path for chromedriver executable file, otherwise its not on other user's system PATH
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

##################### Bot Commands ########################

class CMSBot:
	def __init__(self):
		self.b = webdriver.Chrome(options=chrome_options, executable_path=resource_path('./driver/chromedriver.exe'))

	def edit(self, ID):
		b = self.b
		url = 'http://newcms.warc.com/content/edit'
		b.get(url)
		l.info(f"requested url: '{url}'")
		b.implicitly_wait(5)
		g = b.find_element_by_name('LegacyId')
		g.clear()
		g.send_keys(ID)
		g.send_keys(Keys.RETURN)
		t.sleep(1)

	def save(self):
		b = self.b
		b.find_element_by_xpath('//span[@onclick="onSaveClicked()"]').click()
		l.info('Saved changes')
		t.sleep(2)

	def bullets(self):
		b = self.b
		b.find_element_by_link_text('Summary').click()
		l.info("clicked [Summary] (Expand)")
		b.find_element_by_id('GenerateBullets').click()
		l.info("clicked [Generate Bullets]")
		t.sleep(1)

	def dates(value):
		b = self.b
		b.find_element_by_id("PublicationDate").send_keys(value)
		b.find_element_by_id("LiveDate").send_keys(value)
		t.sleep(1)

##################### Generate Bullets ########################

def generate_bullets(cms, IDs):
	'''Just needs a list of IDs in the CSV column ID'''

	for ID in IDs:
		# checks ID is 6 digits
		if len(ID) == 6:
			l.info(f'-> editing {ID}')
			cms.edit(ID)
			t.sleep(1)
			cms.bullets()
			t.sleep(1)
			# cms.save()
		else:
			l.info('- ID was not 6 digits long')

def generate_bullets_window():
	'''
	# INSTRUCTIONS
	- all you do is paste a column of IDs into the input field
	- the script will automatically generate the IDs in the cms
	- our cms can only be accessed through vpn
	'''
	sg.theme('DarkAmber') 
	layout = [[sg.Text('Paste a column of IDs below:')],
										[sg.InputText()],
										[sg.Submit(), sg.Cancel()]]

	window = sg.Window('Generate Bullets', layout)    
	event, values = window.read()    
	window.close()

	IDs_input = values[0]
	IDs = IDs_input.strip().split('\n')

	try:
		cms = CMSBot()
		generate_bullets(cms, IDs)
		sg.popup('Generated bullets for IDs:', IDs_input)
	except Exception as e:
		l.error(e)
		sg.popup('An error occured, please see log file.')
	finally:
		cms.b.quit()
		l.info('- exited browser correctly')


######################## Live Date ############################

def change_metadata(cms, IDs):
	pass

def change_metadata_window():

	sg.theme('DarkGreen') 
	layout = [[sg.Text('Paste a column of IDs below:')],
										[sg.InputText()],
										[sg.InputText()],
										[sg.Submit(), sg.Cancel()]]

	window = sg.Window('Change Metadata', layout)    
	event, values = window.read()    
	window.close()

	IDs_input = values[0]
	IDs = IDs_input.strip().split('\n')

	try:
		# change_metadata(cms, IDs)
		sg.popup('Changed metadata for IDs:', text_input1)
	except Exception as e:
		l.error(e)
		sg.popup('An error occured, please see log file.')
	finally:
		cms.b.quit()
		l.info('- exited browser correctly')

def main():
	generate_bullets_window()
	change_metadata_window()

if __name__ == '__main__':
	main()