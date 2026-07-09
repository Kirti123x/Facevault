# FaceVault 🔐📸
## Offline AI-Powered Photo Organizer

FaceVault is an **offline desktop application** that automatically organizes your photo collection by detecting, recognizing, and grouping people using Artificial Intelligence.

The application scans a local photo folder, detects faces using **InsightFace**, generates face embeddings, clusters similar faces using **DBSCAN**, and stores all results locally in **SQLite**. Users can browse their photos grouped by person through a simple and intuitive **PyQt6 desktop interface**.

🔒 **Your photos never leave your device. FaceVault works completely offline.**

---

# ✨ Features

## 🤖 AI Face Recognition
- Detects faces from images using InsightFace.
- Generates accurate face embeddings.
- Runs completely offline without cloud services.

## 🧩 Automatic Face Clustering
- Uses DBSCAN clustering algorithm.
- Automatically groups photos containing the same person.
- No manual tagging required.

## 🗃️ Local Database
Stores:
- Photo information
- Face embeddings
- Person clusters
- Image paths

Powered by SQLite.

## 🖥️ Desktop Application
Built using PyQt6.

Features:
- Select photo folders
- Scan and index images
- View indexing progress
- Browse photos by person
- Manage organized photo collections

## 🔒 Privacy Focused
- No cloud uploads
- No external APIs
- No user tracking
- All AI processing happens locally

---

# 🏗️ Project Structure

```
FaceVault/
│
├── main.py                    # Application entry point
│
├── core/
│   ├── detector.py            # Face detection module
│   ├── embedder.py            # Face embedding generation
│   ├── clustering.py          # DBSCAN clustering logic
│   └── indexer.py             # Image indexing pipeline
│
├── database/
│   ├── db.py                  # SQLite database operations
│   └── models.py              # Database models
│
├── gui/
│   ├── main_window.py         # Main application window
│   ├── gallery.py             # Photo gallery interface
│   └── components.py          # Reusable UI components
│
├── assets/
│   └── icons/
│
├── requirements.txt
├── README.md
└── facevault.db               # Generated database
```

---

# 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Programming Language | Python |
| GUI Framework | PyQt6 |
| Face Recognition | InsightFace |
| AI Runtime | ONNX Runtime |
| Image Processing | OpenCV |
| Machine Learning | Scikit-learn |
| Clustering Algorithm | DBSCAN |
| Database | SQLite |
| Image Handling | Pillow |
| Numerical Processing | NumPy |

---

# ⚙️ Installation

## Prerequisites

Make sure you have:

- Python 3.10+
- Git
- pip

Check Python version:

```bash
python --version
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/<username>/FaceVault.git

cd FaceVault
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run Application

```bash
python main.py
```

---

# 📦 Requirements

## Hardware Requirements

### Minimum

- CPU: Dual Core processor
- RAM: 8GB
- Storage: Depends on photo collection size

### Recommended

- CPU: Modern multi-core processor
- RAM: 16GB+
- GPU: Optional

---

## Software Requirements

Supported Operating Systems:

- Windows 10/11
- Linux
- macOS

Required Python Packages:

```
insightface
onnxruntime
opencv-python
numpy
scikit-learn
PyQt6
Pillow
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

# 🚀 Usage

1. Start FaceVault:

```bash
python main.py
```

2. Select a folder containing images.

Example:

```
Photos/
│
├── vacation.jpg
├── family.png
├── birthday.jpeg
└── trip.jpg
```

3. FaceVault performs:

```
Images
  ↓
Face Detection
  ↓
Generate Face Embeddings
  ↓
Cluster Similar Faces
  ↓
Store Results in SQLite
  ↓
Display Gallery
```

4. Browse your photos organized by people.

---

# 🧠 How FaceVault Works

## 1. Face Detection

InsightFace detects faces present in every image.

Example:

```
Image

 ↓

Detected Faces

Face 1
Face 2
Face 3
```

---

## 2. Face Embeddings

Every detected face is converted into a numerical representation.

Example:

```
Face

 ↓

[0.23, 0.54, 0.11, ...]
```

These vectors represent unique facial features.

---

## 3. Face Clustering

DBSCAN compares face embeddings and groups similar faces.

Example:

```
Person 1
 ├── image1.jpg
 ├── image2.jpg
 └── image3.jpg


Person 2
 ├── image4.jpg
 └── image5.jpg
```

---

## 4. Data Storage

Information is stored locally:

```
Database

people
 |
 ├── person_id


photos
 |
 ├── image_path


faces
 |
 ├── embedding
 └── person_id
```

---

# 🤝 Contributing

Contributions are welcome!

If you want to contribute to FaceVault, please follow these guidelines.

---

# Contributor Requirements

## Required Knowledge

Contributors should have understanding of:

- Python programming
- Object-Oriented Programming
- Git and GitHub workflow
- Basic Machine Learning concepts
- Image processing fundamentals
- SQLite database operations

---

# Development Setup

## 1. Fork the Repository

Create your own fork of FaceVault.

---

## 2. Clone Your Fork

```bash
git clone https://github.com/<your-username>/FaceVault.git

cd FaceVault
```

---

## 3. Create a New Branch

Always create a separate branch:

```bash
git checkout -b feature-name
```

Examples:

```
feature/improve-clustering
feature/new-ui
bugfix/database-error
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Test Your Changes

Run:

```bash
python main.py
```

Make sure:

- Application starts correctly
- Image indexing works
- Database updates correctly
- No existing features break

---

## 6. Commit Changes

Use meaningful commit messages.

Example:

```bash
git add .

git commit -m "Improve face clustering accuracy"
```

---

## 7. Push Changes

```bash
git push origin feature-name
```

Then create a Pull Request.

---

# 💡 Contribution Areas

## Artificial Intelligence

Possible improvements:

- Improve face recognition accuracy
- Optimize embedding generation
- Experiment with better clustering methods

## Performance

Ideas:

- Faster image processing
- Multi-threaded indexing
- Memory optimization

## User Interface

Ideas:

- Better PyQt6 design
- Dark mode support
- Improved gallery experience

## Database

Ideas:

- Optimize queries
- Improve database structure
- Add migration support

## Testing

Help with:

- Unit tests
- Integration tests
- Performance testing

---

# 🐛 Bug Reports

When creating an issue, include:

- Operating System
- Python version
- Error message
- Steps to reproduce

Example:

```
OS: Windows 11

Python Version:
3.11

Issue:
Application crashes during indexing

Steps:
1. Open FaceVault
2. Select folder
3. Start indexing
```

---

# 🔮 Future Roadmap

- [ ] Face name tagging
- [ ] Duplicate image detection
- [ ] Timeline-based photo browsing
- [ ] Video face recognition
- [ ] GPU acceleration
- [ ] Better similarity search
- [ ] Database backup/export
- [ ] Mobile companion application

---

# 📜 License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this software.

---

# ⭐ Support

If you like FaceVault:

- Give the repository a ⭐
- Report bugs
- Suggest new features
- Contribute improvements

---

## Built with ❤️ using Python, AI, and Open Source