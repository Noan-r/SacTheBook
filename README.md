# SacTheBook - Chess Opening Trainer

A web-based chess opening trainer that helps you learn and practice chess openings through interactive drills and learning modes.

## Features

- **Learn Mode**: Study openings step by step with hints
- **Drill Mode**: Test your knowledge with randomized openings
- **Best Score Tracking**: Track your longest streaks in drill mode
- **Interactive Chessboard**: Drag and drop pieces with legal move highlighting
- **Promotion System**: Full pawn promotion functionality
- **Sound Effects**: Audio feedback for moves and game events
- **Responsive Design**: Works on desktop, tablet, and mobile

## Local Development

### Prerequisites
- Python 3.8+
- pip

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open http://localhost:5000 in your browser

## Deployment

### Option 1: Render (Recommended - Free)

1. **Create a Render account** at [render.com](https://render.com)

2. **Connect your GitHub repository**

3. **Create a new Web Service**:
   - Choose your repository
   - Name: `sacthebook`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

4. **Deploy** - Render will automatically deploy your app

### Option 2: Railway

1. **Create a Railway account** at [railway.app](https://railway.app)

2. **Connect your GitHub repository**

3. **Deploy** - Railway will automatically detect Flask and deploy

### Option 3: PythonAnywhere

1. **Create a PythonAnywhere account** at [pythonanywhere.com](https://pythonanywhere.com)

2. **Upload your files** via the Files tab

3. **Create a new web app**:
   - Choose Flask
   - Set the working directory to your project folder
   - Set the WSGI configuration file to point to your app

4. **Install dependencies** in the Bash console:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
SacTheBook/
├── app.py                 # Main Flask application
├── config.py             # Configuration and openings data
├── requirements.txt      # Python dependencies
├── Procfile             # Deployment configuration
├── runtime.txt          # Python version specification
├── data/
│   └── openings.json    # Opening data storage
├── static/              # Static assets (CSS, JS, images, sounds)
├── templates/           # HTML templates
└── README.md           # This file
```

## Configuration

The application uses environment variables for production settings:
- `PORT`: Server port (default: 5000)
- `FLASK_ENV`: Set to 'development' for debug mode

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License. 