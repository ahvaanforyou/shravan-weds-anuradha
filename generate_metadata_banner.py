import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def generate_banners():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, 'assets')
    font_dir = 'C:/Windows/Fonts'

    width = 1200
    height = 630

    # Typography
    f_shloka = ImageFont.truetype(os.path.join(font_dir, 'georgia.ttf'), 15)
    f_title = ImageFont.truetype(os.path.join(font_dir, 'georgiab.ttf'), 20)
    f_names = ImageFont.truetype(os.path.join(font_dir, 'georgiab.ttf'), 36)
    f_date = ImageFont.truetype(os.path.join(font_dir, 'georgiab.ttf'), 23)
    f_time = ImageFont.truetype(os.path.join(font_dir, 'georgia.ttf'), 17)
    f_venue = ImageFont.truetype(os.path.join(font_dir, 'georgiai.ttf'), 15)
    f_btn = ImageFont.truetype(os.path.join(font_dir, 'georgiab.ttf'), 14)
    f_card_name = ImageFont.truetype(os.path.join(font_dir, 'georgiab.ttf'), 16)
    f_card_role = ImageFont.truetype(os.path.join(font_dir, 'georgiai.ttf'), 12)

    # Color Palette: Luxury Royal Navy & Radiant Gold
    navy_top = (10, 24, 56)
    navy_mid = (14, 34, 76)
    navy_bottom = (5, 14, 34)
    gold = (212, 175, 55, 255)
    bright_gold = (255, 223, 110, 255)
    deep_gold = (180, 140, 35, 255)
    card_bg = (12, 28, 64, 250)

    # 1. Base Gradient Canvas
    base = Image.new('RGBA', (width, height), navy_top)
    draw = ImageDraw.Draw(base)

    for y in range(height):
        t = y / float(height)
        mid_t = 1.0 - abs(t - 0.45) * 1.5
        mid_t = max(0.0, min(1.0, mid_t))
        r = int(navy_top[0] * (1 - t) + navy_bottom[0] * t + (navy_mid[0] - navy_top[0]) * 0.4 * mid_t)
        g = int(navy_top[1] * (1 - t) + navy_bottom[1] * t + (navy_mid[1] - navy_top[1]) * 0.4 * mid_t)
        b = int(navy_top[2] * (1 - t) + navy_bottom[2] * t + (navy_mid[2] - navy_top[2]) * 0.4 * mid_t)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

    # 2. Ornate Double Gold Borders
    draw.rectangle([18, 18, width - 18, height - 18], outline=gold, width=2)
    draw.rectangle([24, 24, width - 24, height - 24], outline=deep_gold, width=1)
    for cx, cy in [(21, 21), (width - 21, 21), (21, height - 21), (width - 21, height - 21)]:
        draw.rectangle([cx - 4, cy - 4, cx + 4, cy + 4], fill=bright_gold)

    # 3. Subtle Triptych Dividers for WhatsApp Center Safe Zone (285px to 915px)
    draw.line([(285, 24), (285, height - 24)], fill=(212, 175, 55, 55), width=1)
    draw.line([(915, 24), (915, height - 24)], fill=(212, 175, 55, 55), width=1)

    # 4. Left Wing: Bal Krishna
    rk_left_path = os.path.join(assets_dir, 'krishna-peeking.webp')
    if os.path.exists(rk_left_path):
        rk_left = Image.open(rk_left_path).convert('RGBA')
        rk_w = 215
        rk_h = int(rk_left.height * (rk_w / rk_left.width))
        rk_left = rk_left.resize((rk_w, rk_h), Image.Resampling.LANCZOS)
        base.paste(rk_left, (32, height - rk_h - 24), rk_left)

    # 5. Right Wing: Radha Rani
    radha_right_path = os.path.join(assets_dir, 'radha-peeking.webp')
    if os.path.exists(radha_right_path):
        radha_right = Image.open(radha_right_path).convert('RGBA')
        rr_w = 215
        rr_h = int(radha_right.height * (rr_w / radha_right.width))
        radha_right = radha_right.resize((rr_w, rr_h), Image.Resampling.LANCZOS)
        base.paste(radha_right, (width - rr_w - 32, height - rr_h - 24), radha_right)

    # 6. Lotus Motif at Top Center
    lotus_path = os.path.join(assets_dir, 'lotus-gold.webp')
    if os.path.exists(lotus_path):
        lotus = Image.open(lotus_path).convert('RGBA').resize((48, 38), Image.Resampling.LANCZOS)
        base.paste(lotus, (600 - 24, 28), lotus)

    draw = ImageDraw.Draw(base)

    def draw_center(text, y, font, fill, shadow=(0, 0, 0, 230)):
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        tx = 600 - (tw // 2)
        if shadow:
            draw.text((tx + 1, y + 1), text, font=font, fill=shadow)
        draw.text((tx, y), text, font=font, fill=fill)
        return bbox[3] - bbox[1]

    # Header Sacred Inscription
    draw_center('||  SRI RADHA KRISHNAYA NAMAHA  ||', 72, f_shloka, (255, 230, 140, 255))
    draw_center('WEDDING INVITATION', 96, f_title, bright_gold)

    # Decorative Gold Line
    div_w = 280
    draw.line([(600 - div_w // 2, 126), (600 + div_w // 2, 126)], fill=(212, 175, 55, 200), width=1)
    draw.polygon([(600, 122), (600 + 4, 126), (600, 130), (600 - 4, 126)], fill=bright_gold)

    # 7. Dual Couple Portrait Cards in Safe Center Zone
    card_w = 180
    card_h = 246
    card_y = 142
    gap = 20

    def draw_portrait(img_path, name_text, role_text, left_x, top_y):
        c_img = Image.new('RGBA', (card_w, card_h), (0, 0, 0, 0))
        c_draw = ImageDraw.Draw(c_img)
        c_draw.rounded_rectangle([0, 0, card_w, card_h], radius=16, fill=card_bg, outline=gold, width=2)
        c_draw.rounded_rectangle([3, 3, card_w - 3, card_h - 3], radius=14, outline=deep_gold, width=1)

        photo_h = card_h - 56
        raw = Image.open(img_path).convert('RGB')
        scaled = raw.resize((card_w - 12, photo_h - 12), Image.Resampling.LANCZOS)

        mask = Image.new('L', (card_w - 12, photo_h - 12), 0)
        m_draw = ImageDraw.Draw(mask)
        m_draw.rounded_rectangle([0, 0, card_w - 12, photo_h - 12], radius=12, fill=255)
        c_img.paste(scaled, (6, 6), mask)
        c_draw.rounded_rectangle([6, 6, card_w - 6, photo_h], radius=12, outline=deep_gold, width=1)

        bbox_n = c_draw.textbbox((0, 0), name_text, font=f_card_name)
        nw = bbox_n[2] - bbox_n[0]
        c_draw.text(((card_w - nw) // 2 + 1, photo_h + 9), name_text, fill=(0, 0, 0, 220), font=f_card_name)
        c_draw.text(((card_w - nw) // 2, photo_h + 8), name_text, fill=(255, 245, 205), font=f_card_name)

        bbox_r = c_draw.textbbox((0, 0), role_text, font=f_card_role)
        rw = bbox_r[2] - bbox_r[0]
        c_draw.text(((card_w - rw) // 2, photo_h + 30), role_text, fill=bright_gold, font=f_card_role)

        base.paste(c_img, (left_x, top_y), c_img)

    groom_p = os.path.join(assets_dir, 'groom-portrait.webp')
    bride_p = os.path.join(assets_dir, 'bride-portrait.webp')

    draw_portrait(groom_p, 'Shravan Kumar', 'The Groom', 600 - card_w - (gap // 2), card_y)
    draw_portrait(bride_p, 'Hima Bindu', 'The Bride', 600 + (gap // 2), card_y)

    # 8. Essential Wedding Information (Crisp, High Contrast)
    draw_center('Shravan Kumar  weds  Hima Bindu', 400, f_names, (255, 255, 255, 255), shadow=(0, 0, 0, 240))
    draw_center('Wednesday, 04 November 2026', 448, f_date, bright_gold)
    draw_center('Lagna Muhurtham: 07:30 PM Onwards', 482, f_time, (245, 240, 225, 240))
    draw_center('Singi Reddy Shiva Reddy Gardens • Karmanghat, Hyderabad', 512, f_venue, (220, 205, 160, 230))

    # 9. Interactive Call-To-Action Button
    btn_w = 380
    btn_h = 46
    bx1 = 600 - (btn_w // 2)
    by1 = 548
    draw.rounded_rectangle([bx1, by1, bx1 + btn_w, by1 + btn_h], radius=23, fill=(19, 57, 121, 250), outline=gold, width=2)
    draw.rounded_rectangle([bx1 + 2, by1 + 2, bx1 + btn_w - 2, by1 + btn_h - 2], radius=21, outline=bright_gold, width=1)
    btn_txt = 'TAP TO OPEN INVITATION & RSVP'
    bbox_b = draw.textbbox((0, 0), btn_txt, font=f_btn)
    bw = bbox_b[2] - bbox_b[0]
    bh = bbox_b[3] - bbox_b[1]
    draw.text((600 - bw // 2, by1 + (btn_h - bh) // 2 - 2), btn_txt, font=f_btn, fill=(255, 255, 255, 255))

    final_rgb = base.convert('RGB')

    # Save 1200x630 Banners
    banner_jpg = os.path.join(assets_dir, 'og-wedding-banner.jpg')
    banner_png = os.path.join(assets_dir, 'og-wedding-banner.png')
    final_rgb.save(banner_jpg, 'JPEG', quality=95, optimize=True)
    final_rgb.save(banner_png, 'PNG', optimize=True)

    # Save Dedicated 1:1 Square (630x630) for WhatsApp and platforms supporting square OG
    square_crop = final_rgb.crop((285, 0, 915, 630))
    square_jpg = os.path.join(assets_dir, 'og-wedding-square.jpg')
    square_png = os.path.join(assets_dir, 'og-wedding-square.png')
    square_crop.save(square_jpg, 'JPEG', quality=95, optimize=True)
    square_crop.save(square_png, 'PNG', optimize=True)

    print(f'Banner JPG: {banner_jpg} ({os.path.getsize(banner_jpg)/1024:.1f} KB)')
    print(f'Square JPG: {square_jpg} ({os.path.getsize(square_jpg)/1024:.1f} KB)')

if __name__ == '__main__':
    generate_banners()
