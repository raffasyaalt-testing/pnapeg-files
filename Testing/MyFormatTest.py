import struct
import os
from PIL import Image

MAGIC_NUMBER = b'PNAP'
HEADER_FORMAT = '>HIII'

def encode_pnapeg(source_image_path, output_pnapeg_path):
    if not os.path.exists(source_image_path):
        print("Error: Standard image file not found.")
        return

    print("Encoding into custom format...")
    
    with Image.open(source_image_path) as img:
        rgb_img = img.convert('RGB')
        width, height = rgb_img.size
        raw_pixels = rgb_img.tobytes()
        
    version = 1
    
    with open(output_pnapeg_path, 'wb') as f:
        f.write(MAGIC_NUMBER)
        header = struct.pack(HEADER_FORMAT, version, width, height, len(raw_pixels))
        f.write(header)
        f.write(raw_pixels)
        
    print("Success! Created custom file.")


def decode_pnapeg(pnapeg_path):
    if not os.path.exists(pnapeg_path):
        print("Error: Custom format file not found.")
        return

    print("Decoding custom file...")
    
    with open(pnapeg_path, 'rb') as f:
        sig = f.read(4)
        if sig != MAGIC_NUMBER:
            print("Error: Malformed file structure. Not a valid .pnapeg file!")
            return
            
        header_bytes = f.read(14)
        version, width, height, data_length = struct.unpack(HEADER_FORMAT, header_bytes)
        pixel_data = f.read(data_length)

    img = Image.frombytes('RGB', (width, height), pixel_data)
    print("Successfully decoded .pnapeg. Opening viewer...")
    img.show()


if __name__ == "__main__":
    sample_img = Image.new('RGB', (400, 400), color='teal')
    sample_img.save("test_input.png")
    
    encode_pnapeg("test_input.png", "my_photo.pnapeg")
    
    decode_pnapeg("my_photo.pnapeg")
