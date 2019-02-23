# audiophile
Create audio datasets for ML/DL projects by scrapping [FreeSound](https://freesound.org/)! (don't tell anyone...) 🤫


### What is it?

audiophile let you scrape audio files from [FreeSound](https://freesound.org/) directly without asking for API keys or manually browsing files. It is intended to be used for building audio datasets for deep learning projects with minimum effort.

### How to use

* Install dependencies by running the `requirements.txt` file with _pip_: `pip install -r requirements.txt`. Doing this in a _virtualenv_ will minimize disruption to other projects.

* Set your scraping parameters in the `config.json` file:
    * `query_type`: Choose how to query the audio store, either by setting as _search_ (regular search) or _tags_ (search by a tag).
    * `query`: The value for the query (_cars_, _birds_, _conversations_, etc.).
    * `format`: Filter the audio formats to be downloaded (_mp3_, _wav_, etc.).
    * `auth`: Cookies values from an active session in [FreeSound](https://freesound.org/), I recommend that you use the [Cookies](https://chrome.google.com/webstore/detail/cookies/iphcomljdfghbkdcfndaijbokpgddeno?hl=en) extension to get them, these are used for requests validation only.

* Run the `scraper.py` file.

* Your data and cached pages will be downloaded at the _data_ folder.

### Coming soon (maybe not)

* Maximum audio file size filter
* Maximum audio duration filter
* Pack download

**We are open for pull requests!**

### Licence

MIT, attribution is appreciated but not required.
