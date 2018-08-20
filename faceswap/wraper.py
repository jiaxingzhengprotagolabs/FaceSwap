#!/usr/bin/env python3
""" The master faceswap.py script """
import sys
from scripts.convert import Convert as script
import arg as arg
import os 
import shutil
from subprocess import call

if sys.version_info[0] < 3:
    raise Exception("This program requires at least python3.2")
if sys.version_info[0] == 3 and sys.version_info[1] < 2:
    raise Exception("This program requires at least python3.2")



#%%
def delete_file(file_dir):
    if os.path.exists(file_dir):
        try:
            os.remove(file_dir)
            print('Old face alignment file deleted, creating a new one now.')
        except:
            print ("Error: {}.".format(file_dir))
    else:  
        print("No alignment found, creating a new face alignment.json file")



def train(images_A_dir, images_B_dir,face_detect_dir,model_dir,epochs=100,extract=True):

    # To convert image a:
    extract_dir_a = os.path.join(face_detect_dir, 'A')
    cmd_a = ['python', 'faceswap.py', 'extract', '-i', images_A_dir, '-o', extract_dir_a,'-l','0.8']

    

    # To convert image b:
    extract_dir_b = os.path.join(face_detect_dir, 'B')
    cmd_b = ['python', 'faceswap.py', 'extract', '-i', images_B_dir, '-o', extract_dir_b,'-l','0.8']
    


    ## starting training 
    cmd = ['python', 'faceswap.py', 'train', '-A',extract_dir_a, '-B', extract_dir_b, '-m', model_dir,'-it', str(epochs),'-v','-w']
    ##cmd = ['python', 'faceswap.py', 'train', '-A',extract_dir_a, '-B', extract_dir_b, '-m', model_dir,'-ep', str(epochs),'-v','-w']
    

    ## go on to train the exist model is extract == false
    if extract:
        ## reload new images and train the new model
        # delete_file(extract_dir_a)
        # delete_file(extract_dir_b)
        status = call(cmd_a)
        status = call(cmd_b)

        # delete_file(model_dir)
    
    status = call(cmd)
    
    return status



def extract_img(images_dir, extract_img_dir):
    
    cmd = ['python', 'faceswap.py', 'extract', '-i', images_dir, '-o', extract_img_dir,'-l','0.8']
    status = call(cmd)
    print(status)

def convert_img(images_dir, extract_img_dir, output_dir, model_dir):
    alignment_dir = os.path.join(images_dir,'alignments.json')
    if not os.path.exists(alignment_dir):    
        extract_img(images_dir, extract_img_dir)

    cmd = ['python', 'faceswap.py', 'convert', '-i', images_dir, '-o', output_dir, '-m', model_dir, '-S']
    status = call(cmd)
    print(status)

        

## extract only keypoint of the vedio from the original vedio
## our program will only use the keypoint vedio for faceswap
def extract_keypoint_frame(reference_video, keypoint_video):
    cmd = ['ffmpeg', '-i', reference_video, '-strict', '-2', '-qscale', '0', '-intra', keypoint_video]
    status = call(cmd)
    print(status)
    
## ioslate the audio from the keypoint vedio
def ioslate_audio(keypoint_video, audio_file):
    cmd = ['ffmpeg', '-i', keypoint_video, '-f', 'mp3', audio_file]
    status = call(cmd)
    print(status)


def process_vedio(reference_video,keypoint_video, audio_file):
    if reference_video:
        extract_keypoint_frame(reference_video, keypoint_video)

    if keypoint_video:
        ioslate_audio(keypoint_video, audio_file)

## generate frame images from keypoint vedio
def gen_img_from_vedio(reference_video, vedio_img_dir, train=True):
    fps = 1
    if train:
        cmd = ['ffmpeg', '-i', reference_video, '-r', str(fps), './' + vedio_img_dir + '/frame%d.png'] 
    else:
        cmd = ['ffmpeg', '-i', reference_video, './' + vedio_img_dir + '/frame%d.png']
    status = call(cmd)
    print(status)



## generate vedio from the images which are swaped successfuly
def gen_swap_vedio(extract_dir_swap, audio_file, gen_vedio, backup=True):
    ## some vedio needs to change its PTS to make sure their audio and generated vedio match
    if backup == True:
        cmd = ['ffmpeg', '-i', extract_dir_swap + '/frame%d.png', '-i', audio_file, '-c:v', 'libx264', '-vf', "fps=30,format=yuv420p,setpts=0.833333333*PTS", gen_vedio]
    
    else:
        cmd = ['ffmpeg', '-i', extract_dir_swap + '/frame%d.png', '-i', audio_file, gen_vedio]
    
    status = call(cmd)
    print(status)


#%%
#cmd =['python', 'tools.py', 'effmpeg', '-a','gen-vid', '-i', './data/test_images/video_out', '-r', './data/test_images/input_trump_short.mp4','-o', './data/test_images/out_trump_short.mp4', '-fps','-1','-m']
#call(cmd)
#%%
