import os
import math
import discord
import requests
import random
from io import BytesIO
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps
from dotenv import load_dotenv
from server import server_on

intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.typing = False
intents.presences = False
load_dotenv()

bot = commands.Bot(command_prefix='>', intents=intents)

current_directory = os.path.dirname(os.path.abspath(__file__))

#===========================[ CONFIG ]==============================

# Load the bot token from the .env file
TOKEN = os.getenv('TOKEN')
owner_id = os.getenv('owner')

input_image = current_directory + "//src//BG-WelcomeDiscord.png"
linput_image = current_directory + "//src//BG-WelcomeDiscord.png"
profile_img = current_directory + "//src//p.png"

userfont = current_directory + "//src//Montserrat.ttf"
msgfont = current_directory + "//src//p5hatty.ttf"

inoutput = current_directory + '//output//join.png'
loutput = current_directory + '//output//leave.png'
toutput = current_directory + '//output//test.png'

channel_name = os.getenv('channel_name')
test_channel = os.getenv('test_channel')

text_angle = 12.65
user_fsize = 160
msg_fsize = 140
username_test = f"Almer h"

#===================================================================

#===========================[ Main ]================================


def join_member(input_image, text_list, image_data,
                user_data):  #edit user_data
  # Membuka gambar input menggunakan PIL
  image = Image.open(input_image)

  # Membuat objek ImageDraw untuk menggambar teks pada gambar
  draw = ImageDraw.Draw(image)

  for user_data in user_data:
    text = user_data["text"].upper()
    font_path = user_data["font_path"]
    font_size = user_data["font_size"]
    position = user_data["position"]
    fill = user_data["fill"]
    angle = user_data["angle"]

    if (len(text) < 6):
      # Mengatur font yang akan digunakan
      font = ImageFont.truetype(font_path, font_size)

      # Menghitung ukuran teks
      text_width, text_height = font.getsize(text)

      # Mengatur posisi teks pada gambar
      x = position[0]
      y = position[1]

      # Membuat gambar kosong menggunakan mode "RGBA" (transparan)
      text_image = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))

      # Membuat objek ImageDraw untuk menggambar teks pada gambar kosong
      text_draw = ImageDraw.Draw(text_image)

      # Menggambar teks pada posisi yang diinginkan
      text_draw.text((0, 0), text, font=font, fill=(fill[0], fill[1], fill[2]))

      # Merotasi gambar teks sesuai dengan sudut yang diinginkan
      rotated_text_image = text_image.rotate(angle,
                                             resample=Image.BICUBIC,
                                             expand=True)

      # Menghitung pergeseran tinggi dari rotasi sudut
      shift_y = int(math.tan(math.radians(angle)) * text_width)

      # Menyesuaikan posisi teks yang dirotasi
      # rotated_x = x - int(shift_y / 2) + (len(text) * 200)
      # rotated_y = y - int(shift_y / 2) + (len(text) * 4) * 2
      rotated_x = x - int(shift_y / 2) + (len(text) * 2) + int(
        round(160 / len(text)))
      rotated_y = y - int(shift_y / 2) + ((len(text) * 2) - len(text) +
                                          (6 - len(text)))

    if (len(text) > 5):
      # Mengatur font yang akan digunakan
      font = ImageFont.truetype(font_path, (font_size - (len(text) * 2 + 10)))

      # Menghitung ukuran teks
      text_width, text_height = font.getsize(text[:8])

      # Mengatur posisi teks pada gambar
      x = position[0]
      y = position[1]

      # Membuat gambar kosong menggunakan mode "RGBA" (transparan)
      text_image = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))

      # Membuat objek ImageDraw untuk menggambar teks pada gambar kosong
      text_draw = ImageDraw.Draw(text_image)

      # Menggambar teks pada posisi yang diinginkan
      text_draw.text((0, 0), text, font=font, fill=(fill[0], fill[1], fill[2]))

      # Merotasi gambar teks sesuai dengan sudut yang diinginkan
      rotated_text_image = text_image.rotate(angle,
                                             resample=Image.BICUBIC,
                                             expand=True)

      # Menghitung pergeseran tinggi dari rotasi sudut
      shift_y = int(math.tan(math.radians(angle)) * text_width)

      # Menyesuaikan posisi teks yang dirotasi
      rotated_x = x - int(shift_y / 2) - (len(text) * 2) - (28 - len(text))
      rotated_y = y - int(shift_y / 2) - ((len(text) * 2) + len(text) -
                                          (40 + ((len(text) * 2))))

    # Menambahkan gambar teks yang telah dirotasi ke dalam gambar input
    image.paste(rotated_text_image, (rotated_x, rotated_y), rotated_text_image)

  for text_info in text_list:
    text = text_info["text"]
    font_path = text_info["font_path"]
    font_size = text_info["font_size"]
    position = text_info["position"]
    fill = text_info["fill"]

    # Mengatur font yang akan digunakan
    font = ImageFont.truetype(font_path, font_size)

    # Menghitung ukuran teks
    text_width, text_height = font.getsize(text)

    # Mengatur posisi teks pada gambar
    x = position[0]
    y = position[1]

    # Memisahkan teks menjadi beberapa baris berdasarkan '\n'
    lines = text.split('\n')

    # Menggambar setiap baris teks pada gambar
    for line in lines:
      # Menghitung ukuran teks per baris
      text_width, text_height = font.getsize(line)

      # Membuat gambar kosong menggunakan mode "RGBA" (transparan)
      text_image = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))

      # Membuat objek ImageDraw untuk menggambar teks pada gambar kosong
      text_draw = ImageDraw.Draw(text_image)

      # Menggambar teks pada posisi yang diinginkan
      text_draw.text((0, 0), line, font=font, fill=(fill[0], fill[1], fill[2]))

      # Menambahkan gambar teks ke dalam gambar input
      image.paste(text_image, (x, y), text_image)

      # Menggeser posisi y untuk baris teks berikutnya
      y += text_height

  for image_data in image_data:
    img_path = image_data["image"]
    position = image_data["position"]
    img_size = image_data["imgsize"]

    # Download the image from the URL
    response = requests.get(img_path)
    image_data = BytesIO(response.content)

    # Open the image data using PIL
    object_image = Image.open(image_data)

    # Mengubah ukuran objek gambar sesuai dengan parameter yang diberikan
    object_image = object_image.resize(img_size).convert("RGBA")

    # Membuat mask berbentuk lingkaran dengan ukuran yang sama
    mask = Image.new("L", object_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + object_image.size, fill=255)

    object_image = ImageOps.fit(object_image, mask.size, centering=(0.5, 0.5))
    object_image.putalpha(mask)

    # Menggabungkan objek gambar ke dalam gambar input
    image.paste(object_image, position, object_image)

  # Menyimpan gambar yang telah dimodifikasi
  image.save(inoutput)

  print("Teks berhasil ditambahkan pada gambar input.")


def remove_member(linput_image, ltext_list, limage_data,
                  user_data):  #edit user_data
  # Membuka gambar input menggunakan PIL
  image = Image.open(linput_image)

  # Membuat objek ImageDraw untuk menggambar teks pada gambar
  draw = ImageDraw.Draw(image)

  for user_data in user_data:
    text = user_data["text"].upper()
    font_path = user_data["font_path"]
    font_size = user_data["font_size"]
    position = user_data["position"]
    fill = user_data["fill"]
    angle = user_data["angle"]

    if (len(text) < 6):
      # Mengatur font yang akan digunakan
      font = ImageFont.truetype(font_path, font_size)

      # Menghitung ukuran teks
      text_width, text_height = font.getsize(text)

      # Mengatur posisi teks pada gambar
      x = position[0]
      y = position[1]

      # Membuat gambar kosong menggunakan mode "RGBA" (transparan)
      text_image = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))

      # Membuat objek ImageDraw untuk menggambar teks pada gambar kosong
      text_draw = ImageDraw.Draw(text_image)

      # Menggambar teks pada posisi yang diinginkan
      text_draw.text((0, 0), text, font=font, fill=(fill[0], fill[1], fill[2]))

      # Merotasi gambar teks sesuai dengan sudut yang diinginkan
      rotated_text_image = text_image.rotate(angle,
                                             resample=Image.BICUBIC,
                                             expand=True)

      # Menghitung pergeseran tinggi dari rotasi sudut
      shift_y = int(math.tan(math.radians(angle)) * text_width)

      # Menyesuaikan posisi teks yang dirotasi
      # rotated_x = x - int(shift_y / 2) + (len(text) * 200)
      # rotated_y = y - int(shift_y / 2) + (len(text) * 4) * 2
      rotated_x = x - int(shift_y / 2) + (len(text) * 2) + int(
        round(160 / len(text)))
      rotated_y = y - int(shift_y / 2) + ((len(text) * 2) - len(text) +
                                          (6 - len(text)))

    if (len(text) > 5):
      # Mengatur font yang akan digunakan
      font = ImageFont.truetype(font_path, (font_size - (len(text) * 2 + 10)))

      # Menghitung ukuran teks
      text_width, text_height = font.getsize(text[:8])

      # Mengatur posisi teks pada gambar
      x = position[0]
      y = position[1]

      # Membuat gambar kosong menggunakan mode "RGBA" (transparan)
      text_image = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))

      # Membuat objek ImageDraw untuk menggambar teks pada gambar kosong
      text_draw = ImageDraw.Draw(text_image)

      # Menggambar teks pada posisi yang diinginkan
      text_draw.text((0, 0), text, font=font, fill=(fill[0], fill[1], fill[2]))

      # Merotasi gambar teks sesuai dengan sudut yang diinginkan
      rotated_text_image = text_image.rotate(angle,
                                             resample=Image.BICUBIC,
                                             expand=True)

      # Menghitung pergeseran tinggi dari rotasi sudut
      shift_y = int(math.tan(math.radians(angle)) * text_width)

      # Menyesuaikan posisi teks yang dirotasi
      rotated_x = x - int(shift_y / 2) - (len(text) * 2) - (28 - len(text))
      rotated_y = y - int(shift_y / 2) - ((len(text) * 2) + len(text) -
                                          (40 + ((len(text) * 2))))

    # Menambahkan gambar teks yang telah dirotasi ke dalam gambar input
    image.paste(rotated_text_image, (rotated_x, rotated_y), rotated_text_image)

  for text_info in ltext_list:
    text = text_info["text"]
    font_path = text_info["font_path"]
    font_size = text_info["font_size"]
    position = text_info["position"]
    fill = text_info["fill"]

    # Mengatur font yang akan digunakan
    font = ImageFont.truetype(font_path, font_size)

    # Menghitung ukuran teks
    text_width, text_height = font.getsize(text)

    # Mengatur posisi teks pada gambar
    x = position[0]
    y = position[1]

    # Memisahkan teks menjadi beberapa baris berdasarkan '\n'
    lines = text.split('\n')

    # Menggambar setiap baris teks pada gambar
    for line in lines:
      # Menghitung ukuran teks per baris
      text_width, text_height = font.getsize(line)

      # Membuat gambar kosong menggunakan mode "RGBA" (transparan)
      text_image = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))

      # Membuat objek ImageDraw untuk menggambar teks pada gambar kosong
      text_draw = ImageDraw.Draw(text_image)

      # Menggambar teks pada posisi yang diinginkan
      text_draw.text((0, 0), line, font=font, fill=(fill[0], fill[1], fill[2]))

      # Menambahkan gambar teks ke dalam gambar input
      image.paste(text_image, (x, y), text_image)

      # Menggeser posisi y untuk baris teks berikutnya
      y += text_height

  for text_info in limage_data:
    img_path = text_info["image"]
    position = text_info["position"]
    img_size = text_info["imgsize"]

    # Download the image from the URL
    response = requests.get(img_path)
    image_data = BytesIO(response.content)

    # Open the image data using PIL
    object_image = Image.open(image_data)

    # Mengubah ukuran objek gambar sesuai dengan parameter yang diberikan
    object_image = object_image.resize(img_size).convert("RGBA")

    # Membuat mask berbentuk lingkaran dengan ukuran yang sama
    mask = Image.new("L", object_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + object_image.size, fill=255)

    # Menerapkan mask ke objek gambar
    object_image = ImageOps.fit(object_image, mask.size, centering=(0.5, 0.5))
    object_image.putalpha(mask)

    # Menggabungkan objek gambar ke dalam gambar input
    image.paste(object_image, position, object_image)

  # Menyimpan gambar yang telah dimodifikasi
  image.save(loutput)

  print("Teks berhasil ditambahkan pada gambar input.")


def testing(input_image, text_list, user_data, image_data):
  # Membuka gambar input menggunakan PIL
  image = Image.open(input_image)

  # Membuat objek ImageDraw untuk menggambar teks pada gambar
  draw = ImageDraw.Draw(image)

  for user_data in user_data:
    text = user_data["text"].upper()
    font_path = user_data["font_path"]
    font_size = user_data["font_size"]
    position = user_data["position"]
    fill = user_data["fill"]
    angle = user_data["angle"]

    if (len(text) < 6):
      # Mengatur font yang akan digunakan
      font = ImageFont.truetype(font_path, font_size)

      # Menghitung ukuran teks
      text_width, text_height = font.getsize(text)

      # Mengatur posisi teks pada gambar
      x = position[0]
      y = position[1]

      # Membuat gambar kosong menggunakan mode "RGBA" (transparan)
      text_image = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))

      # Membuat objek ImageDraw untuk menggambar teks pada gambar kosong
      text_draw = ImageDraw.Draw(text_image)

      # Menggambar teks pada posisi yang diinginkan
      text_draw.text((0, 0), text, font=font, fill=(fill[0], fill[1], fill[2]))

      # Merotasi gambar teks sesuai dengan sudut yang diinginkan
      rotated_text_image = text_image.rotate(angle,
                                             resample=Image.BICUBIC,
                                             expand=True)

      # Menghitung pergeseran tinggi dari rotasi sudut
      shift_y = int(math.tan(math.radians(angle)) * text_width)

      # Menyesuaikan posisi teks yang dirotasi
      # rotated_x = x - int(shift_y / 2) + (len(text) * 200)
      # rotated_y = y - int(shift_y / 2) + (len(text) * 4) * 2
      rotated_x = x - int(shift_y / 2) + (len(text) * 2) + int(
        round(160 / len(text)))
      rotated_y = y - int(shift_y / 2) + ((len(text) * 2) - len(text) +
                                          (6 - len(text)))

    if (len(text) > 5):
      # Mengatur font yang akan digunakan
      font = ImageFont.truetype(font_path, (font_size - (len(text) * 2 + 10)))

      # Menghitung ukuran teks
      text_width, text_height = font.getsize(text[:8])

      # Mengatur posisi teks pada gambar
      x = position[0]
      y = position[1]

      # Membuat gambar kosong menggunakan mode "RGBA" (transparan)
      text_image = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))

      # Membuat objek ImageDraw untuk menggambar teks pada gambar kosong
      text_draw = ImageDraw.Draw(text_image)

      # Menggambar teks pada posisi yang diinginkan
      text_draw.text((0, 0), text, font=font, fill=(fill[0], fill[1], fill[2]))

      # Merotasi gambar teks sesuai dengan sudut yang diinginkan
      rotated_text_image = text_image.rotate(angle,
                                             resample=Image.BICUBIC,
                                             expand=True)

      # Menghitung pergeseran tinggi dari rotasi sudut
      shift_y = int(math.tan(math.radians(angle)) * text_width)

      # Menyesuaikan posisi teks yang dirotasi
      rotated_x = x - int(shift_y / 2) - (len(text) * 2) - (28 - len(text))
      rotated_y = y - int(shift_y / 2) - ((len(text) * 2) + len(text) -
                                          (40 + ((len(text) * 2))))

    # Menambahkan gambar teks yang telah dirotasi ke dalam gambar input
    image.paste(rotated_text_image, (rotated_x, rotated_y), rotated_text_image)

  for text_info in text_list:
    text = text_info["text"]
    font_path = text_info["font_path"]
    font_size = text_info["font_size"]
    position = text_info["position"]
    fill = text_info["fill"]

    # Mengatur font yang akan digunakan
    font = ImageFont.truetype(font_path, font_size)

    # Menghitung ukuran teks
    text_width, text_height = font.getsize(text)

    # Mengatur posisi teks pada gambar
    x = position[0]
    y = position[1]

    # Memisahkan teks menjadi beberapa baris berdasarkan '\n'
    lines = text.split('\n')

    # Menggambar setiap baris teks pada gambar
    for line in lines:
      # Menghitung ukuran teks per baris
      text_width, text_height = font.getsize(line)

      # Membuat gambar kosong menggunakan mode "RGBA" (transparan)
      text_image = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))

      # Membuat objek ImageDraw untuk menggambar teks pada gambar kosong
      text_draw = ImageDraw.Draw(text_image)

      # Menggambar teks pada posisi yang diinginkan
      text_draw.text((0, 0), line, font=font, fill=(fill[0], fill[1], fill[2]))

      # Menambahkan gambar teks ke dalam gambar input
      image.paste(text_image, (x, y), text_image)

      # Menggeser posisi y untuk baris teks berikutnya
      y += text_height

  for image_data in image_data:
    img_path = image_data["image"]
    position = image_data["position"]
    img_size = image_data["imgsize"]

    # Download the image from the URL
    # response = requests.get(img_path)
    # image_data = BytesIO(response.content)

    # Open the image data using PIL
    object_image = Image.open(img_path)

    # Mengubah ukuran objek gambar sesuai dengan parameter yang diberikan
    object_image = object_image.resize(img_size).convert("RGBA")

    # Membuat mask berbentuk lingkaran dengan ukuran yang sama
    mask = Image.new("L", object_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + object_image.size, fill=255)

    object_image = ImageOps.fit(object_image, mask.size, centering=(0.5, 0.5))
    object_image.putalpha(mask)

    # Menggabungkan objek gambar ke dalam gambar input
    image.paste(object_image, position, object_image)
  # Menyimpan gambar yang telah dimodifikasi
  image.save(toutput)

  print("Teks berhasil ditambahkan pada gambar input.")


@bot.event
async def on_member_join(member):

  user_data = [
    {
      "text": f"{member.display_name}",
      "font_path": userfont,
      "font_size": user_fsize,
      "position": (1374, 220),
      "fill": (0, 0, 0),
      "angle": text_angle
    },
  ]

  # Config untuk merubah font size, font family, posisi, dan rotasi pada sebuah text
  text_list = [
    {
      "text":
      "My mind is focused, my heart is determind, \n and my spirit is unbreakable. Let the mission begin",
      "font_path": msgfont,
      "font_size": msg_fsize,
      "position": (1774, 600),
      "fill": (255, 255, 255),
      "angle": 0
    },
    {
      "text":
      "In this distorted world, we shall \n steal the hearts of the corrupt and bring justice to the \n oppressed. Come, join the party and let's change the world together!",
      "font_path": msgfont,
      "font_size": 120,
      "position": (1574, 550),
      "fill": (255, 255, 255),
      "angle": 0
    },
    {
      "text":
      "The power of unity lies within our party. \n Join us, and let's unravel the mysteries of the world while leaving \n our mark in the hearts of those we touch.",
      "font_path": msgfont,
      "font_size": 130,
      "position": (1574, 550),
      "fill": (255, 255, 255),
      "angle": 0
    },
  ]

  # Config untuk merubah image size, posisi pada sebuah image
  image_data = [
    {
      "image":
      str(member.display_avatar.url),  #bagian ini masih error hehehehe
      "position": (45, 322),
      "imgsize": (632, 632),
    },
  ]
  # Menambahkan multiple teks ke dalam gambar input
  random_elements = random.sample(text_list, k=1)
  join_member(input_image, random_elements, image_data, user_data)

  # Send the welcome message with the image to the designated channel
  channel = discord.utils.get(member.guild.text_channels, name=channel_name)
  if channel:
    with open(inoutput, 'rb') as f:
      picture = discord.File(f)
      await channel.send(content=f"", file=picture)


@bot.event
async def on_member_remove(member):

  luser_data = [
    {
      "text": f"{member.display_name}",
      "font_path": userfont,
      "font_size": user_fsize,
      "position": (1374, 220),
      "fill": (0, 0, 0),
      "angle": text_angle
    },
  ]

  # Config untuk merubah font size, font family, posisi, dan rotasi pada sebuah text
  ltext_list = [
    {
      "text":
      "Leaving is sometimes necessary to find what lies beyond \n the horizon. Thank you all for being a part of my journey.",
      "font_path": msgfont,
      "font_size": msg_fsize,
      "position": (1574, 600),
      "fill": (255, 255, 255),
    },
  ]

  # Config untuk merubah image size, posisi pada sebuah image
  limage_list = [
    {
      "image":
      str(member.display_avatar.url),  #bagian ini masih error hehehehe
      "position": (45, 322),
      "imgsize": (632, 632),
    },
  ]

  # Menambahkan multiple teks ke dalam gambar input
  random_elements = random.sample(ltext_list, k=1)
  remove_member(linput_image, random_elements, limage_list, luser_data)

  # Send the welcome message with the image to the designated channel
  channel = discord.utils.get(member.guild.text_channels, name=channel_name)
  if channel:
    with open(loutput, 'rb') as f:
      picture = discord.File(f)
      await channel.send(content=f"", file=picture)


@bot.command()
async def test(ctx, count: int = None):

  if count is None:
    # Config untuk merubah font size, font family, posisi, dan rotasi pada sebuah text

    user_dummy = [
      {
        "text": "testing>  ",
        "font_path": userfont,
        "font_size": user_fsize,
        "position": (1374, 220),
        "fill": (0, 0, 0),
        "angle": text_angle
      },
    ]

    text_list = [
      {
        "text":
        "My mind is focused, my heart is determind, \n and my spirit is unbreakable. Let the mission begin",
        "font_path": msgfont,
        "font_size": msg_fsize,
        "position": (1774, 600),
        "fill": (255, 255, 255),
        "angle": 0
      },
      {
        "text":
        "In this distorted world, we shall \n steal the hearts of the corrupt and bring justice to the \n oppressed. Come, join the party and let's change the world together!",
        "font_path": msgfont,
        "font_size": 120,
        "position": (1474, 550),
        "fill": (255, 255, 255),
        "angle": 0
      },
      {
        "text":
        "The power of unity lies within our party. \n Join us, and let's unravel the mysteries of the world while leaving \n our mark in the hearts of those we touch.",
        "font_path": msgfont,
        "font_size": 130,
        "position": (1574, 550),
        "fill": (255, 255, 255),
        "angle": 0
      },
    ]

    image_data = [
      {
        "image": profile_img,  #bagian ini masih error hehehehe
        "position": (45, 322),
        "imgsize": (632, 632),
      },
    ]

    # Menambahkan multiple teks ke dalam gambar input
    random_user = random.sample(user_dummy, k=1)
    random_text = random.sample(text_list, k=1)
    testing(input_image, random_text, random_user, image_data)

    # Send the welcome message with the image to the designated channel
    with open(toutput, 'rb') as f:
      picture = discord.File(f)
      await ctx.send(content=f"", file=picture)

  for i in range(count):
    # Config untuk merubah font size, font family, posisi, dan rotasi pada sebuah text
    user_data = [
      {
        "text": "t",
        "font_path": userfont,
        "font_size": user_fsize,
        "position": (1374, 220),
        "fill": (0, 0, 0),
        "angle": text_angle
      },
      {
        "text": "te",
        "font_path": userfont,
        "font_size": user_fsize,
        "position": (1374, 220),
        "fill": (0, 0, 0),
        "angle": text_angle
      },
      {
        "text": "tes",
        "font_path": userfont,
        "font_size": user_fsize,
        "position": (1374, 220),
        "fill": (0, 0, 0),
        "angle": text_angle
      },
      {
        "text": "test",
        "font_path": userfont,
        "font_size": user_fsize,
        "position": (1374, 220),
        "fill": (0, 0, 0),
        "angle": text_angle
      },
      {
        "text": "testu",
        "font_path": userfont,
        "font_size": user_fsize,
        "position": (1374, 220),
        "fill": (0, 0, 0),
        "angle": text_angle
      },
      {
        "text": "testut",
        "font_path": userfont,
        "font_size": user_fsize,
        "position": (1374, 220),
        "fill": (0, 0, 0),
        "angle": text_angle
      },
      {
        "text": "testuto",
        "font_path": userfont,
        "font_size": user_fsize,
        "position": (1374, 220),
        "fill": (0, 0, 0),
        "angle": text_angle
      },
      {
        "text": "testutot",
        "font_path": userfont,
        "font_size": user_fsize,
        "position": (1374, 220),
        "fill": (0, 0, 0),
        "angle": text_angle
      },
      {
        "text": "testutot_",
        "font_path": userfont,
        "font_size": user_fsize,
        "position": (1374, 220),
        "fill": (0, 0, 0),
        "angle": text_angle
      },
      {
        "text": "testutot-",
        "font_path": userfont,
        "font_size": user_fsize,
        "position": (1374, 220),
        "fill": (0, 0, 0),
        "angle": text_angle
      },
      {
        "text": "testutot>",
        "font_path": userfont,
        "font_size": user_fsize,
        "position": (1374, 220),
        "fill": (0, 0, 0),
        "angle": text_angle
      },
    ]

    user_dummy = [
      {
        "text": "testing-",
        "font_path": userfont,
        "font_size": user_fsize,
        "position": (1374, 220),
        "fill": (0, 0, 0),
        "angle": text_angle
      },
    ]

    text_list = [
      {
        "text":
        "My mind is focused, my heart is determind, \n and my spirit is unbreakable. Let the mission begin",
        "font_path": msgfont,
        "font_size": msg_fsize,
        "position": (1774, 600),
        "fill": (255, 255, 255),
        "angle": 0
      },
      {
        "text":
        "In this distorted world, we shall \n steal the hearts of the corrupt and bring justice to the \n oppressed. Come, join the party and let's change the world together!",
        "font_path": msgfont,
        "font_size": 120,
        "position": (1474, 550),
        "fill": (255, 255, 255),
        "angle": 0
      },
      {
        "text":
        "The power of unity lies within our party. \n Join us, and let's unravel the mysteries of the world while leaving \n our mark in the hearts of those we touch.",
        "font_path": msgfont,
        "font_size": 130,
        "position": (1574, 550),
        "fill": (255, 255, 255),
        "angle": 0
      },
    ]

    image_data = [
      {
        "image": profile_img,  #bagian ini masih error hehehehe
        "position": (45, 322),
        "imgsize": (632, 632),
      },
    ]

    # Menambahkan multiple teks ke dalam gambar input
    random_user = random.sample(user_data, k=1)
    random_text = random.sample(text_list, k=1)
    testing(input_image, random_text, random_user, image_data)
    print(i)
    # Send the welcome message with the image to the designated channel
    with open(toutput, 'rb') as f:
      picture = discord.File(f)
      await ctx.send(content=f"", file=picture)


@bot.command()
@commands.is_owner()
async def cls(ctx):
  await ctx.channel.delete()
  new_channel = await ctx.channel.clone(reason="Bersih Bersih Gudang!!")
  await new_channel.edit(position=ctx.channel.position)


#===================================================================


@bot.event
async def on_ready():
  activity = discord.Game(name=">help", type=3)
  await bot.change_presence(status=discord.Status.online, activity=activity)
  print(f'Logged in as {bot.user.name} ({bot.user.id})')


server_on()
bot.run(TOKEN)
