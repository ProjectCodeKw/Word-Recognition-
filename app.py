import streamlit as st
from streamlit_extras import add_vertical_space as avs
from st_audiorec import st_audiorec
from computation import Computation
import random

def get_session_state():
    if 'cap' not in st.session_state:
        cap = generate_capatcha()
        st.session_state.cap = cap

    return st.session_state.cap


def generate_capatcha():
    media = ['yes', 'no']
    capatcha = random.choice(media)
    return capatcha.upper()


def demo_app():
    cap = get_session_state()
    st.image(f'capatcha/{cap.lower()}.png')

    st.title("DSP Captcha Test")
    st.markdown("**:green[⚠️ Before you login we need to make sure you are a human!]**")
    st.markdown('---')
    avs.add_vertical_space(1)
    st.subheader("Using the following recorder say the word that you see: ")

    wav_audio_data = st_audiorec() 

    if wav_audio_data is not None:
        st.audio(wav_audio_data, format='audio/wav') #- WAV, 16 bit, 44.1 kHz

    avs.add_vertical_space(1)

    try:
        if wav_audio_data is not None:
            filename = 'input.wav'
            comp = Computation()

            # Write the bytes to a file in binary mode
            with open(filename, 'wb') as f:
                f.write(wav_audio_data)

            sample_rate, data = comp.adjust_wav_file(filename)
            word = comp.test(sample_rate, data, plot=False)
            # Compute energy for each frequency bin
            avs.add_vertical_space(2)
            if word == cap:
                st.header(":green[✅ CORRECT! welcome human.]")
                avs.add_vertical_space(1)
                st.subheader("Plotting the FFT")
                comp.test(sample_rate, data, plot=word)
            elif word != cap:
                st.header(":red[❌ WRONG! you must be a robot..]")
                st.markdown("Try again by refreshing th epage.")
                
            #st.write("You said:", word)
            #st.write("Correct answer:", cap)
    except ValueError: pass


def streamlit_app():
    st.header("Word Recognition using FFT & Elliptic BPF")
    st.subheader("The app can recognize the words :green['YES'] & :red['NO']")
    avs.add_vertical_space(1)
    st.markdown('---')

    st.subheader("Follow these steps:")
    st.markdown("**1. Press the 'Start Recording' button**")
    st.markdown("**2. Press the 'Reset' button**")
    st.markdown("**3. Press the 'Start Recording' button**")
    st.markdown("**4. Record yourself saying :green[yes] or :red[no]**")
    st.markdown("**5. Press the 'Stop' button**")
    st.markdown("**6. Press the 'Download' button**")
    st.markdown(":green[For better results make your recording shorter than 2 seconds.]")
    avs.add_vertical_space(1)

    wav_audio_data = st_audiorec() 

    if wav_audio_data is not None:
        st.audio(wav_audio_data, format='audio/wav') #- WAV, 16 bit, 44.1 kHz

    #st.markdown("**7. Upload the downloaded .wav file below**")
    avs.add_vertical_space(1)

    if wav_audio_data is not None:
        filename = 'input.wav'
        comp = Computation()

        # Write the bytes to a file in binary mode
        with open(filename, 'wb') as f:
            f.write(wav_audio_data)

        st.markdown("---")
        avs.add_vertical_space(1)
        sample_rate, data = comp.adjust_wav_file(filename)
        word = comp.test(sample_rate, data)
        # Compute energy for each frequency bin
        st.markdown('---')
        avs.add_vertical_space(2)
        st.subheader("**Results After Proccessing The Energy**")
        if word == 'YES':
            st.header("The user said: :green[YES]")
        elif word == 'NO':
            st.header("The user said: :red[NO]")


st.set_page_config('Word Recognition', page_icon='🔊', layout='centered')
#streamlit_app()
demo_app()


