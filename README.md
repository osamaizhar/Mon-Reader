# 32VMKecjMmv755SU

# MonReader - AI-Powered Smart Document Reader

MonReader is an AI-powered mobile document scanning pipeline developed during my AI Residency at **Apziva** for a client specializing in inclusive computer vision solutions. The system is designed to detect page flips, capture still document images automatically, and extract + read out text using OCR and TTS.

## 🚀 Project Goals

- Predict whether a document page is being flipped using a single frame
- Trigger high-quality capture on still frames
- Build and evaluate models (pretrained + custom)
- Extract text from still frames using OCR
- Read out text via TTS (Text-to-Speech)

---

## 🧠 Tech Stack

### Programming Language:
- **Python** 3.9+

### Deep Learning & Machine Learning:
- **PyTorch** (`torch`, `torchvision`) - model building, training, GPU acceleration
- **scikit-learn** - metrics and evaluation (confusion matrix, F1)
- **lion-pytorch** - custom optimizer used for OsamaNet

### Computer Vision & OCR:
- **EasyOCR** - multilingual OCR with GPU support
- **OpenCV (cv2)** - image processing
- **PIL (Pillow)** - image handling and transformations

### Text-to-Speech (TTS):
- **pyttsx3** - offline TTS engine

### Language Detection:
- **langdetect** - automatic detection of extracted text language

### Data Handling & Utilities:
- **NumPy** - numerical operations
- **glob, os** - file handling and pattern matching
- **gc, time, random** - memory and performance utilities

### Data Loading & Augmentation:
- `torchvision.datasets.ImageFolder`
- `torchvision.transforms`
- `torch.utils.data.DataLoader`, `Dataset`, `SubsetRandomSampler`

### Visualization:
- **matplotlib.pyplot** - plotting training metrics and image samples
- **sklearn.metrics.ConfusionMatrixDisplay** - visual confusion matrix

### Development Environment:
- **Jupyter Notebook** - interactive prototyping and visual analysis

---

## 📁 Project Structure

```
Mon-Reader/
├── images/
│   ├── training/
│   │   ├── flip/              # Training flip images
│   │   └── notflip/           # Training notflip images
│   └── testing/
│       ├── flip/              # Testing flip images
│       └── notflip/           # Testing notflip images
├── part_2_images/             # Additional document images for OCR
├── extracted_text/            # OCR output text files
├── tts_outputs/               # TTS audio output (.wav)
├── saved_models/              # Trained PyTorch models (.pth)
├── eda.ipynb                  # Exploratory data analysis
├── model_testing.ipynb        # CNN model training and evaluation
├── ocr_tts_gpu.ipynb          # Final OCR + TTS implementation
├── requirements.txt           # Full dependencies
├── req_min.txt                # Minimal install requirements
├── .gitignore                 # Git ignored files and folders
├── README.md                  # Project documentation
```

---

## 📊 Steps I Completed

### 1. **Exploratory Data Analysis (EDA)**
- Printed folder structure
- Verified label distribution (`flip` vs `notflip`)
- Visualized blurry (flip) vs still (notflip) frames
- Ensured consistent dimensions and formats

### 2. **Image Classification Models**
- Used PyTorch Dataloaders + transforms for augmentation
- Tested 3 pretrained models with transfer learning:
  - ✅ ResNet50
  - ✅ MobileNetV2
  - ✅ EfficientNetB0
- Trained each model for **10 epochs** using binary classification loss
- Evaluated using **accuracy**, **F1 score**, and **confusion matrix**

### 3. **Custom CNN - OsamaNet**
- Designed lightweight CNN architecture
- Added dropout for regularization
- Used **Lion optimizer** for faster convergence and better generalization
- Trained and evaluated using consistent splits

### 4. **OCR + TTS Integration**
- Initial plan with PaddleOCR replaced by **EasyOCR**
- TTS demonstrated with **pyttsx3** (offline)
- Language auto-detection handled with `langdetect`

---

## 📈 Results Summary

| Model          | Accuracy | F1 Score (est.) |
|----------------|----------|-----------------|
| OsamaNet       | 93.97%   | ~0.93            |
| MobileNetV2    | 86.93%   | ~0.87            |
| EfficientNetB0 | 84.09%   | ~0.84            |
| ResNet50       | 71.36%   | ~0.71            |

✅ Custom model (OsamaNet) outperformed all baselines  
✅ MobileNet was lightweight and fast  
✅ EfficientNet showed balanced tradeoff  
✅ ResNet50 struggled with this specific dataset

---

## 🛠️ Installation

```bash
conda create -n monreader python=3.9 -y
conda activate monreader
pip install -r requirements.txt
```

> Ensure compatible NVIDIA drivers and CUDA are installed for GPU acceleration

---

## 🤝 Credits

Developed by **Osama Izhar** during his AI Residency at **Apziva**.  
Dataset and business problem provided by client for internal R&D use.

---

## 📬 Contact
For questions, collaborations, or deployment discussions:
**ahmedosamaizhar21@gmail.com**

---

**#AI #ComputerVision #CNN #OCR #TTS #PyTorch #Accessibility #MonReader**
