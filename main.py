from threading import Thread
import pydirectinput as pdi
import pytesseract
import pyautogui
import keyboard
import time
import cv2


class controller:
    def __init__(self):
        self.width, self.height = pdi.size()

        # statistics
        self.backpack = 0
        self.mined = 0

    def start_at(self, key):
        while True:
            if keyboard.is_pressed(key):
                pdi.doubleClick()
                break

    def wait_for_frame(self):
        self.move(2.115702479338843, 1.263157894736842)
        while True:
            if keyboard.is_pressed('q'):
                break
            pdi.click()

    def get_position(self, type=0):
        if type == 0:
            Thread(target=lambda: self.get_position(type=1)).start()
        else:
            while True:
                if keyboard.is_pressed('q'):
                    x, y = pdi.position()
                    print(f'Ratio: {self.width / x, self.height / y}')
                    time.sleep(0.05)

    def move(self, x_ratio, y_ratio):
        pdi.moveTo(int(self.width/x_ratio), int(self.height/y_ratio))

    def capture(self, x_ratio, y_ratio, width_ratio, height_ratio, path='image.png', type=0):
        if type == 0:
            img = pyautogui.screenshot(region=(int(self.width/x_ratio), int(self.height/y_ratio), int(self.width/width_ratio), int(self.height/height_ratio)))
        else:
            img = pyautogui.screenshot(region=(int(self.width/x_ratio), int(self.height/y_ratio), width_ratio, height_ratio))
        img.save(path)

    def get_text(self, path='image.png'):
        # read image and conver to grayscale
        # function will process the image to make it easier to find text
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # find contours using threshold
        ret, thresh = cv2.threshold(img, 100, 255, cv2.THRESH_OTSU)
        cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.imwrite('image.png', thresh)

        # return image to string
        return pytesseract.image_to_string(path, config='--psm 7')

    def update_statistics(self):
        # update overall statistics
        self.mined, self.backpack = self.read_backpack()

    def read_backpack(self):
        key = {'M': 1000000, 'B': 1000000000, 'T': 1000000000000}

        control.capture(25, 2.35, 10.0392156863, 28.8)
        raw = self.get_text().strip().replace(' ', '')

        mined = raw.split('/')[0]
        if mined[-1] in key:
            mined = int(float(mined[:-1]) * key[mined[-1]])

        backpack = raw.split('/')[1]
        if backpack[-1] in key:
            backpack = int(float(backpack[:-1]) * key[backpack[-1]])

        return mined, backpack


# add tesseract to path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\walke\AppData\Local\Tesseract-OCR\tesseract.exe'

print('Starting...')
control = controller()
control.start_at('q')

# wait for frame to be selected
control.wait_for_frame()
control.update_statistics()


# main loop
while True:
    # switch tool
    pdi.press('1')

    # start mining
    # move to center of screen
    control.move(2.064516129032258, 1.92)
    pdi.mouseDown()

    # check if backpack is full
    while True:
        control.capture(2.8, 3.5, 3.93846153846, 14.4)
        if control.get_text().strip() == 'Backpack Full':
            pdi.mouseUp()

            # click the sell button
            control.move(2.1333333333333333, 2.0719424460431655)
            pdi.click()
            break

    # switch to teleporter again
    pdi.press('3')
    pdi.move(2.115702479338843, 1.263157894736842)
    pdi.click()
