import requests, json
import getopt, sys
import pandas as pd
from imagga_tag.tagging import upload_imagga, tag_imagga, delete_imagga
from esql_db.insert_data_tables import connect_db, read_insert_data_into_tables, report_table_recs

# Sequence of steps:
## 1. Set-up the database table - DONE
## 2. Generate the tags
## 3. Save the tags 

	
def main(argv):
        try:
                opts, args = getopt.getopt(argv,"i:", ["image="]) 
	except getopt.GetoptError:
                print ('Usage: python main.py --image=<image_path>')
                sys.exit(2)
        req_options = 0
	for opt, arg in opts:
                       if opt == '--image':
                               t_image = arg
                               req_options = 1

        if (req_options == 0):
                print ('Usage: python tagging.py --image=<image_path>')
                sys.exit(2)
                        
	# Upload the image 
        print('Uploading image to Imagga: ', t_image)
	upld_id = upload_imagga(t_image)
	
	# Tag the image 
	print('Tagging the image:')
	tags_json = tag_imagga(upld_id)

	## Parse the tags and create a dataframe
	num_tags = len(tags_json['result']['tags'])
        tags_to_print = min(num_tags,5)
	image_n = [t_image]*tags_to_print
	tags_v = []
	confidence_v = []
        #print ('\t Top tags (confidence score):')
	for i in range(tags_to_print):
                tags_v.append(str(tags_json['result']['tags'][i]['tag']['en']))
		confidence_v.append(round(tags_json['result']['tags'][i]['confidence'],1))       
        
	columns = ["image_name","tag", "confidence"]
 	data = {'image_name':image_n,'tag':tags_v,'confidence':confidence_v}
	df = pd.DataFrame(data=data, columns=columns)
       
	# Delete the image
        print('Deleting image from Imagga:')
	delete_imagga(upld_id)

        # Write the tags to a file
	df.to_csv('imagga_tag/tags.csv', index=False,header=False)		

        # Upload the tags into the database table image_tags
        read_insert_data_into_tables(['image_tags'],['imagga_tag/tags.csv'])
	
if __name__ == "__main__":
   main(sys.argv[1:])
