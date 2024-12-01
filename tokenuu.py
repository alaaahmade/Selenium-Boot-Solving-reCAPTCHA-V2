import base64

# Token to decode
token = "03AFcWeA6O76MakS-UqWabCQZ-WbulyQIoWvSB2wPVY0JIb6MRQgjOie_5w40PkVLkF62neNrug..."

# Decode the token assuming base64 encoding
try:
    # Padding may be required for base64 decoding
    missing_padding = len(token) % 4
    if missing_padding:
        token += '=' * (4 - missing_padding)
    decoded_token = base64.urlsafe_b64decode(token)
    try:
        # Try decoding as UTF-8
        decoded_text = decoded_token.decode('utf-8')
        print("Decoded Token (text):", decoded_text)
    except UnicodeDecodeError:
        # If decoding as UTF-8 fails, print the raw bytes
        print("Decoded Token (bytes):", decoded_token)
except Exception as e:
    print("Error decoding token:", e)
