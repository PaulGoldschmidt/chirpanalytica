# Chirpanalytica

## Installation instructions
### Version of this file: 1.1 (September 2021)
Tested for Python 3.8.5 (64-bit)
If you want to host this project yourself, please make the changes in the code open-source for transparency reasons (a political project like chirpanalytica can be used for evil if the changes in code are kept secrect). See the [License](LICENSE) file for details.

### Requirements for installation
All scripts should be called from-directory, not with absulute paths: first go into the desired directory and then start the script/file, because of the use of relative paths throughout the project.
#### Obtaining API-Keys
For any interaction with the Twitter-API, you first have to obtain API-Keys and put them into a file called "twittercredentials.json" (located in backend/, see [example file](backend/twittercredentials.json.example) for the structure). For obtaining API-Keys, see the [Twitter Developer Documentation](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api) for help.
#### Ports used in this project
Used ports (all specifically Cloudflare-compatible): 443 (webserver ssl), ~~2096 (public python backend (flask), served by waitress)~~.
Update with version 1.0: It is recommended to host the api access on a seperate subdomain, e.g. api.chirpanalytica.com.
#### Software requirements
- Python 3.8.5 and above
- Webserver (Nginx highly recommended)
- UNIX-Environment (tested: Ubuntu 20.04 LTS Server) to use the rest of this instruction manual
- If you want to train the model yourself: Installed python dependencies from backend/training/requirements.txt (pip install -r requirements.txt)
- Install the python dependencies from backend/api/requirements.txt (pip install -r requirements.txt)
#### Folder structure
If you don't want to use this recommended folder structure, be sure to change the hard paths in [backend/additional_resources/ca-backend.service](backend/additional_resources/ca-backend.service).

### Setting Chirpanalytica up: Training the model
You can skip this step by downloading a pretrained model from [https://de.chirpanalytica.com/pretrained.zip](https://de.chirpanalytica.com/pretrained.zip)
#### Let's train
After setting up your API-Keys and giving the file [backend/training/train.sh](backend/training/train.sh) executable rights, prepare yourself for a long time of downloading the tweets and training the model.
Basically you could just execute the train.sh-file and let the shell run for around 24 hours (21 hours of downloading around 70.000 Tweets and 3 hours of training on an AMD Epyc 7704 with four cores), although it is recommended to execute the script in background by typing "nohup train.sh &". Now you can even close the shell or log-off from the ssh-connection.
The script will firstly get the new list with all the political accounts associated to partys [(see Wikidata-Query)](https://w.wiki/47Nt), then download the last 200 tweets of every person (agelimits apply). After this went successful, the script moves foreward and trains the multi-layer perceptron classifier.
After around a day you should see the results of the training in the created /export-folder, which also contains statistics about the precision of the newly trained model. 

### Serving the project
#### The frontend
To serve the frontend, just point nginx at the index.html-file in [frontend/](frontend/).

#### The backend
Move the folder [backend/](backend/) into your srv-folder.
Getting the backend to run only requires copying the [ca-backend.service](backend/additional_resources/ca-backend.service)-file into the systemd service folder located at /etc/systemd/system/.
Now you can start the backend by running systemctl start ca-backend and then permanently enable it by typing systemctl enable ca-backend.
If everything worked (you can take a look at the service with systemctl status ca-backend), you should be able to access the backend locally on port 8879 or from the public at port 2096 (prior nginx reverse proxy-configuration required) 