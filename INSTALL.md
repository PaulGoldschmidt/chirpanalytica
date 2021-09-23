# Chirpanalytica

## Installation instructions
### Version 0.9 (September 2021)
Tested for Python 3.8.5 (64-bit)
If you want to host this project yourself, please make the changes in the code open-source for transparency reasons (a political project like chirpanalytica can be used for evil if the changes in code are kept secrect). See the [License](LICENSE) file for details.

### Requirements for installation
All scripts should be called from-directory, not with absulute paths: first go into the desired directory and then start the script/file, because of the use of relative paths throughout the project.
#### Obtaining API-Keys
For any interaction with the Twitter-API, you first have to obtain API-Keys and put them into a file called "twittercredentials.json" (located in backend/, see [example file](backend/twittercredentials.json.example) for the structure). For obtaining API-Keys, see the [Twitter Developer Documentation](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api) for help.
#### Ports used in this project
Used ports (all specifically Cloudflare-compatible): 443 (webserver ssl), 2096 (public python backend (flask), served by waitress)
#### Software requirements
- Python 3.8.5 and above
- Webserver (Nginx highly recommended)
- If you want to train the model yourself: Installed python dependencies from backend/training/requirements.txt (pip install -r requirements.txt)
- Install the python dependencies from backend/api/requirements.txt (pip install -r requirements.txt)
#### Folder structure
If you don't want to use this recommended folder structure, be sure to change the paths in 

### Setting Chirpanalytica up: Training the model
You can skip this step by downloading the currently used and pretrained model by downloading it from 