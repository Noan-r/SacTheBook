#!/usr/bin/env python3
"""
Script de test pour vérifier que les pièces d'échecs se chargent correctement depuis le CDN
"""

import requests
import sys

def test_piece_url(piece):
    """Teste si une pièce d'échecs se charge correctement depuis le CDN"""
    url = f"https://cdn.jsdelivr.net/npm/chessboardjs@1.0.0/img/chesspieces/wikipedia/{piece}.png"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ {piece}.png - OK ({len(response.content)} bytes)")
            return True
        else:
            print(f"❌ {piece}.png - Erreur HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {piece}.png - Erreur: {e}")
        return False

def main():
    """Teste toutes les pièces d'échecs"""
    print("🧪 Test des pièces d'échecs depuis le CDN...")
    print("=" * 50)
    
    # Liste de toutes les pièces d'échecs
    pieces = [
        'wp', 'wr', 'wn', 'wb', 'wq', 'wk',  # Pièces blanches
        'bp', 'br', 'bn', 'bb', 'bq', 'bk'   # Pièces noires
    ]
    
    success_count = 0
    total_count = len(pieces)
    
    for piece in pieces:
        if test_piece_url(piece):
            success_count += 1
    
    print("=" * 50)
    print(f"📊 Résultats: {success_count}/{total_count} pièces chargées avec succès")
    
    if success_count == total_count:
        print("🎉 Toutes les pièces se chargent correctement !")
        return 0
    else:
        print("⚠️  Certaines pièces ne se chargent pas correctement.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
