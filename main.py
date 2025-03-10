import random  # Mengimpor pustaka random untuk menghasilkan nilai acak
import sys  # Mengimpor pustaka sys untuk menangani keluarnya program
import pygame  # Mengimpor pustaka pygame untuk membuat game
from pygame.locals import *  # Mengimpor semua konstanta dari pygame.locals

# Mengatur kecepatan frame per detik
FPS = 32
frame_size_x = 289  # Lebar jendela permainan
frame_size_y = 511  # Tinggi jendela permainan
window_screen = pygame.display.set_mode((frame_size_x, frame_size_y))  # Membuat jendela permainan
game_sprites = {}  # Dictionary untuk menyimpan gambar
game_sounds = {}  # Dictionary untuk menyimpan suara
player = 'gallery/sprites/astro.png'  # Path gambar pemain
background = 'gallery/sprites/bg.jpg'  # Path gambar latar belakang
base = 'gallery/sprites/base.jpg'  # Path gambar dasar
pipe = 'gallery/sprites/pipe.png'  # Path gambar pipa
ground_by = frame_size_y * 0.8  # Posisi dasar permainan

# Inisialisasi pygame
pygame.init()
fps_controller = pygame.time.Clock()
pygame.display.set_caption('Astro Man')  # Mengatur judul jendela permainan

def main_game():
    """Fungsi utama permainan"""
    player_x = int(frame_size_x / 5)  # Posisi awal pemain pada sumbu x
    player_y = int(frame_size_x / 2)  # Posisi awal pemain pada sumbu y
    base_x = 0  # Posisi awal dasar permainan
    player_jump = False  # Status apakah pemain sedang melompat
    player_jump_acc = -8  # Kecepatan awal saat melompat

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_y > 0:
                    player_vel_y = player_jump_acc  # Mengatur kecepatan lompatan
                    player_jump = True  # Menandai bahwa pemain sedang melompat
                    game_sounds['jump'].play()  # Memainkan suara lompatan
        
        # Menampilkan elemen permainan ke layar
        window_screen.blit(game_sprites['background'], (0, 0))
        window_screen.blit(game_sprites['base'], (base_x, ground_by))
        window_screen.blit(game_sprites['player'], (player_x, player_y))
        pygame.display.update()
        fps_controller.tick(FPS)  # Mengontrol kecepatan permainan


def welcome_screen():
    """Menampilkan layar awal permainan"""
    player_x = int(frame_size_x / 5)
    player_y = int((frame_size_y - game_sprites['player'].get_height()) / 2)
    base_x = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return  # Memulai permainan jika tombol ditekan
            else:
                # Menampilkan elemen di layar awal
                window_screen.blit(game_sprites['background'], (0, 0))
                window_screen.blit(game_sprites['player'], (player_x, player_y))
                welcome_text = pygame.font.SysFont('Impact', 32)
                welcome_surface = welcome_text.render("Astro Man", True, (255,255,255))
                welcome_rect = welcome_surface.get_rect()
                welcome_rect.midtop = (frame_size_x / 2, 32)
                window_screen.blit(welcome_surface, welcome_rect)
                window_screen.blit(game_sprites['base'], (base_x, ground_by))
                pygame.display.update()
                fps_controller.tick(FPS)

# Memuat gambar ke dalam dictionary game_sprites
game_sprites['base'] = pygame.image.load(base).convert_alpha()
game_sprites['background'] = pygame.image.load(background).convert()
game_sprites['player'] = pygame.image.load(player).convert_alpha()

# Memuat suara ke dalam dictionary game_sounds
game_sounds['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
game_sounds['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
game_sounds['jump'] = pygame.mixer.Sound('gallery/audio/jump.wav')

# Menjalankan permainan dalam loop utama
while True:
    welcome_screen()
    main_game()
