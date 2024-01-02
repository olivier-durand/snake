import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# Paramètres du jeu
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
GRID_SIZE = 30
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
CELL_SIZE = SCREEN_HEIGHT // GRID_SIZE

# Couleurs
DARK_GREEN = (0, 128, 0)
SNAKE_COLOR = (0, 0, 255)  # Bleu pour le serpent
APPLE_COLOR = (255, 0, 0)  # Rouge pour la pomme
RED = (255, 0, 0)  # Couleur rouge pour le texte

# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Position et dimensions du rectangle initial
snake_segments = [pygame.Rect(CELL_SIZE, CELL_SIZE, CELL_SIZE, CELL_SIZE)]

# Longueur initiale du serpent
snake_length = 1

# Vitesse de déplacement du serpent
speed = 10

# Fichier best_score
score_file = "best_score.txt"

# Direction initiale du serpent
direction = (1, 0)

# Position et dimensions de la pomme
apple = pygame.Rect(5 * CELL_SIZE, 5 * CELL_SIZE, CELL_SIZE, CELL_SIZE)

# Score
score = 0

# Meilleur score
best_score = 0

# Compteur de croissance du serpent
growth_counter = 0

# Horloge de Pygame pour réguler la vitesse
clock = pygame.time.Clock()

# Fonction pour réinitialiser le jeu
def reset_game():
    global snake_segments, snake_length, direction, speed, apple, score, growth_counter, best_score
    snake_segments = [pygame.Rect(CELL_SIZE, CELL_SIZE, CELL_SIZE, CELL_SIZE)]
    snake_length = 1
    growth_counter = 0
    direction = (1, 0)
    speed = 10
    spawn_apple()
    if score > best_score:
        best_score = score
        with open(score_file, "w") as file:
            file.write(str(best_score))
    score = 0
    
# Fonction pour charger le meilleur score depuis le fichier
def load_best_score():
    global best_score
    try:
        with open(score_file, "r") as file:
            best_score = int(file.read())
    except FileNotFoundError:
        # Si le fichier n'existe pas, initialise le meilleur score à 0
        best_score = 0

# Fonction pour réinitialiser le jeu
def reset_game():
    global snake_segments, snake_length, direction, speed, apple, score, growth_counter, best_score
    snake_segments = [pygame.Rect(CELL_SIZE, CELL_SIZE, CELL_SIZE, CELL_SIZE)]
    snake_length = 1
    growth_counter = 0
    direction = (1, 0)
    speed = 10
    spawn_apple()
    score = 0
    load_best_score()  # Charge le meilleur score à chaque réinitialisation

# Fonction pour changer la vitesse et la direction du serpent
def change_speed_direction(key):
    global direction, speed

    if key == pygame.K_LEFT and direction != (1, 0):
        direction = (-1, 0)
    elif key == pygame.K_RIGHT and direction != (-1, 0):
        direction = (1, 0)
    elif key == pygame.K_UP and direction != (0, 1):
        direction = (0, -1)
    elif key == pygame.K_DOWN and direction != (0, -1):
        direction = (0, 1)
    elif key == pygame.K_PLUS or key == pygame.K_KP_PLUS:
        speed += 1
    elif key == pygame.K_MINUS or key == pygame.K_KP_MINUS:
        speed = max(1, speed - 1)

# Fonction pour dessiner la grille
def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.rect(screen, DARK_GREEN, (x, y, CELL_SIZE, CELL_SIZE), 1)

# Fonction pour dessiner le serpent
def draw_snake():
    for segment in snake_segments:
        pygame.draw.rect(screen, SNAKE_COLOR, segment)

# Fonction pour dessiner la pomme
def draw_apple():
    pygame.draw.rect(screen, APPLE_COLOR, apple)

# Fonction pour afficher le score
def display_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score} | Best Score: {best_score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

# Fonction pour faire apparaître une nouvelle pomme à un emplacement aléatoire
def spawn_apple():
    global apple
    apple.x = random.randint(0, GRID_SIZE - 1) * CELL_SIZE
    apple.y = random.randint(0, GRID_SIZE - 1) * CELL_SIZE

# Fonction pour mettre à jour le serpent
def update_snake():
    global snake_segments, direction, snake_length, growth_counter, score

    # Obtenir la nouvelle position de la tête du serpent
    new_head = pygame.Rect(snake_segments[0].x + direction[0] * CELL_SIZE,
                           snake_segments[0].y + direction[1] * CELL_SIZE,
                           CELL_SIZE, CELL_SIZE)

    # Vérifier si la tête du serpent touche la pomme
    if new_head.colliderect(apple):
        spawn_apple()
        score += 5
        growth_counter += 5  # Incrémenter le compteur de croissance

    # Insérer la nouvelle tête du serpent
    snake_segments.insert(0, new_head)

    # Mettre à jour la longueur du serpent en fonction du compteur de croissance
    while growth_counter > 0:
        snake_segments.append(snake_segments[-1].copy())
        growth_counter -= 1

    # Supprimer la queue du serpent si elle dépasse la longueur souhaitée
    if len(snake_segments) > snake_length:
        snake_segments.pop()

# Fonction principale du jeu
def main():
    global snake_segments, snake_length, direction, speed, apple, score

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                change_speed_direction(event.key)

        # Mettre à jour la position du serpent en fonction de la direction
        update_snake()

        # Vérifier si le serpent touche le bord ou lui-même
        if (
            snake_segments[0].x < 0
            or snake_segments[0].x >= SCREEN_WIDTH
            or snake_segments[0].y < 0
            or snake_segments[0].y >= SCREEN_HEIGHT
            or any(segment.colliderect(snake_segments[0]) for segment in snake_segments[1:])
        ):
            # Si le serpent touche le bord ou lui-même, réinitialiser le jeu
            reset_game()

        # Dessiner la grille, le serpent, la pomme et afficher le score
        screen.fill(DARK_GREEN)
        draw_grid()
        draw_snake()
        draw_apple()
        display_score()

        # Mettre à jour l'écran
        pygame.display.flip()

        # Réguler la vitesse avec une horloge Pygame
        clock.tick(speed)

# Fonction pour réinitialiser le jeu
def reset_game():
    global snake_segments, snake_length, direction, speed, apple, score, growth_counter, best_score
    snake_segments = [pygame.Rect(CELL_SIZE, CELL_SIZE, CELL_SIZE, CELL_SIZE)]
    snake_length = 1
    growth_counter = 0
    direction = (1, 0)
    speed = 10
    spawn_apple()
    if score > best_score:
        best_score = score
        with open(score_file, "w") as file:
            file.write(str(best_score))
    score = 0
    load_best_score()  # Charge le meilleur score à chaque réinitialisation

# Fonction pour charger le meilleur score depuis le fichier
def load_best_score():
    global best_score
    try:
        with open(score_file, "r") as file:
            best_score = int(file.read())
    except FileNotFoundError:
        # Si le fichier n'existe pas, initialise le meilleur score à 0
        best_score = 0

# ... (le reste du code)

if __name__ == "__main__":
    reset_game()  # Initialisation du jeu
    main()        # Lancer la boucle principale