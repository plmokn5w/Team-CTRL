import pygame
import time
import os

pygame.init()

size = [100, 100]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("소리 재생")
current_path = os.path.dirname(__file__)
sound_path = os.path.join(current_path, "sound")  # 현재 폴더의 소리 파일이 있는 곳을 지정해 줬습니다.


# 아래 부분을 복사해서 넣으면 소리를 재생할 수 있습니다. 위에 있는 코드들은 테스트를 위해 실행하려고 만들어 놓은 것입니다.

class Sound:
    def __init__(self, path):
        self.sound = pygame.mixer.Sound(os.path.join(sound_path, path))

    def play(self): # 1회 재생
        self.sound.play()

    def play_along(self):  # 무한 재생
        self.sound.play(-1)

    def stop(self):
        self.sound.stop()


# 예제
test_sound = Sound("test.mp3")  # 소리 파일이 있는 곳에서 원하는 파일의 이름을 지정합니다.
test_sound.play()  # 그 파일을 1회 재생합니다.

i = 0
while True:
    pygame.display.update()
    time.sleep(0.001)
    i += 1
    if i == 3000:
        test_sound.stop()
        pygame.quit()
pygame.quit()
