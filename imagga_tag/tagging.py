import requests, json
import getopt, sys
import config_imagga

def upload_imagga(image_path):        	
	response = requests.post('https://api.imagga.com/v2/uploads',
                                 auth=(config_imagga.api_key, config_imagga.api_secret),
                                 files={'image': open(image_path, 'rb')})
        if (response.json()['status']['type'] == 'success'):
                print ('\t Upload successful')
                upld_id = response.json()['result']['upload_id']
                return (upld_id)
        else:
                print('\t Something went wrong. Exiting...')
                sys.exit(2)
        

def tag_imagga(t_image):
	response = requests.get('https://api.imagga.com/v2/tags?image_upload_id=%s' % t_image,
                                auth=(config_imagga.api_key, config_imagga.api_secret))
        if (response.json()['status']['type'] == 'success'):
            print ('\t Tagging successful')
            return(response.json())
        else:
                print('\t Something went wrong. Exiting...')
                sys.exit(2)
        

def delete_imagga(upld_id):
	response = requests.delete('https://api.imagga.com/v2/uploads/%s'
                                   % (upld_id), auth=(config_imagga.api_key, config_imagga.api_secret))
	if (response.json()['status']['type'] == 'success'):
            print ('\t Delete successful')
            return(response.json())
        else:
                print('\t Something went wrong. Exiting...')
                sys.exit(2)

