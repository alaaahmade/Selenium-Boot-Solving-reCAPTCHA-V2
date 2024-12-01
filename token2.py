import base64
import zlib
import gzip
import io

def decode_base64_segment(segment):
    # Add padding to the segment
    missing_padding = len(segment) % 4
    if missing_padding:
        segment += '=' * (4 - missing_padding)
    return base64.urlsafe_b64decode(segment)

# Example token - replace with your actual token if it's JWT-like
token = "03AFcWeA6O76MakS-UqWabCQZ-WbulyQIoWvSB2wPVY0JIb6MRQgjOie_5w40PkVLkF62neNrug..."
parts = token.split('.')

try:
    # Decode each part, assuming JWT structure
    decoded_parts = [decode_base64_segment(part) for part in parts]
    decoded_texts = [part.decode('utf-8', errors='replace') for part in decoded_parts]
    
    print("Decoded Parts (text):", decoded_texts)
    print("Decoded Token (hex):", decoded_parts[0].hex())

    ascii_representation = bytes.fromhex(decoded_parts[0].hex()).decode('utf-8', errors='replace')
    print("ASCII Representation:", ascii_representation)


    try:
        decompressed_data = gzip.decompress(decoded_parts[0])
        print("Gzip Decompressed Data:", decompressed_data)
    except Exception as e:
        print("Error decompressing gzip data:", e)


except Exception as e:
    print("Error decoding token:", e)
