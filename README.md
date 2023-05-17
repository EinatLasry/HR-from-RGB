# HR-from-RGB
# Integration between open source codes
# Einat Lasry & Yaniv Shnur, Under the direction of Hagit Hel Or, Haifa University 08/2021

Goal: extract a pulse rate from RGB videos.
Since there are a lot of codes on the Internet that calculate the heart rate, our goal was to create a combined code that could calculate the heart rate by integrating the methods.

After writing the code, we changed the parameters and calculated statistics on the data we received in Excel.
We tried different techniques and improved the code according to the results.
![image](https://github.com/EinatLasry/HR-from-RGB/assets/82314695/2c1c0665-f103-4613-818c-ca45812f0c7d)

We used 5 different areas of the face, and calculated how much weight it is recommended to give to each area to achieve an optimal result.
![ROIS_EINAT](https://github.com/EinatLasry/HR-from-RGB/assets/82314695/60858dad-32c1-4acb-b442-0cb6e30a22f7)

Part of the DATA was "training", meaning we drew the conclusions from it.
A small part of the DATA was "test", meaning we tested our code on it.
![image](https://github.com/EinatLasry/HR-from-RGB/assets/82314695/c877cef4-e480-419a-a1ec-3aaa139b7f95)
![image](https://github.com/EinatLasry/HR-from-RGB/assets/82314695/c2e8b207-7f54-4dcc-8f1b-b3590a734530)

# The process
We use face detection algorithm, weighting of different areas on the face, FFT, Band pass filter, peak detection, and calculate the BPM.

# Source codes:
