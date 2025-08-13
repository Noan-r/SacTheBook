from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
import chess
import chess.pgn
from io import StringIO
import config
import json
import re

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = 'chess_openings_secret_key'

class OpeningTrainer:
    def __init__(self):
        self.openings_by_category = self.load_openings()
    
    def load_openings(self):
        """Load all openings from config.py, supporting multiple variations per opening"""
        openings_by_cat = {}
        for category, openings_list in config.OPENINGS.items():
            openings_by_cat[category] = []
            for opening_data in openings_list:
                opening_name = opening_data["name"]
                # Chaque ouverture peut avoir plusieurs variations
                lines = []
                for variation in opening_data.get("variations", []):
                    variation_name = variation["name"]
                    pgn_text = variation["pgn"]
                    loaded_lines = self.load_opening_from_pgn_string(pgn_text)
                    # Ajoute chaque ligne avec le nom de la variation
                    for line in loaded_lines:
                        # On remplace le nom par le nom de la variation pour l'affichage
                        line["name"] = variation_name
                        lines.append(line)
                # Inclure toutes les ouvertures, même celles sans variations
                openings_by_cat[category].append({
                    "name": opening_name,
                    "lines": lines
                })
        return openings_by_cat
    
    def load_opening_from_pgn_string(self, pgn_content):
        """Load an opening from a PGN string"""
        lines = []
        pgn_io = StringIO(pgn_content)
        while True:
            try:
                game = chess.pgn.read_game(pgn_io)
                if game is None:
                    break
                
                board = game.board()
                moves = []
                
                # Check that the initial position is valid
                if not board.is_valid():
                    print(f"Invalid initial position for game: {game.headers.get('Event', 'Unknown')}")
                    continue
                
                for move in game.mainline_moves():
                    try:
                        # Check that the move is legal
                        if move in board.legal_moves:
                            san_move = board.san(move)
                            moves.append({
                                "san": san_move,
                                "uci": move.uci()
                            })
                            board.push(move)
                        else:
                            print(f"Illegal move detected: {move.uci()} in {game.headers.get('Event', 'Unknown')}")
                            break
                    except Exception as e:
                        print(f"Error processing move {move.uci()}: {e}")
                        break

                if moves:
                    lines.append({
                        'name': game.headers.get('Event', 'Main Line'),
                        'moves': moves,
                    })
            except Exception as e:
                print(f"Error processing a PGN game: {e}")
                continue
        return lines
    
    def get_openings_by_category(self):
        """Return the openings grouped by category"""
        return self.openings_by_category
    
    def get_opening_lines(self, opening_name):
        """Return the lines of an opening"""
        for category in self.openings_by_category.values():
            for opening in category:
                if opening['name'] == opening_name:
                    return opening['lines']
        return []

    def get_opening_details(self, opening_name):
        """Return the lines and category of an opening"""
        for category, openings_list in self.openings_by_category.items():
            for opening in openings_list:
                if opening['name'] == opening_name:
                    return opening['lines'], category
        return None, None

trainer = OpeningTrainer()

def validate_pgn(pgn, color, category, opening_name, variation_index=None):
    import chess.pgn
    from io import StringIO
    import re
    
    print(f"DEBUG validate_pgn: pgn='{pgn}', color='{color}', category='{category}'")
    
    # Vérifier les caractères autorisés dans le PGN
    allowed_chars = r'^[0-9\.\s\w\+\#\=\-\*\!\?]+$'
    if not re.match(allowed_chars, pgn):
        print(f"DEBUG: Échec - caractères non autorisés")
        return False, "Invalid PGN"
    
    # Vérifier le format PGN de base
    # Doit commencer par 1. et avoir des espaces entre les coups
    if not pgn.strip().startswith('1.'):
        print(f"DEBUG: Échec - ne commence pas par 1.")
        return False, "Invalid PGN"
    
    # Vérifier qu'il y a des espaces entre les coups (pas de format compact comme "bg20")
    if not re.search(r'\d+\.\s+\w+', pgn):
        print(f"DEBUG: Échec - format compact détecté")
        return False, "Invalid PGN"
    
    # Vérifier que les numéros de coups sont séquentiels
    move_numbers = re.findall(r'(\d+)\.', pgn)
    for i, num in enumerate(move_numbers):
        if int(num) != i + 1:
            print(f"DEBUG: Échec - numéros de coups non séquentiels")
            return False, "Invalid PGN"
    
    try:
        pgn_io = StringIO(pgn)
        game = chess.pgn.read_game(pgn_io)
        if game is None:
            print(f"DEBUG: Échec - PGN impossible à lire")
            return False, "Invalid PGN"
        board = game.board()
        moves = list(game.mainline_moves())
        if not moves:
            print(f"DEBUG: Échec - aucun coup trouvé")
            return False, "Invalid PGN"
        print(f"DEBUG: {len(moves)} coups trouvés")
        board = chess.Board()
        for move in moves:
            if move not in board.legal_moves:
                print(f"DEBUG: Échec - coup illégal: {move}")
                return False, "Invalid PGN"
            board.push(move)
        
        # Vérifier que le PGN original correspond au PGN parsé
        # Cela détecte les formats incorrects comme "Bg20" qui sont interprétés comme "Bg2"
        reconstructed_pgn = ""
        board = chess.Board()
        for i, move in enumerate(moves):
            if i % 2 == 0:
                reconstructed_pgn += f"{i//2 + 1}. "
            reconstructed_pgn += board.san(move) + " "
            board.push(move)
        reconstructed_pgn = reconstructed_pgn.strip()
        
        # Normaliser les deux PGNs pour la comparaison (supprimer les espaces multiples, etc.)
        original_normalized = re.sub(r'\s+', ' ', pgn.strip())
        reconstructed_normalized = re.sub(r'\s+', ' ', reconstructed_pgn)
        
        # Supprimer les symboles de fin de partie (*, #, =, etc.) pour la comparaison
        original_clean = re.sub(r'\s*[\*#=]\s*$', '', original_normalized)
        reconstructed_clean = re.sub(r'\s*[\*#=]\s*$', '', reconstructed_normalized)
        
        if original_clean != reconstructed_clean:
            return False, "Invalid PGN"
        
        # Vérifier que le nombre de coups est cohérent avec la couleur du dernier coup
        # Pour une ouverture Attack (blancs), le dernier coup doit être blanc (nombre impair de coups)
        # Pour une ouverture Defense (noirs), le dernier coup doit être noir (nombre pair de coups)
        print(f"DEBUG: len(moves)={len(moves)}, color={color}, len(moves)%2={len(moves)%2}")
        if color == 'white' and len(moves) % 2 == 0:
            print(f"DEBUG: Échec - blancs avec nombre pair de coups")
            return False, "Invalid PGN"
        if color == 'black' and len(moves) % 2 == 1:
            print(f"DEBUG: Échec - noirs avec nombre impair de coups")
            return False, "Invalid PGN"
    except Exception as e:
        print(f"DEBUG: Exception: {e}")
        return False, "Invalid PGN"
    
    print(f"DEBUG: Vérification unicité...")
    all_pgns = set()
    for cat, openings in config.OPENINGS.items():
        for opening in openings:
            for idx, variation in enumerate(opening['variations']):
                if cat == category and opening['name'] == opening_name and variation_index is not None and idx == variation_index:
                    continue
                all_pgns.add(variation['pgn'].strip())
    
    if pgn.strip() in all_pgns:
        print(f"DEBUG: Échec - PGN déjà existant")
        return False, "Invalid PGN"
    
    print(f"DEBUG: Vérification couleur du dernier coup...")
    last_move_color = 'white' if len(moves) % 2 == 1 else 'black'
    print(f"DEBUG: last_move_color={last_move_color}, expected_color={color}")
    if last_move_color != color:
        print(f"DEBUG: Échec - couleur du dernier coup incorrecte")
        return False, "Invalid PGN"
    
    print(f"DEBUG: PGN valide!")
    return True, None

# Supprimer cette fonction dupliquée et utiliser directement config.save_openings_to_json()

@app.route('/')
def index():
    """Home page with the main menu"""
    # Recharger les données depuis le fichier pour s'assurer qu'elles sont à jour
    config.load_openings_from_json()
    # Recréer l'instance trainer avec les données mises à jour
    global trainer
    trainer = OpeningTrainer()
    openings_by_category = trainer.get_openings_by_category()
    
    # Trier les ouvertures par ordre alphabétique dans chaque catégorie
    for category in openings_by_category:
        openings_by_category[category].sort(key=lambda x: x['name'].lower())
    
    # Headers pour éviter le cache
    response = make_response(render_template('index.html', openings_by_category=openings_by_category))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/opening/<opening_name>')
def opening_page(opening_name):
    """Game page for a specific opening"""
    # Recharger les données depuis le fichier pour s'assurer qu'elles sont à jour
    config.load_openings_from_json()
    # Recréer l'instance trainer avec les données mises à jour
    global trainer
    trainer = OpeningTrainer()
    lines, category = trainer.get_opening_details(opening_name)
    if category is None:
        return "Opening not found", 404
    
    orientation = 'black' if category == 'Defense' else 'white'
    
    return render_template('opening.html', opening_name=opening_name, lines=lines, orientation=orientation)

@app.route('/openings/settings', methods=['GET'])
def opening_settings():
    # Recharger les données depuis le fichier pour s'assurer qu'elles sont à jour
    config.load_openings_from_json()
    
    # Préparer la liste des ouvertures sous forme plate (catégorie, nom, variations)
    openings = []
    for category, opening_list in config.OPENINGS.items():
        for opening in opening_list:
            openings.append({
                'category': category,
                'name': opening['name'],
                'variations': opening['variations']
            })
    
    # Trier les ouvertures par ordre alphabétique
    openings.sort(key=lambda x: x['name'].lower())
    
    return render_template('opening_settings.html', openings=openings)

@app.route('/openings/settings/add', methods=['POST'])
def add_opening():
    # Accepte JSON ou form classique
    if request.is_json:
        data = request.get_json()
        category = data.get('category')
        name = data.get('name')
    else:
        category = request.form.get('category')
        name = request.form.get('name')
    
    print(f"DEBUG add_opening: category='{category}', name='{name}'")
    print(f"DEBUG: config.OPENINGS keys avant: {list(config.OPENINGS.keys())}")
    
    if not (category and name):
        return jsonify({'error': 'Données manquantes'}), 400
    
    # Recharger les données depuis le fichier pour s'assurer qu'elles sont à jour
    config.load_openings_from_json()
    print(f"DEBUG: config.OPENINGS keys après rechargement: {list(config.OPENINGS.keys())}")
    print(f"DEBUG: config.OPENINGS[{category}] existe: {category in config.OPENINGS}")
    
    # Vérifier unicité dans toutes les catégories
    for cat, openings in config.OPENINGS.items():
        for opening in openings:
            if opening['name'].strip().lower() == name.strip().lower():
                return jsonify({'error': 'Ce nom existe déjà'}), 400
    
    # Ajoute à la structure en mémoire
    if category in config.OPENINGS:
        config.OPENINGS[category].append({
            'name': name.strip(),
            'variations': []
        })
    else:
        config.OPENINGS[category] = [{
            'name': name.strip(),
            'variations': []
        }]
    
    # Sauvegarder dans le fichier JSON
    print(f"DEBUG: Tentative de sauvegarde pour '{name}' dans la catégorie '{category}'")
    if config.save_openings_to_json():
        print(f"DEBUG: Ouverture '{name}' ajoutée avec succès")
        # Recharger les données après la sauvegarde pour s'assurer qu'elles sont synchronisées
        config.load_openings_from_json()
        print(f"DEBUG: Après rechargement, config.OPENINGS[{category}] contient: {[op['name'] for op in config.OPENINGS.get(category, [])]}")
        
        # Vérifier que l'ouverture a bien été ajoutée
        opening_added = False
        for opening in config.OPENINGS.get(category, []):
            if opening['name'] == name.strip():
                opening_added = True
                break
        
        if opening_added:
            print(f"DEBUG: Ouverture '{name}' confirmée dans la structure")
            return jsonify({'success': True})
        else:
            print(f"DEBUG: ERREUR - Ouverture '{name}' non trouvée après ajout")
            return jsonify({'error': 'Erreur de synchronisation'}), 500
    else:
        print("DEBUG: Erreur lors de la sauvegarde JSON")
        return jsonify({'error': 'Erreur lors de la sauvegarde'}), 500

@app.route('/openings/settings/add_variation', methods=['POST'])
def add_variation():
    # Accepte JSON ou form classique
    if request.is_json:
        data = request.get_json()
        category = data.get('category')
        name = data.get('name')
        var_title = data.get('variation_title')
        var_pgn = data.get('variation_pgn')
    else:
        category = request.form.get('category')
        name = request.form.get('name')
        var_title = request.form.get('variation_title')
        var_pgn = request.form.get('variation_pgn')
    
    print(f"DEBUG add_variation: category='{category}', name='{name}', var_title='{var_title}'")
    print(f"DEBUG config.OPENINGS keys: {list(config.OPENINGS.keys())}")
    print(f"DEBUG: config.OPENINGS[{category}] existe: {category in config.OPENINGS}")
    
    if not (category and name and var_title and var_pgn):
        return jsonify({'error': 'Données manquantes'}), 400
    
    # Recharger les données depuis le fichier pour s'assurer qu'elles sont à jour
    config.load_openings_from_json()
    
    print(f"DEBUG: Après rechargement, config.OPENINGS[{category}] contient: {[op['name'] for op in config.OPENINGS.get(category, [])]}")
    print(f"DEBUG: Recherche de l'ouverture '{name}' dans la catégorie '{category}'")
    
    if category in config.OPENINGS:
        print(f"DEBUG openings in {category}: {[op['name'] for op in config.OPENINGS[category]]}")
        # Vérification détaillée
        for i, opening in enumerate(config.OPENINGS[category]):
            print(f"DEBUG opening {i}: '{opening['name']}' vs '{name}' (match: {opening['name'] == name})")
    else:
        print(f"DEBUG: ERREUR - La catégorie '{category}' n'existe pas dans config.OPENINGS")
        return jsonify({'error': 'Ouverture non trouvée'}), 404
    
    # Chercher l'ouverture et ajouter la variation
    opening_found = False
    for opening in config.OPENINGS.get(category, []):
        if opening['name'] == name:
            opening_found = True
            
            # Déterminer la couleur attendue pour le dernier coup
            color = 'white' if category == 'Attack' else 'black'
            
            # Validation PGN
            is_valid, error_msg = validate_pgn(var_pgn, color, category, name)
            if not is_valid:
                print(f"DEBUG: PGN invalide - {error_msg}")
                return jsonify({'error': error_msg}), 400
            
            # Vérifier l'unicité du nom de variation dans cette ouverture (en ignorant le préfixe #N)
            print(f"DEBUG: Vérification unicité pour '{var_title}'")
            # Extraire le nom sans le préfixe #N
            var_title_clean = re.sub(r'^#\d+\s*', '', var_title.strip().lower())
            print(f"DEBUG: Nom nettoyé: '{var_title_clean}'")
            
            for variation in opening['variations']:
                variation_name_clean = re.sub(r'^#\d+\s*', '', variation['name'].strip().lower())
                print(f"DEBUG: Comparaison '{variation_name_clean}' vs '{var_title_clean}'")
                if variation_name_clean == var_title_clean:
                    print(f"DEBUG: Nom en double trouvé!")
                    return jsonify({'error': 'Une variation avec ce nom existe déjà dans cette ouverture'}), 400
            
            opening['variations'].append({'name': var_title.strip(), 'pgn': var_pgn.strip()})
            # Sauvegarder dans le fichier JSON
            if config.save_openings_to_json():
                print(f"DEBUG: Variation ajoutée avec succès à '{name}'")
                return jsonify({'success': True})
            else:
                print("DEBUG: Erreur lors de la sauvegarde JSON")
                return jsonify({'error': 'Erreur lors de la sauvegarde'}), 500
    
    # Si l'ouverture n'a pas été trouvée, la créer automatiquement
    if not opening_found:
        print(f"DEBUG: Ouverture '{name}' non trouvée, création automatique")
        if category in config.OPENINGS:
            config.OPENINGS[category].append({
                'name': name,
                'variations': []
            })
        else:
            config.OPENINGS[category] = [{
                'name': name,
                'variations': []
            }]
        
        # Sauvegarder l'ouverture
        if not config.save_openings_to_json():
            return jsonify({'error': 'Erreur lors de la création de l\'ouverture'}), 500
        
        # Maintenant ajouter la variation
        for opening in config.OPENINGS.get(category, []):
            if opening['name'] == name:
                opening['variations'].append({'name': var_title.strip(), 'pgn': var_pgn.strip()})
                if config.save_openings_to_json():
                    print(f"DEBUG: Ouverture créée et variation ajoutée avec succès")
                    return jsonify({'success': True})
                else:
                    return jsonify({'error': 'Erreur lors de la sauvegarde'}), 500
        
        return jsonify({'error': 'Erreur inattendue'}), 500

@app.route('/openings/settings/edit_variation', methods=['POST'])
def edit_variation():
    data = request.get_json()
    category = data.get('category')
    opening_name = data.get('opening')
    variation_index = data.get('variation_index')
    new_title = data.get('new_title')
    new_pgn = data.get('new_pgn')
    
    print(f"DEBUG edit_variation: category='{category}', opening='{opening_name}', index={variation_index}")
    
    if not (category and opening_name and new_title and new_pgn and variation_index is not None):
        return jsonify({'error': 'Missing data'}), 400
    
    try:
        variation_index = int(variation_index)
    except Exception:
        return jsonify({'error': 'Invalid index'}), 400
    
    # Recharger les données depuis le fichier pour s'assurer qu'elles sont à jour
    config.load_openings_from_json()
    
    # Déterminer la couleur attendue pour le dernier coup
    color = 'white' if category == 'Attack' else 'black'
    
    # Validation PGN
    is_valid, error_msg = validate_pgn(new_pgn, color, category, opening_name, variation_index)
    if not is_valid:
        return jsonify({'error': error_msg}), 400
    
    # Chercher l'ouverture
    for opening in config.OPENINGS.get(category, []):
        if opening['name'] == opening_name:
            if 0 <= variation_index < len(opening['variations']):
                # Vérifier l'unicité du nom de variation (en excluant la variation actuelle et en ignorant le préfixe #N)
                new_title_clean = re.sub(r'^#\d+\s*', '', new_title.strip().lower())
                for i, variation in enumerate(opening['variations']):
                    if i != variation_index:
                        variation_name_clean = re.sub(r'^#\d+\s*', '', variation['name'].strip().lower())
                        if variation_name_clean == new_title_clean:
                            return jsonify({'error': 'Une variation avec ce nom existe déjà dans cette ouverture'}), 400
                
                opening['variations'][variation_index]['name'] = new_title.strip()
                opening['variations'][variation_index]['pgn'] = new_pgn.strip()
                # Sauvegarder dans le fichier JSON
                if config.save_openings_to_json():
                    print(f"DEBUG: Variation {variation_index} modifiée avec succès dans '{opening_name}'")
                    return jsonify({'success': True})
                else:
                    print("DEBUG: Erreur lors de la sauvegarde JSON")
                    return jsonify({'error': 'Erreur lors de la sauvegarde sur disque'}), 500
            else:
                return jsonify({'error': 'Variation index out of range'}), 400
    
    print(f"DEBUG: Ouverture '{opening_name}' non trouvée dans la catégorie '{category}'")
    return jsonify({'error': 'Opening not found'}), 404

@app.route('/openings/settings/delete_variation', methods=['POST'])
def delete_variation():
    data = request.get_json()
    category = data.get('category')
    opening_name = data.get('opening')
    variation_index = data.get('variation_index')
    
    print(f"DEBUG delete_variation: category='{category}', opening='{opening_name}', index={variation_index}")
    
    if not (category and opening_name and variation_index is not None):
        return jsonify({'error': 'Missing data'}), 400
    
    try:
        variation_index = int(variation_index)
    except Exception:
        return jsonify({'error': 'Invalid index'}), 400
    
    # Recharger les données depuis le fichier pour s'assurer qu'elles sont à jour
    config.load_openings_from_json()
    
    # Chercher l'ouverture
    for opening in config.OPENINGS.get(category, []):
        if opening['name'] == opening_name:
            if 0 <= variation_index < len(opening['variations']):
                # Supprimer la variation
                deleted_variation = opening['variations'].pop(variation_index)
                # Sauvegarder dans le fichier JSON
                if config.save_openings_to_json():
                    print(f"DEBUG: Variation {variation_index} supprimée avec succès de '{opening_name}'")
                    return jsonify({'success': True})
                else:
                    print("DEBUG: Erreur lors de la sauvegarde JSON")
                    return jsonify({'error': 'Erreur lors de la sauvegarde sur disque'}), 500
            else:
                return jsonify({'error': 'Variation index out of range'}), 400
    
    print(f"DEBUG: Ouverture '{opening_name}' non trouvée dans la catégorie '{category}'")
    return jsonify({'error': 'Opening not found'}), 404

@app.route('/openings/settings/delete_opening', methods=['POST'])
def delete_opening():
    data = request.get_json()
    category = data.get('category')
    opening_name = data.get('name')
    
    print(f"DEBUG delete_opening: category='{category}', opening='{opening_name}'")
    
    if not (category and opening_name):
        return jsonify({'error': 'Missing data'}), 400
    
    # Recharger les données depuis le fichier pour s'assurer qu'elles sont à jour
    config.load_openings_from_json()
    
    # Chercher et supprimer l'ouverture
    if category in config.OPENINGS:
        for i, opening in enumerate(config.OPENINGS[category]):
            if opening['name'] == opening_name:
                # Supprimer l'ouverture
                deleted_opening = config.OPENINGS[category].pop(i)
                # Sauvegarder dans le fichier JSON
                if config.save_openings_to_json():
                    print(f"DEBUG: Ouverture '{opening_name}' supprimée avec succès de la catégorie '{category}'")
                    return jsonify({'success': True})
                else:
                    print("DEBUG: Erreur lors de la sauvegarde JSON")
                    return jsonify({'error': 'Erreur lors de la sauvegarde sur disque'}), 500
    
    print(f"DEBUG: Ouverture '{opening_name}' non trouvée dans la catégorie '{category}'")
    return jsonify({'error': 'Opening not found'}), 404

@app.route('/api/validate_move', methods=['POST'])
def validate_move():
    """API for validating a played move"""
    data = request.get_json()
    opening_name = data.get('opening_name')
    line_index = data.get('line_index', 0)
    current_move_index = data.get('current_move_index', 0)
    move_uci = data.get('move')
    
    # Recharger les données depuis le fichier pour s'assurer qu'elles sont à jour
    config.load_openings_from_json()
    # Recréer l'instance trainer avec les données mises à jour
    global trainer
    trainer = OpeningTrainer()
    
    lines = trainer.get_opening_lines(opening_name)
    if not lines:
        return jsonify({'error': 'Opening not found'}), 404
    
    if line_index >= len(lines):
        return jsonify({'error': 'Line not found'}), 404
    
    line = lines[line_index]
    moves = line['moves']
    
    if current_move_index >= len(moves):
        return jsonify({'error': 'End of line reached'}), 400
    
    expected_move = moves[current_move_index]
    expected_uci = expected_move['uci']
    
    if move_uci == expected_uci:
        is_last_move = current_move_index == len(moves) - 1
        
        # The next computer move is the next one in the list
        next_computer_move = None
        if not is_last_move and current_move_index + 1 < len(moves):
            next_computer_move = moves[current_move_index + 1]

        return jsonify({
            'correct': True,
            'next_computer_move': next_computer_move,
            'is_last_move': is_last_move
        })
    else:
        return jsonify({
            'correct': False,
            'expected_move': expected_move['san'],
        })

@app.route('/api/get_hint', methods=['POST'])
def get_hint():
    """API for getting a hint"""
    data = request.get_json()
    opening_name = data.get('opening_name')
    line_index = data.get('line_index', 0)
    current_move_index = data.get('current_move_index', 0)

    # Recharger les données depuis le fichier pour s'assurer qu'elles sont à jour
    config.load_openings_from_json()
    # Recréer l'instance trainer avec les données mises à jour
    global trainer
    trainer = OpeningTrainer()

    lines = trainer.get_opening_lines(opening_name)
    if not lines or line_index >= len(lines):
        return jsonify({'error': 'Line not found'}), 404

    line = lines[line_index]
    moves = line['moves']

    if current_move_index >= len(moves):
        return jsonify({'error': 'End of line reached'}), 400

    expected_move = moves[current_move_index]
    return jsonify({
        'hint': expected_move['uci'],
        'message': f"The correct move is {expected_move['san']}"
    })

@app.route('/api/get_position', methods=['POST'])
def get_position():
    """API for getting the FEN of a position"""
    data = request.get_json()
    opening_name = data.get('opening_name')
    line_index = data.get('line_index', 0)
    move_index = data.get('move_index', 0)

    # Recharger les données depuis le fichier pour s'assurer qu'elles sont à jour
    config.load_openings_from_json()
    # Recréer l'instance trainer avec les données mises à jour
    global trainer
    trainer = OpeningTrainer()

    lines = trainer.get_opening_lines(opening_name)
    if not lines or line_index >= len(lines):
        return jsonify({'error': 'Line not found'}), 404

    line = lines[line_index]
    moves = line['moves']

    board = chess.Board()
    for i in range(min(move_index, len(moves))):
        board.push_uci(moves[i]['uci'])

    return jsonify({
        'fen': board.fen(),
        'is_white_turn': board.turn == chess.WHITE,
        'legal_moves': [move.uci() for move in board.legal_moves]
    })

@app.route('/test_validation', methods=['GET'])
def test_validation():
    """Route de test pour la validation PGN"""
    test_cases = [
        {
            'name': '1.e4 e5 pour les noirs (doit être valide)',
            'pgn': '1. e4 e5',
            'color': 'black',
            'category': 'Defense',
            'opening_name': 'Test Defense',
            'expected': True
        },
        {
            'name': '1.e4 e5 pour les blancs (doit être invalide)',
            'pgn': '1. e4 e5',
            'color': 'white',
            'category': 'Attack',
            'opening_name': 'Test Attack',
            'expected': False
        },
        {
            'name': '1.az4 (doit être invalide)',
            'pgn': '1. az4',
            'color': 'white',
            'category': 'Attack',
            'opening_name': 'Test Attack',
            'expected': False
        },
        {
            'name': 'PGN déjà existant (doit être invalide)',
            'pgn': '1. e4 e5 2. Nf3 Nc6 3. Bc4 Bc5 4. c3 Nf6 5. d3 *',
            'color': 'white',
            'category': 'Attack',
            'opening_name': 'Test Attack',
            'expected': False
        },
        {
            'name': 'PGN avec coup invalide az1 (doit être invalide)',
            'pgn': '1. g3 d5 2. cxd5 Nxd5 3. az1 *',
            'color': 'white',
            'category': 'Attack',
            'opening_name': 'Test Attack',
            'expected': False
        },
        {
            'name': 'PGN avec caractère spécial § (doit être invalide)',
            'pgn': '1. c4 e5 2. Nc3 Nf6 3. g3 d5 4. cxd5 Nxd5 5. Bg2§',
            'color': 'white',
            'category': 'Attack',
            'opening_name': 'Test Attack',
            'expected': False
        },
        {
            'name': 'Format compact bg20 (doit être invalide)',
            'pgn': 'bg20',
            'color': 'white',
            'category': 'Attack',
            'opening_name': 'Test Attack',
            'expected': False
        }
    ]
    
    results = []
    for test in test_cases:
        is_valid, error_msg = validate_pgn(test['pgn'], test['color'], test['category'], test['opening_name'])
        results.append({
            'test_name': test['name'],
            'pgn': test['pgn'],
            'expected': test['expected'],
            'actual': is_valid,
            'error_msg': error_msg,
            'passed': is_valid == test['expected']
        })
    
    return jsonify({
        'test_results': results,
        'summary': {
            'total': len(results),
            'passed': sum(1 for r in results if r['passed']),
            'failed': sum(1 for r in results if not r['passed'])
        }
    })

@app.route('/debug_pgn', methods=['GET'])
def debug_pgn():
    """Route de debug pour tester un PGN spécifique"""
    pgn = request.args.get('pgn', "3. g3 d5 4. cxd5 Nxd5 5. az1 *")
    try:
        import chess.pgn
        from io import StringIO
        pgn_io = StringIO(pgn)
        game = chess.pgn.read_game(pgn_io)
        if game is None:
            return jsonify({'error': 'PGN impossible à lire'})
        
        board = game.board()
        moves = list(game.mainline_moves())
        
        debug_info = {
            'pgn': pgn,
            'moves_count': len(moves),
            'moves_uci': [move.uci() for move in moves],
            'moves_san': []
        }
        
        # Tester chaque coup
        board = chess.Board()
        for i, move in enumerate(moves):
            legal_moves = list(board.legal_moves)
            is_legal = move in legal_moves
            san_move = board.san(move) if is_legal else "ILLÉGAL"
            debug_info['moves_san'].append(san_move)
            debug_info[f'move_{i}_legal'] = is_legal
            debug_info[f'move_{i}_uci'] = move.uci()
            if is_legal:
                board.push(move)
            else:
                break
        
        # Test de validation
        is_valid, error_msg = validate_pgn(pgn, 'white', 'Attack', 'Test', None)
        debug_info['validation_result'] = {
            'is_valid': is_valid,
            'error_msg': error_msg
        }
        
        # Test direct avec les paramètres de la requête
        color_param = request.args.get('color', 'white')
        category_param = request.args.get('category', 'Attack')
        opening_name_param = request.args.get('opening_name', 'Test')
        
        is_valid_direct, error_msg_direct = validate_pgn(pgn, color_param, category_param, opening_name_param, None)
        debug_info['validation_direct'] = {
            'is_valid': is_valid_direct,
            'error_msg': error_msg_direct,
            'color': color_param,
            'category': category_param
        }
        
        return jsonify(debug_info)
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/debug_openings', methods=['GET'])
def debug_openings():
    """Route de débogage pour vérifier l'état des ouvertures"""
    config.load_openings_from_json()
    return jsonify({
        'openings': config.OPENINGS,
        'categories': list(config.OPENINGS.keys()),
        'attack_count': len(config.OPENINGS.get('Attack', [])),
        'defense_count': len(config.OPENINGS.get('Defense', []))
    })

@app.route('/test_add_variation', methods=['GET'])
def test_add_variation():
    """Route de test pour ajouter une variation"""
    # Simuler l'ajout d'une variation
    category = "Defense"
    name = "Test Defense"
    var_title = "b"
    var_pgn = "1. e4 e5"
    
    print(f"DEBUG test_add_variation: category='{category}', name='{name}', var_title='{var_title}'")
    
    # Recharger les données
    config.load_openings_from_json()
    
    # D'abord, créer l'ouverture si elle n'existe pas
    opening_found = False
    for opening in config.OPENINGS.get(category, []):
        if opening['name'] == name:
            opening_found = True
            break
    
    if not opening_found:
        print(f"DEBUG: Création de l'ouverture '{name}'")
        if category in config.OPENINGS:
            config.OPENINGS[category].append({
                'name': name,
                'variations': []
            })
        else:
            config.OPENINGS[category] = [{
                'name': name,
                'variations': []
            }]
        # Sauvegarder l'ouverture
        if not config.save_openings_to_json():
            return jsonify({'success': False, 'message': 'Erreur lors de la création de l\'ouverture'})
        print(f"DEBUG: Ouverture '{name}' créée avec succès")
    
    # Maintenant chercher l'ouverture et ajouter la variation
    for opening in config.OPENINGS.get(category, []):
        if opening['name'] == name:
            # Vérifier la validation PGN
            is_valid, error_msg = validate_pgn(var_pgn, 'black', category, name)
            print(f"DEBUG: Validation PGN - is_valid={is_valid}, error_msg={error_msg}")
            
            if is_valid:
                # Ajouter la variation
                opening['variations'].append({'name': var_title, 'pgn': var_pgn})
                # Sauvegarder
                if config.save_openings_to_json():
                    return jsonify({'success': True, 'message': 'Variation ajoutée'})
                else:
                    return jsonify({'success': False, 'message': 'Erreur de sauvegarde'})
            else:
                return jsonify({'success': False, 'message': f'PGN invalide: {error_msg}'})
    
    return jsonify({'success': False, 'message': 'Erreur inattendue'})

@app.route('/test_reload', methods=['GET'])
def test_reload():
    """Route de test pour vérifier si les données sont bien rechargées"""
    config.load_openings_from_json()
    return jsonify({
        'openings': config.OPENINGS,
        'defense_count': len(config.OPENINGS.get('Defense', [])),
        'test_defense_exists': any(op['name'] == 'Test Defense' for op in config.OPENINGS.get('Defense', []))
    })

@app.route('/test_save', methods=['GET'])
def test_save():
    """Route de test pour vérifier la sauvegarde"""
    # Ajouter une ouverture de test
    test_opening = {
        'name': 'Test Save',
        'variations': [{'name': 'Test Variation', 'pgn': '1. e4 e5'}]
    }
    
    if 'Defense' not in config.OPENINGS:
        config.OPENINGS['Defense'] = []
    
    config.OPENINGS['Defense'].append(test_opening)
    
    # Sauvegarder directement avec la fonction de config.py
    try:
        import os
        os.makedirs('data', exist_ok=True)
        with open('data/openings.json', 'w', encoding='utf-8') as f:
            import json
            json.dump(config.OPENINGS, f, indent=4, ensure_ascii=False)
        success = True
    except Exception as e:
        success = False
        print(f"Erreur de sauvegarde: {e}")
    
    return jsonify({
        'success': success,
        'openings_count': len(config.OPENINGS.get('Defense', [])),
        'test_opening_exists': any(op['name'] == 'Test Save' for op in config.OPENINGS.get('Defense', []))
    })

@app.route('/save_best_score', methods=['POST'])
def save_best_score():
    """Sauvegarde le meilleur score pour une ouverture donnée"""
    try:
        data = request.get_json()
        opening_name = data.get('opening_name')
        best_score = data.get('best_score', 0)
        
        if not opening_name:
            return jsonify({'success': False, 'error': 'Opening name is required'})
        
        # Chercher l'ouverture dans toutes les catégories
        opening_found = False
        for category, openings_list in config.OPENINGS.items():
            for opening in openings_list:
                if opening['name'] == opening_name:
                    opening['best_score'] = best_score
                    opening_found = True
                    print(f"Updated best score for {opening_name}: {best_score}")
                    break
            if opening_found:
                break
        
        if not opening_found:
            return jsonify({'success': False, 'error': f'Opening {opening_name} not found'})
        
        # Sauvegarder dans le fichier JSON
        import os
        os.makedirs('data', exist_ok=True)
        with open('data/openings.json', 'w', encoding='utf-8') as f:
            json.dump(config.OPENINGS, f, indent=4, ensure_ascii=False)
        
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"Error saving best score: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get_best_score')
def get_best_score():
    """Récupère le meilleur score pour une ouverture donnée"""
    try:
        opening_name = request.args.get('opening_name')
        
        if not opening_name:
            return jsonify({'success': False, 'error': 'Opening name is required'})
        
        # Chercher l'ouverture dans toutes les catégories
        best_score = 0
        opening_found = False
        for category, openings_list in config.OPENINGS.items():
            for opening in openings_list:
                if opening['name'] == opening_name:
                    best_score = opening.get('best_score', 0)
                    opening_found = True
                    print(f"Loaded best score for {opening_name}: {best_score}")
                    break
            if opening_found:
                break
        
        if not opening_found:
            print(f"Opening {opening_name} not found, returning default best score 0")
        
        return jsonify({'success': True, 'best_score': best_score})
        
    except Exception as e:
        print(f"Error loading best score: {e}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG) 