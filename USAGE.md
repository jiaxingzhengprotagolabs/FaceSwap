
# Workflow of faceswap: A(face) to B(face)

## 需要用到的函数封装在 wraper.ps里，可以直接引入该模块
1. 用户需要首先上传文件, 可以是任意四种组合
```
a. A 图片 + B 图片
b. A 图片 + B 视频
c. A 视频 + B 图片
d. A视频 + B 视频
上传的所有视频需要用函数 gen_img_from_vedio(reference_video, vedio_img_dir, train=True):生成图片
reference_video 用户上传的视频
vedio_img_dir 生成图片的目录
train=True 当作为训练集的输入图片时，设为True, 表示每秒一帧，视频有多少妙就生成多少图片。默认是False，
表示按照视频原有的的fps生成图片，用于对视频中的人换脸。

```
2. 根据用户上传的文件，得到A， B图片组（数量可以不一致）训练模型
```
调用函数train（imageA_dir, imageb_dir, face_detect_dir, model_dir, epochs = 10000, extract=True）
其中， imageA_dir, imageB_dir分别代表用户上传的两组图片，face_detect_dir 是有图片生成的识别脸部的图片文件夹， 
model_dir是存放训练好的参数, epochs是训练循环次数，默认情况下是10000，extract是一个判断是否需要重新生成新的模型

train函数里，如果要重新生成新的模型的参数，需要首先分别生成的识别脸部的图片A‘ 和 B’， 
生成之后会在原 A， B 文件夹内生成一个alignment.json的文件，用于训练时获取图片和换脸时获取图片。
每一张图片对应json文件中的一部分，如果该图片的参数没有写入json文件，则后续函数进行训练和换脸时获取不到该图片

```
3. 训练结束后，得到models里的参数模型，就可以用来换脸了。
```
a. 对于只换图片的用户，可以直接调用函数 convert_img(images_dir, extract_img_dir, output_dir, model_dir):

images_dir 是用户上传的图片所在文件夹，也可以是新上传的,也可以是原来的文件夹，但是新的和旧的必须分别在不同文件夹。 
extract_img_dir 是图片生成的识别脸部的图片文件夹
output_dir 是换脸成功的图片所在文件夹
model_dir 是模型参数所在的文件夹
```

```
b. 对于需要换视频的用户，需要先对上传的视频作预处理 
调用函数  process_vedio(reference_video,keypoint_video, audio_file):
reference_video 用户上传的视频
keypoint_video 处理得到的仅带关键帧的视频
audio_file 分离出来的视频中的音频
```

```
c. 将关键帧视频变成图片，每一帧一张， 然后将这些帧生成的图片换脸
调用 gen_img_from_vedio 函数， train==False 得到由视频生成的图片
调用convert_img 生成换脸图片组
```

```
d.最后将换脸后的图片还原成视频
最后调用函数 gen_swap_vedio(extract_dir_swap, audio_file, gen_vedio, backup=True)
extract_dir_swap 是视频生成的图片换脸后的图片目录
audio_file  是需要换脸视频的音频
gen_vedio  最后生成的视频名字（可以任意取名字 如 out.mp4）
backup  当生成的视频和音频不同步的时候，将backup设为false，重新生成视频
```



