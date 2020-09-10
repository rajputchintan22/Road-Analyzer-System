# import os
# from PIL import Image
# for filename in os.listdir("D:\\Manan\\04_Amorphous\\"):
#     execution_path = "D:\Manan\\04_Amorphous\\"
#     image_obj = Image.open(execution_path + filename)
#     new_image = image_obj.resize((131, 131))
#     Save_path = 'D:\Manan\\Amorphous\\'+filename[:-4]+'.tiff'
#     new_image.save(Save_path, 'TIFF', compression='None')

# import pydicom as dicom
# import os
# import cv2
# import PIL # optional
# # make it True if you want in PNG format
# PNG = False
# # Specify the .dcm folder path
# folder_path = "D:\Manan\d"
# # Specify the output jpg/png folder path
# jpg_folder_path = "D:\Manan\l"
# images_path = os.listdir(folder_path)
# for n, image in enumerate(images_path):
#     ds = dicom.dcmread(os.path.join(folder_path, image))
#     pixel_array_numpy = ds.pixel_array
#     if PNG == False:
#         image = image.replace('.dcm', '.jpg')
#     else:
#         image = image.replace('.dcm', '.png')
#     cv2.imwrite(os.path.join(jpg_folder_path, image), pixel_array_numpy)
#     if n % 50 == 0:
#         print('{} image converted'.format(n))