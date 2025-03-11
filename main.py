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
fps_controller = pygame.time.Clock()  # Objek untuk mengontrol kecepatan frame per detik
pygame.display.set_caption('Astro Man')  # Mengatur judul jendela permainan

def main_game():
    """Fungsi utama permainan"""
    player_x = int(frame_size_x / 5)  # Posisi awal pemain pada sumbu x
    player_y = int(frame_size_x / 2)  # Posisi awal pemain pada sumbu y
    base_x = 0  # Posisi awal dasar permainan
    player_jump = False  # Status apakah pemain sedang melompat
    player_jump_acc = -8  # Kecepatan awal saat melompat
    player_vel_y = -9  # Kecepatan awal pemain pada sumbu y
    player_max_vel_y = 10  # Kecepatan maksimum jatuh pemain
    player_acc_y = 1  # Percepatan gravitasi pemain
    pipe_vel_x = -4  # Kecepatan gerakan pipa ke kiri

    # Menghasilkan dua pipa secara acak untuk permainan
    new_pipe_1 = get_random_pipe()  
    new_pipe_2 = get_random_pipe()  

    # Menyimpan koordinat pipa atas pertama dan kedua
    upper_pipes = [
        {'x': frame_size_x + 200, 'y': new_pipe_1[0]['y']},  
        {'x': frame_size_x + 200 + (frame_size_x / 2),'y': new_pipe_2[0]['y']},  
    ]

    # Menyimpan koordinat pipa bawah pertama dan kedua
    lower_pipes = [
        {'x': frame_size_x + 200, 'y': new_pipe_1[1]['y']},  
        {'x': frame_size_x + 200 + (frame_size_x / 2),'y': new_pipe_2[1]['y']},  
    ]

    while True:
        # Mengolah event pada permainan (misalnya input dari pemain)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_y > 0:
                    player_vel_y = player_jump_acc  # Mengatur kecepatan lompatan
                    player_jump = True  # Menandai bahwa pemain sedang melompat
                    game_sounds['jump'].play()  # Memainkan suara lompatan

        # Menambahkan percepatan gravitasi saat pemain jatuh
        if player_vel_y < player_max_vel_y and not player_jump:
            player_vel_y += player_acc_y  
        if player_jump:
            player_jump = False  # Reset status lompatan setelah satu frame

        # Menyesuaikan posisi vertikal pemain dengan kecepatan jatuhnya
        player_height = game_sprites['player'].get_height()
        player_y = player_y + min(player_vel_y, ground_by - player_y - player_height)

        # Menampilkan elemen permainan ke layar
        window_screen.blit(game_sprites['background'], (0, 0))  # Menampilkan latar belakang

        # Menampilkan semua pipa di layar
        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            window_screen.blit(game_sprites['pipe'][0], (upper_pipe['x'], upper_pipe['y']))
            window_screen.blit(game_sprites['pipe'][1], (lower_pipe['x'], lower_pipe['y']))

        # Menampilkan dasar dan pemain
        window_screen.blit(game_sprites['base'], (base_x, ground_by))
        window_screen.blit(game_sprites['player'], (player_x, player_y))

        # Memindahkan pipa ke kiri sesuai kecepatan pipe_vel_x
        for upper_pipe , lower_pipe in zip(upper_pipes, lower_pipes):
            upper_pipe['x'] += pipe_vel_x
            lower_pipe['x'] += pipe_vel_x

        # Menambahkan pipa baru saat pipa pertama hampir keluar layar
        if 0 < upper_pipes[0]['x'] < 5:
            new_pipe = get_random_pipe()
            upper_pipes.append(new_pipe[0])
            lower_pipes.append(new_pipe[1])

        # Menghapus pipa yang sudah keluar layar
        if upper_pipes[0]['x'] < -game_sprites['pipe'][0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)

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
                
                # Menampilkan judul permainan
                welcome_text = pygame.font.SysFont('Impact', 32)
                welcome_surface = welcome_text.render("Astro Man", True, (255,255,255))
                welcome_rect = welcome_surface.get_rect()
                welcome_rect.midtop = (frame_size_x / 2, 32)
                window_screen.blit(welcome_surface, welcome_rect)

                window_screen.blit(game_sprites['base'], (base_x, ground_by))
                pygame.display.update()
                fps_controller.tick(FPS)

def get_random_pipe():
    """Menghasilkan posisi acak untuk pipa baru"""
    pipe_height = game_sprites['pipe'][0].get_height()  # Mengambil tinggi sprite pipa
    offset = frame_size_y / 3  # Menentukan batas acak pipa
    y2 = offset + random.randrange(0, int(frame_size_y - game_sprites['base'].get_height() - 1.2 * offset))
    y1 = pipe_height - y2 + offset
    pipe_x = frame_size_x + 10
    
    # Mengembalikan dua pipa: satu atas dan satu bawah
    return [
        {'x': pipe_x, 'y': -y1},  
        {'x': pipe_x, 'y': y2}  
    ]

# Memuat gambar ke dalam dictionary game_sprites
game_sprites['base'] = pygame.image.load(base).convert_alpha()
game_sprites['background'] = pygame.image.load(background).convert()
game_sprites['player'] = pygame.image.load(player).convert_alpha()
game_sprites['pipe'] = (pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(), 180),
                        pygame.image.load(pipe).convert_alpha())

# Memuat suara ke dalam dictionary game_sounds
game_sounds['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
game_sounds['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
game_sounds['jump'] = pygame.mixer.Sound('gallery/audio/jump.wav')

# Menjalankan permainan dalam loop utama
while True:
    welcome_screen()
    main_game()
