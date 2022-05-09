# Brendon Zimmer
# ITP 116, 11:00-11:50
# Final Project — Movie Finder and Explorer

import requests
from tkinter import *
from io import BytesIO
from PIL import ImageTk, Image

API_KEY = "k_8cin941m"

def sourceImage(url: str, size: tuple[int, int]):
    x, y = size
    
    if 'amazon' in url: 
        main = url.split("._V1_U")[0] + "._V1_U"
        uxy = "X" + str(x) if "X" in url.split("._V1_U")[1].split(",")[0].split("_")[0] else "Y" + str(y)
        cr = url.split("._V1_U")[1].split(",")[0].split("_")[1][2:]
        cr2 = url.split("._V1_U")[1].split(",")[1]
        hei = url.split("._V1_U")[1].split(",")[3].split("_")[0]
        rest = url.split("._V1_U")[1].split(",")[3][len(hei):]
        
        url = f"{main}{uxy}_CR{int((int(cr)/int(hei))*y)},{cr2},{x},{y}{rest}"
        jpg = Image.open(BytesIO(requests.get(url).content))
    else: jpg = Image.open(BytesIO(requests.get(url.replace("original", f"{x}x{y}")).content))
    
    return ImageTk.PhotoImage(jpg)


def detailsWindow(movie: dict, state: list, parent: Tk):
    root = Toplevel(parent)
    root.title(movie['fullTitle'])
    root.geometry("800x600")

    detailsFrame = Frame(root)
    detailsFrame.grid()

    ###################################

    topFrame = Frame(detailsFrame)
    topFrame.grid(row=0)

    topLeftFrame = Frame(topFrame)
    topLeftFrame.grid(row=0, column=0)

    topRightFrame = Frame(topFrame)
    topRightFrame.grid(row=0, column=1)

    bytes = sourceImage(movie['image'], (168, 231))
    state.append(bytes)
    poster = Label(topLeftFrame, image=bytes)
    poster.grid(row=0, column=0)

    title = Label(topRightFrame, text=movie['title'], font="Arial 26 bold", wraplength=500, justify=CENTER)
    title.grid(row=0, column=0)

    description = Label(topRightFrame, text=movie['plot'], font="Arial 16", wraplength=600, justify=CENTER)
    description.grid(row=1, column=0)

    ###################################

    bottomFrame = Frame(detailsFrame)
    bottomFrame.grid(row=1, sticky=W)

    director = movie['directors'] if movie['directors'] else "Not Available"
    directors = Label(bottomFrame, text=f"Director(s): {director}", font="Arial 16")
    directors.grid(sticky=W, row=0, column=0)

    writer = movie['writers'] if movie['writers'] else "Not Available"
    writers = Label(bottomFrame, text=f"Writer(s): {writer}", font="Arial 16")
    writers.grid(sticky=W, row=1, column=0)

    actor = movie['stars'] if movie['stars'] else "Not Available"
    actors = Label(bottomFrame, text=f"Star(s): {actor}", font="Arial 16")
    actors.grid(sticky=W, row=5, column=0)

    genre = movie['genres'] if movie['genres'] else "Not Available"
    genres = Label(bottomFrame, text=f"Genre(s): {genre}", font="Arial 16")
    genres.grid(sticky=W, row=6, column=0)

    date = movie['releaseDate'] if movie['releaseDate'] else "Not Available"
    release = Label(bottomFrame, text=f"Release Date: {date}", font="Arial 16")
    release.grid(sticky=W, row=7, column=0)

    runtime = movie['runtimeStr'] if movie['runtimeStr'] else f"{movie['runtime']} mins" if movie['runtime'] else "Not Available"
    runtime = Label(bottomFrame, text=f"Runtime: {runtime}", font="Arial 16")
    runtime.grid(sticky=W, row=8, column=0)

    stars = "⭐️" * int(float(movie['ratings']['imDb'])) if movie['ratings']['imDb'] else "⭐️" * float(movie['ratings']['rottenTomatoes'])//10 if movie['ratings']['rottenTomatoes'] else "Not Available"
    rating = Label(bottomFrame, text=f"Rating: {stars} of 10", font="Arial 16")
    rating.grid(sticky=W, row=9, column=0)

    ###################################

    try:
        img = movie['images']['items'][0]['image']
        bytes = sourceImage(img, (250, 190))
        state.append(bytes)
        img1 = Label(bottomFrame, image=bytes)
        img1.grid(row=10, column=0)

        img = movie['images']['items'][1]['image']
        bytes = sourceImage(img, (250, 190))
        state.append(bytes)
        img2 = Label(bottomFrame, image=bytes)
        img2.grid(row=10, column=1)
    except: pass


def details(id: str, state: list, parent: Tk):
    res = requests.get(f"https://imdb-api.com/en/API/Title/{API_KEY}/{id}/Images,Ratings")
    
    if res.status_code != 200:
        print("\nError:", res.status_code)
    elif not res.json()['id']:
        print(f"\nError: {res.json()['errorMessage']}")
    else:
        movie = res.json()
        detailsWindow(movie, state, parent)


def previewWindow(movie: dict):
    state = []
    root = Tk()
    root.title('Movie Preview')
    root.geometry("520x600")

    rootFrame = Frame(root)
    rootFrame.place(relx=.5, rely=.5, anchor=CENTER)

    previewFrame = Frame(rootFrame)
    previewFrame.grid()
    
    bytes = sourceImage(movie['image'], (336, 462))
    state.append(bytes)
    thumbnail = Label(previewFrame, image=bytes)
    thumbnail.grid(row=0)

    try: title = Label(previewFrame, text=movie['fullTitle'])
    except: title = Label(previewFrame, text=movie['title']+" "+movie['description'])
    title.config(font="Arial 24 bold", wraplength=400, justify=CENTER)
    title.grid(row=1)

    moreInfo = Button(previewFrame, text="View More", command=lambda: details(movie['id'], state, parent=root))
    moreInfo.grid(row=2)

    root.mainloop()


def preview(data: dict):
    print()
    
    while True:
        inp = input("Preview a title (enter # or 'done'): ")

        if "done" in inp.lower(): break

        if inp.isdigit(): 
            inp = int(inp)
            if inp > 0 and inp <= len(data): 
                previewWindow(data[inp-1])


def search(con: bool = True):
    title = input("\nEnter a title: ")
    if con: print("May take a minute. To speed up, try searching for a title with a year.")
    
    print("Searching...")
    res = requests.get(f"https://imdb-api.com/en/API/SearchMovie/{API_KEY}/{title}")
            
    if res.status_code != 200:
        print("\nError:", res.status_code)
    elif res.json()['errorMessage'] != "":
        print(f"\nError: {res.json()['errorMessage']}")
    elif not res.json()['results']:
        print(f"{title} could not be found.")
        search(con=False)
    else:
        data = res.json()['results']
        print("\nResults:")

        for i, movie in enumerate(data): print(f"\t{i+1}. {movie['title']} {movie['description']}")
        preview(data)


def top100():
    print("\nTop 100 most popular movies:")
    res = requests.get(f"https://imdb-api.com/en/API/MostPopularMovies/{API_KEY}")
            
    if res.status_code != 200:
        print("\nError:", res.status_code)
    elif len(res.json()['items']) == 0:
        print(f"\nError: {res.json()['errorMessage']}")
    else:
        data = res.json()['items']
        for movie in data: print(f"\t{movie['rank']}: {movie['fullTitle']}")
        preview(data)


def menu():
    print("Welcome to the IMDb explorer!")
    
    while True:
        print("Menu Items:")
        print("\t1. View top 100 most popular movies")
        print("\t2. Search a title")
        print("\t3. Quit")
        choice = input("What would you like to do? ")

        if choice == "1": top100()
            
        if choice == "2": search()

        if choice == "3":
            print("\nThank you for using IMDb explorer!")
            break

        print("\n-------\n")


def main(): menu()

main()