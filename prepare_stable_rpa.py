#!/usr/bin/env python3
"""Préparer un patch local exact-build ; aucune connexion ni écriture au Stick."""
import argparse
import hashlib
import json
from pathlib import Path
import secrets
import subprocess

ORIGINAL = '50a44a7dfa32e5cea2a46135c8460981609bef99164e0f9bfb3f0ffc23504f3c'
OFFSET = 0x64A562
BEFORE = bytes.fromhex('9df81600bdf81410')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('original', type=Path)
    parser.add_argument('output', type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--new-device', action='store_true', help='PRAND aléatoire neuf, à utiliser avant première association')
    mode.add_argument('--prand-le', help='3 octets hex dans ordre little endian, extraits de la RPA locale fonctionnelle')
    args = parser.parse_args()
    data = args.original.read_bytes()
    if hashlib.sha256(data).hexdigest() != ORIGINAL or data[OFFSET:OFFSET+8] != BEFORE:
        parser.error('Bibliothèque non prise en charge : aucun patch effectué.')
    manifest = args.output.with_suffix(args.output.suffix + '.json')
    if args.output.resolve() == args.original.resolve() or args.output.exists() or manifest.exists():
        parser.error('La copie originale et les sorties existantes ne doivent pas être écrasées.')
    if args.new_device:
        while True:
            p = bytearray(secrets.token_bytes(3))
            p[2] = (p[2] & 0x3f) | 0x40
            if (int.from_bytes(p, 'little') & 0x3fffff) not in (0, 0x3fffff):
                break
    else:
        try:
            p = bytes.fromhex(args.prand_le)
        except ValueError:
            parser.error('PRAND hex invalide.')
        if len(p) != 3 or p[2] & 0xc0 != 0x40 or (int.from_bytes(p, 'little') & 0x3fffff) in (0, 0x3fffff):
            parser.error('PRAND invalide pour une adresse privée résoluble.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(data)
    low = int.from_bytes(p[:2], 'little')
    subprocess.run(['r2', '-w', '-q', '-e', 'scr.color=0', '-e', 'asm.bits=16', '-c',
                    f's 0x64b562;wa movw r0, {p[2]};s 0x64b566;wa movw r1, {low};q',
                    str(args.output)], check=True)
    patched = args.output.read_bytes()
    if len(patched) != len(data) or patched[:OFFSET] != data[:OFFSET] or patched[OFFSET+8:] != data[OFFSET+8:]:
        raise RuntimeError('Sortie refusée : modifications en dehors des deux instructions.')
    # Encoder MOVW Thumb-2 indépendamment pour contrôler le résultat de l'assembleur.
    def movw(reg, immediate):
        first = 0xf240 | ((immediate >> 12) & 15) | (((immediate >> 11) & 1) << 10)
        second = (((immediate >> 8) & 7) << 12) | (reg << 8) | (immediate & 255)
        return first.to_bytes(2, 'little') + second.to_bytes(2, 'little')
    expected = movw(0, p[2]) + movw(1, low)
    if patched[OFFSET:OFFSET+8] != expected:
        raise RuntimeError("Sortie refusée : encodage Thumb-2 inattendu. Ne pas installer.")
    record = {'original_sha256': ORIGINAL, 'patched_sha256': hashlib.sha256(patched).hexdigest(),
              'prand_little_endian': bytes(p).hex(), 'file_offset': hex(OFFSET),
              'before': BEFORE.hex(), 'after': expected.hex(), 'installed': False,
              'validation': 'A effectuer sur appareil ; sortie locale uniquement.'}
    manifest.write_text(json.dumps(record, indent=2) + '\n')
    print('Copie préparée. Vérifier le manifeste et suivre BLUETOOTH.md avant toute installation.')

if __name__ == '__main__':
    main()
