import argparse
import os
import json
import shutil
import string
import random

def main(params):
	image = params['image']
	image_name = os.path.basename(image)
	print("Generating unique id for image")
	folder_id = id_generator()
	print(folder_id)
	if not os.path.isdir('auto/'+ image_name):
   		os.makedirs('auto/'+ folder_id) # Create new (temporary) directory for image
   		print("Creating folder for image and related data")
   		shutil.copy2(image, 'auto/'+ folder_id) # Copy original image to new directory
   		
	
	print("Running py_caffe_feat_extract.py to extract VGG features from image")
	os.system('python py_caffe_feat_extract.py --model_def_path model_def.prototext --model_path VGG_model.caffemodel -i auto/' + folder_id + ' -o auto/' + folder_id)
	print("Finished running feature extraction, creating tasks.txt")
   	file = open('auto/'+ folder_id + "/tasks.txt", "w")
	file.write(image_name)
	file.close()
	print("Now running prediction script")
	os.system('python predict_on_images.py -r  auto/' + folder_id + ' cv/model_checkpoint_flickr8k_NeuralTalk_baseline_16.93.p')
	print("Finished running image prediction. The URL is auto/" + folder_id + "/result.html")


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))


if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument('image', type=str, help='the image to generate a caption for')

  args = parser.parse_args()
  params = vars(args) # convert to ordinary dict
  print 'parsed parameters:'
  print json.dumps(params, indent = 2)
  main(params)
