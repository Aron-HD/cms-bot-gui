
# Generate Bullet Summaries
--- 

Taking the CMSBot class from `cms_edit.py` / `cms_batch_edit.py` from CMS-bot repository and applying a lightweight GUI frontend to it. Choose a script, then paste a list of IDs into the text field and select what you want to happen instead of setting up a csv file to make it more accessible and distributable to the wider team.

### INSTRUCTIONS
- all you do is paste a column of IDs into the input field and select options
- the script will automatically interact with the IDs in the cms
- our cms can only be accessed through vpn

**To do:**
- ~~make a virtual environment with venv / pipenv~~
- ~~make requirements file~~
- ~~use py installer~~
- ~~add an icon~~
- ~~make exe include chromedriver.exe~~
- validate IDs before opening CMSBot()
- clear IDs when finished
- check bullet summary is valid and button clickable
- ~~metadata function~~
- ~~additional information: radio button / dropbox for Shortlisted or Entrant~~
- ~~Publication date~~
- ~~Live date~~
- add LICENCE file

### Screenshots

![cms-bot-bullets](https://user-images.githubusercontent.com/60329603/79757653-4b0dc680-8314-11ea-8166-80084a982523.JPG)

*CMS_Bot Generate Bullets window working with Selenium Chrome driver*

![cms-bot-metadata1](https://user-images.githubusercontent.com/60329603/79757671-4fd27a80-8314-11ea-8895-8a4301e7bd0c.JPG)

*Metadata window before entering ID/s*

![cms-bot-metadata2](https://user-images.githubusercontent.com/60329603/79757673-506b1100-8314-11ea-95dd-f3892f4deed3.JPG)

*Metadata window when ID/s entered*