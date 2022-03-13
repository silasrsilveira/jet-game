# Importando o modulo pygame
from asyncore import loop
from pdb import Restart
import pygame

# Import random para numeros aleatorios
import random


# Importar pygame.locals para facilitar o acesso a cordenadas de teclas
# Atualizado conforme o flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
import pygments

# Definir costante para a tela Altura e Largura
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 300

# Definir o objeto(Jogador) Player exetendend com pygame.sprite.Sprite
# Em vez de usar a superficie desenhanada, use a img para o sprite mais bonito
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    # Mover a srite basenada na tecla pressionada
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Manter o player na tela
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Definir o objeto(inimigo) Enemy extendendo pelo pygame.sprite.Sprite
# A superfice(surface) desenhada agora é atribuidada de 'enemy'

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            # A posição inicial é gerada aleatoriamente, assim como a velocidade
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)


## Mover a sprite se baseando na velocidade
# Remova a sprite quando ela passa pela borda da esquerda
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Nuvem in moviasjkdhashdg ajjj guuggu

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                   # O inicio da posição é gerada aleatoria
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
       
    # Mover as nuvens baseada na constant speed
    # Remove a nuvem quando passar a esquerda da tela

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
        

# Configuração para os sounds. Os padrãos são bom
pygame.mixer.init()


# Inicializar o pygame
pygame.init()

# Carregar e tocar musica de fundo
# Fontes de som: http://ccmixter.org/files/Apoxode/59262
# Licença: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(loops=-1)

# Load all sound files
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")


#Configurar volume medio de todos
move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
collision_sound.set_volume(0.5)


# Configurar o relogio para uma taxa de frame 
clock = pygame.time.Clock()

# Criar o objeto de tela (screen)
# O tamanho é determinado pela constante SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


## Criar um evento customizado para adicionar um novo inimigo
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

## Criar um evento customizado para adicionar nuvens
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Criando o nosso 'player'
player = Player()

## Criar grupos para manter sprites de enyme e todas as sprites
# - enimies é usado para direção de conlisão e posição de update
# - all_sprites é usada para renderizar

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Variavel para fazer nosso loop rodar
running = True


# Our main loop
while running:
    # Olhe para cada evento na fila
    for event in pygame.event.get():
        # O usuário pressionou uma tecla?
        if event.type == KEYDOWN:
            # Foi a tecla Escape(ESC)? Se sim, pare o loop
            if event.key == K_ESCAPE:
                running = False

        # O usuário clicou no botão fechar a janela? Se sim, pare o loop
        elif event.type == QUIT:
            running = False
        
        # Adicionando um novo inimigo?
        elif event.type == ADDENEMY:
            # Criar o novo inimigo e adicionar ele para o grupo de sprites
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        # Adicionar nuvens?
        elif event.type == ADDCLOUD:
            # Criar novas nuvens e adicionar ao grupo de sprites
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    # Obtenha o conjunto de teclas pressionado e verifique a entrada do usuário
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Atualizar posição do inimigo
    enemies.update()
    clouds.update()

    # Preencher a tela com preto
    screen.fill((135, 206, 250))

    # Desenhar todas sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Checar se algum inimigo colidiu com o jogador
    if pygame.sprite.spritecollideany(player, enemies):
        #então se, remover o jogador e parar o loop
        player.kill()
        

        # Parar qualquer som e toque o de colisão
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()

        running = True

        
        

    # Flip everything to the display
    pygame.display.flip()

    # Garantir que o programga use 30 fps
    clock.tick(30)


# All done! Stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()