import base64
import datetime

def make_me_happy():
    today = datetime.datetime.today()
    no_work = datetime.datetime(2018, 12, 25)
    free_food = no_work - today
    print base64.b64decode('RGF5IGxlZnQgdW50aWwgQ2hyaXN0bWFzISE='), free_food

def main():
    make_me_happy()
if __name__ == '__main__':
    main()
