# Brendon Zimmer
# ITP 116, 11:00-11:50
# Final Project — Movie Finder and Explorer

import requests
from tkinter import *
from io import BytesIO
from PIL import ImageTk, Image

API_KEY = "k_t3f76pdi"

def sourceImage(url: str, size: tuple[int, int]):
    x, y = size
    if 'amazon' in url: jpg = Image.open(BytesIO(requests.get(url[0:url.find('@')] + f'@._V1_UX{x}_CR0,0,{x},{y}_AL_.jpg').content))
    else: jpg = Image.open(BytesIO(requests.get(url.replace("original", f"{x}x{y}")).content))
    
    return ImageTk.PhotoImage(jpg)


def detailsWindow(movie: dict, state: list, parent: Tk):
    root = Toplevel(parent)
    root.title(movie['fullTitle'])
    root.geometry("800x600")

    detailsFrame = Frame(root)
    detailsFrame.grid()

    bytes = sourceImage(movie['image'], (168, 231))
    state.append(bytes)
    thumbnail = Label(detailsFrame, image=bytes)
    thumbnail.grid(row=0, column=0)

    label = Label(detailsFrame, text=movie['title'])
    label.grid(row=0, column=1)


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
    title.config(font="Arial 24 bold")
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
            if inp > 0 or inp <= len(data): 
                previewWindow(data[inp-1])


def search(title: str):
    print("May take a minute. To speed up, try searching for a title with a year.")
    print("Searching...")
    res = requests.get(f"https://imdb-api.com/en/API/SearchMovie/{API_KEY}/{title}")
            
    if res.status_code != 200:
        print("\nError:", res.status_code)
    elif not res.json()['results']:
        print(f"\nError: {res.json()['errorMessage']}")
    else:
        data = res.json()['results']
        print("\nResults:")

        for i, movie in enumerate(data): print(f"\t{i+1}. {movie['title']} {movie['description']}")
        preview(data)


def top100():
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
    while True:
        print("Menu Items:")
        print("\t1. View top 100 most popular movies")
        print("\t2. Search a title")
        print("\t3. Quit")
        choice = input("What would you like to do? ")

        if choice == "1":
            print("\nTop 100 most popular movies:")
            top100()
            
        if choice == "2":
            title = input("\nEnter a title: ")
            search(title)

        if choice == "3":
            print("\nThank you for using IMDb explorer!")
            break

        print("\n-------\n")


def main():
    print("Welcome to the IMDb explorer!")
    menu()


main()