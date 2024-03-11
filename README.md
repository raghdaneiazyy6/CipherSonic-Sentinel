# **CipherSonic Sentinel**

## Unlock the Sonic Mysteries

CipherSonic Sentinel transcends the ordinary, offering a dual-mode security system that responds to the symphony of your vocal cords. Whether you're safeguarding secret passages with a vocal code or granting access to individuals based on their unique voiceprints, CipherSonic Sentinel is your key to unlocking the mysteries of voice-activated security.

Embark on a journey into the enigmatic world of a digital sentinel standing guard at the intersection of mystery and security. This desktop application merges the cryptic allure of a dark theme with the prowess of digital signal processing, creating an immersive experience for users seeking a unique blend of security and sophistication.

## Preview
![Animation Gif](Demo.gif)

## Usage
1. Launch the application.
2. Press the microphone icon to start recording your voice.
3. The system will analyze your voice and determine whether to unlock the gate or keep it locked.

## Files

### `main.py`

This file contains the main code for the PyQt5 application. It includes:

- Definition of the `CipherSonicApp` class, which represents the main application window.
- Functions for recording audio, analyzing voice data, and updating the UI accordingly.
- Integration with the `model.py` file for voice recognition.

### `model.py`

This file contains the machine learning model used for voice recognition. It includes:

- Data preprocessing steps, including feature extraction from audio files.
- Training of support vector machine (SVM) models for sentence and speaker recognition.
- Functions for loading and using the trained models in the application.

## Dependencies

- PyQt5
- sounddevice
- librosa
- numpy
- wavio
- matplotlib


## Features

 - ### Fine-Tune Every Frequency
   Unleash the power of a secret vocal symphony to grant access. The application supports three predefined sentences for accessing:
   
    - **"Give me access."** 
    - **"Unlock middle gate."**
    - **"Open the door."**
      
  - ### Crafted for Intuitive Interaction
    Dive into the realm of individuality with voice fingerprints. Select and grant access to specific individuals among the original eight users. The UI provides a seamless experience with features like:

    - **A button to initiate voice-code recording.** 
    - **A spectrogram viewer for the spoken voice-code.**
    - **Analysis results showcasing passcode and voice matches.**
    - **Clear indicators for "Access gained" or "Access denied."**

## Contributors

Heartfelt thanks to the brilliant minds behind CipherSonic Sentinel for their contributions to this project.

<div align="left">
   <a href="https://github.com/AhmeddEmad7">
    <img src="https://github.com/AhmeddEmad7.png" width="100px" alt="@AhmeddEmad7">
  </a>
  <a href="https://github.com/hazemzakariasaad">
    <img src="https://github.com/hazemzakariasaad.png" width="100px" alt="@hazemzakariasaad">
  </a>
  <a href="https://github.com/nourhan-ahmedd">
    <img src="https://github.com/nourhan-ahmedd.png" width="100px" alt="@nourhan-ahmedd">
  </a>
  <a href="https://github.com/raghdaneiazyy6">
    <img src="https://github.com/raghdaneiazyy6.png" width="100px" alt="@raghdaneiazy6">
  </a>
</div>

## Acknowledgments

**This project was supervised by Dr. Tamer Basha & Eng. Abdallah Darwish, who provided invaluable guidance and expertise throughout its development as a part of the Digital Signal Processing course at Cairo University Faculty of Engineering.**

<div style="text-align: right">
    <img src="https://imgur.com/Wk4nR0m.png" alt="Cairo University Logo" width="100" style="border-radius: 50%;"/>
</div>

---
*CipherSonic Sentinel invites you to explore the intersection of mystery and security. Thank you for choosing us on this cryptographic audio journey!**

