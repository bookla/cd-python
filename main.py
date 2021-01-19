import pygame
from PIL import Image
import time
import session_manager
import camera_controller
import image_manager
import user_manager

pygame.init()

background_colour = (255, 255, 255)
(width, height) = (1280, 720)


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Photo Booth')
screen.fill(background_colour)

pygame.display.flip()


def draw_qr(img):
    img.save("qr_temp.png")

    screen.fill(background_colour)
    surface = pygame.image.load('qr_temp.png')

    qr_rect = surface.get_rect()
    qr_rect.center = (width // 2, height // 2 + 30)

    screen.blit(surface, qr_rect)

    t, rect = centered_text("Scan QR Code to Begin", font_size=60, y=100)
    screen.blit(t, rect)

    pygame.display.update()


def centered_text(val, font_size=32, x=width//2, y=height//2):
    font = pygame.font.SysFont('Helvetica', font_size)
    text = font.render(val, True, (0, 0, 0), background_colour)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    return text, text_rect


def countdown():
    print("3")
    screen.fill(background_colour)
    t, rect = centered_text("3", font_size=100)
    screen.blit(t, rect)
    pygame.display.update()

    time.sleep(1)

    print("2")
    screen.fill(background_colour)
    t, rect = centered_text("2", font_size=100)
    screen.blit(t, rect)
    pygame.display.update()

    time.sleep(1)

    print("1")
    screen.fill(background_colour)
    t, rect = centered_text("1", font_size=100)
    screen.blit(t, rect)
    pygame.display.update()

    time.sleep(1)

    screen.fill(background_colour)
    t, rect = centered_text("Smile!", font_size=100)
    screen.blit(t, rect)
    pygame.display.update()


def show_complete():
    screen.fill(background_colour)
    t, rect = centered_text("Photo Taken!", font_size=100)
    screen.blit(t, rect)
    pygame.display.update()


while True:
    email = ""
    initial_files = []
    session, qr = session_manager.create()
    print(session)
    try:
        draw_qr(qr)
        while not session_manager.is_triggered(session):
            time.sleep(0.1)
            pygame.event.get()
        countdown()
        initial_files = image_manager.get_initial()
        camera_controller.take_photo()
        show_complete()
        email = session_manager.get_email(session)
        print(email)
        if not user_manager.user_exists(email):
            email, code = user_manager.create_user(email)
            user_manager.send_create_email(email, code)
    except:
        session_manager.deactivate(session)
    session_manager.deactivate(session)
    new_images = image_manager.register_new_images(email, initial_files)
    print(new_images)
    image_manager.update_image_database(email, new_images)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
