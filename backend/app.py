# from flask import Flask, request, send_file, render_template, url_for
# from PIL import Image, ImageDraw, ImageFont
# import io, os, textwrap, json
# from datetime import datetime

# app = Flask(__name__)

# # Folder to save generated memes (inside static)
# MEME_FOLDER = os.path.join("static", "memes")
# os.makedirs(MEME_FOLDER, exist_ok=True)

# JSON_PATH = "memes.json"
# MAX_SIZE = (800, 800)  # Max width/height for uploaded images

# def add_text(draw, text, font, image_width, y_position, text_color, outline_thick, position="center"):
#     lines = textwrap.wrap(text, width=20)
#     for line in lines:
#         bbox = draw.textbbox((0,0), line, font=font)
#         text_width = bbox[2] - bbox[0]
#         text_height = bbox[3] - bbox[1]

#         if "left" in position:
#             x = 10
#         elif "right" in position:
#             x = image_width - text_width - 10
#         else:  # center
#             x = (image_width - text_width) / 2

#         # Draw outline
#         for dx in range(-outline_thick, outline_thick+1):
#             for dy in range(-outline_thick, outline_thick+1):
#                 if dx != 0 or dy != 0:
#                     draw.text((x+dx, y_position+dy), line, font=font, fill="black")

#         draw.text((x, y_position), line, font=font, fill=text_color)
#         y_position += text_height + 5
#     return y_position

# @app.route("/")
# def home():
#     # Load last 5 memes
#     if os.path.exists(JSON_PATH):
#         with open(JSON_PATH, "r", encoding="utf-8") as f:
#             memes_list = json.load(f)
#     else:
#         memes_list = []

#     last_memes = memes_list[-5:]
#     return render_template("index.html", memes=[m["filename"] for m in last_memes])

# @app.route("/generate_meme", methods=["POST"])
# def generate_meme():
#     # Load image
#     if "image" in request.files and request.files["image"].filename != "":
#         image_file = request.files["image"]
#         img = Image.open(image_file).convert("RGB")
#     else:
#         img = Image.new("RGB", (500, 500), color=(73, 109, 137))

#     # img.thumbnail(MAX_SIZE, Image.ANTIALIAS)
#     img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)

#     draw = ImageDraw.Draw(img)

#     # Font setup
#     font_path = request.form.get("font_type", "arial.ttf")
#     font_size = int(request.form.get("fontsize", 40))
#     try:
#         font = ImageFont.truetype(font_path, font_size)
#     except:
#         font = ImageFont.load_default()

#     text_color = request.form.get("text_color", "#FFFFFF")
#     outline_thick = int(request.form.get("outline_thick", 2))

#     # Top text
#     text_top = request.form.get("text_top", "")
#     position_top = request.form.get("position_top", "top_center")
#     if text_top:
#         add_text(draw, text_top.upper(), font, img.width, 10, text_color, outline_thick, position_top)

#     # Bottom text
#     text_bottom = request.form.get("text_bottom", "")
#     position_bottom = request.form.get("position_bottom", "bottom_center")
#     if text_bottom:
#         wrapped_lines = textwrap.wrap(text_bottom, width=20)
#         line_height = font.getsize("A")[1] if hasattr(font, "getsize") else font_size
#         y_bottom = img.height - (line_height + 5) * len(wrapped_lines) - 10
#         add_text(draw, text_bottom.upper(), font, img.width, y_bottom, text_color, outline_thick, position_bottom)

#     # Save meme
#     filename = f"meme_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
#     save_path = os.path.join(MEME_FOLDER, filename)
#     img.save(save_path)

#     # Save metadata to memes.json
#     meme_data = {
#         "filename": filename,
#         "top_text": text_top,
#         "bottom_text": text_bottom,
#         "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     }

#     if os.path.exists(JSON_PATH):
#         with open(JSON_PATH, "r", encoding="utf-8") as f:
#             memes_list = json.load(f)
#     else:
#         memes_list = []

#     memes_list.append(meme_data)
#     memes_list = memes_list[-50:]  # Keep last 50 memes
#     with open(JSON_PATH, "w", encoding="utf-8") as f:
#         json.dump(memes_list, f, indent=4)

#     # Send image back to frontend
#     img_io = io.BytesIO()
#     img.save(img_io, "PNG")
#     img_io.seek(0)
#     return send_file(img_io, mimetype="image/png")

# if __name__ == "__main__":
#     app.run(debug=True)







from flask import Flask, request, send_file, render_template, url_for
from PIL import Image, ImageDraw, ImageFont
import io, os, textwrap, json
from datetime import datetime

app = Flask(__name__)

# Folders
MEME_FOLDER = os.path.join("static", "memes")
os.makedirs(MEME_FOLDER, exist_ok=True)
JSON_FILE = "memes.json"

# Image max size
MAX_SIZE = (1000, 1000)

def add_text(draw, text, font, img_width, y_pos, color, outline, position="center"):
    lines = textwrap.wrap(text, width=20)
    for line in lines:
        bbox = draw.textbbox((0,0), line, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # X position
        if "left" in position:
            x = 10
        elif "right" in position:
            x = img_width - text_width - 10
        else:  # center
            x = (img_width - text_width)/2

        # Outline
        for dx in range(-outline, outline+1):
            for dy in range(-outline, outline+1):
                if dx != 0 or dy != 0:
                    draw.text((x+dx, y_pos+dy), line, font=font, fill="black")

        # Main text
        draw.text((x, y_pos), line, font=font, fill=color)
        y_pos += text_height + 5
    return y_pos

@app.route("/")
def home():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            memes_list = json.load(f)
    else:
        memes_list = []
    last_memes = memes_list[-5:]  # last 5 memes
    return render_template("index.html", memes=[m["filename"] for m in last_memes])

@app.route("/generate_meme", methods=["POST"])
def generate_meme():
    # Load image
    if "image" in request.files and request.files["image"].filename != "":
        image_file = request.files["image"]
        img = Image.open(image_file).convert("RGB")
    else:
        img = Image.new("RGB", (500,500), color=(73,109,137))

    # Resize large images
    img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)

    draw = ImageDraw.Draw(img)

    # Font setup
    font_path = request.form.get("font_type", "arial.ttf")
    font_size = int(request.form.get("fontsize", 40))
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    text_color = request.form.get("text_color", "#FFFFFF")
    outline_thick = int(request.form.get("outline_thick", 2))

    # Top text
    text_top = request.form.get("text_top", "")
    pos_top = request.form.get("position_top", "top_center")
    y_top = 10
    if text_top:
        add_text(draw, text_top.upper(), font, img.width, y_top, text_color, outline_thick, pos_top)

    # Bottom text
    text_bottom = request.form.get("text_bottom", "")
    pos_bottom = request.form.get("position_bottom", "bottom_center")
    if text_bottom:
        wrapped_lines = textwrap.wrap(text_bottom, width=20)
        line_height = font.getsize("A")[1] if hasattr(font, "getsize") else font_size
        y_bottom = img.height - (line_height + 5) * len(wrapped_lines) - 10
        add_text(draw, text_bottom.upper(), font, img.width, y_bottom, text_color, outline_thick, pos_bottom)

    # Save meme
    filename = f"meme_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    save_path = os.path.join(MEME_FOLDER, filename)
    img.save(save_path)

    # Save metadata
    meme_data = {
        "filename": filename,
        "top_text": text_top,
        "bottom_text": text_bottom,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            memes_list = json.load(f)
    else:
        memes_list = []
    memes_list.append(meme_data)
    memes_list = memes_list[-50:]  # keep last 50
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(memes_list, f, indent=4)

    # Send image back
    img_io = io.BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)
    return send_file(img_io, mimetype="image/png")

# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

