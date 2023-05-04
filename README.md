# A Desktop Interface to Create and Display Lenticular Images

## Abstract 

With the rise of micro-videos (as seen on TikTok, Instagram Reels, or Youtube Shorts), sharing videos with friends and family across platforms feels like an increasingly common past-time of online users. Despite the prevalence of these videos, almost all sharing methods stay within the digital realm. My senior project proposes an analog alternative to the digital reign of video sharing these bite-sized videos. 

By utilizing lenticular images (motion cards), online users can benefit from an “older” technology to create physical DIY lenticular prints. The project is a GUI interface that allows users to upload images they wish to manipulate into an appropriate lenticular image that will become print-ready. The interface walks the user through a step-by-step process: upload, set settings, crop, and interlace. These four steps will use the provided settings for lenticular lens width and printer resolution to crop the uploaded images into their necessary size. With a specified size, the uploaded images will run through the ImageSelection algorithm. Here the algorithm slices the images into rectangular strips that interweave each other and form the final lenticular image. The image downloads onto your device for the user to send to the printer. Finally, by placing the printed photo into a specific photo frame with a lenticular lens cover, the image “animates” and creates the illusion of motion. 

The entire code operates on Python, as I took advantage of the existing Pillow Imaging package and the PySide GUI class. As for testing, the final product of the lenticular print came from an Epson XP6100 with 4x6 photo glossy paper. Any future iterations of the project would add more GUI functionality and populate a working virtual recreation of an interlaced image.

## Getting Started

### Dependencies

Pillow Package (Image, ImageDraw), Sys, OS, Random, Math
Python program has only run on Windows 11 PyCharm 2022.3.2

### Installing

Main.py is the only file necessary to run the lenticular image creator
GUI located in app.py, but not complete as of 5/4/23

### Executing program
 
To execute the program please provide the follow command line arguments:
python main.py [image 1] [image 2] [image 3] [desired DPI] [ LPI ]

where DPI stands for the printer resolution and LPI stands for the lenticulars per inch 
of the lenticular sheet


## Authors
Angelica Pelcatre
ex. [@angelica_pelcastre](https://www.instagram.com/angelica_pelcastre/)

## Version History

* 1.0
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments
Thank you to my advisor Dr. Alan Weide and all CPSC 490 admin
