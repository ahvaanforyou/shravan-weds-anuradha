import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

def generate_banners():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, 'assets')
    font_dir = 'C:/Windows/Fonts'

    width = 1200
    height = 630

    # Typography
    f_shloka = ImageFont.truetype(os.path.join(font_dir, 'georgia.ttf'), 15)
    f_title = ImageFont.truetype(os.path.join(font_dir, 'georgiab.ttf'), 20)
    f_name_big = ImageFont.truetype(os.path.join(font_dir, 'georgiab.ttf'), 40)
    f_weds = ImageFont.truetype(os.path.join(font_dir, 'georgiai.ttf'), 23)
    f_date = ImageFont.truetype(os.path.join(font_dir, 'georgiab.ttf'), 23)
    f_time = ImageFont.truetype(os.path.join(font_dir, 'georgia.ttf'), 17)
    f_venue_bold = ImageFont.truetype(os.path.join(font_dir, 'georgiab.ttf'), 17)
    f_venue = ImageFont.truetype(os.path.join(font_dir, 'georgiai.ttf'), 15)
    f_btn = ImageFont.truetype(os.path.join(font_dir, 'georgiab.ttf'), 14)
    f_card_name = ImageFont.truetype(os.path.join(font_dir, 'georgiab.ttf'), 17)
    f_card_role = ImageFont.truetype(os.path.join(font_dir, 'georgiai.ttf'), 13)

    # Clean Solid Plain Royal Navy Blue & Gold Palette
    bg_color = (12, 28, 64)       # Solid plain luxury royal navy
    gold = (212, 175, 55)         # Classic Gold
    bright_gold = (255, 223, 110) # Bright Gold
    deep_gold = (180, 140, 35)    # Deep Gold
    card_bg = (7, 18, 42)         # Deep contrast card background

    base = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(base)

    # Double Gold Borders
    draw.rectangle([18, 18, width - 18, height - 18], outline=gold, width=2)
    draw.rectangle([24, 24, width - 24, height - 24], outline=deep_gold, width=1)
    for cx, cy in [(21, 21), (width - 21, 21), (21, height - 21), (width - 21, height - 21)]:
        draw.rectangle([cx - 4, cy - 4, cx + 4, cy + 4], fill=bright_gold)

    # Left Column: Couple Portrait Cards
    card_w = 200
    card_h = 445
    card_y = 92

    def draw_card(img_path, name, role, x, y):
        c_img = Image.new('RGBA', (card_w, card_h), (0, 0, 0, 0))
        c_draw = ImageDraw.Draw(c_img)
        c_draw.rounded_rectangle([0, 0, card_w, card_h], radius=16, fill=(*card_bg, 255), outline=gold, width=2)
        c_draw.rounded_rectangle([3, 3, card_w - 3, card_h - 3], radius=14, outline=deep_gold, width=1)

        photo_h = card_h - 76
        raw = Image.open(img_path).convert('RGB')
        enhancer = ImageEnhance.Sharpness(raw)
        sharp = enhancer.enhance(1.15)

        scaled = sharp.resize((card_w - 14, photo_h - 14), Image.Resampling.LANCZOS)
        mask = Image.new('L', (card_w - 14, photo_h - 14), 0)
        m_draw = ImageDraw.Draw(mask)
        m_draw.rounded_rectangle([0, 0, card_w - 14, photo_h - 14], radius=12, fill=255)
        c_img.paste(scaled, (7, 7), mask)
        c_draw.rounded_rectangle([7, 7, card_w - 7, photo_h], radius=12, outline=deep_gold, width=1)

        bbox_n = c_draw.textbbox((0, 0), name, font=f_card_name)
        nw = bbox_n[2] - bbox_n[0]
        c_draw.text(((card_w - nw) // 2 + 1, photo_h + 13), name, fill=(0, 0, 0), font=f_card_name)
        c_draw.text(((card_w - nw) // 2, photo_h + 12), name, fill=(255, 245, 210), font=f_card_name)

        bbox_r = c_draw.textbbox((0, 0), role, font=f_card_role)
        rw = bbox_r[2] - bbox_r[0]
        c_draw.text(((card_w - rw) // 2, photo_h + 38), role, fill=bright_gold, font=f_card_role)

        base.paste(c_img.convert('RGB'), (x, y))

    groom_p = os.path.join(assets_dir, 'groom-portrait.webp')
    bride_p = os.path.join(assets_dir, 'bride-portrait.webp')
    draw_card(groom_p, 'Shravan Kumar', 'The Groom', 52, card_y)
    draw_card(bride_p, 'Hima Bindu', 'The Bride', 52 + card_w + 24, card_y)

    # Right Column: Clean Plain Invitation Content
    center_x = 832

    def draw_c(text, y, font, fill, shadow=(0, 0, 0)):
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        tx = center_x - (tw // 2)
        if shadow:
            draw.text((tx + 1, y + 1), text, font=font, fill=shadow)
        draw.text((tx, y), text, font=font, fill=fill)
        return bbox[3] - bbox[1]

    draw_c('||  SRI RADHA KRISHNAYA NAMAHA  ||', 74, f_shloka, (255, 230, 140))
    draw_c('WEDDING INVITATION', 102, f_title, bright_gold)

    draw.line([(center_x - 170, 134), (center_x + 170, 134)], fill=gold, width=1)
    draw.polygon([(center_x, 130), (center_x + 4, 134), (center_x, 138), (center_x - 4, 134)], fill=bright_gold)

    # Prominent stacked names with zero overflow
    draw_c('Shravan Kumar', 154, f_name_big, (255, 255, 255))
    draw_c('—  weds  —', 202, f_weds, bright_gold)
    draw_c('Hima Bindu', 234, f_name_big, (255, 255, 255))

    draw.line([(center_x - 130, 290), (center_x + 130, 290)], fill=deep_gold, width=1)

    draw_c('Wednesday, 04 November 2026', 308, f_date, bright_gold)
    draw_c('Reception: 07:30 PM Onwards', 346, f_time, (245, 240, 225))
    draw_c('Singi Reddy Shiva Reddy Gardens', 380, f_venue_bold, (230, 210, 150))
    draw_c('Padma Nagar, Karmanghat, Hyderabad', 408, f_venue, (220, 205, 170))

    btn_w = 400
    btn_h = 46
    bx1 = center_x - (btn_w // 2)
    by1 = 450
    draw.rounded_rectangle([bx1, by1, bx1 + btn_w, by1 + btn_h], radius=23, fill=(19, 57, 121), outline=gold, width=2)
    draw.rounded_rectangle([bx1 + 2, by1 + 2, bx1 + btn_w - 2, by1 + btn_h - 2], radius=21, outline=bright_gold, width=1)
    btn_txt = 'TAP TO OPEN INVITATION & RSVP'
    bbox_b = draw.textbbox((0, 0), btn_txt, font=f_btn)
    bw = bbox_b[2] - bbox_b[0]
    bh = bbox_b[3] - bbox_b[1]
    draw.text((center_x - bw // 2, by1 + (btn_h - bh) // 2 - 2), btn_txt, font=f_btn, fill=(255, 255, 255))

    # Save to assets
    share_path = os.path.join(assets_dir, 'shravan-hima-wedding-share.jpg')
    banner_path = os.path.join(assets_dir, 'og-wedding-banner.jpg')
    base.save(share_path, 'JPEG', quality=95, optimize=True)
    base.save(banner_path, 'JPEG', quality=95, optimize=True)

    print(f'Metadata share image created: {share_path} ({os.path.getsize(share_path)/1024:.1f} KB)')

if __name__ == '__main__':
    generate_banners()
