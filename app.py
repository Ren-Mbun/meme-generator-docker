from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image, ImageDraw, ImageFont
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # običajna lokacija v linux image

def draw_text_on_image(img_path, top_text, bottom_text, out_path):
    image = Image.open(img_path).convert("RGBA")
    W, H = image.size
    draw = ImageDraw.Draw(image)

    try:
        # osnovna velikost pisave (približno 1/10 širine slike)
        base_font_size = int(W / 10)
        font = ImageFont.truetype(FONT_PATH, base_font_size)
    except Exception:
        font = ImageFont.load_default()
        base_font_size = 20

    def get_dynamic_font(text, max_width, max_font_size):
        font_size = max_font_size
        fnt = ImageFont.truetype(FONT_PATH, font_size)
        while draw.textlength(text, font=fnt) > max_width and font_size > 10:
            font_size -= 1
            fnt = ImageFont.truetype(FONT_PATH, font_size)
        return fnt

    def draw_text_with_outline(text, x, y, font, fill="white", stroke_fill="black", stroke_width=3):
        draw.text((x, y), text, font=font, fill=fill, stroke_fill=stroke_fill, stroke_width=stroke_width, anchor="ms")

    # zgornji tekst
    if top_text:
        top_font = get_dynamic_font(top_text.upper(), W * 0.9, base_font_size)
        draw_text_with_outline(top_text.upper(), W/2, top_font.size, top_font)

    # spodnji tekst
    if bottom_text:
        bottom_font = get_dynamic_font(bottom_text.upper(), W * 0.9, base_font_size)
        draw_text_with_outline(bottom_text.upper(), W/2, H - bottom_font.size, bottom_font)

    image.convert("RGB").save(out_path, format="JPEG", quality=95)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # pridobi naloženo datoteko in tekst
        file = request.files.get("image")
        top_text = request.form.get("top_text", "")
        bottom_text = request.form.get("bottom_text", "")

        if not file:
            return redirect(request.url)

        # shrani temp datoteko
        ext = os.path.splitext(file.filename)[1].lower()
        uid = str(uuid.uuid4())[:8]
        in_path = os.path.join(UPLOAD_FOLDER, f"input_{uid}{ext or '.png'}")
        out_path = os.path.join(UPLOAD_FOLDER, f"meme_{uid}.jpg")
        file.save(in_path)

        # generiraj meme
        try:
            draw_text_on_image(in_path, top_text, bottom_text, out_path)
        except Exception as e:
            return f"Error generating meme: {e}"

        return redirect(url_for("result", filename=os.path.basename(out_path)))

    return render_template("index.html")

@app.route("/result/<filename>")
def result(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(path):
        return "File not found", 404
    # prikaže stran z rezultatom
    return send_file(path, mimetype="image/jpeg")

if __name__ == "__main__":
    # poslušaj na 0.0.0.0, da bo delovalo tudi znotraj Docker kontejnerja
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=True)
