# Application configuration for Chess Openings Revision

import json
import os

# Server parameters - Production ready
HOST = '0.0.0.0'
PORT = int(os.environ.get('PORT', 5000))  # Use environment variable for port
DEBUG = os.environ.get('FLASK_ENV') == 'development'  # Only debug in development

# Game parameters
DEFAULT_PLAYER_COLOR = 'white'  # 'white' or 'black'
COMPUTER_MOVE_DELAY = 0.5  # Delay in seconds before the computer plays
HINT_DISPLAY_TIME = 3  # Duration to display the hint in seconds

# Messages
MESSAGES = {  # Dictionary containing user-facing messages for the application
    'correct_move': 'Correct move!',  # Message shown when the user plays the correct move
    'incorrect_move': 'Incorrect move. The expected move was {move}',  # Message shown when the user plays an incorrect move; {move} will be replaced by the expected move
    'game_complete': 'Congratulations! You have completed this line!',  # Message shown when the user completes a line of moves
    'your_turn': 'Your turn!',  # Message indicating it's the user's turn to play
    'game_reset': 'Game reset. Your turn!',  # Message shown when the game is reset
    'last_line': 'You are on the last line!',  # Message shown when the user is on the last line of the opening
    'hint_message': 'The correct move is {move}'  # Message shown as a hint; {move} will be replaced by the correct move
}

# Customizable CSS styles
CUSTOM_STYLES = {  # Dictionary containing customizable CSS color styles for the app
    'primary_color': '#667eea',      # Main theme color (used for primary UI elements)
    'secondary_color': '#764ba2',    # Secondary theme color (used for accents, backgrounds)
    'success_color': '#28a745',      # Color for success messages or indicators
    'error_color': '#dc3545',        # Color for error messages or indicators
    'warning_color': '#ffc107',      # Color for warning messages or indicators
    'info_color': '#17a2b8'          # Color for informational messages or indicators
}

def load_openings_from_json():
    """Charge les ouvertures depuis le fichier JSON"""
    try:
        if os.path.exists('data/openings.json'):
            with open('data/openings.json', 'r', encoding='utf-8') as f:
                global OPENINGS
                OPENINGS = json.load(f)
                return True
    except Exception as e:
        print(f"Erreur lors du chargement JSON: {e}")
    return False

def save_openings_to_json():
    """Sauvegarde les ouvertures dans le fichier JSON"""
    try:
        os.makedirs('data', exist_ok=True)
        with open('data/openings.json', 'w', encoding='utf-8') as f:
            json.dump(OPENINGS, f, indent=4, ensure_ascii=False)
        print(f"DEBUG config.py: Sauvegarde réussie de {len(OPENINGS)} catégories")
        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde JSON: {e}")
        return False

# Fonction supprimée car redondante avec save_openings_to_json()


OPENINGS = {
    # =========================
    #        ATTACKS
    # =========================
    "Attack": [
        {
            "name": "Italian Game",
            "variations": [
                {
                    "name": "#1 Main Line",
                    "pgn": "1. e4 e5 2. Nf3 Nc6 3. Bc4 Bc5 4. c3 Nf6 5. d3 *"
                },
                {
                    "name": "#2 Giuoco Piano Variation",
                    "pgn": "1. e4 e5 2. Nf3 Nc6 3. Bc4 Bc5 4. c3 Nf6 5. d4 exd4 6. cxd4 *"
                },
                {
                    "name": "#3 Evans Gambit",
                    "pgn": "1. e4 e5 2. Nf3 Nc6 3. Bc4 Bc5 4. b4 Bxb4 5. c3 *"
                }
            ]
        },
        {
            "name": "English Opening",
            "variations": [
                {
                    "name": "#1 Main Line",
                    "pgn": "1. c4 e5 2. Nc3 Nf6 3. g3 d5 4. cxd5 Nxd5 5. Bg2 *"
                },
                {
                    "name": "#2 Symmetrical Variation",
                    "pgn": "1. c4 c5 2. Nc3 Nc6 3. g3 g6 4. Bg2 Bg7 5. Nf3 *"
                }
            ]
        },
        {
            "name": "Vienna Gambit",
            "variations": [
                {
                    "name": "#1 Popular Line",
                    "pgn": "1. e4 e5 2. Nc3 Nf6 3. f4 exf4 4. e5 Ng8 5. Nf3 Nc6 6. d4 d6 7. Bxf4 dxe5 8. Nxe5 Nxe5 9. Bxe5"
                },
                {
                    "name": "#2 Center Space",
                    "pgn": "1. e4 e5 2. Nc3 Nf6 3. f4 d6 4. Nf3 exf4 5. d4"
                },
                {
                    "name": "#3 Trappy Line",
                    "pgn": "1. e4 e5 2. Nc3 Nf6 3. f4 exf4 4. e5 Nh5 5. Qxh5"
                },
                {
                    "name": "#4 Knight Pinned",
                    "pgn": "1. e4 e5 2. Nc3 Nf6 3. f4 d6 4. Nf3 Nc6 5. Bb5"
                },
                {
                    "name": "#5 Knight Retreats",
                    "pgn": "1. e4 e5 2. Nc3 Nf6 3. f4 Nc6 4. fxe5 Nxe5 5. d4 Ng6 6. e5 Ng8 7. Nf3"
                },
                {
                    "name": "#6 Royal Fork",
                    "pgn": "1. e4 e5 2. Nc3 Nf6 3. f4 exf4 4. e5 Qe7 5. Qe2 Ng8 6. Nf3 d6 7. Nd5 Qe6 8. Nxc7+"
                },
                {
                    "name": "#7 Developed Pieces",
                    "pgn": "1. e4 e5 2. Nc3 Nf6 3. f4 exf4 4. e5 Ng8 5. Nf3 d6 6. d4 dxe5 7. Qe2 Bb4 8. Qxe5+ Qe7 9. Bxf4"
                },
                {
                    "name": "#8 Pawn Frozen",
                    "pgn": "1. e4 e5 2. Nc3 Nf6 3. f4 exf4 4. e5 Ng8 5. Nf3 d6 6. d4 dxe5 7. Qe2 Nc6 8. Bxf4"
                },
                {
                    "name": "#9 Material Sacrifice",
                    "pgn": "1. e4 e5 2. Nc3 Nf6 3. f4 exf4 4. e5 Ng8 5. Nf3 g5 6. d4 g4 7. Bxf4 gxf3 8. Qxf3 d6 9. Bb5+ c6 10. O-O cxb5 11. Bg5"
                },
                {
                    "name": "#10 Queen Discovered",
                    "pgn": "1. e4 e5 2. Nc3 Nf6 3. f4 exf4 4. e5 Qe7 5. Qe2 Ng8 6. Nf3 d6 7. Nd5 Qd7 8. Nxc7+ Qxc7 9. exd6+ Qe7 10. dxe7"
                },
                {
                    "name": "#11 Queen Re-Discovered",
                    "pgn": "1. e4 e5 2. Nc3 Nf6 3. f4 exf4 4. e5 Qe7 5. Qe2 Ng8 6. Nf3 Nc6 7. d4 d6 8. Nd5 Qd8 9. Nxc7+ Qxc7 10. exd6+ Be7 11. dxc7"
                },
                {
                    "name": "#12 Main Line",
                    "pgn": "1. e4 e5 2. Nc3 Nf6 3. f4 d5 4. fxe5 Nxe4 5. Qf3 Nxc3 6. bxc3 Be7 7. d4 O-O 8. Bd3 Be6 9. Ne2"
                },
                {
                    "name": "#13 Easy Position",
                    "pgn": "1. e4 e5 2. Nc3 Nf6 3. f4 exf4 4. e5 Ng8 5. Nf3 d6 6. d4 dxe5 7. Qe2 Be7 8. Qxe5 Nf6 9. Bxf4"
                },
                {
                    "name": "#14 Bishop Blockade",
                    "pgn": "1. e4 e5 2. Nc3 Nf6 3. f4 exf4 4. e5 Ng8 5. Nf3 d6 6. d4 dxe5 7. Qe2 Be7 8. Qxe5 Nc6 9. Bb5 Bd7 10. Bxc6 Bxc6 11. d5 Bd7 12. Bxf4"
                }
            ]
        }
    ],

    # =========================
    #        DEFENSES
    # =========================
    "Defense": [
        {
            "name": "Sicilian Defense",
            "variations": [
                {
                    "name": "#1 Main Line",
                    "pgn": "1. e4 c5 2. Nf3 d6 3. d4 cxd4 4. Nxd4 Nf6 5. Nc3 a6 *"
                },
                {
                    "name": "#2 Najdorf Variation",
                    "pgn": "1. e4 c5 2. Nf3 d6 3. d4 cxd4 4. Nxd4 Nf6 5. Nc3 a6 6. Be3 e5 7. Nb3 Be6 8. f3 Be7 *"
                },
                {
                    "name": "#3 Dragon Variation",
                    "pgn": "1. e4 c5 2. Nf3 d6 3. d4 cxd4 4. Nxd4 Nf6 5. Nc3 g6 6. Be3 Bg7 7. f3 O-O *"
                }
            ]
        },
        {
            "name": "French Defense",
            "variations": [
                {
                    "name": "#1 Main Line",
                    "pgn": "1. e4 e6 2. d4 d5 3. Nc3 Bb4 4. e5 c5 5. a3 Bxc3+ 6. bxc3 Ne7 *"
                },
                {
                    "name": "#2 Tarrasch Variation",
                    "pgn": "1. e4 e6 2. d4 d5 3. Nd2 c5 4. exd5 exd5 5. Ngf3 Nc6 *"
                }
            ]
        },
        {
            "name": "Stafford Gambit",
            "variations": [
                {
                    "name": "#1 Bishop Guillotine",
                    "pgn": "1. e4 e5 2. Nf3 Nf6 3. Nxe5 Nc6 4. Nxc6 dxc6 5. d3 Bc5 6. Bg5 Nxe4 7. Bxd8 Bxf2+ 8. Ke2 Bg4#"
                },
                {
                    "name": "#2 Queen Heist",
                    "pgn": "1. e4 e5 2. Nf3 Nf6 3. Nxe5 Nc6 4. Nxc6 dxc6 5. e5 Ne4 6. d3 Bc5 7. dxe4 Bxf2+ 8. Kxf2 Qxd1"
                },
                {
                    "name": "#3 Dragged Queen",
                    "pgn": "1. e4 e5 2. Nf3 Nf6 3. Nxe5 Nc6 4. Nxc6 dxc6 5. d3 Bc5 6. Bg5 Nxe4 7. dxe4 Bxf2+ 8. Ke2 Bg4+ 9. Kxf2 Qxd1"
                },
                {
                    "name": "#4 Diagonal Doom",
                    "pgn": "1. e4 e5 2. Nf3 Nf6 3. Nxe5 Nc6 4. Nxc6 dxc6 5. d3 Bc5 6. Bg5 Nxe4 7. Be3 Bxe3 8. fxe3 Qh4+ 9. Ke2 Qf2#"
                },
                {
                    "name": "#5 Queen Chase",
                    "pgn": "1. e4 e5 2. Nf3 Nf6 3. Nxe5 Nc6 4. Nxc6 dxc6 5. d3 Bc5 6. Nc3 Ng4 7. Be3 Nxe3 8. fxe3 Bxe3 9. Qf3 Qg5"
                },
                {
                    "name": "#6 Engine Line",
                    "pgn": "1. e4 e5 2. Nf3 Nf6 3. Nxe5 Nc6 4. Nxc6 dxc6 5. Nc3 Bc5 6. d3 Ng4 7. Be3 Nxe3 8. fxe3 Bxe3 9. Qf3 Qg5"
                },
                {
                    "name": "#7 King Walk",
                    "pgn": "1. e4 e5 2. Nf3 Nf6 3. Nxe5 Nc6 4. Nxc6 dxc6 5. e5 Ne4 6. d3 Bc5 7. dxe4 Bxf2+ 8. Ke2 Bg4+ 9. Kxf2 Qxd1"
                },
                {
                    "name": "#8 Center Cracker",
                    "pgn": "1. e4 e5 2. Nf3 Nf6 3. Nxe5 Nc6 4. Nxc6 dxc6 5. Nc3 Bc5 6. d4 Bxd4"
                },
                {
                    "name": "#9 H-File Chase",
                    "pgn": "1. e4 e5 2. Nf3 Nf6 3. Nxe5 Nc6 4. Nxc6 dxc6 5. d3 Bc5 6. Bg5 Nxe4 7. Be3 Bxe3 8. fxe3 Qh4+ 9. g3 Nxg3 10. hxg3 Qxh1"
                },
                {
                    "name": "#10 H-File Sequel",
                    "pgn": "1. e4 e5 2. Nf3 Nf6 3. Nxe5 Nc6 4. Nxc6 dxc6 5. e5 Ne4 6. d3 Bc5 7. Be3 Bxe3 8. fxe3 Qh4+ 9. g3 Nxg3 10. hxg3 Qxh1"
                },
                {
                    "name": "#11 Queen Jail",
                    "pgn": "1. e4 e5 2. Nf3 Nf6 3. Nxe5 Nc6 4. Nxc6 dxc6 5. e5 Ne4 6. d3 Bc5 7. Be3 Bxe3 8. fxe3 Qh4+ 9. Ke2 Qf2#"
                },
                {
                    "name": "#12 Poisoned Center",
                    "pgn": "1. e4 e5 2. Nf3 Nf6 3. Nxe5 Nc6 4. Nxc6 dxc6 5. e5 Ne4 6. d4 Qh4 7. g3 Nxg3 8. fxg3 Qe4+ 9. Qe2 Qxh1"
                },
                {
                    "name": "#13 Stealth Queen",
                    "pgn": "1. e4 e5 2. Nf3 Nf6 3. Nxe5 Nc6 4. Nxc6 dxc6 5. f3 Nh5 6. Nc3 Qh4+ 7. g3 Nxg3 8. hxg3 Qxh1"
                },
                {
                    "name": "#14 Swarm Attack",
                    "pgn": "1. e4 e5 2. Nf3 Nf6 3. Nxe5 Nc6 4. Nxc6 dxc6 5. d3 Bc5 6. Be2 h5 7. O-O Ng4 8. h3 Qd6 9. Bxg4 hxg4 10. e5 Qg6 11. d4 gxh3 12. g3 h2+ 13. Kh1 Qe4+ 14. f3 Qxd4 15. Qxd4 Bxd4"
                },
                {
                    "name": "#15 Rude Knight",
                    "pgn": "1. e4 e5 2. Nf3 Nf6 3. Nxe5 Nc6 4. Nxc6 dxc6 5. d3 Bc5 6. Nc3 Ng4 7. f3 Nf2 8. Qe2 Nxh1"
                },
                {
                    "name": "#16 Bishop Blitz",
                    "pgn": "1. e4 e5 2. Nf3 Nf6 3. Nxe5 Nc6 4. Nxc6 dxc6 5. d3 Bc5 6. Nc3 Ng4 7. Qf3 Nxf2 8. Rg1 Nxd3+ 9. Bxd3 Bxg1"
                },
                {
                    "name": "#17 Knight Spiral",
                    "pgn": "1. e4 e5 2. Nf3 Nf6 3. Nxe5 Nc6 4. Nxc6 dxc6 5. Nc3 Bc5 6. Bc4 Ng4 7. O-O Qh4 8. h3 Nxf2 9. Qf3 Nxh3+ 10. Kh2 Nf2+ 11. Kg1 Qh1#"
                },
                {
                    "name": "#18 Pawn Stormer",
                    "pgn": "1. e4 e5 2. Nf3 Nf6 3. Nxe5 Nc6 4. Nxc6 dxc6 5. d3 Bc5 6. Be2 h5 7. c3 Ng4 8. d4 Qh4 9. g3 Qf6 10. f3 h4 11. fxg4 hxg3 12. Rf1 gxh2 13. Rxf6 gxf6"
                },
                {
                    "name": "#19 Family Fork",
                    "pgn": "1. e4 e5 2. Nf3 Nf6 3. Nxe5 Nc6 4. Nxc6 dxc6 5. Nc3 Bc5 6. Bc4 Ng4 7. O-O Qh4 8. h3 Nxf2 9. Bxf7+ Kf8 10. Qh5 Nxe4+ 11. Kh1 Ng3+"
                },
                {
                    "name": "#20 Quiet Line",
                    "pgn": "1. e4 e5 2. Nf3 Nf6 3. Nxe5 Nc6 4. Nf3 Nxe4 5. Qe2 Qe7 6. Nc3 Nxc3 7. Qxe7+ Bxe7 8. dxc3 d6"
                }
            ]
        }
    ]
}