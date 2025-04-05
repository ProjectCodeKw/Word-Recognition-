# DSP Word Recognition Streamlit APP
## Description
This project utilizes the functionalities of bandpass filters and the frequency domain energy formula for a given audio signal to differentiate between words. The computation in this project is done in the frequency domain after converting the signal from the time domain using the Fast Fourier Transform (FFT) on the signal. The algorithm is then used in a simple Captcha security model on a webpage.
For further details check the report PDF file.

## Installation
1- to run this code through the demo website download these libraries:

`pip install streamlit`

`pip install streamlit-extras`

`pip install numpy`

`pip install streamlit-audiorec`

`pip install pyaudio`

`pip install matplotlib`

2- Check the installation for the libraries
   
run the following command for all the libraries you just installed:
   
`library_name --version`
   
**If you got an error it means the library was not installed correctly**
   
*a video that might help you install streamlit if this problem occured:*
   
--> https://youtu.be/Uloc4Z0SUks?si=KZmxrbT8ycPoyK7q

3- Through ur favourite terminal type the following command to run the website on ur local host

`streamlit run app.py`

## REFERENCES:
https://github.com/stefanrmmr/streamlit-audio-recorder
