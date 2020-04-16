import os, sys, time as t, logging as log, PySimpleGUI as sg

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
# chrome_options.add_argument("--start-maximized")
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

	def dates(self, value):
		b = self.b
		b.find_element_by_id("PublicationDate").send_keys(value)
		b.find_element_by_id("LiveDate").send_keys(value)
		t.sleep(1)

	def additional_info(self, award):
		b = self.b
		i = b.find_element_by_id('AdditionalInformation')
		v = i.get_attribute('value') # get existing info
		i.clear()
		l.info('existing info - ' + v) 
		i.send_keys(award + ', ' + v) # append award and strip existing Shortlisted if present
		l.info('appending - ' + award)
		n = b.find_element_by_id('AdditionalInformation').get_attribute('value')
		l.info('new info - ' + n)

##################### Generate Bullets ########################

def generate_bullets_window(cms):
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

	while True:
		event, values = window.read()

		if event in ('Cancel', None):
			break

		if event == 'Submit':
			try:
				IDs_input = values[0]
				IDs = IDs_input.strip().split('\n')

				for ID in IDs:
					# checks ID is 6 digits
					if len(ID) == 6:
						l.info(f'-> editing {ID}')
						cms.edit(ID)
						t.sleep(1)
						cms.bullets()
						t.sleep(1)
						# cms.save()
						# t.sleep(1)
						sg.popup('Generated bullets for IDs:', IDs_input)
					else:
						l.info('- ID was not 6 digits long')
						sg.popup('ID needs to be 6 digits long')
	
			except Exception as e:
				l.error(e)
				sg.popup('An error occured, please see log file.')

	window.close()


######################## Change Metadata ############################

def change_metadata_window(cms):

	sg.theme('DarkGreen') 
	layout = [
		[sg.Text('Paste a column of IDs and select the status of entries')],
		[sg.Text('IDs'), sg.InputText()],
		[sg.Frame(layout=[
		[sg.Radio('Shortlisted', 'RADIO1'), sg.Radio('Entrant', 'RADIO2')]], title='Status',title_color='green', relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags')],
		[sg.Submit(), sg.Cancel()]
	]

	window = sg.Window('Change Metadata', layout)    
	
	while True:
		event, values = window.read()

		if event in ('Cancel', None):
			break

		if event == 'Submit':
			IDs_input = values[0]
			IDs = IDs_input.strip().split('\n')

			try:
				IDs_input = values[0]
				IDs = IDs_input.strip().split('\n')

				for ID in IDs:
					# checks ID is 6 digits
					if len(ID) == 6:
						l.info(f'-> editing {ID}')
						cms.edit(ID)
						t.sleep(1)

############## [cms.dates() if x > 1 else pass]

############## [cms.additional_info() if RADIO1,  elif RADIO2..]

						# t.sleep(1)
						# cms.save()
						# t.sleep(1)
						sg.popup('Changed metadata for IDs:', IDs_input)
					else:
						l.info('- ID was not 6 digits long')
						sg.popup('ID needs to be 6 digits long')
				
			except Exception as e:
				l.error(e)
				sg.popup('An error occured, please see log file.')

	window.close()

######################## Main Window ############################

def main():

	sg.theme('DarkBlue') 

	layout = [
		[sg.Text('Choose a script: ')],
		[sg.Button('Bullets'), sg.Button('Metadata')],
		[sg.Exit()]
	]

	window = sg.Window('CMS Bot', layout)

	cms = CMSBot()

	while True:
		event, values = window.read()
		if event in ('Exit', None):
			break

		if event == 'Bullets':
			try:
				generate_bullets_window(cms)
			except Exception as e:
				l.error(e)

		if event == 'Metadata':
			try:
				change_metadata_window(cms)
			except Exception as e:
				l.error(e)

	cms.b.quit()
	l.info('- exited browser correctly')

	window.close()

if __name__ == '__main__':
	main()