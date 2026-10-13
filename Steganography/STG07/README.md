# 🕵️ Steganography CTF — Hidden Meme Dialogue

## 📌 Challenge Description
A famous face, a memorable expression, and a dialogue everyone loves! 😎

But there is more to this image than meets the eye. A famous meme dialogue has been secretly hidden inside the image.

Can you uncover the hidden dialogue and retrieve the flag?

## 🎯 Objective
Analyze the provided image and extract the hidden meme dialogue using steganography techniques.

## 📁 Challenge File
- `challenge.png`

## 💡 Hints
1. The secret is hidden inside the image.
2. Try analyzing the image using steganography tools.
3. Check the image for hidden text or embedded data.
4. The recovered text is a famous meme dialogue.

## 🛠️ Tools
- `exiftool`
- `strings`
- `binwalk`
- `zsteg`

## 🚩 Flag Format
```text
cebroid{famous_meme_dialogue}
```

## ✅ Solution Approach

### Step 1: Inspect image metadata
```bash
exiftool challenge.png
```

### Step 2: Search for readable strings
```bash
strings challenge.png
```

### Step 3: Check for hidden files
```bash
binwalk challenge.png
```

### Step 4: Analyze PNG pixel data
```bash
zsteg -a challenge.png
```

### Step 5: Recover the dialogue
Examine the extracted output to find the famous meme dialogue. Normalize it according to the challenge's flag format.

## 🏁 Final Flag
```text
cebroid{replace_with_the_actual_dialogue}
```

## 📚 Learning Outcomes
- Understand image steganography.
- Practice extracting hidden messages from image files.
- Learn basic CTF investigation techniques.
- Explore how ordinary images can carry secret information.

