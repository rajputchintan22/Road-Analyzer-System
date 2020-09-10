import os
from PIL import Image
save_path = "D:\\Test\\Show2\\Final_With_Sides\\"
os.mkdir(save_path)
for filename in os.listdir("D:\Test\Show2\Final"):
    execution_path = "D:\Test\Show2\Final\\"
    image_obj = Image.open(execution_path + filename)
    width, height = image_obj.size
    cropped_image_left = image_obj.crop((0, 0, width/3, height))
    cropped_image_center = image_obj.crop((width/3, 0, 2*width/3, height))
    cropped_image_right = image_obj.crop((2*width/3, 0, width, height))
    cropped_image_left.save(save_path+filename[:-4]+'_right_.jpg')
    cropped_image_center.save(save_path+filename[:-4]+'_center_.jpg')
    cropped_image_right.save(save_path+filename[:-4]+'_left_.jpg')