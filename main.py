import random  # Mengimpor pustaka random untuk menghasilkan nilai acak
import sys  # Mengimpor pustaka sys untuk menangani keluarnya program
import pygame  # Mengimpor pustaka pygame untuk membuat game
from pygame.locals import *  # Mengimpor semua konstanta dari pygame.locals

# Mengatur kecepatan frame per detik
FPS = 32
frame_size_x = 289  # Lebar jendela permainan
frame_size_y = 511  # Tinggi jendela permainan
window_screen = pygame.display.set_mode((frame_size_x, frame_size_y))  # Membuat jendela permainan
high_score = 0
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
    global high_score
    base_x = 0  # Posisi awal dasar permainan
    player_jump = False  # Status apakah pemain sedang melompat
    player_jump_acc = -8  # Kecepatan awal saat melompat
    player_vel_y = -9  # Kecepatan awal pemain pada sumbu y
    player_max_vel_y = 10  # Kecepatan maksimum jatuh pemain
    player_acc_y = 1  # Percepatan gravitasi pemain
    pipe_vel_x = -4  # Kecepatan gerakan pipa ke kiri
    score = 0

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
        crash_test= is_collide(player_x, player_y, upper_pipes, lower_pipes)
        if crash_test:
            if score > high_score :
                high_score = score
            return score
        player_mid_pos = player_x + game_sprites['player'].get_width()/2
        for pipe in upper_pipes:
            pipe_mid_pos = pipe['x'] + game_sprites['pipe'][0].get_width()/2
            if pipe_mid_pos<= player_mid_pos < pipe_mid_pos +4:
                score +=1
                print(f"Your score is {score}")
                game_sounds['point'].play()
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
        score_font = pygame.font.SysFont('Impact', 32)
        score_surface = score_font.render(str(score), True,(255,255,255))
        score_rect = score_surface.get_rect()
        score_rect.midtop = (frame_size_x/2, 32)
        window_screen.blit(score_surface, score_rect)
        pygame.display.update()
        fps_controller.tick(FPS)  # Mengontrol kecepatan permainan

def game_over_screen(score):
    global high_score
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_UP):
                return
            else:
                window_screen.blit(game_sprites['background'], (0, 0))
                text_font = pygame.font.SysFont('Impact', 24)
                game_over_surface = text_font.render("Game Over !", True, (255,255,255))
                score_surface = text_font.render("Score : " + str(score), True, (255,255,255))
                continue_surface = text_font.render("Press 'ENTER' To Continue !", True, (255,255,255))
                high_score_surface = text_font.render("High Score : " + str(high_score), True, (255,255,255))
                window_screen.blit(game_over_surface, (80, 100))
                window_screen.blit(score_surface, (100, 170))
                window_screen.blit(continue_surface, (20, 230))
                window_screen.blit(high_score_surface, (80,430))
                pygame.display.update()
                fps_controller.tick(FPS)

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

def is_collide(player_x, player_y, upper_pipes, lower_pipes):
    """Fungsi untuk mendeteksi tabrakan pemain dengan pipa atau tanah."""
    if player_y > frame_size_y * 0.7 or player_y < 0:  
        game_sounds['hit'].play()  # Memainkan suara tabrakan
        return True  # Mengembalikan True jika pemain menabrak tanah atau keluar layar atas

    # Mengecek apakah pemain bertabrakan dengan pipa atas
    for pipe in upper_pipes:
        pipe_height = game_sprites['pipe'][0].get_height()  # Mendapatkan tinggi pipa
        if(player_y < pipe_height + pipe['y'] and abs(player_x - pipe['x']) < game_sprites['pipe'][0].get_width()):
            game_sounds['hit'].play()  # Memainkan suara tabrakan
            return True  # Mengembalikan True jika bertabrakan dengan pipa atas

    # Mengecek apakah pemain bertabrakan dengan pipa bawah
    for pipe in lower_pipes:
        if (player_y + game_sprites['player'].get_height() > pipe['y']) and abs(player_x - pipe['x']) < game_sprites['pipe'][0].get_width():
            game_sounds['hit'].play()  # Memainkan suara tabrakan
            return True  # Mengembalikan True jika bertabrakan dengan pipa bawah

    return False  # Mengembalikan False jika tidak ada tabrakan

def get_random_pipe():
    """Menghasilkan posisi acak untuk pipa baru."""
    pipe_height = game_sprites['pipe'][0].get_height()  # Mendapatkan tinggi sprite pipa
    offset = frame_size_y / 3  # Menentukan jarak minimal antara pipa atas dan bawah
    y2 = offset + random.randrange(0, int(frame_size_y - game_sprites['base'].get_height() - 1.2 * offset))  
    y1 = pipe_height - y2 + offset  # Menyesuaikan posisi pipa atas agar sejajar dengan pipa bawah
    pipe_x = frame_size_x + 10  # Menempatkan pipa di luar layar untuk muncul dari kanan

    # Mengembalikan dua pipa dalam bentuk dictionary: satu pipa atas dan satu pipa bawah
    return [
        {'x': pipe_x, 'y': -y1},  # Pipa atas (negatif karena posisinya di atas layar)
        {'x': pipe_x, 'y': y2}  # Pipa bawah
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
    welcome_screen() # Menampilkan layar awal
    score = main_game() # Memulai permainan utama dan mendapatkan skor
    game_over_screen(score) # Menampilkan layar game over dan menunggu input untuk memulai ulang
